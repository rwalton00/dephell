# built-in
from copy import deepcopy
from typing import Iterable, Optional

# external
from dephell_markers import Markers
from packaging.utils import canonicalize_name

# project
import attr

# app
from ..repositories import GitRepo
from ..utils import cached_property
from .constraint import Constraint
from .groups import Groups


@attr.s(cmp=False)
class Dependency:
    raw_name = attr.ib(type=str)
    constraint = attr.ib(type=Constraint, repr=False)
    repo = attr.ib(repr=False)
    link = attr.ib(default=None, repr=False)

    # flags
    applied = attr.ib(type=bool, default=False, repr=False)

    # optional info
    description = attr.ib(type=str, default='', repr=False)     # summary
    authors = attr.ib(factory=tuple, repr=False)                # author{,_email}, maintainer{,_email}
    links = attr.ib(factory=dict, repr=False)                   # project_url{,s}, package_url
    classifiers = attr.ib(factory=tuple, repr=False)            # classifiers

    # info from requirements file
    editable = attr.ib(type=bool, default=False, repr=False)
    # https://github.com/pypa/packaging/blob/master/packaging/markers.py
    marker = attr.ib(type=Optional[Markers], default=None, repr=False)
    envs = attr.ib(type=set, factory=set, repr=False)  # which root extras cause this dep

    extra = None

    # properties

    @cached_property
    def name(self) -> str:
        return canonicalize_name(self.raw_name)

    @property
    def base_name(self) -> str:
        return self.name

    @cached_property
    def groups(self) -> Groups:
        return Groups(dep=self)

    @cached_property
    def group(self):
        """By first access choose and save best group
        """
        self.groups.actualize()
        for group in self.groups:
            if not group.empty:
                return group

    @property
    def dependencies(self) -> tuple:
        deps = self.__dict__.get('dependencies')
        if deps is not None:
            return deps

        from ..controllers import DependencyMaker
        deps = []
        for dep in self.group.dependencies:
            if isinstance(dep, Dependency):
                deps.append(dep)
            elif isinstance(dep, Iterable):
                deps.append(dep)
            else:
                deps.extend(DependencyMaker.from_requirement(self, dep))
        return tuple(deps)

    @dependencies.setter
    def dependencies(self, dependencies: tuple) -> None:
        constraint = str(self.constraint)
        if not constraint.startswith('==') or ',' in constraint or '||' in constraint:
            raise ValueError('cannot set deps for non-locked dependency')
        self.__dict__['dependencies'] = dependencies

    @property
    def locked(self) -> bool:
        return 'group' in self.__dict__

    @property
    def python_compat(self) -> bool:
        if self.marker is None:
            return True
        needed = self.marker.python_version
        if needed is None:
            return True

        if self.locked:
            required = self.group.best_release.python
            if required is None:
                return True
            return (needed + required).python_compat

        for group in self.groups:
            if group.empty:
                continue
            required = group.best_release.python
            if required is None:
                return True
            if (needed + required).python_compat:
                return True
        return False

    @property
    def compat(self) -> bool:
        # if group has already choosed
        if self.locked:
            return not self.group.empty
        # if group hasn't choosed
        for group in self.groups:
            if not group.empty:
                return True
        return False

    @property
    def used(self) -> bool:
        """True if some deps in graph depends on this dep.
        """
        return not self.constraint.empty

    # methods

    def unlock(self) -> None:
        del self.__dict__['group']
        # if 'dependencies' in self.__dict__:
        #     del self.__dict__['dependencies']

    def unapply(self, name: str) -> None:
        self.constraint.unapply(name)
        if self.locked:
            self.unlock()

    def copy(self) -> 'Dependency':
        obj = deepcopy(self)
        obj.constraint = self.constraint.copy()
        if obj.locked:
            obj.unlock()
        return obj

    # magic methods

    def __str__(self) -> str:
        result = self.name
        if self.extra:
            result += '[{}]'.format(self.extra)
        if self.constraint:
            result += str(self.constraint)
        if self.marker:
            result += '; ' + str(self.marker)
        return result

    def __iadd__(self, dep: 'Dependency') -> 'Dependency':
        if not isinstance(dep, type(self)):
            return NotImplemented

        # some checks when we merge two git based dep
        if isinstance(self.link, GitRepo) and isinstance(dep.link, GitRepo):
            # links point to different revisions
            if self.link.rev and dep.link.rev and self.link.rev != dep.link.rev:
                return NotImplemented
            # links point to different servers
            if self.link.server != dep.link.server:
                return NotImplemented
            ...

        # if ...
        # .. 1. we don't use repo in self,
        # .. 2. it's a git repo,
        # .. 3. dep has non-git repo,
        # .. 4. self has no rev,
        # then prefer non-git repo, because it's more accurate and fast.
        if isinstance(self.link, GitRepo) and not isinstance(dep.link, GitRepo):
            if not self.link.rev:
                if not self.groups._loaded_groups:
                    self.repo = dep.repo

        if not isinstance(self.link, GitRepo) and isinstance(dep.link, GitRepo):
            self.link = dep.link
            self.repo = dep.repo

        self.constraint &= dep.constraint
        self.groups.actualize()
        self.envs.update(dep.envs)
        return self

    def __add__(self, dep: 'Dependency') -> 'Dependency':
        new = self.copy()
        new += dep
        return dep

    def __lt__(self, other):
        return self.name < other.name

# DepHell

**DepHell** -- project management for Python.

+ Manage dependencies: [convert between formats](cmd-deps-convert), [install](cmd-deps-install), lock, [add new](cmd-deps-add), resolve conflicts.
+ Manage virtual environments: [create](cmd-venv-create), [remove](cmd-venv-destroy), [inspect](cmd-inspect-venv), [run shell](cmd-venv-shell), [run commands inside](cmd-venv-run).
+ [Install CLI tools](cmd-jail-install) into isolated environments.
+ Manage packages: [install](cmd-package-install), [list](cmd-package-list), [search](cmd-package-search) on PyPI.
+ [Build](cmd-project-build) packages (to upload on PyPI), [test](cmd-project-test), [bump project version](cmd-project-bump).
+ [Discover licenses](cmd-deps-licenses) of all project dependencies, show [outdated](cmd-deps-outdated) packages, [find security issues](cmd-deps-audit).
+ Generate [.editorconfig](cmd-generate-editorconfig), [LICENSE](cmd-generate-license), [AUTHORS](cmd-generate-authors), [.travis.yml](cmd-generate-travis).

```eval_rst
.. toctree::
    :maxdepth: 1
    :caption: Main Info

    installation
    config
    params
    filters
    python-lookup

.. toctree::
    :maxdepth: 1
    :caption: Project dependencies

    cmd-deps-add
    cmd-deps-audit
    cmd-deps-check
    cmd-deps-convert
    cmd-deps-install
    cmd-deps-licenses
    cmd-deps-outdated
    cmd-deps-sync
    cmd-deps-tree

.. toctree::
    :maxdepth: 1
    :caption: Files generation

    cmd-generate-authors
    cmd-generate-config
    cmd-generate-editorconfig
    cmd-generate-license
    cmd-generate-travis

.. toctree::
    :maxdepth: 1
    :caption: Inspect

    cmd-inspect-config
    cmd-inspect-self
    cmd-inspect-venv

.. toctree::
    :maxdepth: 1
    :caption: Isolation

    cmd-jail-install
    cmd-jail-list
    cmd-jail-remove
    cmd-jail-try

.. toctree::
    :maxdepth: 1
    :caption: Single package actions

    cmd-package-downloads
    cmd-package-install
    cmd-package-list
    cmd-package-purge
    cmd-package-releases
    cmd-package-remove
    cmd-package-search
    cmd-package-show

.. toctree::
    :maxdepth: 1
    :caption: Project

    cmd-project-build
    cmd-project-bump
    cmd-project-test

.. toctree::
    :maxdepth: 1
    :caption: Virtual environment

    cmd-venv-create
    cmd-venv-destroy
    cmd-venv-run
    cmd-venv-shell

.. toctree::
    :maxdepth: 1
    :caption: Other commands

    cmd-autocomplete

.. toctree::
    :maxdepth: 1
    :caption: Dive deeper

    badge
    changelog
    hell

.. toctree::
    :maxdepth: 1
    :caption: Recipes and examples

    use-git-hook
    use-tree-git
    use-poetry-lock
    use-licenses
```

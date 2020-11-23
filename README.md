# Wack

## Aim
Wack is a personal project to provide a simple [click](https://github.com/pallets/click) (maybe [typer](https://github.com/tiangolo/typer) / or custom in the future) cli tool.

Wack gives the user the ability to make simple files quickly (e.g. setup.py)

## Install:
```
pip install wack
```

Now `wack` will be added to your terminal commands. Typing `wack` will give you:
```
Usage: wack [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  install
  make
```

`wack install` will install my most used packages: Flask, IPython, pytest, sqlalchemy, attrs, requests, pre-commit, python-dotenv

`wack make` will give a list of files wack will make:
```
Usage: wack make [OPTIONS] COMMAND [ARGS]...

  make files from templates

Options:
  --help  Show this message and exit.

Commands:
  gitignore   make a `.gitignore` file with pycharm basics
  license     make a `LICENSE` file with MIT license
  package     make a `__init__.py` file in a package
  pre-commit  make a `.pre-commit-config.yaml` file to allow for pre-commit
  setup.py    make a `setup.py` file to allow for `pip install -e .`
  travis      make a `.travis.yml` file for pypi auto publishing packages
  upload      make a `.gitignore` file with pycharm basics

```

#### TODO
* cookie-cutter for simple flask app?
* sqlalchemy / alembic setup

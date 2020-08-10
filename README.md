# Wack

## Aim
Wack is a personal project to provide a simple [click](https://github.com/pallets/click) (maybe [typer](https://github.com/tiangolo/typer) / or custom in the future) cli tool. 

Wack gives the user the ability to:
* Make simple files quickly (e.g. setup.py)
* Ability to write simple and quick cli commands, found when typing `$ wack` into the terminal
* To automate simple tasks (e.g. making `pip install` write to requirements.txt by default)

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
  init
  install
  make
```

## Setup wack:
```
wack init
```

This will make a wack.py file in the directory you're in. My recommendation is to do this in the root dir. It will look like the below:
```
from wack import command
from wack import echo


@command()
def hello_world():
    echo("hello world")
```

Now when typing `$ wack` you will get:
```
Usage: wack [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  hello_world
  init
  install
  make
```

FYI, as of 0.0.1 (current version), click groups aren't supported, only commands, which need to be imported from `wack`. All other click features should work by default and can be imported from click or wack (as wack impliments `from click import *`).

## TODO
* have a `make` command for:
    * dotenv
    * pre-commit
* more tests
* cookie-cutter for simple flask app?
* sqlalchemy / alembic setup
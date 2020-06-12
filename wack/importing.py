import importlib.util
import os
from pathlib import Path

import click


def get_package():
    packages = [
        i
        for i in os.listdir(".")
        if os.path.isdir(i) and "__init__.py" in os.listdir("./" + i)
    ]
    if len(packages) > 1:
        raise ValueError("Only one package allowed")
    elif len(packages) == 0:
        return ""
    else:
        return packages.pop()


def get_wack_py_dir(path: str) -> str:
    path = Path(path).resolve()
    print(path)
    if "wack.py" in os.listdir(path):
        print('returning', path.as_posix())
        return path.as_posix()

    elif path.as_posix() == "/":
        raise ValueError(f"No wack.py file found")
    else:
        get_wack_py_dir(path.parent)


def get_wack_py() -> str:
    current_dir = os.getcwd()
    try:
        wack_py_dir = get_wack_py_dir(current_dir)
        print(wack_py_dir)
    except ValueError as e:
        raise ValueError(e)

    return wack_py_dir + "/wack.py"


def import_wack():
    try:
        wack_py = get_wack_py()
    except ValueError as e:
        raise ImportError(e)
    spec = importlib.util.spec_from_file_location("wack", wack_py)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_wack_to_cli(cli):
    try:
        wack = import_wack()
        commands_and_groups_to_add = {
            name: value
            for name, value in vars(wack).items()
            if isinstance(value, click.core.Command)
            and name
            not in [
                item
                for sublist in [
                    group.commands
                    for group in {
                        name: value
                        for name, value in vars(wack).items()
                        if isinstance(value, click.core.Group)
                    }.values()
                ]
                for item in sublist
            ]
        }

        for i, j in commands_and_groups_to_add.items():
            cli.add_command(j, name=i)

    except ImportError:
        pass

    return cli

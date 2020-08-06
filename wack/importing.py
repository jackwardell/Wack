import importlib
import importlib.util
import os
from contextlib import contextmanager
from pathlib import Path

import click


@contextmanager
def operate_in_dir(new_dir):
    current_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield
    except Exception as e:
        raise e
    finally:
        os.chdir(current_dir)


# class File:
#     """a representation of a file, essentially a wrapper around pathlib.Path"""
#
#     def __init__(self, filepath: str):
#         self.filepath = filepath
#
#     @property
#     def exists(self) -> bool:
#         return self.to_path().exists()
#
#     @property
#     def name(self) -> str:
#         """get file e.g. hello.py"""
#         return self.to_path().name
#
#     @property
#     def stem(self) -> str:
#         """get file name e.g. hello (if file was hello.py)"""
#         return self.to_path().stem
#
#     @property
#     def extension(self) -> str:
#         """get file extension e.g. py (if file was hello.py)"""
#         return self.to_path().suffix
#
#     @property
#     def dir(self) -> str:
#         """get directory of a file"""
#         return self.to_path().parent.as_posix()
#
#     def to_path(self):
#         return Path(self.filepath)
#
#     def to_module(self):
#         with operate_in_dir(self.dir):
#             return importlib.import_module(self.stem)
#
#     def make(self):
#         return self.to_path().touch()
#
#     @classmethod
#     def from_path(cls, path: Path):
#         return cls(path.resolve().as_posix())


# def get_package():
#     packages = [
#         i
#         for i in os.listdir(".")
#         if os.path.isdir(i) and "__init__.py" in os.listdir("./" + i)
#     ]
#     if len(packages) > 1:
#         raise ValueError("Only one package allowed")
#     elif len(packages) == 0:
#         return ""
#     else:
#         return packages.pop()


def find_file_recursively_backwards(file, directory) -> Path:
    directory = Path(directory).resolve()
    print(directory)
    if file in os.listdir(directory):
        return directory.with_name(file)
    elif directory.as_posix() == "/":
        raise FileNotFoundError(f"{file} not found")
    else:
        return find_file_recursively_backwards(file, directory.parent)


def get_wack_py() -> Path:
    return find_file_recursively_backwards("wack.py", Path.cwd())


def import_wack():
    wack_py = get_wack_py()
    with operate_in_dir(wack_py.parent.as_posix()):
        module = importlib.import_module(wack_py.stem)

    # spec = importlib.util.spec_from_file_location("wack", wack_py)
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)
    return module


def add_wack_to_cli(cli):
    try:
        # import IPython; IPython.embed()
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


# def as_module(self) -> types.ModuleType:
#     """import file as module"""
#     # check to see if exists
#     if not self.exists:
#         raise FileNotFoundError(f"{self.filepath} does not exist")
#
#     else:
#         # try to import the wack module
#         try:
#             # get module spec
#             spec = importlib.util.spec_from_file_location(self.name, self.filepath)
#             # import module
#             module = importlib.util.module_from_spec(spec)
#             # load module
#             spec.loader.exec_module(module)
#             # check we have something
#             assert module, f"failed to import {self.filepath}"
#             # return module
#             return module
#
#         # import may fail for many reasons
#         except Exception as e:
#             # so display the exception to the user
#             raise ImportError(f"failed to import {self.filepath} due to: {e}")

# @classmethod
# def from_current_dir(cls, filename: str):
#     """find file recursively from current dir backwards"""
#     return cls(search_for_file_in_path(filename, os.getcwd()))

# def __eq__(self, other):
#     return type(self) == type(other) and self.filepath == other.filepath

# def __repr__(self):
#     return f"File({self.file}, exists={self.exists})"


# def get_file_in_current_path(filename: str) -> File:
#     """
#     get any file in current dir or any parent dir, starting with current dir
#     moving towards the root dir, first found wins
#     """
#     return File(search_for_file_in_path(filename, "."))


# def get_wack_file() -> File:
#     """
#     get wack.py in current dir or any parent dir, starting with current dir
#     moving towards the root dir, first found wins
#     """
#     return get_file_in_current_path("wack.py")


# def get_requirements_txt_file() -> File:
#     """
#     get requirements.txt in current dir or any parent dir, starting with current dir
#     moving towards the root dir, first found wins
#     """
#     return get_file_in_current_path("requirements.txt")


# def get_requirements_ini_file() -> File:
#     """
#     get requirements.ini in current dir or any parent dir, starting with current dir
#     moving towards the root dir, first found wins
#     """
#     return get_file_in_current_path("requirements.ini")

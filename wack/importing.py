import importlib.util
import os
import types
from contextlib import contextmanager
from pathlib import Path
import importlib
import click


# def inspect(obj):
#     attrs = dir(obj)
#
#     for attr in attrs:
#         attr_name, attr_value = attr, getattr(obj, attr)
#         if callable(attr_value):
#             try:
#                 print(attr_name, attr_value())
#             except TypeError:
#                 print(attr_name, "failed with TypeError")
#                 # print(attr_name, attr_value)
#         else:
#             print(attr_name, attr_value)


# def search_for_file_in_path(file: str, path: str) -> str:
#     """find a file in path hierarchy"""
#     # resolve for '.' case
#     path = Path(path).resolve()
#     if file in os.listdir(path):
#         # return file if found
#         return (path / file).as_posix()
#     elif path.as_posix() == "/":
#         # break if no file found by root
#         raise FileNotFoundError(f"No {file} file found in path hierarchy: {path}")
#     else:
#         # else repeat for the parent dir
#         return search_for_file_in_path(file, path.parent)


class File:
    """a representation of a file"""

    def __init__(self, filepath):
        # set full filepath
        self.filepath = filepath

        # set a pathlib Path for easy use
        self.path = Path(self.filepath)

        # set if exists
        self.exists = self.path.is_file()

    def make(self):
        self.path.touch()
        self.exists = True
        return self.exists

    @property
    def file(self):
        """get file e.g. hello.py"""
        return self.path.name

    @property
    def name(self):
        """get file name e.g. hello (if file was hello.py)"""
        return self.file.split(".").pop(0)

    @property
    def extension(self):
        """get file extension e.g. py (if file was hello.py)"""
        return "." + self.file.split(".").pop()

    @property
    def dir(self) -> str:
        """get directory of a file"""
        return self.path.parent.as_posix()

    def as_module(self) -> types.ModuleType:
        """import file as module"""
        # check to see if exists
        if not self.exists:
            raise FileNotFoundError(f"{self.filepath} does not exist")

        else:
            # try to import the wack module
            try:
                # get module spec
                spec = importlib.util.spec_from_file_location(self.name, self.filepath)
                # import module
                module = importlib.util.module_from_spec(spec)
                # load module
                spec.loader.exec_module(module)
                # check we have something
                assert module, f"failed to import {self.filepath}"
                # return module
                return module

            # import may fail for many reasons
            except Exception as e:
                # so display the exception to the user
                raise ImportError(f"failed to import {self.filepath} due to: {e}")

    @classmethod
    def from_current_dir(cls, filename: str):
        """find file recursively from current dir backwards"""
        return cls(search_for_file_in_path(filename, os.getcwd()))

    def __eq__(self, other):
        return type(self) == type(other) and self.filepath == other.filepath

    def __repr__(self):
        return f"File({self.file}, exists={self.exists})"


def get_file_in_current_path(filename: str) -> File:
    """
    get any file in current dir or any parent dir, starting with current dir
    moving towards the root dir, first found wins
    """
    return File(search_for_file_in_path(filename, "."))


def get_wack_file() -> File:
    """
    get wack.py in current dir or any parent dir, starting with current dir
    moving towards the root dir, first found wins
    """
    return get_file_in_current_path("wack.py")


def get_requirements_txt_file() -> File:
    """
    get requirements.txt in current dir or any parent dir, starting with current dir
    moving towards the root dir, first found wins
    """
    return get_file_in_current_path("requirements.txt")


def get_requirements_ini_file() -> File:
    """
    get requirements.ini in current dir or any parent dir, starting with current dir
    moving towards the root dir, first found wins
    """
    return get_file_in_current_path("requirements.ini")


# class WackFile:
#     """a representation of the wack.py local file"""
#
#     name = "wack"
#     file = name + ".py"
#
#     def __init__(self, filepath):
#         # set full filepath
#         self.filepath = self.resolve_filepath(filepath)
#
#         # raise FileNotFound if the file doesn't exist
#         if not os.path.exists(self.filepath):
#             raise FileNotFoundError(f"{self.filepath} does not exist")
#
#         # get module
#         # we only want to load the module once
#         # but theoretically can be loaded again by calling self.import_module
#         self.module = self.import_module()
#         # make sure there is a module
#         assert self.module, f"failed to import {self.filepath}"
#
#     @property
#     def dir(self) -> str:
#         """get directory of self.file"""
#         return Path(self.filepath).parent.as_posix()
#
#     def import_module(self) -> types.ModuleType:
#         """import self.file as module"""
#         # try to import the wack module
#         try:
#             # get module spec
#             spec = importlib.util.spec_from_file_location(self.name, self.filepath)
#             # import module
#             module = importlib.util.module_from_spec(spec)
#             # load module
#             spec.loader.exec_module(module)
#             # return module
#             return module
#
#         # import may fail for many reasons
#         except Exception as e:
#             # so display the exception to the user
#             raise ImportError(f"failed to import {self.filepath} due to: {e}")
#
#     def resolve_filepath(self, filepath: str) -> str:
#         """make the absolute filepath for self.file"""
#         # get filepath as string
#         filepath = Path(filepath).resolve().as_posix()
#         # then if it ends with self.file
#         # it's ok
#         if filepath.endswith(self.file):
#             return filepath
#         # else add the file to the end
#         else:
#             return filepath + "/" + self.file
#
#     @classmethod
#     def from_current_dir(cls):
#         """find cls.file recursively from current dir backwards"""
#
#         def iter_search(file: str, path: str) -> str:
#             """find a file in path"""
#             # resolve for '.' case
#             path = Path(path).resolve()
#             if file in os.listdir(path):
#                 # embed()
#                 # return cls.file if found
#                 return path.as_posix()
#             elif path.as_posix() == "/":
#                 # break if no file found by root
#                 raise FileNotFoundError(f"No wack.py file found")
#             else:
#                 # else repeat for the parent dir
#                 return iter_search(file, path.parent)
#
#         # get current dir
#         current_dir = os.getcwd()
#         # search for cls.file from current dir
#         wack_py_dir = iter_search(cls.file, current_dir)
#         # return a instance of cls
#         return cls(wack_py_dir)
#
#     def __eq__(self, other):
#         return type(self) == type(other) and self.filepath == other.filepath


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


#
# def get_wack_py_dir(path: str) -> Path:
#     path = Path(path).resolve()
#     import IPython;
#     IPython.embed()
#
#     if "wack.py" in os.listdir(path):
#         return path.as_posix()
#
#     elif path.as_posix() == "/":
#         raise ValueError(f"No wack.py file found")
#     else:
#         get_wack_py_dir(path.parent)


def find_file_recursively_backwards(file, directory) -> Path:
    directory = Path(directory).resolve()
    if file in os.listdir(directory):
        return directory.with_name(file)
    elif directory.as_posix() == "/":
        raise FileNotFoundError(f"{file} not found")
    else:
        return find_file_recursively_backwards(file, directory.parent)


# def find_wack_py_file():
#     current_dir = os.getcwd()
#     cwd = Path(current_dir).resolve()
#
#     if "wack.py" in os.listdir(cwd)
#
#     try:
#         wack_py_dir = get_wack_py_dir(current_dir)
#         print(wack_py_dir)
#     except ValueError as e:
#         raise ValueError(e)
#
#     return wack_py_dir + "/wack.py"


def get_wack_py() -> Path:
    return find_file_recursively_backwards("wack.py", Path.cwd())


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

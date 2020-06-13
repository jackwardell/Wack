import importlib.util
import os
import types
from pathlib import Path
from IPython import embed


def inspect(obj):
    attrs = dir(obj)

    for attr in attrs:
        attr_name, attr_value = attr, getattr(obj, attr)
        if callable(attr_value):
            try:
                print(attr_name, attr_value())
            except TypeError:
                print(attr_name, "failed with TypeError")
                # print(attr_name, attr_value)
        else:
            print(attr_name, attr_value)


class WackFile:
    """a representation of the wack.py local file"""

    name = "wack"
    file = name + ".py"

    def __init__(self, filepath):
        # set full filepath
        self.filepath = self.resolve_filepath(filepath)

        # raise FileNotFound if the file doesn't exist
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"{self.filepath} does not exist")

        # get module
        # we only want to load the module once
        # but theoretically can be loaded again by calling self.import_module
        self.module = self.import_module()
        # make sure there is a module
        assert self.module, f"failed to import {self.filepath}"

    @property
    def dir(self) -> str:
        """get directory of self.file"""
        return Path(self.filepath).parent.as_posix()

    def import_module(self) -> types.ModuleType:
        """import self.file as module"""
        # try to import the wack module
        try:
            # get module spec
            spec = importlib.util.spec_from_file_location(self.name, self.filepath)
            # import module
            module = importlib.util.module_from_spec(spec)
            # load module
            spec.loader.exec_module(module)
            # return module
            return module

        # import may fail for many reasons
        except Exception as e:
            # so display the exception to the user
            raise ImportError(f"failed to import {self.filepath} due to: {e}")

    def resolve_filepath(self, filepath: str) -> str:
        """make the absolute filepath for self.file"""
        # get filepath as string
        filepath = Path(filepath).resolve().as_posix()
        # then if it ends with self.file
        # it's ok
        if filepath.endswith(self.file):
            return filepath
        # else add the file to the end
        else:
            return filepath + "/" + self.file

    @classmethod
    def from_current_dir(cls):
        """find cls.file recursively from current dir backwards"""

        def iter_search(file: str, path: str) -> str:
            """find a file in path"""
            # resolve for '.' case
            path = Path(path).resolve()
            if file in os.listdir(path):
                # embed()
                # return cls.file if found
                return path.as_posix()
            elif path.as_posix() == "/":
                # break if no file found by root
                raise FileNotFoundError(f"No wack.py file found")
            else:
                # else repeat for the parent dir
                return iter_search(file, path.parent)

        # get current dir
        current_dir = os.getcwd()
        # search for cls.file from current dir
        wack_py_dir = iter_search(cls.file, current_dir)
        # return a instance of cls
        return cls(wack_py_dir)

    def __eq__(self, other):
        return type(self) == type(other) and self.filepath == other.filepath

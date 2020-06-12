import importlib.util
import os
from pathlib import Path


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
    name = "wack"
    file = name + ".py"

    def __init__(self, filepath):
        self.filepath = self.resolve_filepath(filepath)

    @property
    def dir(self):
        return Path(self.filepath).parent.as_posix()

    @property
    def module(self):
        spec = importlib.util.spec_from_file_location(self.name, self.file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def resolve_filepath(self, filepath):
        filepath = Path(filepath).resolve().as_posix()
        if filepath.endswith(self.file):
            return filepath
        else:
            return filepath + "/" + self.file

    @classmethod
    def from_current_dir(cls):
        def iter_search(path):
            path = Path(path).resolve()
            if cls.file in os.listdir(path):
                return path.as_posix()
            elif path.as_posix() == "/":
                raise ValueError(f"No wack.py file found")
            else:
                iter_search(path.parent)

        current_dir = os.getcwd()
        wack_py_dir = iter_search(current_dir)
        return cls(wack_py_dir)

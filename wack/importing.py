import importlib
import importlib.util
import os
from pathlib import Path


def find_file_recursively_backwards(file, directory) -> Path:
    directory = Path(directory).resolve()
    if file in os.listdir(directory):
        return directory / file
    elif directory.as_posix() == "/":
        raise FileNotFoundError(f"{file} not found")
    else:
        return find_file_recursively_backwards(file, directory.parent)


def get_wack_py() -> Path:
    return find_file_recursively_backwards("wack.py", Path.cwd())


def import_wack():
    wack_py = get_wack_py()
    spec = importlib.util.spec_from_file_location(wack_py.stem, wack_py)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PackageNotFoundError(Exception):
    pass


class TooManyPackagesFound(Exception):
    pass


def get_package():
    packages = [
        package
        for package in os.listdir(".")
        if os.path.isdir(package) and "__init__.py" in os.listdir("./" + package)
    ]
    if len(packages) > 1:
        # todo allow more packages?
        raise TooManyPackagesFound("Only one package allowed")
    elif len(packages) == 0:
        raise PackageNotFoundError("No package found")
    else:
        return packages.pop()

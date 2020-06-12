from wack.helpers import WackFile
from pathlib import Path
import types
import importlib.util
import pytest


def test_wack_file_init(tempdir):
    assert WackFile.name == "wack"
    assert WackFile.file == "wack.py"

    with open(WackFile.file, "w+") as _:
        pass

    # test current working dir
    wack_file = WackFile(".")

    assert wack_file
    assert isinstance(wack_file, WackFile)

    tempdir_wack_py = tempdir + "/" + WackFile.file

    assert wack_file.filepath == tempdir_wack_py
    assert wack_file.dir == tempdir


def test_wack_file_module(tempdir):
    with open("wack.py", "w+") as _:
        pass

    wack_file = WackFile(".")
    assert isinstance(wack_file.module, types.ModuleType)
    spec = importlib.util.spec_from_file_location("wack", tempdir + "/wack.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert wack_file.module.__name__ == module.__name__
    # todo better assertion for wack_file.module

    with open("wack.py", "w+") as f:
        f.write('def hello(): raise ValueError("this is a test")')

    wack_file = WackFile(".")

    assert wack_file.module.hello
    assert isinstance(wack_file.module.hello, types.FunctionType)

    with pytest.raises(ValueError, match="this is a test"):
        wack_file.module.hello()

    wack_file = WackFile(tempdir)

    assert wack_file.filepath == tempdir + "/wack.py"

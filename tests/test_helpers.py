from wack.helpers import WackFile
from pathlib import Path
import types
import importlib.util
import pytest
import os

import inspect


def test_wack_file():
    assert WackFile.name == "wack"
    assert WackFile.file == "wack.py"


def test_wack_file_init_in_cwd_as_dot(tempdir):
    """test when there is a wack.py in cwd, but using '.' as the path"""

    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as _:
        pass

    # quick check file has been created
    assert os.path.exists(tempdir_wack_py)

    # test current working dir
    wack_file = WackFile(".")

    # test object instantiated
    assert wack_file
    assert isinstance(wack_file, WackFile)

    # test we get right filepath
    # expecting: tempdir/wack.py
    assert wack_file.filepath == tempdir_wack_py
    # expecting: tempdir
    assert wack_file.dir == tempdir


def test_wack_file_init_in_cwd_as_path(tempdir):
    """test when there is a wack.py in cwd, but using absolute path"""

    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as _:
        pass

    # quick check file has been created
    assert os.path.exists(tempdir_wack_py)

    cwd = os.getcwd()
    # quick check it's tempdir
    assert cwd == tempdir

    # test current working dir as path
    wack_file = WackFile(cwd)

    # test object instantiated
    assert wack_file
    assert isinstance(wack_file, WackFile)

    # test we get right filepath
    # expecting: tempdir/wack.py
    assert wack_file.filepath == tempdir_wack_py
    # expecting: tempdir
    assert wack_file.dir == tempdir


def test_wack_file_init_breaks(tempdir):
    """test when file doesn't exist it breaks"""

    with pytest.raises(FileNotFoundError):
        WackFile(".")


def test_wack_file_init_breaks_when_exists_in_parent(tempdir):
    """test when file doesn't exist it breaks, even if one is in parent"""

    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as _:
        pass

    # quick check file has been created
    assert os.path.exists(tempdir_wack_py)

    # make a new dir and cd into
    new_dir = "new_dir"
    os.mkdir(new_dir)
    os.chdir(new_dir)

    with pytest.raises(FileNotFoundError):
        WackFile(".")


def test_wack_file_init_breaks_in_child_dir(tempdir):
    """test when there is a wack.py in parent dir, but using '.' as path"""

    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as _:
        pass

    # quick check file has been created
    assert os.path.exists(tempdir_wack_py)

    # make a new dir and cd into
    new_dir = "new_dir"
    os.mkdir(new_dir)
    os.chdir(new_dir)

    # quick check we're where we want to be
    assert os.getcwd() == tempdir + "/" + new_dir

    # test current working dir as path
    with pytest.raises(FileNotFoundError):
        WackFile(".")

    # use parent dir
    wack_file = WackFile(tempdir)

    # test object instantiated
    assert wack_file
    assert isinstance(wack_file, WackFile)

    # test we get right filepath
    # expecting: tempdir/wack.py
    assert wack_file.filepath == tempdir_wack_py
    # expecting: tempdir
    assert wack_file.dir == tempdir


def test_wack_file_import_module_breaks(tempdir):
    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as f:
        # make it break
        f.write("bakldnklans=")

    # should break due to syntax error
    with pytest.raises(ImportError):
        WackFile(".")


def test_wack_file_from_current_dir(tempdir):
    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as _:
        pass

    # quick check file has been created
    assert os.path.exists(tempdir_wack_py)

    # make a new dir and cd into
    new_dir = "new_dir"
    os.mkdir(new_dir)
    os.chdir(new_dir)

    cwd = os.getcwd()
    # quick check it's tempdir + new dir
    assert cwd == tempdir + "/" + new_dir

    # test breaks
    # there is no wack.py in cwd so it shouldn't be able to find it
    with pytest.raises(FileNotFoundError):
        WackFile(cwd)

    # test breaks
    # there is no wack.py in cwd so it shouldn't be able to find it
    with pytest.raises(FileNotFoundError):
        WackFile(".")

    # this should be able to find the wack.py
    # it will iterate through parents to get it
    wack_file = WackFile.from_current_dir()

    # test object instantiated
    assert wack_file
    assert isinstance(wack_file, WackFile)

    # make sure its parents file
    assert wack_file.dir == tempdir

    # make sure its the file created above
    assert wack_file.filepath == tempdir_wack_py


def test_multiple_nesting(tempdir):
    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as _:
        pass

    # quick check file has been created
    assert os.path.exists(tempdir_wack_py)

    # make and cd into new folders
    nested_files = ["nest1", "nest2", "nest3"]
    for i in nested_files:
        os.mkdir(i)
        os.chdir(i)

    wack_file = WackFile.from_current_dir()

    # test object instantiated
    assert wack_file
    assert isinstance(wack_file, WackFile)

    # make sure its parents file
    assert wack_file.dir == tempdir

    # make sure its the file created above
    assert wack_file.filepath == tempdir_wack_py


def test_insane_nesting(tempdir):
    wack_file = "wack.py"
    tempdir_wack_py = tempdir + "/" + wack_file

    # make a wack file
    with open(wack_file, "w+") as _:
        pass

    # quick check file has been created
    assert os.path.exists(tempdir_wack_py)

    # make and cd into new folders
    nested_files = [f"nest{i}" for i in range(25)]
    for i in nested_files:
        os.mkdir(i)
        os.chdir(i)

    # quick check we are where we want to be
    assert os.getcwd() == tempdir + "/" + "/".join(nested_files)

    wack_file = WackFile.from_current_dir()

    # test object instantiated
    assert wack_file
    assert isinstance(wack_file, WackFile)

    # make sure its parents file
    assert wack_file.dir == tempdir

    # make sure its the file created above
    assert wack_file.filepath == tempdir_wack_py

    # # go back
    # os.chdir('..')
    # # quick check
    # cwd = os.getcwd()
    # assert cwd == tempdir
    #
    # wack_file = WackFile(cwd)
    #
    # # test object instantiated
    # assert wack_file
    # assert isinstance(wack_file, WackFile)
    #
    # # test we get right filepath
    # # expecting: tempdir/wack.py
    # assert wack_file.filepath == tempdir_wack_py
    # # expecting: tempdir
    # assert wack_file.dir == tempdir


# def test_wack_file_init_in_parent_dir_from_cwd_as_path(tempdir):
#     """test when there is a wack.py in parent dir, but using '.' as path"""
#
# wack_file = "wack.py"
# tempdir_wack_py = tempdir + "/" + wack_file
#
# # make a wack file
# with open(wack_file, "w+") as _:
#     pass
#
# # quick check file has been created
# assert os.path.exists(tempdir_wack_py)
#
# # make a new dir and cd into
# new_dir = "new_dir"
# os.mkdir(new_dir)
# os.chdir(new_dir)
#
# cwd = os.getcwd()
# # quick check it's tempdir + new dir
# assert cwd == tempdir + "/" + new_dir
#
# # test current working dir as path
# wack_file = WackFile(cwd)
#
# # test object instantiated
# assert wack_file
# assert isinstance(wack_file, WackFile)
#
# # test we get right filepath
# # expecting: tempdir/wack.py
# assert wack_file.filepath == tempdir_wack_py
# # expecting: tempdir
# assert wack_file.dir == tempdir


def test_wack_file_module(tempdir):
    with open("wack.py", "w+") as _:
        pass

    wack_file = WackFile(".")
    assert isinstance(wack_file.module, types.ModuleType)
    assert isinstance(wack_file.import_module, types.MethodType)

    spec = importlib.util.spec_from_file_location("wack", tempdir + "/wack.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert wack_file.module.__name__ == module.__name__
    assert wack_file.import_module().__name__ == module.__name__
    # todo better assertion for wack_file.module


def test_wack_file_module_with_raise(tempdir):
    with open("wack.py", "w+") as f:
        f.write('def hello(): raise ValueError("this is a test")')

    wack_file = WackFile(".")

    assert wack_file.module.hello
    assert isinstance(wack_file.module.hello, types.FunctionType)

    with pytest.raises(ValueError, match="this is a test"):
        wack_file.module.hello()

    wack_file = WackFile(tempdir)


def test_wack_file_module_with_cls(tempdir):
    class Hello:
        def __init__(self, who):
            self.who = who

        def whats_up(self):
            return f"what's up {self.who}?"

        def __eq__(self, other):
            return type(self) == type(other) and self.who == other.who

    # cls = 'class Hello:\n    def __init__(self, who):\n        self.who = who\n\n    def whats_up(self):\n        return f"what\'s up {self.who}?"\n    def __eq__(self, other):\n        return self.who == other.who\n'

    src = inspect.getsource(Hello)

    with open("wack.py", "w+") as f:
        f.write(src.strip())

    # exec(cls)
    # NB not in namespace until exec
    hello_jack = Hello("jack")

    # quick check
    assert hello_jack.who == "jack"
    assert hello_jack.whats_up() == "what's up jack?"

    wack_file = WackFile(".")

    assert wack_file.module.Hello

    attr = "who"
    assert getattr(hello_jack, attr) == getattr(wack_file.module.Hello("jack"), attr)
    assert getattr(hello_jack, attr) != getattr(wack_file.module.Hello("jill"), attr)

    attr = "whats_up"
    assert (
            getattr(hello_jack, attr)() == getattr(wack_file.module.Hello("jack"), attr)()
    )
    assert (
            getattr(hello_jack, attr)() != getattr(wack_file.module.Hello("jill"), attr)()
    )


def test_cant_find_wack_py(tempdir):
    with pytest.raises(FileNotFoundError):
        _ = WackFile(".")

    with pytest.raises(FileNotFoundError):
        _ = WackFile(tempdir)

    with pytest.raises(FileNotFoundError):
        _ = WackFile.from_current_dir()

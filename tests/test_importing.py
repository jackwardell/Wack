import os
from pathlib import Path

import pytest

# from wack.importing import get_package
from wack.importing import get_wack_py


# from wack.importing import get_wack_py_dir


def test_get_package(tempdir):
    package = get_package()
    assert not package

    package_name = "crazy_badass_package"
    os.mkdir(package_name)
    with open(package_name + "/__init__.py", "w+") as _:
        pass

    package = get_package()
    assert package
    assert package == package_name

    package_name2 = "crazy_badass_package2"
    os.mkdir(package_name2)
    with open(package_name2 + "/__init__.py", "w+") as _:
        pass

    with pytest.raises(ValueError):
        _ = get_package()


def test_get_wack_py_dir(tempdir):
    with pytest.raises(ValueError):
        get_wack_py_dir(".")

    with open("wack.py", "w+") as _:
        pass

    assert isinstance(get_wack_py_dir("."), str)
    assert get_wack_py_dir(".") == tempdir

    os.mkdir("nested")
    os.chdir("nested")

    wack_dir = get_wack_py_dir(".")
    # todo: fix below
    # assert wack_dir == "/private" + tempdir


# import tempfile
# with tempfile.TemporaryDirectory() as temp_dir:
#     os.chdir(temp_dir)
#     get_wack_py_dir(".")


def test_get_wack_py(tempdir):
    with pytest.raises(ValueError):
        get_wack_py()

    with open("wack.py", "w+") as _:
        pass

    assert isinstance(get_wack_py(), str)
    assert str(get_wack_py()) == tempdir + "/wack.py"

    nested_files = ['nest1', 'nest2', 'nest3']
    for i in nested_files:
        os.mkdir(i)
        os.chdir(i)

    assert str(os.getcwd()) == tempdir + "/" + "/".join(nested_files)
    # assert False

    # todo: fix below
    # assert get_wack_py() == tempdir + "/wack.py"

# def test_import_wack(tempdir):
#     import_wack()

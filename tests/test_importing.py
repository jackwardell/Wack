from wack.importing import find_file_recursively_backwards, get_wack_py, import_wack
import os
import pytest


def make_file(filename, directory):
    # make file
    file_to_find = directory / filename
    file_to_find.touch()
    # quick check
    assert file_to_find.exists()
    assert filename in os.listdir()
    return file_to_find


def make_dir(dirname, directory):
    # make dir
    dir_to_make = directory / dirname
    dir_to_make.mkdir()
    # quick check
    assert dir_to_make.exists()
    assert dirname in os.listdir()
    os.chdir(dir_to_make)
    assert not os.listdir()
    return dir_to_make


def make_dirs(dir_names, directory):
    for dir_name in dir_names:
        directory = make_dir(dir_name, directory)
    return directory


def test_find_file_recursively_no_file(tempdir):
    with pytest.raises(FileNotFoundError):
        find_file_recursively_backwards("hell0.world", tempdir)


def test_find_file_recursively_same_dir(tempdir):
    filename = 'hello.world'
    file_to_find = make_file(filename, tempdir)
    file_found = find_file_recursively_backwards(filename, tempdir)
    assert str(file_found) == str(file_to_find)


def test_find_file_recursively_backwards_once(tempdir):
    # make file
    filename = 'hello.world'
    file_to_find = make_file(filename, tempdir)

    # make dir
    dirname = "some-directory"
    dir_to_make = make_dir(dirname, tempdir)
    file_found = find_file_recursively_backwards(filename, dir_to_make)
    assert str(file_found) == str(file_to_find)


def test_find_file_recursively_backwards_10_times(tempdir):
    # make file
    filename = 'hello.world'
    file_to_find = make_file(filename, tempdir)

    # make dirs
    dir_to_make = make_dirs([f"dir-{i}" for i in range(10)], tempdir)

    # dir_to_make = make_dirs(dirs, tempdir)
    file_found = find_file_recursively_backwards(filename, dir_to_make)
    assert str(file_found) == str(file_to_find)


def test_get_wack_py_no_file(tempdir):
    with pytest.raises(FileNotFoundError):
        get_wack_py()


def test_get_wack_py_same_file(tempdir):
    wack_py = make_file('wack.py', tempdir)
    assert str(get_wack_py()) == str(wack_py)


def test_get_wack_py_backwards_once(tempdir):
    filename = 'wack.py'
    wack_py = make_file(filename, tempdir)
    # make dir
    make_dir("some-directory", tempdir)
    assert str(get_wack_py()) == str(wack_py)


def test_get_wack_py_backwards_10_times(tempdir):
    filename = 'wack.py'
    wack_py = make_file(filename, tempdir)
    # make dirs
    make_dirs([f"dir-{i}" for i in range(10)], tempdir)
    assert str(get_wack_py()) == str(wack_py)


def test_import_wack_py(tempdir):
    wack_py = make_file('wack.py', tempdir)
    with open(wack_py, "w") as f:
        f.write("a = 1")

    wack = import_wack()
    assert getattr(wack, "a") == 1
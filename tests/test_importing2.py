from wack.importing import find_file_recursively_backwards
import os


def test_find_file_recursively_backwards_once(tempdir):
    assert False
    # make file
    filename = "hello.world"
    file_to_find = tempdir / filename
    file_to_find.touch()
    # quick check
    assert file_to_find.exists()

    # make dir
    dirname = "kjadsfkad"
    dir_to_make = tempdir / dirname
    dir_to_make.mkdir()
    # quick check
    assert dir_to_make.exists()

    # quick check to make sure file and folder created
    assert filename in os.listdir()
    assert dirname in os.listdir()

    # change into folder
    os.chdir(dir_to_make)

    # quick check to make sure folder is empty
    assert not os.listdir()

    file_found = find_file_recursively_backwards(filename, dir_to_make)

    assert str(file_found) == str(file_to_find)

# import os
# from pathlib import Path
#
# import pytest
#
# # from wack.importing import get_package
# from wack.importing import get_wack_py
#
#
# # from wack.importing import get_wack_py_dir
#
#
# def test_get_package(tempdir):
#     package = get_package()
#     assert not package
#
#     package_name = "crazy_badass_package"
#     os.mkdir(package_name)
#     with open(package_name + "/__init__.py", "w+") as _:
#         pass
#
#     package = get_package()
#     assert package
#     assert package == package_name
#
#     package_name2 = "crazy_badass_package2"
#     os.mkdir(package_name2)
#     with open(package_name2 + "/__init__.py", "w+") as _:
#         pass
#
#     with pytest.raises(ValueError):
#         _ = get_package()
#
#
# def test_get_wack_py_dir(tempdir):
#     with pytest.raises(ValueError):
#         get_wack_py_dir(".")
#
#     with open("wack.py", "w+") as _:
#         pass
#
#     assert isinstance(get_wack_py_dir("."), str)
#     assert get_wack_py_dir(".") == tempdir
#
#     os.mkdir("nested")
#     os.chdir("nested")
#
#     wack_dir = get_wack_py_dir(".")
#     # todo: fix below
#     # assert wack_dir == "/private" + tempdir
#
#
# # import tempfile
# # with tempfile.TemporaryDirectory() as temp_dir:
# #     os.chdir(temp_dir)
# #     get_wack_py_dir(".")
#
#
# def test_get_wack_py(tempdir):
#     with pytest.raises(ValueError):
#         get_wack_py()
#
#     with open("wack.py", "w+") as _:
#         pass
#
#     assert isinstance(get_wack_py(), str)
#     assert str(get_wack_py()) == tempdir + "/wack.py"
#
#     nested_files = ['nest1', 'nest2', 'nest3']
#     for i in nested_files:
#         os.mkdir(i)
#         os.chdir(i)
#
#     assert str(os.getcwd()) == tempdir + "/" + "/".join(nested_files)
#     # assert False
#
#     # todo: fix below
#     # assert get_wack_py() == tempdir + "/wack.py"
#
# # def test_import_wack(tempdir):
# #     import_wack()
# import importlib.util
# import inspect
# import os
# import types
#
# import pytest
#
# from wack.helpers import File
# from wack.helpers import get_wack_file
#
#
# def test_wack_file_init_in_cwd_as_dot(tempdir):
#     """test when there is a wack.py in cwd, but using '.' as the path"""
#
#     filename = "hello_world.txt"
#     tempdir_wack_py = tempdir + "/" + filename
#
#     # make a wack file
#     with open(filename, "w+") as _:
#         pass
#
#     # quick check file has been created
#     assert os.path.exists(tempdir_wack_py)
#
#     # test current working dir
#     wack_file = get_wack_file()
#
#     # test object instantiated
#     assert wack_file
#     assert isinstance(wack_file, File)
#
#     # test we get right filepath
#     # expecting: tempdir/wack.py
#     assert wack_file.filepath == tempdir_wack_py
#     # expecting: tempdir
#     assert wack_file.dir == tempdir
#
#
# def test_wack_file_init_in_cwd_as_path(tempdir):
#     """test when there is a wack.py in cwd, but using absolute path"""
#
#     wack_file = "wack.py"
#     tempdir_wack_py = tempdir + "/" + wack_file
#
#     # make a wack file
#     with open(wack_file, "w+") as _:
#         pass
#
#     # quick check file has been created
#     assert os.path.exists(tempdir_wack_py)
#
#     cwd = os.getcwd()
#     # quick check it's tempdir
#     assert cwd == tempdir
#
#     # test current working dir as path
#     wack_file = get_wack_file()
#
#     # test object instantiated
#     assert wack_file
#     assert isinstance(wack_file, File)
#
#     # test we get right filepath
#     # expecting: tempdir/wack.py
#     assert wack_file.filepath == tempdir_wack_py
#     # expecting: tempdir
#     assert wack_file.dir == tempdir
#
#
# def test_wack_file_init_breaks(tempdir):
#     """test when file doesn't exist it breaks"""
#
#     with pytest.raises(FileNotFoundError):
#         get_wack_file()
#
#
# def test_get_wack_file_from_child_dir(tempdir):
#     """test if wack file is found from a child dir of temp dir with wack.py in"""
#
#     wack_file = "wack.py"
#     tempdir_wack_py = tempdir + "/" + wack_file
#
#     # make a wack file
#     with open(wack_file, "w+") as _:
#         pass
#
#     # quick check file has been created
#     assert os.path.exists(tempdir_wack_py)
#
#     # make a new dir and cd into
#     new_dir = "new_dir"
#     os.mkdir(new_dir)
#     os.chdir(new_dir)
#
#     # quick check we're where we want to be
#     assert os.getcwd() == tempdir + "/" + new_dir
#
#     # use parent dir
#     wack_file = get_wack_file()
#
#     # test object instantiated
#     assert wack_file
#     assert isinstance(wack_file, File)
#
#     # test we get right filepath
#     # expecting: tempdir/wack.py
#     assert wack_file.filepath == tempdir_wack_py
#     # expecting: tempdir
#     assert wack_file.dir == tempdir
#
#
# def test_wack_file_import_module_breaks(tempdir):
#     wack_file = "wack.py"
#
#     # make a wack file
#     with open(wack_file, "w+") as f:
#         # make it break
#         f.write("bakldnklans=")
#
#     # get the file
#     wack_file = get_wack_file()
#
#     # should break due to syntax error when used as module
#     with pytest.raises(ImportError):
#         wack_file.as_module()
#
#
# # TODO: use for file tests?
# def test_wack_file_from_current_dir(tempdir):
#     wack_file = "wack.py"
#     tempdir_wack_py = tempdir + "/" + wack_file
#
#     # make a wack file
#     with open(wack_file, "w+") as _:
#         pass
#
#     # quick check file has been created
#     assert os.path.exists(tempdir_wack_py)
#
#     # make a new dir and cd into
#     new_dir = "new_dir"
#     os.mkdir(new_dir)
#     os.chdir(new_dir)
#
#     cwd = os.getcwd()
#     # quick check it's tempdir + new dir
#     assert cwd == tempdir + "/" + new_dir
#
#     # this should be able to find the wack.py
#     # it will iterate through parents to get it
#     wack_file = get_wack_file()
#
#     # test object instantiated
#     assert wack_file
#     assert isinstance(wack_file, File)
#
#     # make sure its parents file
#     assert wack_file.dir == tempdir
#
#     # make sure its the file created above
#     assert wack_file.filepath == tempdir_wack_py
#
#
# def test_multiple_nesting(tempdir):
#     wack_file = "wack.py"
#     tempdir_wack_py = tempdir + "/" + wack_file
#
#     # make a wack file
#     with open(wack_file, "w+") as _:
#         pass
#
#     # quick check file has been created
#     assert os.path.exists(tempdir_wack_py)
#
#     # make and cd into new folders
#     nested_files = ["nest1", "nest2", "nest3"]
#     for i in nested_files:
#         os.mkdir(i)
#         os.chdir(i)
#
#     wack_file = get_wack_file()
#
#     # test object instantiated
#     assert wack_file
#     assert isinstance(wack_file, File)
#
#     # make sure its parents file
#     assert wack_file.dir == tempdir
#
#     # make sure its the file created above
#     assert wack_file.filepath == tempdir_wack_py
#
#
# def test_insane_nesting(tempdir):
#     wack_file = "wack.py"
#     tempdir_wack_py = tempdir + "/" + wack_file
#
#     # make a wack file
#     with open(wack_file, "w+") as _:
#         pass
#
#     # quick check file has been created
#     assert os.path.exists(tempdir_wack_py)
#
#     # make and cd into new folders
#     nested_files = [f"nest{i}" for i in range(25)]
#     for i in nested_files:
#         os.mkdir(i)
#         os.chdir(i)
#
#     # quick check we are where we want to be
#     assert os.getcwd() == tempdir + "/" + "/".join(nested_files)
#
#     wack_file = get_wack_file()
#
#     # test object instantiated
#     assert wack_file
#     assert isinstance(wack_file, File)
#
#     # make sure its parents file
#     assert wack_file.dir == tempdir
#
#     # make sure its the file created above
#     assert wack_file.filepath == tempdir_wack_py
#
#
# def test_wack_file_module(tempdir):
#     with open("wack.py", "w+") as _:
#         pass
#
#     wack_file = get_wack_file()
#     # assert isinstance(wack_file.module, types.ModuleType)
#     assert isinstance(wack_file.as_module, types.MethodType)
#
#     spec = importlib.util.spec_from_file_location("wack", tempdir + "/wack.py")
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#
#     # assert wack_file.module.__name__ == module.__name__
#     assert wack_file.as_module().__name__ == module.__name__
#     # todo better assertion for wack_file.module
#
#
# def test_wack_file_module_with_raise(tempdir):
#     with open("wack.py", "w+") as f:
#         f.write('def hello(): raise ValueError("this is a test")')
#
#     wack_file = get_wack_file()
#
#     assert wack_file.as_module().hello
#     assert isinstance(wack_file.as_module().hello, types.FunctionType)
#
#     with pytest.raises(ValueError, match="this is a test"):
#         wack_file.as_module().hello()
#
#
# def test_wack_file_module_with_cls(tempdir):
#     class Hello:
#         def __init__(self, who):
#             self.who = who
#
#         def whats_up(self):
#             return f"what's up {self.who}?"
#
#         def __eq__(self, other):
#             return type(self) == type(other) and self.who == other.who
#
#     src = inspect.getsource(Hello)
#
#     with open("wack.py", "w+") as f:
#         f.write(src.strip())
#
#     hello_jack = Hello("jack")
#
#     # quick check
#     assert hello_jack.who == "jack"
#     assert hello_jack.whats_up() == "what's up jack?"
#
#     wack_file = get_wack_file()
#
#     assert wack_file.as_module().Hello
#
#     attr = "who"
#     assert getattr(hello_jack, attr) == getattr(wack_file.as_module().Hello("jack"), attr)
#     assert getattr(hello_jack, attr) != getattr(wack_file.as_module().Hello("jill"), attr)
#
#     attr = "whats_up"
#     assert (
#             getattr(hello_jack, attr)() == getattr(wack_file.as_module().Hello("jack"), attr)()
#     )
#     assert (
#             getattr(hello_jack, attr)() != getattr(wack_file.as_module().Hello("jill"), attr)()
#     )
#
#
# def test_cant_find_wack_py(tempdir):
#     with pytest.raises(FileNotFoundError):
#         _ = get_wack_file()

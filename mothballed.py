# # # # # # # import os
# # # # # # # from abc import ABC
# # # # # # #
# # # # # # # import jinja2
# # # # # # #
# # # # # # # THIS_DIR = os.path.dirname(os.path.realpath(__file__))
# # # # # # # TEMPLATES_DIR = THIS_DIR + "/templates"
# # # # # # #
# # # # # # #
# # # # # # # # todo use pathlib
# # # # # # #
# # # # # # # # todo refactor this
# # # # # # # class Entity:
# # # # # # #     def __init__(self, **kwargs):
# # # # # # #         for k, v in kwargs.items():
# # # # # # #             setattr(self, k, v)
# # # # # # #
# # # # # # #     def __bool__(self):
# # # # # # #         return all([i for i in vars(self).values()])
# # # # # # #
# # # # # # #
# # # # # # # class BuildResource(ABC):
# # # # # # #     @property
# # # # # # #     def resource(self):
# # # # # # #         raise NotImplementedError()
# # # # # # #
# # # # # # #     @property
# # # # # # #     def filename(self):
# # # # # # #         return self.resource
# # # # # # #
# # # # # # #     @property
# # # # # # #     def filename_parts(self):
# # # # # # #         return self.filename.split("/")
# # # # # # #
# # # # # # #     @property
# # # # # # #     def resource_parts(self):
# # # # # # #         return self.resource.split("/")
# # # # # # #
# # # # # # #     @property
# # # # # # #     def content(self):
# # # # # # #         return ""
# # # # # # #
# # # # # # #     def is_done(self):
# # # # # # #         path = "."
# # # # # # #         for part in self.filename_parts:
# # # # # # #             if part not in os.listdir(path):
# # # # # # #                 return False
# # # # # # #             else:
# # # # # # #                 path += "/" + part
# # # # # # #                 continue
# # # # # # #         return True
# # # # # # #
# # # # # # #     def not_done(self):
# # # # # # #         return not self.is_done()
# # # # # # #
# # # # # # #     def do(self, force=False):
# # # # # # #         if self.not_done() or force:
# # # # # # #             dirname = os.path.dirname(self.filename)
# # # # # # #             if dirname and not os.path.exists(dirname):
# # # # # # #                 os.makedirs(dirname)
# # # # # # #             with open(self.filename, "w+") as f:
# # # # # # #                 f.write(self.content)
# # # # # # #             return True
# # # # # # #         else:
# # # # # # #             return False
# # # # # # #
# # # # # # #     def undo(self):
# # # # # # #         if self.is_done():
# # # # # # #             os.remove(self.filename)
# # # # # # #             return True
# # # # # # #         else:
# # # # # # #             return False
# # # # # # #
# # # # # # #
# # # # # # # class BuildTemplate(BuildResource, ABC):
# # # # # # #     @property
# # # # # # #     def jinja_template_filename(self):
# # # # # # #         return TEMPLATES_DIR + "/" + self.resource + ".jinja2"
# # # # # # #
# # # # # # #     @property
# # # # # # #     def template(self):
# # # # # # #         with open(self.jinja_template_filename) as f:
# # # # # # #             return f.read()
# # # # # # #
# # # # # # #     @property
# # # # # # #     def content(self):
# # # # # # #         return self.render_template()
# # # # # # #
# # # # # # #     def render_template(self):
# # # # # # #         return ""
# # # # # # #
# # # # # # #
# # # # # # # class PipInstallable(BuildTemplate):
# # # # # # #     resource = "setup.py"
# # # # # # #
# # # # # # #     def __init__(
# # # # # # #         self, project_name, version="0.1.0", cli_command="", cli_func=""
# # # # # # #     ):
# # # # # # #         self.project_name = project_name
# # # # # # #         self.version = version
# # # # # # #         self.requirements = []
# # # # # # #         self.entry_point = Entity(cli_command=cli_command, cli_func=cli_func)
# # # # # # #
# # # # # # #     def render_template(self):
# # # # # # #         template = jinja2.Template(self.template)
# # # # # # #         rendered_template = template.render(
# # # # # # #             name=self.project_name,
# # # # # # #             version=self.version,
# # # # # # #             requirements=self.requirements,
# # # # # # #             entry_point=self.entry_point,
# # # # # # #         )
# # # # # # #         return rendered_template
# # # # # # #
# # # # # # #
# # # # # # # class PackageBuilt(BuildResource):
# # # # # # #     resource = "{package_name}/__init__.py"
# # # # # # #
# # # # # # #     def __init__(self, package_name):
# # # # # # #         self.package_name = package_name
# # # # # # #         self.resource = self.resource.format(package_name=self.package_name)
# # # # # # #
# # # # # # #
# # # # # # # class WackBuilt(BuildTemplate):
# # # # # # #     resource = "wack.py"
# # # # # # #
# # # # # # #     def render_template(self):
# # # # # # #         template = jinja2.Template(self.template)
# # # # # # #         return template.render()
# # # # # # #
# # # # # # #
# # # # # # # class PreCommitConfigBuilt(BuildTemplate):
# # # # # # #     resource = "pre-commit-config.yaml"
# # # # # # #     filename = ".pre-commit-config.yaml"
# # # # # # #
# # # # # # #     def render_template(self):
# # # # # # #         template = jinja2.Template(self.template)
# # # # # # #         return template.render()
# # # # # # #
# # # # # # #
# # # # # # # class TravisPyPiYAMLBuilt(BuildTemplate):
# # # # # # #     resource = "travis.yml"
# # # # # # #     filename = ".travis.yml"
# # # # # # #
# # # # # # #     def render_template(self):
# # # # # # #         template = jinja2.Template(self.template)
# # # # # # #         return template.render()
# # # # # # import click
# # # # # # from wack.importing import import_wack
# # # # # #
# # # # # #
# # # # # # class WackCommand(click.Command):
# # # # # #     pass
# # # # # #
# # # # # #
# # # # # # echo = click.echo
# # # # # #
# # # # # #
# # # # # # def command(*args, **kwargs):
# # # # # #     """copied from click.decorators.command"""
# # # # # #     from click.decorators import command
# # # # # #
# # # # # #     def decorator(f):
# # # # # #         # todo allow passing of other Command classes
# # # # # #         kwargs["cls"] = WackCommand
# # # # # #         cmd = command(*args, **kwargs)(f)
# # # # # #         return cmd
# # # # # #
# # # # # #     return decorator
# # # # # #
# # # # # #
# # # # # # class CLI(click.Group):
# # # # # #     """custom base cli for $ wack"""
# # # # # #
# # # # # #     def __init__(self, *args, **kwargs):
# # # # # #         super().__init__(*args, **kwargs)
# # # # # #         self.add_commands()
# # # # # #
# # # # # #     def add_commands(self):
# # # # # #         """add commands from wack.py to cli"""
# # # # # #         try:
# # # # # #             wack = import_wack()
# # # # # #             for name, item in vars(wack).items():
# # # # # #                 if isinstance(item, WackCommand):
# # # # # #                     self.add_command(item, name=name)
# # # # # #         except FileNotFoundError:
# # # # # #             pass
# # # # # import importlib.util
# # # # # import os
# # # # # from pathlib import Path
# # # # #
# # # # #
# # # # # def find_file_recursively_backwards(file, directory) -> Path:
# # # # #     directory = Path(directory).resolve()
# # # # #     if file in os.listdir(directory):
# # # # #         return directory / file
# # # # #     elif directory.as_posix() == "/":
# # # # #         raise FileNotFoundError(f"{file} not found")
# # # # #     else:
# # # # #         return find_file_recursively_backwards(file, directory.parent)
# # # # #
# # # # #
# # # # # def get_wack_py() -> Path:
# # # # #     return find_file_recursively_backwards("wack.py", Path.cwd())
# # # # #
# # # # #
# # # # # def import_wack():
# # # # #     wack_py = get_wack_py()
# # # # #     spec = importlib.util.spec_from_file_location(wack_py.stem, wack_py)
# # # # #     module = importlib.util.module_from_spec(spec)
# # # # #     spec.loader.exec_module(module)
# # # # #     return module
# # # # #
# # # # #
# # # # # class PackageNotFoundError(Exception):
# # # # #     pass
# # # # #
# # # # #
# # # # # class TooManyPackagesFound(Exception):
# # # # #     pass
# # # # #
# # # # #
# # # # # def get_package():
# # # # #     packages = [
# # # # #         package
# # # # #         for package in os.listdir(".")
# # # # #         if os.path.isdir(package)
# # # # #         and "__init__.py" in os.listdir("./" + package)
# # # # #     ]
# # # # #     if len(packages) > 1:
# # # # #         # todo allow more packages?
# # # # #         raise TooManyPackagesFound("Only one package allowed")
# # # # #     elif len(packages) == 0:
# # # # #         raise PackageNotFoundError("No package found")
# # # # #     else:
# # # # #         return packages.pop()
# # # # import subprocess
# # # # import sys
# # # #
# # # # import click
# # # # from wack.builders import PackageBuilt
# # # # from wack.builders import PipInstallable
# # # # from wack.builders import PreCommitConfigBuilt
# # # # from wack.builders import TravisPyPiYAMLBuilt
# # # # from wack.builders import WackBuilt
# # # # from wack.core import CLI
# # # # from wack.importing import get_package
# # # #
# # # # cli = CLI()
# # # #
# # # #
# # # # @cli.command()
# # # # @click.option("--force", "-f", required=False, default=False, is_flag=True)
# # # # def init(force):
# # # #     wack_built = WackBuilt()
# # # #     done = wack_built.do(force=force)
# # # #     message = (
# # # #         "Built wack.py file"
# # # #         if done
# # # #         else "wack.py file already exists, use --force to overwrite"
# # # #     )
# # # #     click.echo(message)
# # # #
# # # #
# # # # class NoDistributionFound(Exception):
# # # #     pass
# # # #
# # # #
# # # # @cli.command()
# # # # @click.argument("package")
# # # # def install(package):
# # # #     # todo add option to add to requirements.txt
# # # #     try:
# # # #         subprocess.check_call(
# # # #             [sys.executable, "-m", "pip", "install", package]
# # # #         )
# # # #     except subprocess.CalledProcessError:
# # # #         raise NoDistributionFound(f"No distribution found called: {package}")
# # # #
# # # #
# # # # @cli.group()
# # # # def make():
# # # #     pass
# # # #
# # # #
# # # # @make.command()
# # # # @click.argument("project", required=False)
# # # # @click.option("--force", "-f", required=False, default=False, is_flag=True)
# # # # @click.option("--entry-points", nargs=2, required=False, default=("", ""))
# # # # def installable(project, force, entry_points):
# # # #     project_name = project if project else get_package()
# # # #     click.echo("Building setup.py for: " + project_name)
# # # #     command, func = entry_points
# # # #     pip_installable = PipInstallable(
# # # #         project_name, cli_command=command, cli_func=func
# # # #     )
# # # #     done = pip_installable.do(force=force)
# # # #     message = (
# # # #         "Built setup.py file"
# # # #         if done
# # # #         else "setup.py file already exists, use --force to overwrite"
# # # #     )
# # # #     click.echo(message)
# # # #
# # # #
# # # # @make.command()
# # # # @click.argument("name")
# # # # @click.option("--force", "-f", required=False, default=False, is_flag=True)
# # # # def package(name, force):
# # # #     package_built = PackageBuilt(name)
# # # #     done = package_built.do(force=force)
# # # #     message = (
# # # #         "Built {name}/__init__.py file"
# # # #         if done
# # # #         else f"{name}/__init__.py file already exists, "
# # # #         "use --force to overwrite"
# # # #     )
# # # #     click.echo(message)
# # # #
# # # #
# # # # @make.command()
# # # # @click.option("--force", "-f", required=False, default=False, is_flag=True)
# # # # def pre_commit(force):
# # # #     package_built = PreCommitConfigBuilt()
# # # #     done = package_built.do(force=force)
# # # #     message = (
# # # #         "Built .pre-commit-config.yaml file"
# # # #         if done
# # # #         else ".pre-commit-config.yaml file already exists, "
# # # #         "use --force to overwrite"
# # # #     )
# # # #     click.echo(message)
# # # #
# # # #
# # # # @make.command()
# # # # @click.option("--force", "-f", required=False, default=False, is_flag=True)
# # # # def travis(force):
# # # #     package_built = TravisPyPiYAMLBuilt()
# # # #     done = package_built.do(force=force)
# # # #     message = (
# # # #         "Built .travis.yaml file"
# # # #         if done
# # # #         else ".travis.yaml file already exists, use --force to overwrite"
# # # #     )
# # # #     click.echo(message)
# # # # import os
# # # # from pathlib import Path
# # # #
# # # # import pytest
# # # #
# # # # # from wack.importing import get_package
# # # # from wack.importing import get_wack_py
# # # #
# # # #
# # # # # from wack.importing import get_wack_py_dir
# # # #
# # # #
# # # # def test_get_package(tempdir):
# # # #     package = get_package()
# # # #     assert not package
# # # #
# # # #     package_name = "crazy_badass_package"
# # # #     os.mkdir(package_name)
# # # #     with open(package_name + "/__init__.py", "w+") as _:
# # # #         pass
# # # #
# # # #     package = get_package()
# # # #     assert package
# # # #     assert package == package_name
# # # #
# # # #     package_name2 = "crazy_badass_package2"
# # # #     os.mkdir(package_name2)
# # # #     with open(package_name2 + "/__init__.py", "w+") as _:
# # # #         pass
# # # #
# # # #     with pytest.raises(ValueError):
# # # #         _ = get_package()
# # # #
# # # #
# # # # def test_get_wack_py_dir(tempdir):
# # # #     with pytest.raises(ValueError):
# # # #         get_wack_py_dir(".")
# # # #
# # # #     with open("wack.py", "w+") as _:
# # # #         pass
# # # #
# # # #     assert isinstance(get_wack_py_dir("."), str)
# # # #     assert get_wack_py_dir(".") == tempdir
# # # #
# # # #     os.mkdir("nested")
# # # #     os.chdir("nested")
# # # #
# # # #     wack_dir = get_wack_py_dir(".")
# # # #     # todo: fix below
# # # #     # assert wack_dir == "/private" + tempdir
# # # #
# # # #
# # # # # import tempfile
# # # # # with tempfile.TemporaryDirectory() as temp_dir:
# # # # #     os.chdir(temp_dir)
# # # # #     get_wack_py_dir(".")
# # # #
# # # #
# # # # def test_get_wack_py(tempdir):
# # # #     with pytest.raises(ValueError):
# # # #         get_wack_py()
# # # #
# # # #     with open("wack.py", "w+") as _:
# # # #         pass
# # # #
# # # #     assert isinstance(get_wack_py(), str)
# # # #     assert str(get_wack_py()) == tempdir + "/wack.py"
# # # #
# # # #     nested_files = ['nest1', 'nest2', 'nest3']
# # # #     for i in nested_files:
# # # #         os.mkdir(i)
# # # #         os.chdir(i)
# # # #
# # # #     assert str(os.getcwd()) == tempdir + "/" + "/".join(nested_files)
# # # #     # assert False
# # # #
# # # #     # todo: fix below
# # # #     # assert get_wack_py() == tempdir + "/wack.py"
# # # #
# # # # # def test_import_wack(tempdir):
# # # # #     import_wack()
# # # # import importlib.util
# # # # import inspect
# # # # import os
# # # # import types
# # # #
# # # # import pytest
# # # #
# # # # from wack.helpers import File
# # # # from wack.helpers import get_wack_file
# # # #
# # # #
# # # # def test_wack_file_init_in_cwd_as_dot(tempdir):
# # # #     """test when there is a wack.py in cwd, but using '.' as the path"""
# # # #
# # # #     filename = "hello_world.txt"
# # # #     tempdir_wack_py = tempdir + "/" + filename
# # # #
# # # #     # make a wack file
# # # #     with open(filename, "w+") as _:
# # # #         pass
# # # #
# # # #     # quick check file has been created
# # # #     assert os.path.exists(tempdir_wack_py)
# # # #
# # # #     # test current working dir
# # # #     wack_file = get_wack_file()
# # # #
# # # #     # test object instantiated
# # # #     assert wack_file
# # # #     assert isinstance(wack_file, File)
# # # #
# # # #     # test we get right filepath
# # # #     # expecting: tempdir/wack.py
# # # #     assert wack_file.filepath == tempdir_wack_py
# # # #     # expecting: tempdir
# # # #     assert wack_file.dir == tempdir
# # # #
# # # #
# # # # def test_wack_file_init_in_cwd_as_path(tempdir):
# # # #     """test when there is a wack.py in cwd, but using absolute path"""
# # # #
# # # #     wack_file = "wack.py"
# # # #     tempdir_wack_py = tempdir + "/" + wack_file
# # # #
# # # #     # make a wack file
# # # #     with open(wack_file, "w+") as _:
# # # #         pass
# # # #
# # # #     # quick check file has been created
# # # #     assert os.path.exists(tempdir_wack_py)
# # # #
# # # #     cwd = os.getcwd()
# # # #     # quick check it's tempdir
# # # #     assert cwd == tempdir
# # # #
# # # #     # test current working dir as path
# # # #     wack_file = get_wack_file()
# # # #
# # # #     # test object instantiated
# # # #     assert wack_file
# # # #     assert isinstance(wack_file, File)
# # # #
# # # #     # test we get right filepath
# # # #     # expecting: tempdir/wack.py
# # # #     assert wack_file.filepath == tempdir_wack_py
# # # #     # expecting: tempdir
# # # #     assert wack_file.dir == tempdir
# # # #
# # # #
# # # # def test_wack_file_init_breaks(tempdir):
# # # #     """test when file doesn't exist it breaks"""
# # # #
# # # #     with pytest.raises(FileNotFoundError):
# # # #         get_wack_file()
# # # #
# # # #
# # # # def test_get_wack_file_from_child_dir(tempdir):
# # # #     """test if wack file is found from a child dir of temp dir with wack.py in"""
# # # #
# # # #     wack_file = "wack.py"
# # # #     tempdir_wack_py = tempdir + "/" + wack_file
# # # #
# # # #     # make a wack file
# # # #     with open(wack_file, "w+") as _:
# # # #         pass
# # # #
# # # #     # quick check file has been created
# # # #     assert os.path.exists(tempdir_wack_py)
# # # #
# # # #     # make a new dir and cd into
# # # #     new_dir = "new_dir"
# # # #     os.mkdir(new_dir)
# # # #     os.chdir(new_dir)
# # # #
# # # #     # quick check we're where we want to be
# # # #     assert os.getcwd() == tempdir + "/" + new_dir
# # # #
# # # #     # use parent dir
# # # #     wack_file = get_wack_file()
# # # #
# # # #     # test object instantiated
# # # #     assert wack_file
# # # #     assert isinstance(wack_file, File)
# # # #
# # # #     # test we get right filepath
# # # #     # expecting: tempdir/wack.py
# # # #     assert wack_file.filepath == tempdir_wack_py
# # # #     # expecting: tempdir
# # # #     assert wack_file.dir == tempdir
# # # #
# # # #
# # # # def test_wack_file_import_module_breaks(tempdir):
# # # #     wack_file = "wack.py"
# # # #
# # # #     # make a wack file
# # # #     with open(wack_file, "w+") as f:
# # # #         # make it break
# # # #         f.write("bakldnklans=")
# # # #
# # # #     # get the file
# # # #     wack_file = get_wack_file()
# # # #
# # # #     # should break due to syntax error when used as module
# # # #     with pytest.raises(ImportError):
# # # #         wack_file.as_module()
# # # #
# # # #
# # # # # TODO: use for file tests?
# # # # def test_wack_file_from_current_dir(tempdir):
# # # #     wack_file = "wack.py"
# # # #     tempdir_wack_py = tempdir + "/" + wack_file
# # # #
# # # #     # make a wack file
# # # #     with open(wack_file, "w+") as _:
# # # #         pass
# # # #
# # # #     # quick check file has been created
# # # #     assert os.path.exists(tempdir_wack_py)
# # # #
# # # #     # make a new dir and cd into
# # # #     new_dir = "new_dir"
# # # #     os.mkdir(new_dir)
# # # #     os.chdir(new_dir)
# # # #
# # # #     cwd = os.getcwd()
# # # #     # quick check it's tempdir + new dir
# # # #     assert cwd == tempdir + "/" + new_dir
# # # #
# # # #     # this should be able to find the wack.py
# # # #     # it will iterate through parents to get it
# # # #     wack_file = get_wack_file()
# # # #
# # # #     # test object instantiated
# # # #     assert wack_file
# # # #     assert isinstance(wack_file, File)
# # # #
# # # #     # make sure its parents file
# # # #     assert wack_file.dir == tempdir
# # # #
# # # #     # make sure its the file created above
# # # #     assert wack_file.filepath == tempdir_wack_py
# # # #
# # # #
# # # # def test_multiple_nesting(tempdir):
# # # #     wack_file = "wack.py"
# # # #     tempdir_wack_py = tempdir + "/" + wack_file
# # # #
# # # #     # make a wack file
# # # #     with open(wack_file, "w+") as _:
# # # #         pass
# # # #
# # # #     # quick check file has been created
# # # #     assert os.path.exists(tempdir_wack_py)
# # # #
# # # #     # make and cd into new folders
# # # #     nested_files = ["nest1", "nest2", "nest3"]
# # # #     for i in nested_files:
# # # #         os.mkdir(i)
# # # #         os.chdir(i)
# # # #
# # # #     wack_file = get_wack_file()
# # # #
# # # #     # test object instantiated
# # # #     assert wack_file
# # # #     assert isinstance(wack_file, File)
# # # #
# # # #     # make sure its parents file
# # # #     assert wack_file.dir == tempdir
# # # #
# # # #     # make sure its the file created above
# # # #     assert wack_file.filepath == tempdir_wack_py
# # # #
# # # #
# # # # def test_insane_nesting(tempdir):
# # # #     wack_file = "wack.py"
# # # #     tempdir_wack_py = tempdir + "/" + wack_file
# # # #
# # # #     # make a wack file
# # # #     with open(wack_file, "w+") as _:
# # # #         pass
# # # #
# # # #     # quick check file has been created
# # # #     assert os.path.exists(tempdir_wack_py)
# # # #
# # # #     # make and cd into new folders
# # # #     nested_files = [f"nest{i}" for i in range(25)]
# # # #     for i in nested_files:
# # # #         os.mkdir(i)
# # # #         os.chdir(i)
# # # #
# # # #     # quick check we are where we want to be
# # # #     assert os.getcwd() == tempdir + "/" + "/".join(nested_files)
# # # #
# # # #     wack_file = get_wack_file()
# # # #
# # # #     # test object instantiated
# # # #     assert wack_file
# # # #     assert isinstance(wack_file, File)
# # # #
# # # #     # make sure its parents file
# # # #     assert wack_file.dir == tempdir
# # # #
# # # #     # make sure its the file created above
# # # #     assert wack_file.filepath == tempdir_wack_py
# # # #
# # # #
# # # # def test_wack_file_module(tempdir):
# # # #     with open("wack.py", "w+") as _:
# # # #         pass
# # # #
# # # #     wack_file = get_wack_file()
# # # #     # assert isinstance(wack_file.module, types.ModuleType)
# # # #     assert isinstance(wack_file.as_module, types.MethodType)
# # # #
# # # #     spec = importlib.util.spec_from_file_location("wack", tempdir + "/wack.py")
# # # #     module = importlib.util.module_from_spec(spec)
# # # #     spec.loader.exec_module(module)
# # # #
# # # #     # assert wack_file.module.__name__ == module.__name__
# # # #     assert wack_file.as_module().__name__ == module.__name__
# # # #     # todo better assertion for wack_file.module
# # # #
# # # #
# # # # def test_wack_file_module_with_raise(tempdir):
# # # #     with open("wack.py", "w+") as f:
# # # #         f.write('def hello(): raise ValueError("this is a test")')
# # # #
# # # #     wack_file = get_wack_file()
# # # #
# # # #     assert wack_file.as_module().hello
# # # #     assert isinstance(wack_file.as_module().hello, types.FunctionType)
# # # #
# # # #     with pytest.raises(ValueError, match="this is a test"):
# # # #         wack_file.as_module().hello()
# # # #
# # # #
# # # # def test_wack_file_module_with_cls(tempdir):
# # # #     class Hello:
# # # #         def __init__(self, who):
# # # #             self.who = who
# # # #
# # # #         def whats_up(self):
# # # #             return f"what's up {self.who}?"
# # # #
# # # #         def __eq__(self, other):
# # # #             return type(self) == type(other) and self.who == other.who
# # # #
# # # #     src = inspect.getsource(Hello)
# # # #
# # # #     with open("wack.py", "w+") as f:
# # # #         f.write(src.strip())
# # # #
# # # #     hello_jack = Hello("jack")
# # # #
# # # #     # quick check
# # # #     assert hello_jack.who == "jack"
# # # #     assert hello_jack.whats_up() == "what's up jack?"
# # # #
# # # #     wack_file = get_wack_file()
# # # #
# # # #     assert wack_file.as_module().Hello
# # # #
# # # #     attr = "who"
# # # #     assert getattr(hello_jack, attr) == getattr(wack_file.as_module().Hello("jack"), attr)
# # # #     assert getattr(hello_jack, attr) != getattr(wack_file.as_module().Hello("jill"), attr)
# # # #
# # # #     attr = "whats_up"
# # # #     assert (
# # # #             getattr(hello_jack, attr)() == getattr(wack_file.as_module().Hello("jack"), attr)()
# # # #     )
# # # #     assert (
# # # #             getattr(hello_jack, attr)() != getattr(wack_file.as_module().Hello("jill"), attr)()
# # # #     )
# # # #
# # # #
# # # # def test_cant_find_wack_py(tempdir):
# # # #     with pytest.raises(FileNotFoundError):
# # # #         _ = get_wack_file()
# # # import os
# # # from abc import ABC
# # # from abc import ABCMeta
# # #
# # # import pytest
# # # from wack import PackageBuilt
# # # from wack import PipInstallable
# # # from wack.builders import BuildResource
# # # from wack.builders import BuildTemplate
# # #
# # # file_content = 'from setuptools import find_packages\nfrom setuptools import setup\n\nsetup(\n    name="{project_name}",\n    version="0.1.0",\n    packages=find_packages(),\n    include_package_data=True,\n    \n    \n)'
# # #
# # #
# # # def test_build_resource(tempdir):
# # #     assert isinstance(BuildResource, ABCMeta)
# # #     assert issubclass(BuildResource, ABC)
# # #
# # #     resource = BuildResource()
# # #     assert isinstance(resource, BuildResource)
# # #     assert resource
# # #
# # #     assert resource.content == ""
# # #     with pytest.raises(NotImplementedError):
# # #         assert resource.resource
# # #         assert resource.is_done()
# # #         assert resource.not_done()
# # #         assert resource.do()
# # #         assert resource.undo()
# # #
# # #
# # # def test_template_resource(tempdir):
# # #     assert isinstance(BuildTemplate, ABCMeta)
# # #     assert issubclass(BuildTemplate, BuildResource)
# # #     assert issubclass(BuildTemplate, ABC)
# # #
# # #     template = BuildTemplate()
# # #
# # #     with pytest.raises(NotImplementedError):
# # #         assert template.jinja_template_filename
# # #         assert template.template
# # #
# # #     assert template.content == ""
# # #     assert template.render_template() == ""
# # #
# # #
# # # def test_pip_installable(tempdir):
# # #     project_name = "Hello-World"
# # #     pip_installable = PipInstallable(project_name)
# # #
# # #     assert not pip_installable.is_done()
# # #     assert pip_installable.not_done()
# # #
# # #     assert not os.path.exists(tempdir / pip_installable.resource)
# # #
# # #     pip_installable.do()
# # #     assert pip_installable.is_done()
# # #     assert not pip_installable.not_done()
# # #
# # #     assert os.path.exists(tempdir / pip_installable.resource)
# # #
# # #     with open("setup.py") as f:
# # #         file = f.read()
# # #
# # #     assert file == file_content.format(project_name=project_name)
# # #
# # #     assert pip_installable.is_done()
# # #
# # #     pip_installable.do()
# # #     assert pip_installable.is_done()
# # #
# # #     pip_installable.undo()
# # #     assert pip_installable.not_done()
# # #
# # #     # if .do() and .undo() work they return True
# # #     # if the files already exist or don't for .do() and .undo() respectively
# # #     # then returns False
# # #     assert pip_installable.do()
# # #     assert not pip_installable.do()
# # #
# # #     assert pip_installable.undo()
# # #     assert not pip_installable.undo()
# # #
# # #     assert pip_installable.do()
# # #
# # #     new_project_name = "xXXX"
# # #     pip_installable.project_name = new_project_name
# # #
# # #     assert not pip_installable.do()
# # #     assert pip_installable.do(force=True)
# # #
# # #     with open("setup.py") as f:
# # #         file = f.read()
# # #     assert file == file_content.format(project_name=new_project_name)
# # #
# # #
# # # def test_build_package(tempdir):
# # #     package_name = "hello_world"
# # #     package_init = package_name + "/__init__.py"
# # #     package_built = PackageBuilt(package_name)
# # #     assert package_built
# # #     assert isinstance(package_built, PackageBuilt)
# # #
# # #     assert package_built.package_name == package_name
# # #     assert package_built.resource == f"{package_name}/__init__.py"
# # #
# # #     assert package_built.do()
# # #     assert package_built.is_done()
# # #
# # #     assert not package_built.do()
# # #
# # #     assert package_built.undo()
# # #     assert package_built.not_done()
# # #     assert not package_built.undo()
# # #
# # #     assert package_built.do()
# # #     with open(package_init) as f:
# # #         assert f.read() == ""
# # #
# # #     assert os.path.exists(package_init)
# # #
# # #     assert package_built.undo()
# # #     assert not os.path.exists(package_init)
# # import os
# #
# # from wack.cli import cli
# # from wack.cli import make
# # from wack.importing import PackageNotFoundError
# #
# # # import click
# #
# # file_content = 'from setuptools import find_packages\nfrom setuptools import setup\n\nsetup(\n    name="{project_name}",\n    version="0.1.0",\n    packages=find_packages(),\n    include_package_data=True,\n    \n    \n)'
# #
# #
# # def test_cli(tempdir, runner):
# #     result = runner.invoke(cli)
# #     assert result
# #     # assert result.stdout.startswith(
# #     #     "Usage: cli [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:"
# #     # )
# #     assert result.exit_code == 0
# #
# #
# # def test_make(tempdir, runner):
# #     result = runner.invoke(make)
# #     assert result.exit_code == 0
# #     assert "installable" in result.stdout
# #     assert "package" in result.stdout
# #
# #     word = "words-not-allowed"
# #     result = runner.invoke(make, [word])
# #     assert result.exit_code == 2
# #     assert "Error" in result.stdout
# #
# #
# # def test_make_installable_fails_no_package(tempdir, runner):
# #     result = runner.invoke(make, ["installable"])
# #     assert isinstance(result.exc_info[1], PackageNotFoundError)
# #
# #
# # def test_make_installable_works(tempdir, runner):
# #     pkg = tempdir / "random-pkg"
# #     pkg.mkdir()
# #     init = pkg / "__init__.py"
# #     init.touch()
# #
# #     result = runner.invoke(make, ["installable"])
# #     assert result.exit_code == 0
# #     assert (
# #         result.output
# #         == f"Building setup.py for: {pkg.stem}\nBuilt setup.py file\n"
# #     )
# #     with open("setup.py") as f:
# #         file = f.read()
# #     assert os.path.exists("setup.py")
# #     assert file == file_content.format(project_name=pkg.stem)
# #
# #
# # def test_make_installable_doesnt_work(tempdir, runner):
# #     pkg = tempdir / "random-pkg"
# #     pkg.mkdir()
# #     init = pkg / "__init__.py"
# #     init.touch()
# #     setup_py = tempdir / "setup.py"
# #     setup_py.touch()
# #
# #     result = runner.invoke(make, ["installable"])
# #     assert result.exit_code == 0
# #     assert "setup.py file already exists" in result.output
# #     assert "use --force to overwrite" in result.output
# #
# #
# # def test_make_installable_with_args(tempdir, runner):
# #     # project
# #     project_name = "Whatever"
# #     result = runner.invoke(make, ["installable", project_name])
# #     # check we get a correct result
# #     assert result.exit_code == 0
# #     # check text output is correct
# #     assert (
# #         result.output
# #         == f"Building setup.py for: {project_name}\nBuilt setup.py file\n"
# #     )
# #     result = runner.invoke(make, ["installable", project_name])
# #     assert (
# #         result.output
# #         == f"Building setup.py for: {project_name}\nsetup.py file already exists, use --force to overwrite\n"
# #     )
# #     result = runner.invoke(make, ["installable", project_name, "--force"])
# #     assert (
# #         result.output
# #         == f"Building setup.py for: {project_name}\nBuilt setup.py file\n"
# #     )
# #     # entry points
# import os
#
# import pytest
# from wack.importing import find_file_recursively_backwards
# from wack.importing import get_wack_py
# from wack.importing import import_wack
#
#
# def make_file(filename, directory):
#     # make file
#     file_to_find = directory / filename
#     file_to_find.touch()
#     # quick check
#     assert file_to_find.exists()
#     assert filename in os.listdir()
#     return file_to_find
#
#
# def make_dir(dirname, directory):
#     # make dir
#     dir_to_make = directory / dirname
#     dir_to_make.mkdir()
#     # quick check
#     assert dir_to_make.exists()
#     assert dirname in os.listdir()
#     os.chdir(dir_to_make)
#     assert not os.listdir()
#     return dir_to_make
#
#
# def make_dirs(dir_names, directory):
#     for dir_name in dir_names:
#         directory = make_dir(dir_name, directory)
#     return directory
#
#
# def test_find_file_recursively_no_file(tempdir):
#     with pytest.raises(FileNotFoundError):
#         find_file_recursively_backwards("hell0.world", tempdir)
#
#
# def test_find_file_recursively_same_dir(tempdir):
#     filename = "hello.world"
#     file_to_find = make_file(filename, tempdir)
#     file_found = find_file_recursively_backwards(filename, tempdir)
#     assert str(file_found) == str(file_to_find)
#
#
# def test_find_file_recursively_backwards_once(tempdir):
#     # make file
#     filename = "hello.world"
#     file_to_find = make_file(filename, tempdir)
#
#     # make dir
#     dirname = "some-directory"
#     dir_to_make = make_dir(dirname, tempdir)
#     file_found = find_file_recursively_backwards(filename, dir_to_make)
#     assert str(file_found) == str(file_to_find)
#
#
# def test_find_file_recursively_backwards_10_times(tempdir):
#     # make file
#     filename = "hello.world"
#     file_to_find = make_file(filename, tempdir)
#
#     # make dirs
#     dir_to_make = make_dirs([f"dir-{i}" for i in range(10)], tempdir)
#
#     # dir_to_make = make_dirs(dirs, tempdir)
#     file_found = find_file_recursively_backwards(filename, dir_to_make)
#     assert str(file_found) == str(file_to_find)
#
#
# def test_get_wack_py_no_file(tempdir):
#     with pytest.raises(FileNotFoundError):
#         get_wack_py()
#
#
# def test_get_wack_py_same_file(tempdir):
#     wack_py = make_file("wack.py", tempdir)
#     assert str(get_wack_py()) == str(wack_py)
#
#
# def test_get_wack_py_backwards_once(tempdir):
#     filename = "wack.py"
#     wack_py = make_file(filename, tempdir)
#     # make dir
#     make_dir("some-directory", tempdir)
#     assert str(get_wack_py()) == str(wack_py)
#
#
# def test_get_wack_py_backwards_10_times(tempdir):
#     filename = "wack.py"
#     wack_py = make_file(filename, tempdir)
#     # make dirs
#     make_dirs([f"dir-{i}" for i in range(10)], tempdir)
#     assert str(get_wack_py()) == str(wack_py)
#
#
# def test_import_wack_py(tempdir):
#     wack_py = make_file("wack.py", tempdir)
#     with open(wack_py, "w") as f:
#         f.write("a = 1")
#
#     wack = import_wack()
#     assert wack.a == 1

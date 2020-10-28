# # # # import os
# # # # from abc import ABC
# # # #
# # # # import jinja2
# # # #
# # # # THIS_DIR = os.path.dirname(os.path.realpath(__file__))
# # # # TEMPLATES_DIR = THIS_DIR + "/templates"
# # # #
# # # #
# # # # # todo use pathlib
# # # #
# # # # # todo refactor this
# # # # class Entity:
# # # #     def __init__(self, **kwargs):
# # # #         for k, v in kwargs.items():
# # # #             setattr(self, k, v)
# # # #
# # # #     def __bool__(self):
# # # #         return all([i for i in vars(self).values()])
# # # #
# # # #
# # # # class BuildResource(ABC):
# # # #     @property
# # # #     def resource(self):
# # # #         raise NotImplementedError()
# # # #
# # # #     @property
# # # #     def filename(self):
# # # #         return self.resource
# # # #
# # # #     @property
# # # #     def filename_parts(self):
# # # #         return self.filename.split("/")
# # # #
# # # #     @property
# # # #     def resource_parts(self):
# # # #         return self.resource.split("/")
# # # #
# # # #     @property
# # # #     def content(self):
# # # #         return ""
# # # #
# # # #     def is_done(self):
# # # #         path = "."
# # # #         for part in self.filename_parts:
# # # #             if part not in os.listdir(path):
# # # #                 return False
# # # #             else:
# # # #                 path += "/" + part
# # # #                 continue
# # # #         return True
# # # #
# # # #     def not_done(self):
# # # #         return not self.is_done()
# # # #
# # # #     def do(self, force=False):
# # # #         if self.not_done() or force:
# # # #             dirname = os.path.dirname(self.filename)
# # # #             if dirname and not os.path.exists(dirname):
# # # #                 os.makedirs(dirname)
# # # #             with open(self.filename, "w+") as f:
# # # #                 f.write(self.content)
# # # #             return True
# # # #         else:
# # # #             return False
# # # #
# # # #     def undo(self):
# # # #         if self.is_done():
# # # #             os.remove(self.filename)
# # # #             return True
# # # #         else:
# # # #             return False
# # # #
# # # #
# # # # class BuildTemplate(BuildResource, ABC):
# # # #     @property
# # # #     def jinja_template_filename(self):
# # # #         return TEMPLATES_DIR + "/" + self.resource + ".jinja2"
# # # #
# # # #     @property
# # # #     def template(self):
# # # #         with open(self.jinja_template_filename) as f:
# # # #             return f.read()
# # # #
# # # #     @property
# # # #     def content(self):
# # # #         return self.render_template()
# # # #
# # # #     def render_template(self):
# # # #         return ""
# # # #
# # # #
# # # # class PipInstallable(BuildTemplate):
# # # #     resource = "setup.py"
# # # #
# # # #     def __init__(
# # # #         self, project_name, version="0.1.0", cli_command="", cli_func=""
# # # #     ):
# # # #         self.project_name = project_name
# # # #         self.version = version
# # # #         self.requirements = []
# # # #         self.entry_point = Entity(cli_command=cli_command, cli_func=cli_func)
# # # #
# # # #     def render_template(self):
# # # #         template = jinja2.Template(self.template)
# # # #         rendered_template = template.render(
# # # #             name=self.project_name,
# # # #             version=self.version,
# # # #             requirements=self.requirements,
# # # #             entry_point=self.entry_point,
# # # #         )
# # # #         return rendered_template
# # # #
# # # #
# # # # class PackageBuilt(BuildResource):
# # # #     resource = "{package_name}/__init__.py"
# # # #
# # # #     def __init__(self, package_name):
# # # #         self.package_name = package_name
# # # #         self.resource = self.resource.format(package_name=self.package_name)
# # # #
# # # #
# # # # class WackBuilt(BuildTemplate):
# # # #     resource = "wack.py"
# # # #
# # # #     def render_template(self):
# # # #         template = jinja2.Template(self.template)
# # # #         return template.render()
# # # #
# # # #
# # # # class PreCommitConfigBuilt(BuildTemplate):
# # # #     resource = "pre-commit-config.yaml"
# # # #     filename = ".pre-commit-config.yaml"
# # # #
# # # #     def render_template(self):
# # # #         template = jinja2.Template(self.template)
# # # #         return template.render()
# # # #
# # # #
# # # # class TravisPyPiYAMLBuilt(BuildTemplate):
# # # #     resource = "travis.yml"
# # # #     filename = ".travis.yml"
# # # #
# # # #     def render_template(self):
# # # #         template = jinja2.Template(self.template)
# # # #         return template.render()
# # # import click
# # # from wack.importing import import_wack
# # #
# # #
# # # class WackCommand(click.Command):
# # #     pass
# # #
# # #
# # # echo = click.echo
# # #
# # #
# # # def command(*args, **kwargs):
# # #     """copied from click.decorators.command"""
# # #     from click.decorators import command
# # #
# # #     def decorator(f):
# # #         # todo allow passing of other Command classes
# # #         kwargs["cls"] = WackCommand
# # #         cmd = command(*args, **kwargs)(f)
# # #         return cmd
# # #
# # #     return decorator
# # #
# # #
# # # class CLI(click.Group):
# # #     """custom base cli for $ wack"""
# # #
# # #     def __init__(self, *args, **kwargs):
# # #         super().__init__(*args, **kwargs)
# # #         self.add_commands()
# # #
# # #     def add_commands(self):
# # #         """add commands from wack.py to cli"""
# # #         try:
# # #             wack = import_wack()
# # #             for name, item in vars(wack).items():
# # #                 if isinstance(item, WackCommand):
# # #                     self.add_command(item, name=name)
# # #         except FileNotFoundError:
# # #             pass
# # import importlib.util
# # import os
# # from pathlib import Path
# #
# #
# # def find_file_recursively_backwards(file, directory) -> Path:
# #     directory = Path(directory).resolve()
# #     if file in os.listdir(directory):
# #         return directory / file
# #     elif directory.as_posix() == "/":
# #         raise FileNotFoundError(f"{file} not found")
# #     else:
# #         return find_file_recursively_backwards(file, directory.parent)
# #
# #
# # def get_wack_py() -> Path:
# #     return find_file_recursively_backwards("wack.py", Path.cwd())
# #
# #
# # def import_wack():
# #     wack_py = get_wack_py()
# #     spec = importlib.util.spec_from_file_location(wack_py.stem, wack_py)
# #     module = importlib.util.module_from_spec(spec)
# #     spec.loader.exec_module(module)
# #     return module
# #
# #
# # class PackageNotFoundError(Exception):
# #     pass
# #
# #
# # class TooManyPackagesFound(Exception):
# #     pass
# #
# #
# # def get_package():
# #     packages = [
# #         package
# #         for package in os.listdir(".")
# #         if os.path.isdir(package)
# #         and "__init__.py" in os.listdir("./" + package)
# #     ]
# #     if len(packages) > 1:
# #         # todo allow more packages?
# #         raise TooManyPackagesFound("Only one package allowed")
# #     elif len(packages) == 0:
# #         raise PackageNotFoundError("No package found")
# #     else:
# #         return packages.pop()
# import subprocess
# import sys
#
# import click
# from wack.builders import PackageBuilt
# from wack.builders import PipInstallable
# from wack.builders import PreCommitConfigBuilt
# from wack.builders import TravisPyPiYAMLBuilt
# from wack.builders import WackBuilt
# from wack.core import CLI
# from wack.importing import get_package
#
# cli = CLI()
#
#
# @cli.command()
# @click.option("--force", "-f", required=False, default=False, is_flag=True)
# def init(force):
#     wack_built = WackBuilt()
#     done = wack_built.do(force=force)
#     message = (
#         "Built wack.py file"
#         if done
#         else "wack.py file already exists, use --force to overwrite"
#     )
#     click.echo(message)
#
#
# class NoDistributionFound(Exception):
#     pass
#
#
# @cli.command()
# @click.argument("package")
# def install(package):
#     # todo add option to add to requirements.txt
#     try:
#         subprocess.check_call(
#             [sys.executable, "-m", "pip", "install", package]
#         )
#     except subprocess.CalledProcessError:
#         raise NoDistributionFound(f"No distribution found called: {package}")
#
#
# @cli.group()
# def make():
#     pass
#
#
# @make.command()
# @click.argument("project", required=False)
# @click.option("--force", "-f", required=False, default=False, is_flag=True)
# @click.option("--entry-points", nargs=2, required=False, default=("", ""))
# def installable(project, force, entry_points):
#     project_name = project if project else get_package()
#     click.echo("Building setup.py for: " + project_name)
#     command, func = entry_points
#     pip_installable = PipInstallable(
#         project_name, cli_command=command, cli_func=func
#     )
#     done = pip_installable.do(force=force)
#     message = (
#         "Built setup.py file"
#         if done
#         else "setup.py file already exists, use --force to overwrite"
#     )
#     click.echo(message)
#
#
# @make.command()
# @click.argument("name")
# @click.option("--force", "-f", required=False, default=False, is_flag=True)
# def package(name, force):
#     package_built = PackageBuilt(name)
#     done = package_built.do(force=force)
#     message = (
#         "Built {name}/__init__.py file"
#         if done
#         else f"{name}/__init__.py file already exists, "
#         "use --force to overwrite"
#     )
#     click.echo(message)
#
#
# @make.command()
# @click.option("--force", "-f", required=False, default=False, is_flag=True)
# def pre_commit(force):
#     package_built = PreCommitConfigBuilt()
#     done = package_built.do(force=force)
#     message = (
#         "Built .pre-commit-config.yaml file"
#         if done
#         else ".pre-commit-config.yaml file already exists, "
#         "use --force to overwrite"
#     )
#     click.echo(message)
#
#
# @make.command()
# @click.option("--force", "-f", required=False, default=False, is_flag=True)
# def travis(force):
#     package_built = TravisPyPiYAMLBuilt()
#     done = package_built.do(force=force)
#     message = (
#         "Built .travis.yaml file"
#         if done
#         else ".travis.yaml file already exists, use --force to overwrite"
#     )
#     click.echo(message)

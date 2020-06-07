# todo
# dotenv
# pre-commit
import os
from abc import ABC

import click
import jinja2
from contextlib import contextmanager
import warnings

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = THIS_DIR + "/templates"


@contextmanager
def current_dir():
    pass


def get_package():
    packages = [
        i
        for i in os.listdir(".")
        if os.path.isdir(i) and "__init__.py" in os.listdir("./" + i)
    ]
    if len(packages) > 1:
        raise ValueError("Only one package allowed")
    else:
        return packages.pop()


def get_project():
    return os.path.dirname(".")


class Entity:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __bool__(self):
        return all([i for i in vars(self).values()])


class BuildResource(ABC):
    @property
    def resource(self):
        raise NotImplementedError()

    @property
    def resource_parts(self):
        return self.resource.split("/")

    @property
    def content(self):
        return ""

    def is_done(self):
        path = "."
        for part in self.resource_parts:
            if part not in os.listdir(path):
                return False
            else:
                path += "/" + part
                continue
        return True

    def not_done(self):
        return not self.is_done()

    def do(self, force=False):
        if self.not_done() or force:
            dirname = os.path.dirname(self.resource)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(self.resource, "w+") as f:
                f.write(self.content)
            return True
        else:
            return False

    def undo(self):
        if self.is_done():
            os.remove(self.resource)
            return True
        else:
            return False


class BuildTemplate(BuildResource, ABC):
    @property
    def jinja_template_filename(self):
        return TEMPLATES_DIR + "/" + self.resource + ".jinja2"

    @property
    def template(self):
        with open(self.jinja_template_filename) as f:
            return f.read()

    @property
    def content(self):
        return self.render_template()

    def render_template(self):
        return ""


class PipInstallable(BuildTemplate):
    resource = "setup.py"

    def __init__(self, project_name, version="0.1.0", cli_command="", cli_func=""):
        self.project_name = project_name
        self.version = version
        self.requirements = []
        self.entry_point = Entity(cli_command=cli_command, cli_func=cli_func)

    def render_template(self):
        template = jinja2.Template(self.template)
        rendered_template = template.render(
            name=self.project_name,
            version=self.version,
            requirements=self.requirements,
            entry_point=self.entry_point,
        )
        return rendered_template


class PackageBuilt(BuildResource):
    resource = "{package_name}/__init__.py"

    def __init__(self, package_name):
        self.package_name = package_name
        self.resource = self.resource.format(package_name=self.package_name)


@click.group()
def cli():
    pass


@cli.command()
def init():
    pass


@cli.command()
@click.argument("what")
@click.option("--project", required=False)
@click.option("--force", required=False, default=False, is_flag=True)
@click.option("--entry-points", nargs=2, required=False, default=("", ""))
def make(what, project, force, entry_points):
    if what.lower() == "installable":
        project_name = project if project else get_project()
        click.echo("Building setup.py for:" + project_name)
        command, func = entry_points
        pip_installable = PipInstallable(project_name, cli_command=command, cli_func=func)
        done = pip_installable.do(force=force)
        if done:
            click.echo("Built setup.py file")
        else:
            click.echo("setup.py file already exists, use --force to overwrite")


@cli.command()
def make_installable():
    pass

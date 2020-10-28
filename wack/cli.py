import click

from .app import Application

SETUP_PY = "setup.py"
PRE_COMMIT = ".pre-commit-config.yaml"
LICENSE = "LICENSE"
TRAVIS = ".travis.yml"
GITIGNORE = ".gitignore"
UPLOAD = "upload.sh"


@click.group()
@click.pass_context
def cli(context):
    context.ensure_object(type("context", (), {}))
    context.obj.app = Application()


@cli.command()
@click.pass_context
def install(context):
    """install all of my most used packages"""
    context.obj.app.install_packages()
    click.echo("Packages installed")


@cli.group()
def make():
    """make files from templates"""
    pass


@make.command("setup.py")
@click.pass_context
def setup_py(context):
    """make a `setup.py` file to allow for `pip install -e .`"""
    click.echo(f"Making: {SETUP_PY}")
    context.obj.app.make_template(SETUP_PY)
    click.echo(f"Made: {SETUP_PY}")


@make.command()
@click.pass_context
def pre_commit(context):
    """make a `.pre-commit-config.yaml` file to allow for pre-commit"""
    click.echo(f"Making: {PRE_COMMIT}")
    context.obj.app.make_template(PRE_COMMIT)
    click.echo(f"Made: {PRE_COMMIT}")


@make.command()
@click.pass_context
def license(context):
    """make a `LICENSE` file with MIT license"""
    click.echo(f"Making: {LICENSE}")
    context.obj.app.make_template(LICENSE)
    click.echo(f"Made: {LICENSE}")


@make.command()
@click.pass_context
def travis(context):
    """make a `.travis.yml` file for pypi auto publishing packages"""
    click.echo(f"Making: {TRAVIS}")
    context.obj.app.make_template(TRAVIS)
    click.echo(f"Made: {TRAVIS}")


@make.command()
@click.pass_context
def gitignore(context):
    """make a `.gitignore` file with pycharm basics"""
    click.echo(f"Making: {GITIGNORE}")
    context.obj.app.make_template(GITIGNORE)
    click.echo(f"Made: {GITIGNORE}")


@make.command()
@click.pass_context
def upload(context):
    """make a `.gitignore` file with pycharm basics"""
    click.echo(f"Making: {UPLOAD}")
    context.obj.app.make_template(UPLOAD)
    click.echo(f"Made: {UPLOAD}")


@make.command()
@click.argument("name")
@click.pass_context
def package(context, name):
    """make a `__init__.py` file in a package"""
    click.echo(f"Making: {name}")
    context.obj.app.make_package(name)
    click.echo(f"Made: {name}")


if __name__ == "__main__":
    cli()

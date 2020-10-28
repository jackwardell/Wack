import click

from .app import Application

SETUP_PY = "setup.py"
PRE_COMMIT = ".pre-commit-config.yaml"
LICENSE = "LICENSE"
TRAVIS = ".travis.yml"
GITIGNORE = ".gitignore"


@click.group()
@click.pass_context
def cli(context):
    context.ensure_object(type("context", (), {}))
    context.obj.app = Application()


@cli.command()
@click.pass_context
def setup(context):
    context.obj.app.install_packages()
    click.echo("Packages installed")


@cli.group()
def make():
    pass


@make.command("setup.py")
@click.pass_context
def setup_py(context):
    click.echo(f"Making: {SETUP_PY}")
    context.obj.app.make_template(SETUP_PY)
    click.echo(f"Made: {SETUP_PY}")


@make.command()
@click.pass_context
def pre_commit(context):
    click.echo(f"Making: {PRE_COMMIT}")
    context.obj.app.make_template(PRE_COMMIT)
    click.echo(f"Made: {PRE_COMMIT}")


@make.command()
@click.pass_context
def license(context):
    click.echo(f"Making: {LICENSE}")
    context.obj.app.make_template(LICENSE)
    click.echo(f"Made: {LICENSE}")


@make.command()
@click.pass_context
def travis(context):
    click.echo(f"Making: {TRAVIS}")
    context.obj.app.make_template(TRAVIS)
    click.echo(f"Made: {TRAVIS}")


@make.command()
@click.pass_context
def gitignore(context):
    click.echo(f"Making: {GITIGNORE}")
    context.obj.app.make_template(GITIGNORE)
    click.echo(f"Made: {GITIGNORE}")


@make.command()
@click.argument("name")
@click.pass_context
def package(context, name):
    click.echo(f"Making: {name}")
    context.obj.app.make_package(name)
    click.echo(f"Made: {name}")


if __name__ == "__main__":
    cli()

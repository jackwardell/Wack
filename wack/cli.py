import click
import setuptools

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
    context.ensure_object(type("Context", (), {}))
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
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def setup_py(context, force, file=SETUP_PY):
    """make a `setup.py` file to allow for `pip install -e .`"""
    click.echo(f"Making: {file}")
    author = context.obj.app.get_author()
    packages = setuptools.find_packages()
    package_name = packages.pop()
    click.echo(f"Found: {packages}. Assuming: {package_name}")
    click.echo(f"Assuming github is: {author.github}")
    done = context.obj.app.make_template(
        file,
        package_name=package_name,
        author=author.name,
        author_email=author.email,
        author_github=author.github,
        force=force,
    )
    click.echo(
        f"Made: {file}" if done else f"{file} already exists, use --force to overwrite"
    )


@make.command()
@click.pass_context
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def pre_commit(context, force, file=PRE_COMMIT):
    """make a `.pre-commit-config.yaml` file to allow for pre-commit"""
    click.echo(f"Making: {file}")
    done = context.obj.app.make_template(file, force=force)
    click.echo(
        f"Made: {file}" if done else f"{file} already exists, use --force to overwrite"
    )


@make.command()
@click.pass_context
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def license(context, force, file=LICENSE):
    """make a `LICENSE` file with MIT license"""
    click.echo(f"Making: {file}")
    author = context.obj.app.get_author()
    done = context.obj.app.make_template(file, author=author.name, force=force)
    click.echo(
        f"Made: {file}" if done else f"{file} already exists, use --force to overwrite"
    )


@make.command()
@click.pass_context
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def travis(context, force, file=TRAVIS):
    """make a `.travis.yml` file for pypi auto publishing packages"""
    click.echo(f"Making: {file}")
    done = context.obj.app.make_template(file, force=force)
    click.echo(
        f"Made: {file}" if done else f"{file} already exists, use --force to overwrite"
    )


@make.command()
@click.pass_context
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def gitignore(context, force, file=GITIGNORE):
    """make a `.gitignore` file with pycharm basics"""
    click.echo(f"Making: {file}")
    done = context.obj.app.make_template(file, force=force)
    click.echo(
        f"Made: {file}" if done else f"{file} already exists, use --force to overwrite"
    )


@make.command()
@click.pass_context
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def upload(context, force, file=UPLOAD):
    """make a `.gitignore` file with pycharm basics"""
    click.echo(f"Making: {file}")
    done = context.obj.app.make_template(file, force=force)
    click.echo(
        f"Made: {file}" if done else f"{file} already exists, use --force to overwrite"
    )


@make.command()
@click.argument("name")
@click.pass_context
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def package(context, name, force):
    """make a `__init__.py` file in a package"""
    click.echo(f"Making: {name}")
    done = context.obj.app.make_package(name, force=force)
    click.echo(
        f"Made: {name}" if done else f"{name} already exists, use --force to overwrite"
    )


if __name__ == "__main__":
    cli()

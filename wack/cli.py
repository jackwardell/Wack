import click

from wack.builders import PackageBuilt
from wack.builders import PipInstallable, WackBuilt
from wack.importing import add_wack_to_cli
from wack.importing import get_package
import subprocess
import sys


@click.group()
def cli():
    pass


add_wack_to_cli(cli)


@cli.command()
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def init(force):
    wack_built = WackBuilt()
    done = wack_built.do(force=force)
    if done:
        click.echo("Built wack.py file")
        return
    else:
        click.echo("wack.py file already exists, use --force to overwrite")
        return


@cli.command()
@click.argument("package")
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


@cli.group()
def make():
    pass


@make.command()
@click.argument("project", required=False)
@click.option("--force", "-f", required=False, default=False, is_flag=True)
@click.option("--entry-points", nargs=2, required=False, default=("", ""))
def installable(project, force, entry_points):
    project_name = project if project else get_package()
    click.echo("Building setup.py for: " + project_name)
    command, func = entry_points
    pip_installable = PipInstallable(project_name, cli_command=command, cli_func=func)
    done = pip_installable.do(force=force)
    if done:
        click.echo("Built setup.py file")
        return
    else:
        click.echo("setup.py file already exists, use --force to overwrite")
        return


@make.command()
@click.argument("package name")
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def package(package_name, force):
    package_built = PackageBuilt(package_name)
    done = package_built.do(force=force)
    if done:
        click.echo(f"Built {package_name}/__init__.py file")
        return
    else:
        click.echo(
            f"{package_name}/__init__.py file already exists, "
            f"use --force to overwrite"
        )
        return

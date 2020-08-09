import subprocess
import sys

import click

from wack.builders import PackageBuilt
from wack.builders import PipInstallable
from wack.builders import WackBuilt
from wack.core import CLI
from wack.importing import get_package

cli = CLI()


@cli.command()
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def init(force):
    wack_built = WackBuilt()
    done = wack_built.do(force=force)
    message = (
        "Built wack.py file"
        if done
        else "wack.py file already exists, use --force to overwrite"
    )
    click.echo(message)


class NoDistributionFound(Exception):
    pass


@cli.command()
@click.argument("package")
def install(package):
    # todo add option to add to requirements.txt
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        raise NoDistributionFound(f"No distribution found called: {package}")


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
    message = (
        "Built setup.py file"
        if done
        else "setup.py file already exists, use --force to overwrite"
    )
    click.echo(message)


@make.command()
@click.argument("name")
@click.option("--force", "-f", required=False, default=False, is_flag=True)
def package(name, force):
    package_built = PackageBuilt(name)
    done = package_built.do(force=force)
    message = (
        f"Built {name}/__init__.py file"
        if done
        else f"{name}/__init__.py file already exists, "
        f"use --force to overwrite"
    )
    click.echo(message)

import click
from click import Command

from wack.builders import PackageBuilt
from wack.builders import PipInstallable, WackBuilt
from wack.importing import add_wack_to_cli
import subprocess
import sys
from typer import Typer


# command =
#
#
# def command(name=None, cls=None, **attrs):
#     if cls is None:
#         cls = click.Command
#
#     def decorator(f):
#         cmd = _make_command(f, name, attrs, cls)
#         cmd.__doc__ = f.__doc__
#         return cmd
#
#     return decorator
#     return click.command
#
#
# @click.group()
# def cli():
#     wack = import_wack()
#     for name, item in vars(wack).items():
#         if

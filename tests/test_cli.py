import os

import click

from wack.cli import cli
from wack.cli import make

file_content = 'from setuptools import find_packages\nfrom setuptools import setup\n\nsetup(\n    name="{project_name}",\n    version="0.1.0",\n    packages=find_packages(),\n    include_package_data=True,\n    \n    \n)'


def test_cli(tempdir, runner):
    assert isinstance(cli, click.core.Group)
    result = runner.invoke(cli)
    assert result
    assert (
        result.stdout
        == 'Usage: cli [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  init\n  make\n'
    )
    assert result.exit_code == 0


def test_make(tempdir, runner):
    result = runner.invoke(make)
    assert result.exit_code == 0
    assert (
        result.stdout
        == "Usage: make [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  installable\n  package\n"
    )

    word = "random_thing_"
    result = runner.invoke(make, [word])
    assert result.exit_code == 2
    assert (
        result.output
        == f"Usage: make [OPTIONS] COMMAND [ARGS]...\nTry 'make --help' for help.\n\nError: No such command '{word}'.\n"
    )


def test_make_installable(tempdir, runner):
    project_name = ""

    result = runner.invoke(make, ["installable"])
    assert result.exit_code == 0
    assert result.output == "Building setup.py for: \nBuilt setup.py file\n"

    with open("setup.py") as f:
        file = f.read()

    assert file == file_content.format(project_name=project_name)

    assert os.path.exists("setup.py")

    result = runner.invoke(make, ["installable"])
    assert result.exit_code == 0
    assert (
        result.output
        == "Building setup.py for: \nsetup.py file already exists, use --force to overwrite\n"
    )

    os.remove("setup.py")

    assert not os.path.exists("setup.py")
    runner.invoke(make, ["installable"])
    assert os.path.exists("setup.py")

    with open("setup.py") as f:
        file = f.read()

    assert file == file_content.format(project_name=project_name)


def test_make_installable_with_args(tempdir, runner):
    # project
    project_name = "Whatever"
    result = runner.invoke(make, ["installable", project_name])

    # check we get a correct result
    assert result.exit_code == 0

    # check text output is correct
    assert (
        result.output == f"Building setup.py for: {project_name}\nBuilt setup.py file\n"
    )

    result = runner.invoke(make, ["installable", project_name])
    assert (
        result.output
        == f"Building setup.py for: {project_name}\nsetup.py file already exists, use --force to overwrite\n"
    )

    result = runner.invoke(make, ["installable", project_name, "--force"])
    assert (
        result.output == f"Building setup.py for: {project_name}\nBuilt setup.py file\n"
    )

    # entry points

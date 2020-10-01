import os

from wack.cli import cli
from wack.cli import make
from wack.importing import PackageNotFoundError

# import click

file_content = 'from setuptools import find_packages\nfrom setuptools import setup\n\nsetup(\n    name="{project_name}",\n    version="0.1.0",\n    packages=find_packages(),\n    include_package_data=True,\n    \n    \n)'


def test_cli(tempdir, runner):
    result = runner.invoke(cli)
    assert result
    # assert result.stdout.startswith(
    #     "Usage: cli [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:"
    # )
    assert result.exit_code == 0


def test_make(tempdir, runner):
    result = runner.invoke(make)
    assert result.exit_code == 0
    assert "installable" in result.stdout
    assert "package" in result.stdout

    word = "words-not-allowed"
    result = runner.invoke(make, [word])
    assert result.exit_code == 2
    assert "Error" in result.stdout


def test_make_installable_fails_no_package(tempdir, runner):
    result = runner.invoke(make, ["installable"])
    assert isinstance(result.exc_info[1], PackageNotFoundError)


def test_make_installable_works(tempdir, runner):
    pkg = tempdir / "random-pkg"
    pkg.mkdir()
    init = pkg / "__init__.py"
    init.touch()

    result = runner.invoke(make, ["installable"])
    assert result.exit_code == 0
    assert (
        result.output
        == f"Building setup.py for: {pkg.stem}\nBuilt setup.py file\n"
    )
    with open("setup.py") as f:
        file = f.read()
    assert os.path.exists("setup.py")
    assert file == file_content.format(project_name=pkg.stem)


def test_make_installable_doesnt_work(tempdir, runner):
    pkg = tempdir / "random-pkg"
    pkg.mkdir()
    init = pkg / "__init__.py"
    init.touch()
    setup_py = tempdir / "setup.py"
    setup_py.touch()

    result = runner.invoke(make, ["installable"])
    assert result.exit_code == 0
    assert "setup.py file already exists" in result.output
    assert "use --force to overwrite" in result.output


def test_make_installable_with_args(tempdir, runner):
    # project
    project_name = "Whatever"
    result = runner.invoke(make, ["installable", project_name])
    # check we get a correct result
    assert result.exit_code == 0
    # check text output is correct
    assert (
        result.output
        == f"Building setup.py for: {project_name}\nBuilt setup.py file\n"
    )
    result = runner.invoke(make, ["installable", project_name])
    assert (
        result.output
        == f"Building setup.py for: {project_name}\nsetup.py file already exists, use --force to overwrite\n"
    )
    result = runner.invoke(make, ["installable", project_name, "--force"])
    assert (
        result.output
        == f"Building setup.py for: {project_name}\nBuilt setup.py file\n"
    )
    # entry points

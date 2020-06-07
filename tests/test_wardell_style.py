from abc import ABC
from abc import ABCMeta
import os
import pytest

from wardell_style import BuildResource
from wardell_style import BuildTemplate
from wardell_style import PipInstallable, PackageBuilt, make
from click.testing import CliRunner


def test_build_resource(tempdir):
    assert isinstance(BuildResource, ABCMeta)
    assert issubclass(BuildResource, ABC)

    resource = BuildResource()
    assert isinstance(resource, BuildResource)
    assert resource

    assert resource.content == ""
    with pytest.raises(NotImplementedError):
        assert resource.resource
        assert resource.is_done()
        assert resource.not_done()
        assert resource.do()
        assert resource.undo()


def test_template_resource(tempdir):
    assert isinstance(BuildTemplate, ABCMeta)
    assert issubclass(BuildTemplate, BuildResource)
    assert issubclass(BuildTemplate, ABC)

    template = BuildTemplate()

    with pytest.raises(NotImplementedError):
        assert template.jinja_template_filename
        assert template.template

    assert template.content == ""
    assert template.render_template() == ""


def test_pip_installable(tempdir):
    project_name = "Hello-World"
    pip_installable = PipInstallable(project_name)

    assert not pip_installable.is_done()
    assert pip_installable.not_done()

    assert not os.path.exists(tempdir + "/" + pip_installable.resource)

    pip_installable.do()
    assert pip_installable.is_done()
    assert not pip_installable.not_done()

    assert os.path.exists(tempdir + "/" + pip_installable.resource)

    with open("setup.py") as f:
        file = f.read()

        assert (
            file
            == 'from setuptools import find_packages\nfrom setuptools import setup\n\nsetup(\n    name="Hello-World",\n    version="0.1.0",\n    packages=find_packages(),\n    include_package_data=True,\n    \n    \n)'
        )

    assert pip_installable.is_done()

    pip_installable.do()
    assert pip_installable.is_done()

    pip_installable.undo()
    assert pip_installable.not_done()

    # if .do() and .undo() work they return True
    # if the files already exist or don't for .do() and .undo() respectively
    # then returns False
    assert pip_installable.do()
    assert not pip_installable.do()

    assert pip_installable.undo()
    assert not pip_installable.undo()

    assert pip_installable.do()

    new_project_name = "xXXX"
    pip_installable.project_name = new_project_name

    assert not pip_installable.do()
    assert pip_installable.do(force=True)

    with open("setup.py") as f:
        file = f.read()
        assert (
            file
            == f'from setuptools import find_packages\nfrom setuptools import setup\n\nsetup(\n    name="{new_project_name}",\n    version="0.1.0",\n    packages=find_packages(),\n    include_package_data=True,\n    \n    \n)'
        )


def test_build_package(tempdir):
    package_name = "hello_world"
    package_init = package_name + "/__init__.py"
    package_built = PackageBuilt(package_name)
    assert package_built
    assert isinstance(package_built, PackageBuilt)

    assert package_built.package_name == package_name
    assert package_built.resource == f"{package_name}/__init__.py"

    assert package_built.do()
    assert package_built.is_done()

    assert not package_built.do()

    assert package_built.undo()
    assert package_built.not_done()
    assert not package_built.undo()

    assert package_built.do()
    with open(package_init) as f:
        assert f.read() == ""

    assert os.path.exists(package_init)

    assert package_built.undo()
    assert not os.path.exists(package_init)


def test_make(tempdir):
    runner = CliRunner()
    result = runner.invoke(make, ["HelloW"])
    assert result.exit_code == 0
    # assert False
    # assert result.output == 'Hello Peter!\n'

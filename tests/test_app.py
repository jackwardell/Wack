import os
from unittest.mock import patch

import pytest

from wack.app import Application
from wack.app import DESIRED_PACKAGES
from wack.cli import GITIGNORE
from wack.cli import LICENSE
from wack.cli import PRE_COMMIT
from wack.cli import SETUP_PY
from wack.cli import TRAVIS
from wack.cli import UPLOAD

FILES = [SETUP_PY, PRE_COMMIT, LICENSE, TRAVIS, GITIGNORE, UPLOAD]

app = Application()


def test_application_install_packages(tempdir):
    with patch("subprocess.check_call") as call:
        app.install_packages()
    assert call.call_count == len(DESIRED_PACKAGES)


@pytest.mark.parametrize("template_name", FILES)
def test_application_make_template(template_name, tempdir):
    app.make_template(template_name)
    assert template_name in os.listdir()


def test_make_package(tempdir):
    package_name = "hello"
    app.make_package(package_name)
    assert package_name in os.listdir()
    os.chdir(package_name)
    assert "__init__.py" in os.listdir()

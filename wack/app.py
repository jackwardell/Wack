import os
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

import jinja2

# import attr

THIS_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_DIR = THIS_DIR / "templates"

DESIRED_PACKAGES = [
    "Flask",
    "IPython",
    "pytest",
    "sqlalchemy",
    "attrs",
    "requests",
    "pre-commit",
]

author = namedtuple("Author", ["name", "email", "github"])


class CommandFailure(Exception):
    pass


def get_template(template_name) -> jinja2.Template:
    template = str(TEMPLATES_DIR.resolve() / template_name) + ".jinja2"
    with open(template) as f:
        return jinja2.Template(f.read())


def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        raise CommandFailure(e)


def get_author():
    try:
        name = (
            subprocess.run(
                ["git", "config", "--global", "user.name"],
                capture_output=True,
            )
            .stdout.decode()
            .strip()
        )
        email_address = (
            subprocess.run(
                ["git", "config", "--global", "user.email"],
                capture_output=True,
            )
            .stdout.decode()
            .strip()
        )
        github = "https://github.com/" + name
        return author(name, email_address, github)
    except subprocess.CalledProcessError as e:
        raise CommandFailure(e)


# @attr.s
class Application:
    def make_template(self, template_name, force=False, **kwargs):
        if self.item_not_created(template_name) or force:
            template = get_template(template_name)
            with open(template_name, "w+") as f:
                f.write(template.render(**kwargs))
            return True
        else:
            return False

    def make_package(self, package_name, force=False):
        if self.item_not_created(package_name) or force:
            os.mkdir(package_name)
            with open(package_name + "/__init__.py", "w+") as _:
                pass
            return True
        else:
            return False

    @staticmethod
    def item_not_created(item):
        if item in os.listdir():
            return False
        else:
            return True

    @staticmethod
    def get_author():
        return get_author()

    @staticmethod
    def install_packages():
        for package in DESIRED_PACKAGES:
            install_package(package)

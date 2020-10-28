import os
import subprocess
import sys
from pathlib import Path

import attr
import jinja2

THIS_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_DIR = THIS_DIR / "templates"

DESIRED_PACKAGES = [
    "Flask",
    "IPython",
    "pytest",
    "sqlalchemy",
    "attrs",
    "requests",
]


def get_template(template_name) -> jinja2.Template:
    template = str(TEMPLATES_DIR.resolve() / template_name) + ".jinja2"
    with open(template) as f:
        return jinja2.Template(f.read())


class CommandFailure(Exception):
    pass


@attr.s
class Application:
    def install_packages(self):
        for package in DESIRED_PACKAGES:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package]
                )
            except subprocess.CalledProcessError as e:
                raise CommandFailure(e)

    def make_template(self, template_name, **kwargs):
        template = get_template(template_name)
        with open(template_name, "w+") as f:
            f.write(template.render(**kwargs))

    def make_package(self, package_name):
        os.mkdir(package_name)
        with open(package_name + "/__init__.py", "w+") as _:
            pass

    def get_email_address(self):
        try:
            email_address = subprocess.run(
                ["git", "config", "--global", "user.email"],
                capture_output=True,
            )
            return email_address.stdout.decode().strip()
        except subprocess.CalledProcessError as e:
            raise CommandFailure(e)

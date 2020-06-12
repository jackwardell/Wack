from setuptools import find_packages
from setuptools import setup

setup(
    name="Wack",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Jinja2>=2.10.1",
        "click>=7",
    ],
    entry_points='''
        [console_scripts]
        wack=wack.cli:cli
    ''',
)

from setuptools import setup

# IN BETA
__version__ = "0.1.5"

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="Wack",
    version=__version__,
    author="Jack Wardell",
    author_email="jack@wardell.xyz",
    packages=["wack"],
    package_dir={"wack": "wack"},
    package_data={"wack": ["templates/*.jinja2"]},
    include_package_data=True,
    description="A simple CLI and automation tool",
    url="https://github.com/jackwardell/Wack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Jinja2>=2.10.1", "click>=7"],
    entry_points="""
        [console_scripts]
        wack=wack.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

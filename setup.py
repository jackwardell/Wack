from setuptools import find_packages
from setuptools import setup

setup(
    name="Wardell-Style",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    
    
    entry_points='''
        [console_scripts]
        wardell=wardell_style:cli
    ''',
    
)
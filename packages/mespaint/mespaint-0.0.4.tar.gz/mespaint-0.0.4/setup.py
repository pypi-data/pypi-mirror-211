import pathlib
from os.path import join

from src import *

from setuptools import setup, find_packages
here = pathlib.Path(__file__).parent.resolve()
readme = open(join(here,'README.md')).read()

setup(
        name=package_name,
        version=version,
        url=url,
        license=license,
        author=version,
        author_email=email,
        description=description,
        long_description=readme,
        long_description_content_type='text/markdown',
        install_requires=['PyQt5', 'PyQt5-Qt5', 'PyQt5-sip'],
        entry_points='''
            [console_scripts]
            mespaint=src.main:main
        ''',
        packages=find_packages()
        # packages = ["menga_chart"],
        # packages=find_packages(where="src", include="menga_chart")
)
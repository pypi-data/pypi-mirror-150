import os
import subprocess

from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


# This call to setup() does all the work
setup(
    name="s2i2a",
    version="0.0.0",
    description="Sweep to int to arguments. Map parameter sweeps to ints to program arguments. Specifically useful "
                "for compute canada.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Velythyl/s2i2a",
    author="Charlie Gauthier",
    author_email="charlie.gauthier@umontreal.ca",
    license="MIT",
    packages=find_packages(),
    package_data={"s2i2a": ["*.yaml"]},
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "s2i2a=s2i2a.main:main",
        ]
    },
)
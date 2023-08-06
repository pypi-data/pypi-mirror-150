#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number,
# edit gridify/__init__.py


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="gridify",
    version=find_version("gridify", "__init__.py"),
    license="apache-2.0",
    description="This tools takes geometries to describe areas to in- and exclude, and generates a list of points that form a grid covering the described area.",
    long_description=readme + "\n\n",
    author="Rijkswaterstaat Datalab",
    author_email="datalab.codebase@rws.nl",
    url="https://gitlab.com/rwsdatalab/codebase-opensource/image/gridify",
    packages=["gridify"],
    include_package_data=True,
    package_data={"gridify": ["py.typed"]},
    zip_safe=False,
    keywords="gridify",
    license_files=["LICENSE.rst"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    test_suite="tests",
    install_requires=[
        "geopandas",
        "rtree",
    ],
    setup_requires=[
        # dependency for `python setup.py test`
        "pytest-runner",
        # dependencies for `python setup.py build_sphinx`
        "sphinx",
        "sphinx_rtd_theme",
    ],
    tests_require=["pytest", "pytest-cov"],
    extras_require={
        "dev": [
            "bandit",
            "black",
            "flake8",
            "flake8-bugbear",
            "flake8-comprehensions",
            "flake8-docstrings",
            "flake8-polyfill",
            "isort",
            "mypy",
            "pre-commit",
            "pylint",
            "pylint[prospector]",
            "pytest",
            "pytest-cov",
            "radon",
            "safety",
        ],
    },
)

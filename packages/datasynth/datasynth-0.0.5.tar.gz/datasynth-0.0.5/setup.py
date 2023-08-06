#!/usr/bin/env python

import configparser
import os
from codecs import open

from setuptools import find_packages, setup

# Import the package module code from local directory.
repo_path = os.path.abspath(os.path.dirname(__file__))

packages = find_packages(exclude=("examples",))

# Open requirements files to grab package dependencies
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("requirements-test.txt") as f:
    tests_require = [line for line in f if "==" in line]

with open("requirements-dev.txt") as f:
    dev_requires = [line for line in f if "==" in line]

# Open README file to attach readme as package description.
with open("README.md", "r", "utf-8") as f:
    readme = f.read()

about = configparser.ConfigParser()
about.read(os.path.join(repo_path, "pyproject.toml"))
author = about["default"]["__author__"].strip('"')
author_email = about["default"]["__author_email__"].strip('"')
description = about["default"]["__description__"].strip('"')
github_organization = about["default"]["github_organization"].strip('"')
license = about["default"]["__url__"].strip('"')
package_name = about["default"]["__title__"].strip('"')
url = about["default"]["__url__"].strip('"')
version = about["default"]["__version__"].strip('"')

setup(
    name=package_name,
    version=version,
    description=description,
    long_description=readme,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url=url,
    packages=packages,
    package_dir={package_name: package_name},
    package_data={"": []},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=install_requires,
    setup_requires=install_requires,
    extras_require={"test": tests_require, "dev": dev_requires},
    entry_points={"console_scripts": [f"{package_name}={package_name}.cli:cli"]},
    license=license,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    tests_require=tests_require,
    project_urls={"Source": f"https://github.com/{github_organization}/{package_name}"},
)

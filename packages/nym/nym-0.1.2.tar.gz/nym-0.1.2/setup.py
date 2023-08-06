#!/usr/bin/env python

"""The setup script."""

import nimporter
from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "nimporter"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Goncalo Magno",
    author_email="goncalo.magno@gmail.com",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    description="Nim extension for Python, example project",
    entry_points={
        "console_scripts": [
            "nym=nym.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    # include_package_data=True,
    keywords="nym",
    name="nym",
    packages=find_packages(include=["nym", "nym.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/gmagno/nym",
    version="0.1.2",
    zip_safe=False,
    ext_modules=nimporter.get_nim_extensions(
        platforms=[nimporter.WINDOWS, nimporter.LINUX, nimporter.MACOS]
    ),
    package_data={"": ["*.nim*"]},  # Distribute *.nim & *.nim.cfg source files
    setup_requires=[
        "choosenim_install",  # Optional. Auto-installs Nim compiler
    ],
)

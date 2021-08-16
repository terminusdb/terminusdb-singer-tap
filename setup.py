#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-terminusdb",
    version="0.1.0",
    description="Singer.io tap for extracting data from TerminusDB",
    author="Cheuk",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_terminusdb"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-terminusdb=tap_terminusdb:main
    """,
    packages=["tap_terminusdb"],
    package_data = {
        "schemas": ["tap_terminusdb/schemas/*.json"]
    },
    include_package_data=True,
)

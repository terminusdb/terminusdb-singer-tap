#!/usr/bin/env python
# read the contents of your README file
import re
from os import path

from setuptools import setup

# Add README.md in PyPI project description, reletive links are changes to obsolute

page_target = "https://github.com/terminusdb/terminusdb-client-python/blob/master/"
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

matched = re.finditer(r"\]\(\S+\)", long_description)
replace_pairs = {}
for item in matched:
    if item.group(0)[2:10] != "https://" and item.group(0)[2:9] != "http://":
        replace_pairs[item.group(0)] = (
            item.group(0)[:2] + page_target + item.group(0)[2:]
        )
for old_str, new_str in replace_pairs.items():
    long_description = long_description.replace(old_str, new_str)

# ---

setup(
    name="tap-terminusdb",
    version="0.1.1",
    description="Singer.io tap for extracting data from TerminusDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cheuk",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_terminusdb"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python>=5.12.2",
        "terminusdb-client>=10.0.10",
    ],
    entry_points="""
    [console_scripts]
    tap-terminusdb=tap_terminusdb:main
    """,
    packages=["tap_terminusdb"],
    package_data={"schemas": ["tap_terminusdb/schemas/*.json"]},
    include_package_data=True,
)

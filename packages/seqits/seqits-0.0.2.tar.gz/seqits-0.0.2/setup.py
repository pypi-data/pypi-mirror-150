#!/usr/bin/env python
# coding=utf-8
from setuptools import setup, find_packages
import os,re
from seqits import seqits_version

try:
    with open(os.path.join(os.path.abspath(os.path.dirname("__file__")),"README.md")) as f:
        long_description=f.read()
except:
    long_description="Seqits"

setup(
    name="seqits",
    version=seqits_version,
    description="Tools for sequences process",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/sfjdx1144/seqits',
    author="Fujun Sun",
    author_email="sfjdx1144@live.com",
    packages=find_packages(),
    install_requires=['argparse','colorama'],
    platforms="any",
    license="GPL-3.0 license",
    python_requires=">=3.4.0",
    include_package_data=True
)

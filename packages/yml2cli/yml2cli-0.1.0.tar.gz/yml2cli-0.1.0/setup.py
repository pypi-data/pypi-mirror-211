#!/usr/bin/env python
# Copyright (c) 2023 Krishna Miriyala
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
import os
import sys

import setuptools

TOP_DIR = os.path.dirname(__file__)
README = os.path.join(TOP_DIR, "README.md")
REQUIREMENTS = [
    "pyyaml",
]


setuptools.setup(
    name="yml2cli",
    version="v0.1.0",

    author="Krishna Miriyala",
    author_email="krishnambm@gmail.com",
    url="https://github.com/krishnamiriyala/yml2cli",
    description="Yaml to cli params converter",
    long_description=open(README, "r").read(),
    packages=setuptools.find_packages(),
    license="AS IS",
    entry_points={
        'console_scripts': [
            'yml2cli=yml2cli:yml2cli.main',
        ],
    },
    install_requires=REQUIREMENTS,
)

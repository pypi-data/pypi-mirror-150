#!/usr/bin/python3
# -*- coding: utf8 -*-

# Copyright (c) 2021 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
 Setup Installation for Uploading to PyPI. References:
 + https://packaging.python.org/en/latest/tutorials/packaging-projects/
"""

from __future__ import absolute_import
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='qcompute-qep',
    version='0.1.0',
    description='A Quantum Error Processing toolkit developed '
                'by the Institute for Quantum Computing at Baidu Research.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Baidu Quantum',
    author_email='quantum@baidu.com',
    url="https://quantum-hub.baidu.com/qep/",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        'qcompute>=2.0.4',
        'numpy>=1.22.3',
        'scipy>=1.8.0',
        'qiskit>=0.36.1',
        'qutip>=4.6.2',
        'bidict>=0.22.0',
        'protobuf>=3.20.1',
        'requests>=2.27.1',
        'matplotlib>=3.5.2',
        'bce-python-sdk>=0.8.64',
        'antlr4-python3-runtime==4.9.3',
        'py-expression-eval>=0.3.14',
        'websocket-client>=1.3.2',
        'tqdm>=4.64.0',
        'networkx>=2.8',
        'sparse>=0.13.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='Apache 2.0',
)

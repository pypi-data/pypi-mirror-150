#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "twin-client-sdk",
    version = "0.1.1",
    url = 'https://github.com/sxhxliang',
    # long_description = open('README.md').read(),
    packages = find_packages(),
    author='Shihua Liang',
    author_email='sxhx.liang@gmail.com',
    description='twin client sdk',
    install_requires=['pydantic'],
    python_requires='>=3.6',
)
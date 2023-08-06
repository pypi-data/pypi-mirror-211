import io
import os
import sys
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xlyy_toolkit',
    version='1.0.2',
    author='NatsuriTsukine',
    author_email='398339897@qq.com',
    description="xlyy's toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
    ],
)


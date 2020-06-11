#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solaredge_setapp",
    version="0.1.3",
    description="SolarEdge SetApp protocol buffers parser library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    author="nmakel",
    author_email="",
    url="https://github.com/nmakel/solaredge_setapp",
    packages=["solaredge_setapp"],
    include_package_data=True,
    install_requires=[
        "protobuf>=3.6.1",
        "requests>=2.12.4"
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ]
)

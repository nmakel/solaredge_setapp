#!/usr/bin/env python3

from distutils.core import setup


setup(
    name='solaredge_setapp',
    version='0.1',
    description=' SolarEdge SetApp protocol buffers parser library',
    license='MIT License',
    author='nmakel',
    author_email="",
    url='https://github.com/nmakel/solaredge_setapp',
    packages=['solaredge_setapp'],
    requires=[
        'protobuf',
        'requests'
    ]
)
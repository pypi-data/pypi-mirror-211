#! /usr/bin/env python
from io import open
from setuptools import setup, find_packages
setup(
    name='PyArrShow',
    version='1.0.0',
    description='Python ArrayShow for MRI data visualization.',
    long_description='Python ArrayShow for MRI data visualization.',
    author="kaixuan,zhao",
    author_email='kaixuan_zhao@163.com',
    license='Apache License 2.0',
    url="https://github.com/15625148866/PyArrShow",
    download_url="https://github.com/15625148866/PyArrShow/archive/refs/tags/v1.0.2.tar.gz",
    keywords = ["MRI",'visualization'],
    install_requires=[
        'numpy',
        'PySide6',
        'matplotlib'
    ],
    classifiers=[
        'Development status :: 3 - Alpha',
        'Intended Audience :: MRI scientists',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
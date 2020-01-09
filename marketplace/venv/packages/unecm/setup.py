# -*- coding: utf-8 -*-
import setuptools
from distutils.extension import Extension
import os


path = os.path.dirname(os.path.realpath(__file__))

setuptools.setup(
    name="unecm",
    version="0.1.0",
    author="Philipp Glaw",
    description="C++ Extension to decode ECM-files and generate a cue file for the retropie-marketplace project",
    url="https://github.com/pgmystery/retropie-marketplace",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "License :: Freeware",
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    ext_modules=[
        Extension("unecm",
            sources = [os.path.join(path, "unecm.cpp")]
        )
    ]
)

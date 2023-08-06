#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import setuptools
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

with open("README.md","r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="heteroverlap",
    version="0.0.4",
    author="ZiyeLuo",
    author_email="2017100369@ruc.edu.cn",
    description="Regression-based heterogeneity analysis to identify overlapping subgroup structure in high-dimensional data",
    long_description_content_type = "text/markdown",
    long_description=long_description,
    url="https://github.com/foliag/subgroup",
    packages=setuptools.find_packages(),
    install_requires=["numpy",
                      "openpyxl",
                      "pandas",
                      "scikit-learn",
                      "scipy",
                      "seaborn"
                      
        ],
    classifiers=[
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",]
    
    )




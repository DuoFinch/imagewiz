# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:05:03 2019

Setup file for imageWiz module

@author: Evan Gibson
"""

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='imagewiz',
                 version='0.3',
                 author="Evan Gibson",
                 author_email="evan.gibson@duofinch.com",
                 description="A image preprocessing module to compliment Tensorflow/Keras",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/evangibson/imagewiz",
                 packages=['imagewiz',],
                 classifiers=["Programming Language :: Python :: 3",
                              "License :: MIT License",
                              "Operating System :: OS Independent"])
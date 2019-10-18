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
                 version='0.6',
                 author="Evan Gibson",
                 author_email="evan.gibson@duofinch.com",
                 description="A image preprocessing module to compliment Tensorflow/Keras",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/DuoFinch/imagewiz",
                 packages=['imagewiz',],
                 install_requires=['pydicom', 'png', 'tqdm'],
                 classifiers=["Development Status :: 2 - Pre-Alpha",
                              "Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              "Topic :: Scientific/Engineering :: Image Recognition"])
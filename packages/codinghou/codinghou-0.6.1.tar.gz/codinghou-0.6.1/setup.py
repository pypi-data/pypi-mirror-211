# -*- coding: utf-8 -*-
"""
 @Date    : 2021/2/3 21:51
 @Author  : Douglee
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codinghou",
    version="0.6.1",
    author="douglee",
    description="CodingHou package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Douglee/codinghou",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyfiglet>=0.8.post1",
    ]
)

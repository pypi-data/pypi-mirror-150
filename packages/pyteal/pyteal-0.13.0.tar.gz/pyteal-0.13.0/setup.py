#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyteal",
    version="0.13.0",
    author="Algorand",
    author_email="pypiservice@algorand.com",
    description="Algorand Smart Contracts in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/algorand/pyteal",
    packages=setuptools.find_packages(),
    install_requires=["py-algorand-sdk"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"pyteal": ["*.pyi"]},
    python_requires=">=3.10",
)

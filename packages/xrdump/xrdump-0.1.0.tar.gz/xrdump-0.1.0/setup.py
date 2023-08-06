#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    "xarray>=0.14",
]

setup_requirements = []

test_requirements = ["pytest"]

setup(
    author="Allen Institute for Artificial Intelligence",
    author_email="jeremym@allenai.org",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Replacement for ncdump using xarray.",
    install_requires=requirements,
    extras_require={},
    entry_points={
        "console_scripts": [
            "xrdump=xrdump.__main__:main",
            "zarr2nc=xrdump.zarr2nc:main",
        ]
    },
    license="BSD license",
    long_description="Replacement for ncdump using xarray.",
    include_package_data=True,
    name="xrdump",
    packages=find_packages(include=["xrdump", "xrdump.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    version="0.1.0",
    zip_safe=False,
)

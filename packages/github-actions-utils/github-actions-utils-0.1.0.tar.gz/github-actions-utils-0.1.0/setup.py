"""
Setup to create the package
"""
from setuptools import setup, find_packages

import github_actions_utils

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=github_actions_utils.NAME,
    version=github_actions_utils.VERSION,
    description='Package of useful functions for GitHub Actions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/heitorpolidoro/github_actions_utils',
    author='Heitor Polidoro',
    license='unlicense',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    python_requires=">=3.9"
)

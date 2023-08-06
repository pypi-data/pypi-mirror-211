# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="GaikevichSerialization",
    version="0.1.1",
    description="Library for class and function serialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Egor Gaikevich",
    author_email="egaikevich@yahoo.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["Serialization"],
    include_package_data=True,
    install_requires=["regex"]
)

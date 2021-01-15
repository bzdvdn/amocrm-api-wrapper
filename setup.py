from os import path
from io import open
from setuptools import setup, find_packages


def read(f):
    return open(f, "r", encoding='utf-8').read()


setup(
    name="amocrm-api-wrapper",
    version='0.0.9',
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests",],
    description="Amocrm api wrapper v4",
    author="bzdvdn",
    author_email="bzdv.dn@gmail.com",
    url="https://github.com/bzdvdn/amocrm-api-wrapper",
    license="MIT",
    python_requires=">=3.6",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
)

import setuptools
from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

NAME = 'bounded'
VERSION = '0.0.0'
URL = 'https://github.com/SSripilaipong/chamber'
LICENSE = 'MIT'
AUTHOR = 'SSripilaipong'
EMAIL = 'SHSnail@mail.com'

setup(
    name=NAME,
    version=VERSION,
    packages=[package for package in setuptools.find_packages() if not package.startswith('tests.')],
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=None,
    long_description=None,
    python_requires='>=3.6',
    install_requires=requirements,
    classifiers=[],
)

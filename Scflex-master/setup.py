# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Scflex Distributed Computing System',
    version='0.0.1',
    description='Distributed Computing System powered by Apache Spark and MongoDB',
    long_description=readme,
    author='Tan Kuan Pern',
    author_email='kptan86@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)


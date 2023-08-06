#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='fantasybert',
    version='0.1.1',
    description='an easy module for bert models',
    long_description='fantasybert: ',
    license='Apache License 2.0',
    url='https://github.com/Changanyue/easytransformers',
    author='Changanyue',
    install_requires=['torch>1.4', 'numpy>=1.17'],
    packages=find_packages()
)
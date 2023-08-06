#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='fantasybert',
    version='0.1.2',
    description='an easy module for bert models',
    long_description='fantasybert: ',
    license='Apache License 2.0',
    url='https://github.com/Changanyue/fantasybert',
    author='Changanyue',
    install_requires=['torch>1.4', 'numpy>=1.17', 'transformers>=4.5.1', 'fitlog'],
    packages=find_packages()
)
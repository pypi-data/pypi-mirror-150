from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Package to Clean Telecom Data'

# Setting up
setup(
    name='cleand_df',
    version=VERSION,
    author='Faith Bagire',
    author_email='faibagire@gmail.com',
    descrption=DESCRIPTION,
    package=find_packages(),
    install_requires=[],
    keywords=['Python', 'Data', 'Usage', 'Behavior', 'Bytes'],
    classifiers=[])

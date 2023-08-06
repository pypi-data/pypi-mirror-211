#!/usr/bin/env python

from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='fse.torii',
      version='1.0.2',
      description='Torii',
      author='Fujitsu Systems Europe',
      packages=['torii', 'torii.services', 'torii.data'],
      install_requires=requirements,
      )

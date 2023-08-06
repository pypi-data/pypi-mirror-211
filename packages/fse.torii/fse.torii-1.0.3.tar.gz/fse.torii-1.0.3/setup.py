#!/usr/bin/env python

from distutils.core import setup


setup(name='fse.torii',
      version='1.0.3',
      description='Torii',
      author='Fujitsu Systems Europe',
      packages=['torii', 'torii.services', 'torii.data'],
      install_requires=[
            'requests-toolbelt==0.10.1',
            'numpy==1.24.2',
            'pymongo==4.3.3'
        ]
      )

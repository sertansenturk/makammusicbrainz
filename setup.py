#!/usr/bin/env python

from setuptools import setup

setup(name='makammusicbrainz',
      version='1.3.0',
      description='Tools fetch metadata related to the CompMusic makam corpus '
                  'from MusicBrainz',
      author='Sertan Senturk',
      author_email='contact AT sertansenturk DOT com',
      license='agpl 3.0',
      url='http://sertansenturk.com',
      packages=['makammusicbrainz'],
      include_package_data=True,
      install_requires=[
            'six >= 1.10.0',  # Python 2*3 support
            'eyeD3 == 0.7.9',
      ],
      )

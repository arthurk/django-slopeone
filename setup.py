#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-slopeone',
    version='0.1dev',
    description='Rating predictions based on the Slope One algorithm',
    author='Arthur Koziel',
    author_email='arthur@arthurkoziel.com',
    url='http://github.com/arthurk/django-slopeone',
    license='New BSD License',
    classifiers=[
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python',
    ],
    packages=find_packages(),
    zip_safe=False,
)

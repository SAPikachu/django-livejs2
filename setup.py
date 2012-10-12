#!/usr/bin/env python

from setuptools import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='django-livejs2',
    version='1.0',
    description='Integrate live.js into django site',
    long_description=long_description,
    author='Joe Hu (SAPikachu)',
    author_email='sapikachu@gmail.com',
    url='https://github.com/SAPikachu/django-livejs2',
    packages=['django_livejs2'],
    package_data={'django_livejs2': ['static/**/*']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

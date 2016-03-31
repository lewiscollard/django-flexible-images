#!/usr/bin/env python
# coding: utf-8
from setuptools import find_packages, setup

setup(
    name="django-flexible-images",
    version="1.0.6",
    url="https://github.com/lewiscollard/django-flexible-images",
    author="Lewis Collard",
    author_email="lewis.collard@onespacemedia.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    description='A responsive image solution for Django.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    ],
    install_requires=[
        'django',
        'sorl-thumbnail'
    ]
)

#!/usr/bin/env python

from setuptools import setup, find_packages

tests_require = [
    'django',
    'mysqlclient',
    # also requires the disqus fork of haystack
]

setup(
    name='django-ratings-underwave',
    version="0.1.0",
    author='Yoonsoek Choi`',
    author_email='yacaeh@gmail.com',
    description='Generic Ratings in Django',
    url='http://github.com/yacaeh/django-ratings',
    install_requires=[
        'django',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)

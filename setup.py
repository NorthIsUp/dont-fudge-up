#! /usr/bin/env python
from setuptools import (
    setup,
    find_packages,
)

setup(
    name='dont-fudge-up',
    version='1.0.0',
    description='Find operations that might fudge up production, like a pdb.set_trace',
    author='Adam Hitchcock',
    author_email='adam@disqus.com',
    url='http://github.com/NorthIsUp/pylint-dfu',
    py_modules=find_packages(exclude=['tests']),
    install_requires=['setuptools', 'pylint', 'flake8'],
    entry_points={
        'flake8.extension': [
            'D4 = dfu.flake8.check:DFUChecker',
        ],
    },
    zip_safe=False,

)

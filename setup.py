#! /usr/bin/env python

from distutils.core import setup

setup(
    name='pylint-dfu',
    version='1.0.0',
    description='Find operations that might fudge up production, like a pdb.set_trace',
    author='Adam Hitchcock',
    author_email='adam@disqus.com',
    url='http://github.com/NorthIsUp/pylint-dfu',
    py_modules=['dfu'],
    install_requires=['pylint'],
)

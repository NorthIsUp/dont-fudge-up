#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = []

tests_require = [
    'flake8',
]


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='dont-fudge-up',
    version='0.0.6',
    author='Adam Hitchcock',
    author_email='adam@disqus.com',
    url='https://github.com/NorthIsUp/dont-fudge-up',
    bugtrack_url='https://github.com/NorthIsUp/dont-fudge-up/issues',
    description='Find operations that might fudge up production, like a pdb.set_trace',
    license='BSD',
    entry_points={
        'flake8.extension': [
            'D = dfu.flake8.check:DFUChecker',
        ],
    },
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'tests': tests_require,
    },
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)

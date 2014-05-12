#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

install_requires = []

tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-django-lite',
    'flake8',
]


with open('README.rst') as f:
    long_description = f.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import sys
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='dont-fudge-up',
    version='0.0.1',
    author='Adam Hitchcock',
    author_email='adam@disqus.com',
    url='https://github.com/NorthIsUp/dont-fudge-up',
    description='Find operations that might fudge up production, like a pdb.set_trace',
    license='BSD',
    entry_points={
        'flake8.extension': [
            'D4 = dfu.flake8.check:DFUChecker',
        ],
    },
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
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
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)

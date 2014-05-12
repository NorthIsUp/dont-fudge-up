==============
Don't Fudge Up
==============

Don't Fudge Up production with extra prints, import debug, or an erroneous pdb.set_trace.

Instalation
-----------
such pip so wow::

    $ pip install dont-fudge-up

Flake8
------
super easy::

    $ flake8 --version
    2.1.0 (pep8: 1.5.6, dfu: 1.0.0, pyflakes: 0.8.1, mccabe: 0.2.1) CPython 2.7.6
    # see it here -------^

Pylint
------

it should work something like this::

    $ pylint --reports=n --load-plugins=dfu.pylint tests/input.py


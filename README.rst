==============
Don't Fudge Up
==============

Don't Fudge Up production with extra prints, import debug, or an erroneous pdb.set_trace.

Installation
------------
such pip so wow::

    $ pip install dont-fudge-up

Flake8
------
The plug-in will automatically register with Flake8::

    $ flake8 --version
    2.1.0 (pep8: 1.5.6, dfu: 1.0.0, pyflakes: 0.8.1, mccabe: 0.2.1) CPython 2.7.6
    # see it here -------^

Pylint
------

It should work something like this::

    $ pylint --load-plugins=dfu.pylint tests/input.py

Error Codes
-----------

D000: stylistically bad for production but mostly harmless
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

D001
    raised on leaving a print statement in the code

D100: warnings which effect production performance but are usually not fatal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

D101
    Cautioned import for production
    ::
        import pdb #  on its own, harmless...

D102
    set_trace may be fatal in production (set_trace might be from pdb)

D500: errors that are forbidden for production and are near always fatal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


D501
    Forbidden import for production
    ::
        import debug # woah there cowboy, that's an issue

D502
    pdb.set_trace is forbidden in production

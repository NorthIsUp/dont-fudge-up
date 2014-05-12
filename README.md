pylint-dfu
=============

Don't Fudge Up production with extra prints, import debug, or an erroneous pdb.set_trace.

it should work something like this

```bash
$ pylint --reports=n --load-plugins=dfu tests/input.py
```

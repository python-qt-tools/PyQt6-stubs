<img src="http://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# Mypy stubs for the PyQt6 framework

This repository holds the stubs of the PyQt6 framework. The stubs are based on the stubs
which are delivered with the PyQt6 package.

My work relies on the PyQt5-stubs and this is an intermediate solution until the PyQt5-stubs are ready for PyQt6. The idea of stub generation is based on this post of The-Compiler (https://github.com/python-qt-tools/PyQt5-stubs/issues/6).

Please note that this work is far from complete. You can use the stubs to get rid of some annoying things that are present in the original stubs, nevertheless, other things which are fixed already in the PyQt5-stubs might still be present here.

# Installation

**WARNING: The Stubs are not yet on pypi**

Clone the latest version from Github and install it via Python setuptools:

    $ git clone https://github.com/TilmanK/PyQt6-stubs
    $ python setup.py install

# Generation of stubs

Stubs are generated by running `generate_upstream.py`. It will download the latest PyQt6 release, extract the stubs and rewrite them. Currently, the following changes are made:

* Simple errors from mypy are fixed on the go (like adding ignore comments).
* Obsolete annotations are removed.
* All signals are fixed.
* Custom fixes are applied.

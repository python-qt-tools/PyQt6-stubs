"""Script for installation with pip."""
from setuptools import setup  # type: ignore

from version import PYQT_VERSION, STUB_VERSION

setup(
    name="PyQt6-stubs",
    url="https://github.com/TilmanK/PyQt6-stubs",
    author="Tilman Krummeck",
    maintainer_email="tilman@krummeck.de",
    description="PEP561 stub files for the PyQt6 framework",
    version=".".join((str(nbr) for nbr in PYQT_VERSION + (STUB_VERSION,))),
    python_requires=">= 3.6",
    package_data={
        "PyQt6-stubs": ["*.pyi"],
        "PyQt6-stubs/uic": ["*.pyi"],
        "PyQt6-stubs/uic/Compiler": ["*.pyi"],
        "PyQt6-stubs/uic/Loader": ["*.pyi"],
    },
    packages=[
        "PyQt6-stubs",
        "PyQt6-stubs/uic",
        "PyQt6-stubs/uic/Compiler",
        "PyQt6-stubs/uic/Loader",
    ],
)

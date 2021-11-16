"""Script for installation with pip."""
from setuptools import setup  # type: ignore

from PyQt6_stubs import PYQT_VERSION

setup(
    name="PyQt6_stubs",
    url="https://github.com/TilmanK/PyQt6-stubs",
    author="Tilman Krummeck",
    maintainer_email="tilman@krummeck.de",
    description="PEP561 stub files for the PyQt6 framework",
    version=PYQT_VERSION,
    python_requires=">= 3.6",
    package_data={"PyQt6_stubs": ["*.pyi"]},
    packages=["PyQt6_stubs"],
    tests_require=["PyQt6==6.2.0"],
)

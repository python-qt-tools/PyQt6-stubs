"""Script for installation with pip."""
from setuptools import setup  # type: ignore

setup(
    name="PyQt5-stubs",
    url="https://github.com/TilmanK/PyQt6-stubs",
    author="Tilman Krummeck",
    maintainer_email="tilman@krummeck.de",
    description="PEP561 stub files for the PyQt6 framework",
    version="6.2.0",
    python_requires=">= 3.6",
    package_data={"PyQt6-stubs": ["*.pyi"]},
    packages=["PyQt6-stubs"],
    tests_require=["PyQt6==6.2.0"],
)

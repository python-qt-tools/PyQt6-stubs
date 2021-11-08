"""Base class for PyQt6 stub fixes."""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from typing import List


class FixBase:
    """Base class for PyQt6 stub fixes."""

    qt_module: str
    qt_class: str | None = None
    qt_method: str

    fixed_code: str | List[str]

"""Fixes setWriteable argument of array type."""
# pylint: disable=too-few-public-methods
from fixes.base_fix import FixBase


class FixSetWriteableArray(FixBase):
    """Fixes setWriteable argument of array type."""

    qt_module = "sip"
    qt_class = "voidptr"
    qt_method = "setwriteable"

    fixed_code = "def setwriteable(self, bool: bool) -> None: ..."

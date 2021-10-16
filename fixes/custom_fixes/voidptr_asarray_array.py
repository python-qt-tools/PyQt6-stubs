"""Fixes array type for asarray of voidptr."""
# pylint: disable=too-few-public-methods
from fixes.base_fix import FixBase


class FixAsArrayVoidPtr(FixBase):
    """Fixes array type for asarray of voidptr."""

    qt_module = "sip"
    qt_class = "voidptr"
    qt_method = "asarray"

    fixed_code = "def asarray(self, size: int = -1) -> array[int]: ..."

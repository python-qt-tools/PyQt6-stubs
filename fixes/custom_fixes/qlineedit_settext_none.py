"""Fixes setText of QLineEdit to accept None as argument."""
# pylint: disable=too-few-public-methods
from fixes.base_fix import FixBase


class FixQLineEditSetTextNone(FixBase):
    """Fixes setText of QLineEdit to accept None as argument."""

    qt_module = "QtWidgets"
    qt_class = "QLineEdit"
    qt_method = "setText"

    fixed_code = "def setText(self, a0: typing.Optional[str]) -> None: ..."

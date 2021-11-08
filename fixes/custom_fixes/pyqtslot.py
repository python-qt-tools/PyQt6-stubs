"""Fixes pyqtSlot decorator.."""
# pylint: disable=too-few-public-methods
from fixes.base_fix import FixBase


class FixPyQtSlotDecorator(FixBase):
    """Fixes pyqtSlot decorator.."""

    qt_module = "QtCore"
    qt_class = None
    qt_method = "pyqtSlot"

    fixed_code = [
        "T = typing.TypeVar('T')",
        "FuncT = typing.Callable[..., T]",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, name: str) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, result: typing.Type[T]) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, result: str) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, revision: int) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, name: str, result: typing.Type[T]) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, name: str, result: str) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, name: str, revision: int) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, result: typing.Type[T], revision: int) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, result: str, revision: int) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, name: str, result: typing.Type[T], revision: int) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
        "@typing.overload\ndef pyqtSlot(*types: typing.Any, name: str, result: str, revision: int) -> typing.Callable[[FuncT[T]], FuncT[T]]: ...",
    ]

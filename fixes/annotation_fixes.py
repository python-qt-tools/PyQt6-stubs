"""Definition of all annotation fixes."""

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, List, Optional, Union

from libcst import Decorator, FunctionDef


@dataclass
class FixParameter:
    """Defines a single Parameter for a fix in AnnotationFix."""

    name: str  # name of the parameter
    annotation: str  # desired annotation as str
    # todo: Use to check if something expected has changed
    current_annotation: Optional[str]  # current annotation as str
    # todo: return values!


@dataclass
class AnnotationFix:
    """Defines a Fix for an annotation of function parameter."""

    module_name: str  # name of the module in which the fix will be applied
    class_name: str  # name of the class the method belongs to
    method_name: str  # name of the method
    params: List[FixParameter]  # List of the method's parameters
    custom_type: Optional[
        str
    ] = None  # Defines a custom type that will be added once to the module
    static: bool = False  # Is the method static?


@dataclass
class CommentFix:
    """Fixes a FunctionDef or a Decorator by appending a comment to it."""

    node: Union[FunctionDef, Decorator]
    comment: str


@dataclass
class RemoveFix:
    """Remove a node because mypy detected it as obsolete."""

    node: Union[FunctionDef, Decorator]


@dataclass
class RemoveOverloadDecoratorFix:
    """Remove an overload Decorator because the method is the last method left."""

    node: Decorator


@dataclass
class AddImportFix:
    """Add missing imports to PyQt6 imports."""

    missing_imports: List[str]


@dataclass
class MypyFix:
    """Fix that was detected by mypy."""

    class Type(IntEnum):
        """Type of fix that was detected by mypy."""

        # When a child class implements an overridden method different from
        # its parent
        OVERRIDE = 1
        # If a function's signature will never be matched since another
        # signature has same or broader parameters.
        SIGNATURE_MISMATCH = 2
        # Mismatch when some but not all functions are decorated with
        # @staticmethod
        STATIC_MISMATCH = 3
        # Imports from PyQt6 that are missing.
        MISSING_IMPORT = 4

    module_name: str  # name of the module in which the fix will be applied
    line_nbr: Optional[int]  # line in which the fix will be done
    fix_type: Type
    data: Any = None


# Fix definitions
ANNOTATION_FIXES = [
    AnnotationFix(
        "QtWidgets",
        "QLineEdit",
        "setText",
        [FixParameter("a0", "typing.Optional[str]", "str")],
    ),
    AnnotationFix(
        "sip",
        "voidptr",
        "setwriteable",
        [FixParameter("bool", "bool", None)],
    ),
    AnnotationFix(
        "QtCore",
        "QObject",
        "findChildren",
        [
            FixParameter(
                "types",
                "typing.Tuple[typing.Type[QObjectT], ...]",
                "typing.Tuple",
            ),
            FixParameter("name", "str", "str"),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        'QObjectT = typing.TypeVar("QObjectT", bound=QObject)',
    ),
    AnnotationFix(
        "QtCore",
        "QObject",
        "findChildren",
        [
            FixParameter(
                "types",
                "typing.Tuple[typing.Type[QObjectT], ...]",
                "typing.Tuple",
            ),
            FixParameter("re", '"QRegularExpression"', '"QRegularExpression"'),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        'QObjectT = typing.TypeVar("QObjectT", bound=QObject)',
    ),
    AnnotationFix(
        "QtCore",
        "QObject",
        "findChild",
        [
            FixParameter(
                "types",
                "typing.Tuple[typing.Type[QObjectT], ...]",
                "typing.Tuple",
            ),
            FixParameter("name", '"str"', '"str"'),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        'QObjectT = typing.TypeVar("QObjectT", bound=QObject)',
    ),
    AnnotationFix(
        "QtDBus",
        "QDBusAbstractInterface",
        "asyncCall",
        [
            FixParameter("method", "str", "str"),
            FixParameter("*a1", "typing.Any", None),
        ],
    ),
    AnnotationFix(
        "QtDBus",
        "QDBusAbstractInterface",
        "call",
        [
            FixParameter("method", "str", "str"),
            FixParameter("*a1", "typing.Any", None),
        ],
    ),
    AnnotationFix(
        "QtDBus",
        "QDBusAbstractInterface",
        "call",
        [
            FixParameter("mode", '"QDBus.CallMode"', '"QDBus.CallMode"'),
            FixParameter("method", "str", "str"),
            FixParameter("*a2", "typing.Any", None),
        ],
    ),
    AnnotationFix(
        "QtWidgets",
        "QAbstractItemView",
        "setModel",
        [
            FixParameter(
                "model",
                "typing.Optional[QtCore.QAbstractItemModel]",
                "QtCore.QAbstractItemModel",
            ),
        ],
    ),
    AnnotationFix(
        "QtWidgets",
        "QColumnView",
        "setModel",
        [
            FixParameter(
                "model",
                "typing.Optional[QtCore.QAbstractItemModel]",
                "QtCore.QAbstractItemModel",
            ),
        ],
    ),
    AnnotationFix(
        "QtWidgets",
        "QHeaderView",
        "setModel",
        [
            FixParameter(
                "model",
                "typing.Optional[QtCore.QAbstractItemModel]",
                "QtCore.QAbstractItemModel",
            ),
        ],
    ),
    AnnotationFix(
        "QtWidgets",
        "QTableView",
        "setModel",
        [
            FixParameter(
                "model",
                "typing.Optional[QtCore.QAbstractItemModel]",
                "QtCore.QAbstractItemModel",
            ),
        ],
    ),
    AnnotationFix(
        "QtWidgets",
        "QTreeView",
        "setModel",
        [
            FixParameter(
                "model",
                "typing.Optional[QtCore.QAbstractItemModel]",
                "QtCore.QAbstractItemModel",
            ),
        ],
    ),
    AnnotationFix(
        "QtWidgets",
        "QMessageBox",
        "aboutQt",
        [
            FixParameter(
                "parent",
                "typing.Optional[QWidget]",
                "QWidget",
            ),
            FixParameter("title", "str", "str"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtWidgets",
        "QMessageBox",
        "about",
        [
            FixParameter(
                "parent",
                "typing.Optional[QWidget]",
                "QWidget",
            ),
            FixParameter("caption", "str", "str"),
            FixParameter("text", "str", "str"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtWidgets",
        "QProgressDialog",
        "setCancelButton",
        [
            FixParameter(
                "button",
                "typing.Optional[QPushButton]",
                "QPushButton",
            ),
        ],
    ),
]

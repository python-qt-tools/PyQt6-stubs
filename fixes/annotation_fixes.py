"""Definition of all annotation fixes."""

from dataclasses import dataclass
from typing import List, Optional


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
]
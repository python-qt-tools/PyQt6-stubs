"""Definition of all annotation fixes."""

from dataclasses import dataclass
from typing import List, Optional, Union

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
    return_value: Optional[str] = None
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
class AddAnnotationFix:
    """Adds annotations to a class."""

    module_name: str  # name of the module in which the fix will be applied
    class_name: str  # name of the class the method belongs to
    annotations: List[str]  # annotations to be added.


# Fix definitions
ANNOTATION_FIXES: List[Union[AnnotationFix, AddAnnotationFix]] = [
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
                "type",
                "typing.Type[QObjectT]",
                "type",
            ),
            FixParameter("name", "str", "str"),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        'typing.List["QObjectT"]',
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
            FixParameter("name", "str", "str"),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        'typing.List["QObjectT"]',
        'QObjectT = typing.TypeVar("QObjectT", bound=QObject)',
    ),
    AnnotationFix(
        "QtCore",
        "QObject",
        "findChildren",
        [
            FixParameter(
                "type",
                "typing.Type[QObjectT]",
                "type",
            ),
            FixParameter("re", '"QRegularExpression"', '"QRegularExpression"'),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        'typing.List["QObjectT"]',
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
        'typing.List["QObjectT"]',
        'QObjectT = typing.TypeVar("QObjectT", bound=QObject)',
    ),
    AnnotationFix(
        "QtCore",
        "QObject",
        "findChild",
        [
            FixParameter(
                "type",
                "typing.Type[QObjectT]",
                "type",
            ),
            FixParameter("name", "str", "str"),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        '"QObjectT"',
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
            FixParameter("name", "str", "str"),
            FixParameter(
                "options", "Qt.FindChildOption", "Qt.FindChildOption"
            ),
        ],
        '"QObjectT"',
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
    AddAnnotationFix(
        "QtWidgets",
        "QTreeWidgetItem",
        ['def __lt__(self, other: "QTreeWidgetItem") -> bool: ...'],
    ),
    AddAnnotationFix(
        "QtWidgets",
        "QTableWidgetItem",
        [
            "def __eq__(self, other: object) -> bool: ...",
            "def __ge__(self, other: object) -> bool: ...",
            "def __gt__(self, other: object) -> bool: ...",
            "def __le__(self, other: object) -> bool: ...",
            "def __lt__(self, other: object) -> bool: ...",
            "def __ne__(self, other: object) -> bool: ...",
        ],
    ),
    AnnotationFix(
        "QtCore",
        "QCoreApplication",
        "instance",
        [],
        'typing.Optional["QCoreApplication"]',
        static=True,
    ),
    AddAnnotationFix(
        "QtCore",
        "QCoreApplication",
        [
            "applicationNameChanged: typing.ClassVar[pyqtSignal]",
            "applicationVersionChanged: typing.ClassVar[pyqtSignal]",
            "organizationDomainChanged: typing.ClassVar[pyqtSignal]",
            "organizationNameChanged: typing.ClassVar[pyqtSignal]",
        ],
    ),
    AnnotationFix(
        "QtCore",
        "QJsonDocument",
        "__init__",
        [
            FixParameter(
                "array",
                'typing.Iterable[typing.Union["QJsonValue", "QJsonValue.Type", typing.Dict[str, "QJsonValue"], bool, int, float, str]]',
                'typing.Iterable["QJsonValue"]',
            ),
        ],
    ),
    AnnotationFix(
        "QtCore",
        "QJsonDocument",
        "setArray",
        [
            FixParameter(
                "array",
                'typing.Iterable[typing.Union["QJsonValue", "QJsonValue.Type", typing.Dict[str, "QJsonValue"], bool, int, float, str]]',
                'typing.Iterable["QJsonValue"]',
            ),
        ],
    ),
    AnnotationFix(
        "QtCore",
        "QJsonValue",
        "toArray",
        [
            FixParameter(
                "defaultValue",
                'typing.Iterable[typing.Union["QJsonValue", "QJsonValue.Type", typing.Dict[str, "QJsonValue"], bool, int, float, str]]',
                'typing.Iterable["QJsonValue"]',
            ),
        ],
    ),
    AddAnnotationFix(
        "QtCore",
        "QPoint",
        [
            'def __add__(self, point: "QPoint") -> "QPoint": ...',
            'def __sub__(self, point: "QPoint") -> "QPoint": ...',
            'def __mul__(self, factor: float) -> "QPoint": ...',
            'def __truediv__(self, divisor: float) -> "QPoint": ...',
        ],
    ),
    AddAnnotationFix(
        "QtCore",
        "QPointF",
        [
            'def __add__(self, point: "QPointF") -> "QPointF": ...',
            'def __sub__(self, point: "QPointF") -> "QPointF": ...',
            'def __mul__(self, factor: float) -> "QPointF": ...',
            'def __truediv__(self, divisor: float) -> "QPointF": ...',
        ],
    ),
    AddAnnotationFix(
        "QtCore",
        "QSize",
        [
            "def __eq__(self, value: object) -> bool: ...",
            "def __ne__(self, value: object) -> bool: ...",
            'def __add__(self, value: "QSize") -> "QSize": ...',
            'def __iadd__(self, value: "QSize") -> "QSize": ...',
            'def __sub__(self, value: "QSize") -> "QSize": ...',
            'def __isub__(self, value: "QSize") -> "QSize": ...',
            'def __mul__(self, value: float) -> "QSize": ...',
            'def __rmul__(self, value: float) -> "QSize": ...',
            'def __imul__(self, value: float) -> "QSize": ...',
            'def __truediv__(self, value: float) -> "QSize": ...',
            'def __itruediv__(self, value: float) -> "QSize": ...',
        ],
    ),
    AddAnnotationFix(
        "QtCore",
        "QSizeF",
        [
            "def __eq__(self, value: object) -> bool: ...",
            "def __ne__(self, value: object) -> bool: ...",
            'def __add__(self, value: "QSizeF") -> "QSizeF": ...',
            'def __iadd__(self, value: "QSizeF") -> "QSizeF": ...',
            'def __sub__(self, value: "QSizeF") -> "QSizeF": ...',
            'def __isub__(self, value: "QSizeF") -> "QSizeF": ...',
            'def __mul__(self, value: float) -> "QSizeF": ...',
            'def __rmul__(self, value: float) -> "QSizeF": ...',
            'def __imul__(self, value: float) -> "QSizeF": ...',
            'def __truediv__(self, value: float) -> "QSizeF": ...',
            'def __itruediv__(self, value: float) -> "QSizeF": ...',
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawConvexPolygon",
        [
            FixParameter("point", "QtCore.QPointF", "QtCore.QPointF"),
            FixParameter("*a1", "QtCore.QPointF", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawConvexPolygon",
        [
            FixParameter("point", "QtCore.QPoint", "QtCore.QPoint"),
            FixParameter("*a1", "QtCore.QPoint", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawPolygon",
        [
            FixParameter("point", "QtCore.QPointF", "QtCore.QPointF"),
            FixParameter("*a1", "QtCore.QPointF", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawPolygon",
        [
            FixParameter("point", "QtCore.QPoint", "QtCore.QPoint"),
            FixParameter("*a1", "QtCore.QPoint", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawPolyline",
        [
            FixParameter("point", "QtCore.QPointF", "QtCore.QPointF"),
            FixParameter("*a1", "QtCore.QPointF", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawPolyline",
        [
            FixParameter("point", "QtCore.QPoint", "QtCore.QPoint"),
            FixParameter("*a1", "QtCore.QPoint", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawRects",
        [
            FixParameter("rect", "QtCore.QRectF", "QtCore.QRectF"),
            FixParameter("*a1", "QtCore.QRectF", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawRects",
        [
            FixParameter("rect", "QtCore.QRect", "QtCore.QRect"),
            FixParameter("*a1", "QtCore.QRect", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawLines",
        [
            FixParameter("line", "QtCore.QLineF", "QtCore.QLineF"),
            FixParameter("*a1", "QtCore.QLineF", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawLines",
        [
            FixParameter("line", "QtCore.QLine", "QtCore.QLine"),
            FixParameter("*a1", "QtCore.QLine", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawLines",
        [
            FixParameter("pointPair", "QtCore.QPointF", "QtCore.QPointF"),
            FixParameter("*a1", "QtCore.QPointF", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawLines",
        [
            FixParameter("pointPair", "QtCore.QPoint", "QtCore.QPoint"),
            FixParameter("*a1", "QtCore.QPoint", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawPoints",
        [
            FixParameter("point", "QtCore.QPointF", "QtCore.QPointF"),
            FixParameter("*a1", "QtCore.QPointF", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPainter",
        "drawPoints",
        [
            FixParameter("point", "QtCore.QPoint", "QtCore.QPoint"),
            FixParameter("*a1", "QtCore.QPoint", None),
        ],
    ),
]

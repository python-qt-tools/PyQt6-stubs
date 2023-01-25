"""Definition of all annotation fixes."""

from dataclasses import dataclass
from typing import List, Optional, Union

from libcst import ClassDef, Decorator, FunctionDef


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

    node: Union[ClassDef, FunctionDef, Decorator]
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
        "QAbstractEventDispatcher",
        "filterNativeEvent",
        [
            FixParameter("eventType", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
            FixParameter("message", "PyQt6.sip.voidptr", "PyQt6.sip.voidptr"),
        ],
    ),


    AnnotationFix(
        "QtCore",
        "QAbstractNativeEventFilter",
        "nativeEventFilter",
        [
            FixParameter("eventType", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
            FixParameter("message", "PyQt6.sip.voidptr", "PyQt6.sip.voidptr"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QBuffer",
        "setData",
        [
            FixParameter("data", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
        ],
    ),


    AnnotationFix(
        "QtCore",
        "QByteArray",
        "__init__",
        [
            FixParameter("a", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QByteArray",
        "fromBase64Encoding",
        [
            FixParameter("base64", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
            FixParameter("options", '"QByteArray.Base64Option"', '"QByteArray.Base64Option"'),
        ],
        static = True,
    ),

    AnnotationFix(
        "QtCore",
        "QByteArray",
        "fromPercentEncoding",
        [
            FixParameter("input", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
            FixParameter("percent", "str", "str"),
        ],
        static = True,
    ),

    AnnotationFix(
        "QtCore",
        "QByteArray",
        "toPercentEncoding",
        [
            FixParameter("exclude", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
            FixParameter("include", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
            FixParameter("percent", "str", "str"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QByteArray",
        "fromHex",
        [
            FixParameter("hexEncoded", 'typing.Union["QByteArray", bytes, bytearray]', '"QByteArray"'),
        ],
        static = True,
    ),


    AnnotationFix(
        "QtCore",
        "QByteArrayMatcher",
        "setPattern",
        [
            FixParameter("pattern", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QCborStreamReader",
        "__init__",
        [
            FixParameter("data", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QCborStreamReader",
        "addData",
        [
            FixParameter("data", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QDynamicPropertyChangeEvent",
        "__init__",
        [
            FixParameter("name", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),


    AnnotationFix(
        "QtCore",
        "QFile",
        "decodeName",
        [
            FixParameter("localFileName", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static = True,
    ),

    AnnotationFix(
        "QtCore",
        "QJsonDocument",
        "fromJson",
        [
            FixParameter("json", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("error", "typing.Optional[QJsonParseError]", "typing.Optional[QJsonParseError]"),
        ],
        static = True,
    ),

    AnnotationFix(
        "QtCore",
        "QMessageAuthenticationCode",
        "__init__",
        [
            FixParameter("method", "QCryptographicHash.Algorithm", "QCryptographicHash.Algorithm"),
            FixParameter("key", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QMessageAuthenticationCode",
        "hash",
        [
            FixParameter("message", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("key", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("method", "QCryptographicHash.Algorithm", "QCryptographicHash.Algorithm")
        ],
        static = True,
    ),

    AnnotationFix(
        "QtCore",
        "QMimeData",
        "setData",
        [
            FixParameter("mimetype", "str", "str"),
            FixParameter("data", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QMimeDatabase",
        "mimeTypeForFileNameAndData",
        [
            FixParameter("fileName", "str", "str"),
            FixParameter("data", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QMimeDatabase",
        "mimeTypeForData",
        [
            FixParameter("data", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
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

    AnnotationFix(
        "QtCore",
        "QPropertyAnimation",
        "__init__",
        [
            FixParameter("target", "QObject", "QObject"),
            FixParameter("propertyName", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("parent", "typing.Optional[QObject]", "typing.Optional[QObject]"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QPropertyAnimation",
        "setPropertyName",
        [
            FixParameter("propertyName", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
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
        "QtCore",
        "QTimeZone",
        "__init__",
        [
            FixParameter("ianaId", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtCore",
        "QTimeZone",
        "__init__",
        [
            FixParameter("zoneId", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("offsetSeconds", "int", "int"),
            FixParameter("name", "str", "str"),
            FixParameter("abbreviation", "str", "str"),
            FixParameter("territory", "QLocale.Country", "QLocale.Country"),
            FixParameter("comment", "str", "str"),
        ],
    ),
    AnnotationFix(
        "QtCore",
        "QTimeZone",
        "windowsIdToIanaIds",
        [
            FixParameter("windowsId", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QTimeZone",
        "windowsIdToDefaultIanaId",
        [
            FixParameter("windowsId", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QTimeZone",
        "windowsIdToDefaultIanaId",
        [
            FixParameter("windowsId", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("territory", "QLocale.Country", "QLocale.Country"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QTimeZone",
        "ianaIdToWindowsId",
        [
            FixParameter("ianaId", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QTimeZone",
        "isTimeZoneIdAvailable",
        [
            FixParameter("ianaId", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),


    AnnotationFix(
        "QtCore",
        "QUrl",
        "fromAce",
        [
            FixParameter("domain", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("options", '"QUrl.AceProcessingOption"', '"QUrl.AceProcessingOption"'),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QUrl",
        "toPercentEncoding",
        [
            FixParameter("input", "str", "str"),
            FixParameter("exclude", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("include", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QUrl",
        "fromPercentEncoding",
        [
            FixParameter("a0", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QUrl",
        "fromEncoded",
        [
            FixParameter("u", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
            FixParameter("mode", '"QUrl.ParsingMode"', '"QUrl.ParsingMode"'),
        ],
        static=True,
    ),

    AnnotationFix(
        "QtCore",
        "QUuid",
        "__init__",
        [
            FixParameter("string", "typing.Union[QByteArray, str, bytes, bytearray]", "typing.Union[QByteArray, str]"),
        ],
    ),
    AnnotationFix(
        "QtCore",
        "QUuid",
        "createUuidV5",
        [
            FixParameter("ns", '"QUuid"', '"QUuid"'),
            FixParameter("baseData", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtCore",
        "QUuid",
        "createUuidV3",
        [
            FixParameter("ns", '"QUuid"', '"QUuid"'),
            FixParameter("baseData", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
        static=True,
    ),

    AnnotationFix(
        "QtCore",
        "QXmlStreamReader",
        "__init__",
        [
            FixParameter("data", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QXmlStreamReader",
        "addData",
        [
            FixParameter("data", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtCore",
        "QXmlStreamWriter",
        "__init__",
        [
            FixParameter("array", "typing.Union[QByteArray, bytes, bytearray]", "QByteArray"),
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
    AnnotationFix(
        "QtGui",
        "QPolygon",
        "putPoints",
        [
            FixParameter("index", "int", "int"),
            FixParameter("firstx", "int", "int"),
            FixParameter("firsty", "int", "int"),
            FixParameter("*a3", "int", None),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QPolygon",
        "setPoints",
        [
            FixParameter("firstx", "int", "int"),
            FixParameter("firsty", "int", "int"),
            FixParameter("*a2", "int", None),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QPixmap",
        "loadFromData",
        [
            FixParameter("buf", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("format", "typing.Optional[str]", "typing.Optional[str]"),
            FixParameter("flags", "QtCore.Qt.ImageConversionFlag", "QtCore.Qt.ImageConversionFlag"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QColor",
        "isValidColorName",
        [
            FixParameter("a0", "typing.Union[QtCore.QByteArray, bytes, bytearray, str]", "typing.Union[QtCore.QByteArray, str]"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtGui",
        "QColor",
        "fromString",
        [
            FixParameter("name", "typing.Union[QtCore.QByteArray, bytes, bytearray, str]", "typing.Union[QtCore.QByteArray, str]"),
        ],
        static=True,
    ),


    AnnotationFix(
        "QtGui",
        "QColorSpace",
        "fromIccProfile",
        [
            FixParameter("iccProfile", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
        static=True,
    ),

    AnnotationFix(
        "QtGui",
        "QFontDatabase",
        "addApplicationFontFromData",
        [
            FixParameter("fontData", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
        static=True,
    ),

    AnnotationFix(
        "QtGui",
        "QImageIOHandler",
        "setFormat",
        [
            FixParameter("format", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QImageReader",
        "__init__",
        [
            FixParameter("device", "QtCore.QIODevice", "QtCore.QIODevice"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QImageReader",
        "__init__",
        [
            FixParameter("fileName", "str", "str"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QImageReader",
        "imageFormatsForMimeType",
        [
            FixParameter("mimeType", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtGui",
        "QImageReader",
        "setFormat",
        [
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QImageWriter",
        "__init__",
        [
            FixParameter("device", "QtCore.QIODevice", "QtCore.QIODevice"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QImageWriter",
        "__init__",
        [
            FixParameter("fileName", "str", "str"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QImageWriter",
        "imageFormatsForMimeType",
        [
            FixParameter("mimeType", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtGui",
        "QImageWriter",
        "setSubType",
        [
            FixParameter("type", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QImageWriter",
        "setFormat",
        [
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QMovie",
        "__init__",
        [
            FixParameter("device", "QtCore.QIODevice", "QtCore.QIODevice"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("parent", "typing.Optional[QtCore.QObject]", "typing.Optional[QtCore.QObject]"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QMovie",
        "__init__",
        [
            FixParameter("fileName", "str", "str"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("parent", "typing.Optional[QtCore.QObject]", "typing.Optional[QtCore.QObject]"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QMovie",
        "setFormat",
        [
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QOpenGLContext",
        "hasExtension",
        [
            FixParameter("extension", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QOpenGLContext",
        "getProcAddress",
        [
            FixParameter("procName", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QPdfWriter",
        "setDocumentXmpMetadata",
        [
            FixParameter("xmpMetadata", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QRawFont",
        "__init__",
        [
            FixParameter("fontData", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("pixelSize", "float", "float"),
            FixParameter("hintingPreference", "QFont.HintingPreference", "QFont.HintingPreference"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QRawFont",
        "loadFromData",
        [
            FixParameter("fontData", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("pixelSize", "float", "float"),
            FixParameter("hintingPreference", "QFont.HintingPreference", "QFont.HintingPreference"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QStandardItemModel",
        "setItemRoleNames",
        [
            FixParameter("roleNames", "typing.Dict[int, typing.Union[QtCore.QByteArray, bytes, bytearray]]", "typing.Dict[int, QtCore.QByteArray]"),
        ],
    ),

    AnnotationFix(
        "QtGui",
        "QTextDocumentWriter",
        "__init__",
        [
            FixParameter("device", "QtCore.QIODevice", "QtCore.QIODevice"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QTextDocumentWriter",
        "__init__",
        [
            FixParameter("fileName", "str", "str"),
            FixParameter("format", "typing.Union[QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtGui",
        "QTextDocumentWriter",
        "setFormat",
        [
            FixParameter("format", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtNetwork",
        "QHttpPart",
        "setBody",
        [
            FixParameter("body", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QHttpPart",
        "setRawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("headerValue", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QHttpMultiPart",
        "setBoundary",
        [
            FixParameter("boundary", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtNetwork",
        "QNetworkAccessManager",
        "put",
        [
            FixParameter("request", '"QNetworkRequest"', '"QNetworkRequest"'),
            FixParameter("data", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkAccessManager",
        "post",
        [
            FixParameter("request", '"QNetworkRequest"', '"QNetworkRequest"'),
            FixParameter("data", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtNetwork",
        "QNetworkCookie",
        "__init__",
        [
            FixParameter("name", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("value", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    AnnotationFix(
        "QtNetwork",
        "QSslCertificate",
        "__init__",
        [
            FixParameter("data", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("format", "QSsl.EncodingFormat", "QSsl.EncodingFormat"),
        ],
    ),

    AnnotationFix(
        "QtNetwork",
        "QNetworkCookie",
        "parseCookies",
        [
            FixParameter("cookieString", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
        static=True,
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkProxy",
        "setRawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("value", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkProxy",
        "rawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkProxy",
        "hasRawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkReply",
        "setRawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("value", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkReply",
        "rawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkReply",
        "hasRawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkRequest",
        "setRawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("value", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkRequest",
        "rawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QNetworkRequest",
        "hasRawHeader",
        [
            FixParameter("headerName", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslCertificate",
        "importPkcs12",
        [
            FixParameter("device", "QtCore.QIODevice", "QtCore.QIODevice"),
            FixParameter("key", '"QSslKey"', '"QSslKey"'),
            FixParameter("certificate", '"QSslCertificate"', '"QSslCertificate"'),
            FixParameter("caCertificates", 'typing.Optional[typing.Iterable["QSslCertificate"]]', 'typing.Optional[typing.Iterable["QSslCertificate"]]'),
            FixParameter("passPhrase", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
        static=True
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslCertificate",
        "fromData",
        [
            FixParameter("data", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("format", "QSsl.EncodingFormat", "QSsl.EncodingFormat"),
        ],
        static=True
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslCertificate",
        "subjectInfo",
        [
            FixParameter("attribute", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslCertificate",
        "issuerInfo",
        [
            FixParameter("attribute", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    #AnnotationFix(
    #    "QtNetwork",
    #    "QSslConfiguration",
    #    "setBackendConfiguration",
    #    [
    #        FixParameter("backendConfiguration", "typing.Dict[typing.Union[QtCore.QByteArray, bytes, bytearray], typing.Any]", "typing.Dict[QtCore.QByteArray, typing.Any]"),
    #    ],
    #),
    AnnotationFix(
        "QtNetwork",
        "QSslConfiguration",
        "setBackendConfigurationOption",
        [
            FixParameter("name", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("value", "typing.Any", "typing.Any"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslConfiguration",
        "setPreSharedKeyIdentityHint",
        [
            FixParameter("hint", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    #AnnotationFix(
    #    "QtNetwork",
    #    "QSslConfiguration",
    #    "setAllowedNextProtocols",
    #    [
    #        FixParameter("protocols", "typing.Iterable[typing.Union[QtCore.QByteArray, bytes, bytearray]]", "typing.Iterable[QtCore.QByteArray]"),
    #    ],
    #),
    AnnotationFix(
        "QtNetwork",
        "QSslConfiguration",
        "setSessionTicket",
        [
            FixParameter("sessionTicket", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslDiffieHellmanParameters",
        "fromEncoded",
        [
            FixParameter("encoded", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
            FixParameter("encoding", "QSsl.EncodingFormat", "QSsl.EncodingFormat"),
        ],
        static=True
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslKey",
        "toDer",
        [
            FixParameter("passPhrase", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslKey",
        "toPem",
        [
            FixParameter("passPhrase", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslPreSharedKeyAuthenticator",
        "setPreSharedKey",
        [
            FixParameter("preSharedKey", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslPreSharedKeyAuthenticator",
        "setIdentity",
        [
            FixParameter("identity", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),
    AnnotationFix(
        "QtNetwork",
        "QSslSocket",
        "setPrivateKey",
        [
            FixParameter("fileName", "str", "str"),
            FixParameter("algorithm", "QSsl.KeyAlgorithm", "QSsl.KeyAlgorithm"),
            FixParameter("format", "QSsl.EncodingFormat", "QSsl.EncodingFormat"),
            FixParameter("passPhrase", "typing.Union[QtCore.QByteArray, bytes, bytearray]", "QtCore.QByteArray"),
        ],
    ),

    #{ mimeData fixes
    AnnotationFix(
        "QtCore",
        "QAbstractItemModel",
        "mimeData",
        [
            FixParameter("indexes", "typing.Iterable[QModelIndex]", "typing.Iterable[QModelIndex]"),
        ],
        return_value = '"QMimeData" | None',
    ),

    AnnotationFix(
        "QtCore",
        "QAbstractProxyModel",
        "mimeData",
        [
            FixParameter("indexes", "typing.Iterable[QModelIndex]", "typing.Iterable[QModelIndex]"),
        ],
        return_value = '"QMimeData" | None',
    ),
    AnnotationFix(
        "QtCore",
        "QConcatenateTablesProxyModel",
        "mimeData",
        [
            FixParameter("indexes", "typing.Iterable[QModelIndex]", "typing.Iterable[QModelIndex]"),
        ],
        return_value = '"QMimeData" | None',
    ),
    AnnotationFix(
        "QtCore",
        "QSortFilterProxyModel",
        "mimeData",
        [
            FixParameter("indexes", "typing.Iterable[QModelIndex]", "typing.Iterable[QModelIndex]"),
        ],
        return_value = '"QMimeData" | None',
    ),

    AnnotationFix(
        "QtGui",
        "QFileSystemModel",
        "mimeData",
        [
            FixParameter("indexes", "typing.Iterable[QtCore.QModelIndex]", "typing.Iterable[QtCore.QModelIndex]"),
        ],
        return_value = "QtCore.QMimeData | None",
    ),
    AnnotationFix(
        "QtGui",
        "QStandardItemModel",
        "mimeData",
        [
            FixParameter("indexes", "typing.Iterable[QtCore.QModelIndex]", "typing.Iterable[QtCore.QModelIndex]"),
        ],
        return_value = "QtCore.QMimeData | None",
    ),

    AnnotationFix(
        "QtWidgets",
        "QListWidget",
        "mimeData",
        [
            FixParameter("items", "typing.Iterable[QListWidgetItem]", "typing.Iterable[QListWidgetItem]"),
        ],
        return_value = "QtCore.QMimeData | None",
    ),
    AnnotationFix(
        "QtWidgets",
        "QTableWidget",
        "mimeData",
        [
            FixParameter("items", "typing.Iterable[QTableWidgetItem]", "typing.Iterable[QTableWidgetItem]"),
        ],
        return_value = "QtCore.QMimeData | None",
    ),
    AnnotationFix(
        "QtWidgets",
        "QTreeWidget",
        "mimeData",
        [
            FixParameter("items", "typing.Iterable[QTreeWidgetItem]", "typing.Iterable[QTreeWidgetItem]"),
        ],
        return_value = "QtCore.QMimeData | None",
    ),
    #}
]

"""Definition of all annnotation fixes."""

from dataclasses import dataclass
from typing import List


@dataclass
class Param:
    """Defines a single Parameter for a fix in AnnotationFix."""

    name: str  # name of the parameter
    annotation: str  # desired annotation as str
    # todo: Use to check if something expected has changed
    current_annotation: str | None  # current annotation as str
    # todo: return values!


@dataclass
class AnnotationFix:
    """Defines a Fix for an annotation of function parameter."""

    module_name: str  # name of the module in which the fix will be applied
    class_name: str  # name of the class the method belongs to
    method_name: str  # name of the method
    params: List[Param]  # List of the method's parameters


# Fix definitions
ANNOTATION_FIXES = [
    AnnotationFix(
        "QtWidgets",
        "QLineEdit",
        "setText",
        [Param("a0", "typing.Optional[str]", "str")],
    ),
    AnnotationFix(
        "sip",
        "voidptr",
        "setwriteable",
        [Param("bool", "bool", None)],
    ),
]

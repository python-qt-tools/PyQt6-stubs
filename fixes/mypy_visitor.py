"""Visitor that created AnnotationFixes from MypyFixes for a file."""
from __future__ import annotations

import re
from enum import IntEnum
from pathlib import Path
from typing import Dict, List, Tuple

from libcst import ClassDef, CSTVisitor, Decorator, FunctionDef, Name
from libcst.metadata import PositionProvider
from mypy import api as mypy_api

from fixes.annotation_fixes import (
    AddImportFix,
    CommentFix,
    RemoveFix,
    RemoveOverloadDecoratorFix,
)


class MypyVisitor(CSTVisitor):
    """Visitor that created AnnotationFixes from MypyFixes for a file."""

    METADATA_DEPENDENCIES = (PositionProvider,)
    RE_NAME_NOT_DEFINED = re.compile(r'Name "(.+)" is not defined')

    class ErrorType(IntEnum):
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

    def __init__(self, file: Path) -> None:
        super().__init__()
        self._path = file
        # collect all functions within a class
        self._class_functions: List[FunctionDef] = []
        self.fixes: List[
            CommentFix | RemoveFix | RemoveOverloadDecoratorFix | AddImportFix
        ] = []

        self._errors: Dict[int, MypyVisitor.ErrorType] = {}
        self._missing_imports: List[str] = []

        self.last_class_method: Dict[str, FunctionDef] = {}
        self._last_class: List[ClassDef] = []

        self._parse_mypy_result()
        if self._missing_imports:
            self._add_fix_for_missing_imports()

    def _parse_mypy_result(self) -> None:
        """Parse the results from a mypy run on the file."""
        print(f"Running mypy on file {self._path}")
        mypy_result = mypy_api.run([str(self._path), "--warn-unused-ignores"])[
            0
        ]

        if mypy_result.startswith("Success"):
            print(f"Mypy did not detect any errors for file {self._path}")
            return

        for line in mypy_result.split("\n"):
            try:
                line_nbr, error_msg = self._parse_line(line)
            except IndexError:
                continue

            match = self.RE_NAME_NOT_DEFINED.match(error_msg)
            if match:
                self._missing_imports.append(match.group(1))
            elif error_msg == (
                'Overload does not consistently use the "@staticmethod" '
                "decorator on all function signatures."
            ):
                self._add_error_type(
                    line_nbr, MypyVisitor.ErrorType.STATIC_MISMATCH
                )
            elif (
                (
                    "Signature of" in error_msg
                    and "incompatible with supertype" in error_msg
                )
                or (
                    " is incompatible with supertype " in error_msg
                    or " incompatible with return type " in error_msg
                )
                or (
                    "is incompatible with definition in base class"
                    in error_msg
                )
            ):
                # Those errors are violations of the Liskov Principle and can
                # only be ignored, since this is valid in Qt/C++.
                self._add_error_type(line_nbr, MypyVisitor.ErrorType.OVERRIDE)
            elif (
                "Overloaded function signature" in error_msg
                and "will never be matched: signature" in error_msg
                and "parameter type(s) are the same or broader" in error_msg
            ):
                self._add_error_type(
                    line_nbr, MypyVisitor.ErrorType.SIGNATURE_MISMATCH
                )
            else:
                print(
                    f"WARNING: Could not fix error in line {line_nbr}: {error_msg}"
                )

    def _add_fix_for_missing_imports(self) -> None:
        """Add a fix for missing imports."""
        # todo: could be done with libcst.codemod.visitors.AddImportsVisitor
        print(f"Missing imports: {self._missing_imports}")
        assert all(
            missing_import in ("QtCore", "QtGui")
            for missing_import in self._missing_imports
        )
        self.fixes.append(AddImportFix(list(set(self._missing_imports))))

    def _add_error_type(
        self, line_nbr: int, error_type: MypyVisitor.ErrorType
    ) -> None:
        """
        Add an error type for the given line.

        This is method will accept duplicate entries, but will raise a
        AssertionError, if the another type is already stored for the same
        line.
        """
        try:
            assert self._errors[line_nbr] == error_type
        except KeyError:
            self._errors[line_nbr] = error_type

    @staticmethod
    def _parse_line(line: str) -> Tuple[int, str]:
        try:
            line_nbr = int(line.split(":", 2)[1])
        except IndexError:
            # Ignore first line ("Found x errors[...]" and empty last line.
            # Raise an AssertionError for all others, to detect unhandled
            # messages.
            assert not line or (
                line.startswith("Found ") and line.endswith("source file)")
            )
            raise

        # Extract the error message:
        error_msg = line.split("error: ")[1]
        # If error is not in line (i.e. for notes), an IndexError is raised
        return line_nbr, error_msg

    def visit_FunctionDef(self, node: "FunctionDef") -> bool | None:
        """Visit a FunctionDef to co"""
        self._class_functions.append(node)
        return False

    def leave_FunctionDef(self, original_node: FunctionDef) -> None:
        """Leave the method and change signature if a signal."""
        # check if a decorator is the source of the problem
        try:
            fix = self._get_fix_for_function(original_node)
            self.fixes.append(fix)
        except ValueError:
            pass
        try:
            self.last_class_method[
                self._last_class[-1].name.value
            ] = original_node
        except IndexError:
            # If not in a class, skip.
            pass

    def visit_ClassDef(self, node: ClassDef) -> bool:
        """Put a class on top of the stack when visiting."""
        self._last_class.append(node)

        # Check if class needs to be fixed
        line = self.get_metadata(PositionProvider, node).start.line
        if line in self._errors:
            # Currently, only override comment is supported for classes.
            assert self._errors[line] == MypyVisitor.ErrorType.OVERRIDE
            print(f"Adding override comment to class: {node.name.value}")
            self.fixes.append(CommentFix(node, "# type: ignore[misc]"))

        # Visit every class in case there's a class in a class.
        return True

    def leave_ClassDef(self, original_node: ClassDef) -> None:
        """Check if any RemoveFixes made Decorators obsolete."""
        for fix in self.fixes:
            if (
                isinstance(fix, RemoveFix)
                and fix.node in self._class_functions
            ):
                remaining_functions = [
                    function
                    for function in self._class_functions
                    if isinstance(fix.node, FunctionDef)
                    and function.name.value == fix.node.name.value
                    and fix.node is not function
                ]
                if len(remaining_functions) == 1:
                    for decorator in remaining_functions[0].decorators:
                        if self._is_overload_decorator(decorator):
                            self.fixes.append(
                                RemoveOverloadDecoratorFix(decorator)
                            )
        self._class_functions.clear()
        self._last_class.pop()

    @staticmethod
    def _is_overload_decorator(decorator: Decorator) -> bool:
        """Check if a Decorator is an overload decorator."""
        return (
            len(decorator.decorator.children) >= 3
            and isinstance(decorator.decorator.children[0], Name)
            and isinstance(decorator.decorator.children[2], Name)
            and decorator.decorator.children[0].value == "typing"
            and decorator.decorator.children[2].value == "overload"
        )

    @staticmethod
    def _generate_fix(
        node: FunctionDef | Decorator, fix_type: MypyVisitor.ErrorType
    ) -> CommentFix | RemoveFix:
        """Generates a fix for a FunctionDef from a MypyFix."""
        if fix_type == MypyVisitor.ErrorType.OVERRIDE:
            return CommentFix(node, "# type: ignore[override]")
        if fix_type == MypyVisitor.ErrorType.SIGNATURE_MISMATCH:
            return RemoveFix(node)
        if fix_type == MypyVisitor.ErrorType.STATIC_MISMATCH:
            return CommentFix(node, "# type: ignore[misc]")
        raise ValueError(f"Could not detect fix type: {fix_type}")

    def _get_fix_for_function(
        self, function: FunctionDef
    ) -> CommentFix | RemoveFix:
        for decorator in function.decorators:
            try:
                error_type = self._errors[
                    self.get_metadata(PositionProvider, decorator).start.line
                ]
            except KeyError:
                continue
            return self._generate_fix(decorator, error_type)
        pos = self.get_metadata(PositionProvider, function).start.line
        try:
            error_type = self._errors[pos]
        except KeyError as exc:
            raise ValueError("No fix available for function") from exc
        return self._generate_fix(function, error_type)

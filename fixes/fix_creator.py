"""Visitor that created AnnotationFixes from MypyFixes for a file."""
from __future__ import annotations

from typing import List

from libcst import ClassDef, CSTVisitor, Decorator, FunctionDef, Name
from libcst.metadata import PositionProvider

from fixes.annotation_fixes import (
    AddImportFix,
    CommentFix,
    MypyFix,
    RemoveFix,
    RemoveOverloadDecoratorFix,
)


class FixCreator(CSTVisitor):
    """Visitor that created AnnotationFixes from MypyFixes for a file."""

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, mod_name: str, mypy_fixes: List[MypyFix]):
        super().__init__()
        self._module_name = mod_name
        # collect all functions within a class
        self._class_functions: List[FunctionDef] = []
        self._mypy_fixes = mypy_fixes
        self.fixes: List[
            CommentFix | RemoveFix | RemoveOverloadDecoratorFix | AddImportFix
        ] = []

        for fix in self._mypy_fixes:
            if fix.fix_type == MypyFix.Type.MISSING_IMPORT:
                self.fixes.append(AddImportFix(list(fix.data)))

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
                    if function.name.value == fix.node.name.value
                    and isinstance(fix.node, FunctionDef)
                    and fix.node is not function
                ]
                if len(remaining_functions) == 1:
                    for decorator in remaining_functions[0].decorators:
                        if self._is_overload_decorator(decorator):
                            self.fixes.append(
                                RemoveOverloadDecoratorFix(decorator)
                            )
        self._class_functions.clear()

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
        node: FunctionDef | Decorator, fix: MypyFix
    ) -> CommentFix | RemoveFix:
        """Generates a fix for a FunctionDef from a MypyFix."""
        if fix.fix_type == MypyFix.Type.OVERRIDE:
            return CommentFix(node, "# type: ignore[override]")
        if fix.fix_type == MypyFix.Type.SIGNATURE_MISMATCH:
            return RemoveFix(node)
        if fix.fix_type == MypyFix.Type.STATIC_MISMATCH:
            return CommentFix(node, "# type: ignore[misc]")
        raise ValueError(f"Could not detect fix type: {fix.fix_type}")

    def _get_fix_for_function(
        self, function: FunctionDef
    ) -> CommentFix | RemoveFix:
        for decorator in function.decorators:
            try:
                fix = self._get_mypy_fix(
                    self.get_metadata(PositionProvider, decorator).start.line
                )
                return self._generate_fix(decorator, fix)
            except ValueError:
                continue
        pos = self.get_metadata(PositionProvider, function).start.line
        end_pos = self.get_metadata(PositionProvider, function).end.line
        try:
            fix = self._get_mypy_fix(pos, end_pos)
            return self._generate_fix(function, fix)
        except ValueError:
            pass
        raise ValueError("No fix available for function")

    def _get_mypy_fix(
        self, start: int, end: int | None = None
    ) -> MypyFix | None:
        """Return a MypyFix for the given start and end line."""
        if end is None:
            end = start
        for mypy_fix in self._mypy_fixes:
            if mypy_fix.line_nbr and start <= mypy_fix.line_nbr <= end:
                return mypy_fix
        raise ValueError("No fix available")

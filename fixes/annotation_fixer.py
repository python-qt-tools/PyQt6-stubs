"""AnnotationFixer that will fix annotations on class methods."""
from __future__ import annotations

from typing import List, Union

from libcst import (
    Annotation,
    Assign,
    BaseSmallStatement,
    BaseStatement,
    ClassDef,
    CSTTransformer,
    FlattenSentinel,
    FunctionDef,
    Module,
    RemovalSentinel,
    SimpleStatementLine,
    parse_expression,
    parse_statement,
)

from fixes.annotation_fixes import ANNOTATION_FIXES, AnnotationFix


class AnnotationFixer(CSTTransformer):
    """AnnotationFixer that will fix annotations on class methods."""

    def __init__(self, mod_name: str):
        super().__init__()

        # ClassDef and FunctionDef visit stack
        self._last_class: List[ClassDef] = []
        self._last_function: List[FunctionDef] = []

        # Fixes that will be applied for the current module.
        self._fixes: List[AnnotationFix] = [
            fix for fix in ANNOTATION_FIXES if fix.module_name == mod_name
        ]

        # Custom type definitons to be inserted after PYQT_SLOT/PYQT_SIGNAL
        self._type_defs = set(
            fix.custom_type for fix in self._fixes if fix.custom_type
        )
        self._insert_type_defs = False

    @property
    def class_name(self) -> str | None:
        """Return the name of the current class."""
        try:
            return self._last_class[-1].name.value
        except IndexError:
            return None

    @property
    def function_name(self) -> str | None:
        """Return the name of the current function."""
        try:
            return self._last_function[-1].name.value
        except IndexError:
            return None

    def leave_Assign(
        self, original_node: Assign, updated_node: Assign
    ) -> Union[
        BaseSmallStatement,
        FlattenSentinel[BaseSmallStatement],
        RemovalSentinel,
    ]:
        name = original_node.targets[0].target.value  # type: ignore
        if name == "PYQT_SLOT":
            self._insert_type_defs = True
        return original_node

    def leave_SimpleStatementLine(
        self,
        original_node: SimpleStatementLine,
        updated_node: SimpleStatementLine,
    ) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        if self._insert_type_defs and self._type_defs:
            type_defs = list(map(parse_statement, self._type_defs))
            self._insert_type_defs = False
            return FlattenSentinel([updated_node, *type_defs])
        return updated_node

    def visit_ClassDef(self, node: ClassDef) -> bool:
        """Put a class on top of the stack when visiting."""
        self._last_class.append(node)
        # Visit every class in case there's a class in a class.
        return True

    def visit_FunctionDef(self, node: FunctionDef) -> bool:
        self._last_function.append(node)
        return False

    def leave_FunctionDef(
        self, original_node: FunctionDef, updated_node: FunctionDef
    ):
        """Remove a function from the stack and return the updated node."""
        if not self._last_class:
            # We need a class to operate, currently.
            self._last_function.pop()
            return updated_node

        # Check if we can fix the function.
        fix = self._get_fix()
        if fix:
            # Check every parameter and find the appropriate one to fix in the
            # source code.
            for param in fix.params:
                for original_param in updated_node.params.params:
                    if original_param.name.value == "self":
                        # Can we fix self? ;)
                        continue
                    # Fix the parameter
                    if original_param.name.value == param.name:
                        print(
                            f"Changing annotation of "
                            f"{self.function_name}:{original_param.name.value}"
                            f" to {param.annotation}"
                        )
                        expr = parse_expression(param.annotation)
                        anno = Annotation(annotation=expr)
                        updated_node = updated_node.with_deep_changes(
                            original_param, annotation=anno
                        )
            # Remove the fix from the class.
            self._fixes.remove(fix)
            self._last_function.pop()
            return updated_node
        self._last_function.pop()
        return updated_node

    def leave_ClassDef(
        self, original_node: ClassDef, updated_node: ClassDef
    ) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        """Remove a class from the stack and return the updated node."""
        self._last_class.pop()
        return updated_node

    def leave_Module(
        self, original_node: Module, updated_node: Module
    ) -> Module:
        """Check if all fixes were applied before leaving the module."""
        for fix in self._fixes:
            print(f"ERROR: Fix was not applied: {fix}")
        return updated_node

    def _get_fix(self) -> AnnotationFix | None:
        """Return the AnnotationFix for the current method if available."""
        for fix in self._fixes:
            if (
                fix.class_name == self.class_name
                and fix.method_name == self.function_name
            ):
                for param in self._last_function[-1].params.params:
                    if param.name.value == "self":
                        # ignore self params
                        continue
                    if not any(
                        fix_param.name == param.name.value
                        for fix_param in fix.params
                    ):
                        print(f"Fix does not match due to param: {param.name}")
                        break
                else:
                    print(f"Found fix to apply: {fix}")
                    return fix
        return None

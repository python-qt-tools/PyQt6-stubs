"""AnnotationFixer that will fix annotations on class methods."""
from __future__ import annotations

from typing import List

from libcst import (
    Annotation,
    BaseStatement,
    ClassDef,
    CSTTransformer,
    FlattenSentinel,
    FunctionDef,
    Module,
    RemovalSentinel,
    parse_expression,
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
        fix = self._get_fix()
        if fix:
            for param in fix.params:
                for idx, original_param in enumerate(
                    updated_node.params.params
                ):
                    if original_param.name.value == "self":
                        continue
                    if original_param.name.value == param.name:
                        print(
                            f"Changing annotation of "
                            f"{self.function_name}:{original_param.name.value}"
                            f" to {param.annotation}"
                        )
                        # if param.annotation not in ("bool", "str", "int", "float", "None"):
                        #     stmt = parse_statement(param.annotation)
                        #     # use the idx to access the params if changing more
                        #     # than one parameter
                        #     par_ref = updated_node.params.params[idx]
                        #     updated_node = updated_node.with_deep_changes(
                        #         par_ref, annotation=stmt
                        #     )
                        # else:
                        anno_ref = updated_node.params.params[idx]
                        expr = parse_expression(param.annotation)
                        # if anno_ref.annotation:
                        #     updated_node = updated_node.deep_replace(
                        #         anno_ref.annotation, expr
                        #     )
                        # else:
                        anno = Annotation(annotation=expr)
                        updated_node = updated_node.with_deep_changes(
                            anno_ref, annotation=anno
                        )
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

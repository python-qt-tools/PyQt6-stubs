"""Fixer that applies custom fixes."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import List, Type

from libcst import BaseStatement, ClassDef, CSTTransformer, FlattenSentinel, FunctionDef, RemovalSentinel, parse_statement

from fixes.base_fix import FixBase


class CustomFixer(CSTTransformer):
    """Fixer that applies custom fixes."""

    def __init__(self, mod_name: str):
        super().__init__()
        self._mod_name = mod_name
        self._last_class: List[ClassDef] = []

        self._fixes: List[Type[FixBase]] = []

        for path in Path("fixes").joinpath("custom_fixes").glob("*.py"):
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if spec is None or spec.loader is None:
                print(f"Warning, import did not work from {path}")
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
            for obj in module.__dict__.values():
                try:
                    if issubclass(obj, FixBase) and obj is not FixBase:
                        self._fixes.append(obj)
                except TypeError:
                    # If obj isn't a class
                    continue

    def visit_ClassDef(self, node: ClassDef) -> bool:
        """Put a class on top of the stack when visiting."""
        self._last_class.append(node)
        return True

    def leave_FunctionDef(self, original_node: FunctionDef, _: FunctionDef) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        """Leave the method and change signature if a signal."""
        for fix in self._fixes:
            try:
                if fix.qt_class == self._last_class[0].name.value and fix.qt_method == original_node.name.value:
                    return self.create_fix(fix)
            except IndexError:
                if fix.qt_class is None and fix.qt_method == original_node.name.value:
                    return self.create_fix(fix)
        return original_node

    @staticmethod
    def create_fix(fix: Type[FixBase]) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        """Creates a fix depending on the code to fix."""
        if isinstance(fix.fixed_code, str):
            # If the fix is just one statement, replace it.
            return parse_statement(fix.fixed_code)
        # For multiple statements a FlattenSentinel is returned.
        return FlattenSentinel([parse_statement(fix_str) for fix_str in fix.fixed_code])

    def leave_ClassDef(self, original_node: ClassDef, updated_node: ClassDef) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        """Remove a class from the stack and return the updated node."""
        self._last_class.pop()
        return updated_node

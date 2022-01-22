"""Fixer that visits classes and methods to fix unmatched signatures."""
from __future__ import annotations

from typing import List

from libcst import (
    BaseStatement,
    CSTTransformer,
    FlattenSentinel,
    FunctionDef,
    RemovalSentinel,
)
from libcst.metadata import PositionProvider


class SigMatchFixer(CSTTransformer):
    """Fixer that visits classes and methods to fix unmatched signatures."""

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, mod_name: str, remove_lines: List[int]):
        super().__init__()
        print(f"Removing from {mod_name} lines: {remove_lines}")
        self._module_name = mod_name
        self._remove_lines = remove_lines

    def leave_FunctionDef(
        self, original_node: FunctionDef, _: FunctionDef
    ) -> BaseStatement | FlattenSentinel[BaseStatement] | RemovalSentinel:
        """Leave the method and change signature if a signal."""
        pos = self.get_metadata(PositionProvider, original_node).start.line
        end_pos = self.get_metadata(PositionProvider, original_node).end.line
        if any(pos <= value <= end_pos for value in self._remove_lines):
            print(
                f"Removing node in modules {self._module_name} lines {pos}:{end_pos}"
            )
            return RemovalSentinel.REMOVE
        return original_node

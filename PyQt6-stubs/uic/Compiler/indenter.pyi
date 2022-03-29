from typing import Any

indentwidth: int

class _IndentedCodeWriter:
    level: int
    output: Any
    def __init__(self, output) -> None: ...
    def indent(self) -> None: ...
    def dedent(self) -> None: ...
    def write(self, line) -> None: ...

def createCodeIndenter(output) -> None: ...
def getIndenter(): ...
def write_code(string) -> None: ...
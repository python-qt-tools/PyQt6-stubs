from _typeshed import Incomplete

from .Compiler import compiler as compiler
from .Compiler import indenter as indenter

def compileUiDir(dir, recurse: bool = ..., map: Incomplete | None = ..., **compileUi_args) -> None: ...
def compileUi(uifile, pyfile, execute: bool = ..., indent: int = ...) -> None: ...

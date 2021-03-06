from ..properties import Properties as Properties
from ..uiparser import UIParser as UIParser
from . import qtproxies as qtproxies
from .indenter import createCodeIndenter as createCodeIndenter
from .indenter import getIndenter as getIndenter
from .indenter import write_code as write_code
from .qobjectcreator import CompilerCreatorPolicy as CompilerCreatorPolicy

class UICompiler(UIParser):
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def setContext(self, context) -> None: ...
    def createToplevelWidget(self, classname, widgetname): ...
    def setDelayedProps(self) -> None: ...
    def finalize(self) -> None: ...
    def compileUi(self, input_stream, output_stream): ...

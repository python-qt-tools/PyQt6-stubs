from typing import Any

from PyQt6 import QtCore as QtCore
from PyQt6 import QtGui as QtGui
from PyQt6 import QtWidgets as QtWidgets

from ..uiparser import UIParser as UIParser
from .qobjectcreator import LoaderCreatorPolicy as LoaderCreatorPolicy

class DynamicUILoader(UIParser):
    def __init__(self, package) -> None: ...
    def createToplevelWidget(self, classname, widgetname): ...
    toplevelInst: Any
    def loadUi(self, filename, toplevelInst): ...

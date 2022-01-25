import typing

from PyQt6 import QtCore, QtWidgets

q = QtCore.QObject()

a = q.findChildren(QtCore.QObject)  # type: typing.List[QtCore.QObject]
b = q.findChildren(QtWidgets.QWidget)  # type: typing.List[QtWidgets.QWidget]
c = q.findChildren((QtCore.QObject,))  # type: typing.List[QtCore.QObject]
d = q.findChildren((QtWidgets.QWidget,))  # type: typing.List[QtCore.QObject]
# desired error
# Incompatible types in assignment (expression has type "List[QObject]", variable has type "List[QWidget]")
# e = q.findChildren((QtWidgets.QWidget,))  # type: typing.List[QtWidgets.QWidget]

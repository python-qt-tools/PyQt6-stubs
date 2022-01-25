from PyQt6 import QtWidgets

a = (
    QtWidgets.QMessageBox.StandardButton.Ok
    | QtWidgets.QMessageBox.StandardButton.Ok
)  # type: QtWidgets.QMessageBox.StandardButton
b = QtWidgets.QMessageBox.StandardButton.Ok | 0  # type: int
c = a | 0  # type: QtWidgets.QMessageBox.StandardButton
d = (
    a | QtWidgets.QMessageBox.StandardButton.Ok
)  # type: QtWidgets.QMessageBox.StandardButton
e = a | a  # type: QtWidgets.QMessageBox.StandardButton

from PyQt6 import QtWidgets

a = (
    QtWidgets.QDialogButtonBox.StandardButton.Ok
    | QtWidgets.QDialogButtonBox.StandardButton.Ok
)  # type: QtWidgets.QDialogButtonBox.StandardButton
d = (
    a | QtWidgets.QDialogButtonBox.StandardButton.Ok
)  # type: QtWidgets.QDialogButtonBox.StandardButton
e = a | a  # type: QtWidgets.QDialogButtonBox.StandardButton

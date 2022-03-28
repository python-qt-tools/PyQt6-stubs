from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(["my_program", "-platform", "offscreen"])
widget = QWidget()
widget.ungrabGesture(Qt.GestureType.TapGesture)
widget.ungrabGesture(1)

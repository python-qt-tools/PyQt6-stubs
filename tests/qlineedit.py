"""Tests for QLineEdit."""
from PyQt6.QtWidgets import QApplication, QLineEdit

# test that QLineEdit.setText() accepts None as parameter
app = QApplication(["my_program", "-platform", "offscreen"])
edit = QLineEdit()
edit.setText(None)

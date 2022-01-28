from PyQt6.QtGui import QPolygon

polygon = QPolygon()
polygon.putPoints(1, 2, 3)
polygon.putPoints(1, 2, 3, 4)
polygon.putPoints(1, 2, 3, 5, 4, 3)

polygon.setPoints(1, 2)
polygon.setPoints(1, 2, 3)
polygon.setPoints(1, 2, 3, 4)

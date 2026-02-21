from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QRect
from typing import Callable

class MyWidget(QtWidgets.QWidget):
    def __init__(self, callback: Callable[[QRect], None]):
        super().__init__()
        self.callback = callback

        geometry = QtGui.QGuiApplication.primaryScreen().geometry()
        self.setGeometry(geometry)

        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )

        self.setWindowOpacity(0.3)
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("white"), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.unsetCursor()
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        rect = QRect(x1, y1, x2 - x1, y2 - y1)
        self.callback(rect)

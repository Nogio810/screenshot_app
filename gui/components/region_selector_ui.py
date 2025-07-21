import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QPainter, QPen, QColor, QCursor, QGuiApplication
from PyQt6.QtCore import QRect
from typing import Callable

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        geomtry = QGuiApplication.primaryScreen().geometry()
        screen_width = geomtry.width()
        screen_height = geomtry.height()
        self.setGeometry(0,0,screen_width, screen_height)
        self.setWindowTitle("")
        self.setWindowOpacity(0.3)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("White"), 3))
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
        self.close()
           
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.showWifget()
    sys.exit(app.exec())
from PyQt6 import QtWidgets, QtCore

class CountdownWindow(QtWidgets.Qwidget):
    def __init__(self, seconds:int, on_finish: callable[[], None]):
        super().__init__()
        self.seconds = seconds
        self.on_finish = on_finish
        
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel(str(self.seconds), self)
        self.label.setStyleSheet("font-size: 64px; color: white; background: rgba(0, 0, 0, 128); padding: 20px;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(200, 150)
        self.center_on_Screen()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def center_on_Screen(self):
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        self.move(screen.center() - self.rect().center())

    def update_countdown(self):
        self.seconds -= 1
        if self.seconds <= 0:
            self.timer.stop()
            self.hide()
            self.on_finish()
        else:
            self.label.setText(str(self.seconds))
from PyQt6 import QtWidgets, QtCore, QtGui


class CountdownWindow(QtWidgets.QWidget):
    def __init__(self, seconds: int, rect: QtCore.QRect, on_finish):
        super().__init__()

        self.seconds = seconds
        self.target_rect = rect
        self.on_finish = on_finish

        # フルスクリーン・枠なし・最前面
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        screen_geometry = QtWidgets.QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)

        # 中央ラベル（選択範囲の中央に配置）
        self.label = QtWidgets.QLabel(str(self.seconds), self)
        self.label.setStyleSheet("""
            font-size: 80px;
            color: white;
            background: rgba(0, 0, 0, 200);
            padding: 40px;
            border-radius: 30px;
        """)
        self.label.adjustSize()

        self._position_label()

        # タイマー
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

        self.show()

    # -------------------------
    # 数字を選択範囲中央へ配置
    # -------------------------
    def _position_label(self):
        center = self.target_rect.center()
        label_rect = self.label.rect()
        self.label.move(
            center.x() - label_rect.width() // 2,
            center.y() - label_rect.height() // 2
        )

    # -------------------------
    # 描画（選択範囲を半透明で暗くする）
    # -------------------------
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # 選択範囲に半透明黒
        overlay_color = QtGui.QColor(0, 0, 0, 120)
        painter.fillRect(self.target_rect, overlay_color)

    # -------------------------
    # カウント更新
    # -------------------------
    def update_countdown(self):
        self.seconds -= 1

        if self.seconds <= 0:
            self.timer.stop()
            self.close()
            self.on_finish()
        else:
            self.label.setText(str(self.seconds))
            self.label.adjustSize()
            self._position_label()

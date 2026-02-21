# core/capture_service.py

import mss
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QGuiApplication


def capture_region(rect: QRect | None):
    with mss.mss() as sct:

        if rect is None:
            screen = QGuiApplication.primaryScreen()
            geometry = screen.geometry()
            scale = screen.devicePixelRatio()

            monitor = {
                "top": int(geometry.y() * scale),
                "left": int(geometry.x() * scale),
                "width": int(geometry.width() * scale),
                "height": int(geometry.height() * scale)
            }
        else:
            screen = QGuiApplication.screenAt(rect.center())
            scale = screen.devicePixelRatio()

            monitor = {
                "top": int(rect.y() * scale),
                "left": int(rect.x() * scale),
                "width": int(rect.width() * scale),
                "height": int(rect.height() * scale)
            }

        return sct.grab(monitor)

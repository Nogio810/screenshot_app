# core/capture_controller.py

from PyQt6.QtCore import QTimer, Qt
from core.capture_service import capture_region
from core.save_service import SaveService


class CaptureController:
    def __init__(self, settings, rect, finished_callback):
        self.settings = settings
        self.rect = rect
        self.finished_callback = finished_callback

        self.save_service = SaveService(settings)

        self.timer = QTimer()
        self.timer.timeout.connect(self._capture_step)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)

        self.current_count = 0

    # -------------------------
    # 撮影開始
    # -------------------------
    def start(self):
        self.current_count = 0
        self._capture_step()

    def _capture_step(self):
        rect = None if self.settings.use_fullscreen else self.rect

        image = capture_region(rect)
        self.save_service.save_image(image)

        self.current_count += 1

        if (not self.settings.use_burst or
                self.current_count >= self.settings.burst_count):
            self._finish()
            return

        self._start_interval()

    def _start_interval(self):
        from gui.components.countdown_window import CountdownWindow

        self.countdown = CountdownWindow(
            seconds=self.settings.interval,
            rect=self.rect,
            on_finish=self._capture_step
        )

    # -------------------------
    # 終了処理
    # -------------------------
    def _finish(self):
        self.timer.stop()
        self.finished_callback()

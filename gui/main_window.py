from PyQt6 import QtWidgets
from PyQt6.QtCore import QRect, QTimer, Qt
from gui.components.settings_panel import SettingsPanel
from gui.components.region_selector_ui import MyWidget
from core.capture_controller import CaptureController


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot Tool")

        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.MSWindowsFixedSizeDialogHint
        )

        self.setFixedSize(self.sizeHint())

        self.is_running = False
        self.selected_rect: QRect | None = None

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.settings_panel = SettingsPanel()
        layout.addWidget(self.settings_panel)

        # 範囲選択はSettingsPanelのシグナル経由で受け取る
        self.settings_panel.select_region_requested.connect(self.select_region)

        self.start_button = QtWidgets.QPushButton("スタート")
        self.start_button.clicked.connect(self.start_clicked)
        layout.addWidget(self.start_button)

    def select_region(self):
        self.hide()
        QTimer.singleShot(200, self.start_selector)

    def start_selector(self):
        self.selector = MyWidget(self.region_selected)

    def region_selected(self, rect: QRect):
        self.selected_rect = rect
        self.show()

        self.settings_panel.region_x_edit.setText(str(rect.x()))
        self.settings_panel.region_y_edit.setText(str(rect.y()))
        self.settings_panel.region_w_edit.setText(str(rect.width()))
        self.settings_panel.region_h_edit.setText(str(rect.height()))

    def start_clicked(self):
        if self.is_running:
            return

        settings = self.settings_panel.get_settings()

        if not settings.use_fullscreen and settings.region_width == 0:
            QtWidgets.QMessageBox.warning(self, "エラー", "範囲を指定してください")
            return

        if not settings.save_dir:
            QtWidgets.QMessageBox.warning(self, "エラー", "保存先を指定してください")
            return

        self.is_running = True
        self.start_button.setEnabled(False)

        rect = None
        if not settings.use_fullscreen:
            rect = QRect(
                settings.region_x,
                settings.region_y,
                settings.region_width,
                settings.region_height
            )

        self.controller = CaptureController(
            settings,
            rect,
            self.capture_finished
        )
        self.hide()
        self.controller.start()

    def capture_finished(self):
        self.is_running = False
        self.start_button.setEnabled(True)
        self.show()
        QtWidgets.QMessageBox.information(self, "完了", "撮影終了")
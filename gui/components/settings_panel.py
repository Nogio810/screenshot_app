import os
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog
from models.settings_model import SettingsModel
from datetime import datetime


class SettingsPanel(QtWidgets.QWidget):
    select_region_requested = pyqtSignal()  # 範囲選択ボタンが押されたときにMainWindowへ通知

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_settings()
        self.create_widgets()

    def dirdialog_clicked(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        iDirPath = QFileDialog.getExistingDirectory(self, "保存先を選択", iDir)
        if iDirPath:
            self.settings.save_dir = iDirPath
            self.save_dir_edit.setText(iDirPath)

    def init_settings(self):
        self.settings = SettingsModel(
            save_dir=os.path.join(os.path.expanduser("~"), "Pictures"),
            filename="screenshot",
            use_timestamp=False,
            timestamp_format="%Y%m%d_%H%M%S",
            use_serial=True,
            serial_start=1,
            use_burst=False,
            burst_count=2,
            interval=1,
            image_format="png",
            use_fullscreen=False,
            region_x=0,
            region_y=0,
            region_width=0,
            region_height=0
        )

    def create_widgets(self):
        row = 0

        layout = QtWidgets.QGridLayout(self)

        # 保存場所
        layout.addWidget(QtWidgets.QLabel("保存場所："), row, 0)
        self.save_dir_edit = QtWidgets.QLineEdit(self.settings.save_dir)
        layout.addWidget(self.save_dir_edit, row, 1)
        self.save_dir_button = QtWidgets.QPushButton("参照")
        self.save_dir_button.clicked.connect(self.dirdialog_clicked)
        layout.addWidget(self.save_dir_button, row, 2)
        row += 1

        # ファイル名
        layout.addWidget(QtWidgets.QLabel("保存ファイル名："), row, 0)
        self.filename_edit = QtWidgets.QLineEdit(self.settings.filename)
        layout.addWidget(self.filename_edit, row, 1)
        row += 1

        # 画像保存形式
        layout.addWidget(QtWidgets.QLabel("保存形式:"), row, 0)
        self.image_format_combo = QtWidgets.QComboBox()
        self.image_format_combo.addItems(["png", "jpg", "bmp", "webp"])
        self.image_format_combo.setFixedWidth(80)
        self.image_format_combo.setCurrentText(self.settings.image_format)
        layout.addWidget(self.image_format_combo, row, 1)
        row += 1

        # タイムスタンプ使用
        self.use_timestamp_checkbox = QtWidgets.QCheckBox("タイムスタンプ")
        self.use_timestamp_checkbox.setChecked(self.settings.use_timestamp)
        layout.addWidget(self.use_timestamp_checkbox, row, 0, 1, 2)
        row += 1

        # タイムスタンプ形式
        layout.addWidget(QtWidgets.QLabel("タイムスタンプ形式："), row, 0)
        self.timestamp_format_edit = QtWidgets.QLineEdit(self.settings.timestamp_format)
        layout.addWidget(self.timestamp_format_edit, row, 1)
        row += 1

        # タイムスタンプ例表示
        self.timestamp_example_label = QtWidgets.QLabel()
        self.timestamp_example_label.setStyleSheet("color: gray;")
        layout.addWidget(self.timestamp_example_label, row, 1)
        row += 1

        # 連番使用
        self.use_serial_checkbox = QtWidgets.QCheckBox("連番")
        self.use_serial_checkbox.setChecked(self.settings.use_serial)
        layout.addWidget(self.use_serial_checkbox, row, 0, 1, 2)
        row += 1

        # 開始番号
        layout.addWidget(QtWidgets.QLabel("開始番号:"), row, 0)
        self.serial_start_spinbox = QtWidgets.QSpinBox()
        self.serial_start_spinbox.setMinimum(1)
        self.serial_start_spinbox.setMaximum(1000)
        self.serial_start_spinbox.setFixedWidth(80)
        self.serial_start_spinbox.setValue(self.settings.serial_start)
        layout.addWidget(self.serial_start_spinbox, row, 1)
        row += 1

        # 連続撮影
        self.use_burst_checkbox = QtWidgets.QCheckBox("連続撮影")
        self.use_burst_checkbox.setChecked(self.settings.use_burst)
        layout.addWidget(self.use_burst_checkbox, row, 0, 1, 2)
        row += 1

        # 連続撮影枚数
        layout.addWidget(QtWidgets.QLabel("連続撮影枚数:"), row, 0)
        self.burst_count_spinbox = QtWidgets.QSpinBox()
        self.burst_count_spinbox.setMinimum(1)
        self.burst_count_spinbox.setMaximum(1000)
        self.burst_count_spinbox.setFixedWidth(80)
        self.burst_count_spinbox.setValue(self.settings.burst_count)
        layout.addWidget(self.burst_count_spinbox, row, 1)
        row += 1

        # 撮影間隔
        layout.addWidget(QtWidgets.QLabel("撮影間隔 (秒):"), row, 0)
        self.interval_spinbox = QtWidgets.QSpinBox()
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setMaximum(1000)
        self.interval_spinbox.setFixedWidth(80)
        self.interval_spinbox.setValue(self.settings.interval)
        layout.addWidget(self.interval_spinbox, row, 1)
        row += 1

        # ---- 撮影範囲セクション ----

        # 範囲を選択ボタン（全画面チェック時はdisabled）
        self.select_region_button = QtWidgets.QPushButton("範囲を選択")
        self.select_region_button.clicked.connect(self.select_region_requested.emit)
        layout.addWidget(self.select_region_button, row, 0, 1, 3)
        row += 1

        # 全画面チェックボックス
        self.fullscreen_checkbox = QtWidgets.QCheckBox("全画面で撮影")
        self.fullscreen_checkbox.setChecked(False)
        layout.addWidget(self.fullscreen_checkbox, row, 0, 1, 2)
        row += 1

        # 座標
        validator = QtGui.QIntValidator(0, 10000)

        layout.addWidget(QtWidgets.QLabel("座標"), row, 0)

        xy_layout = QtWidgets.QHBoxLayout()
        xy_layout.setSpacing(5)

        xy_layout.addWidget(QtWidgets.QLabel("X:"))
        self.region_x_edit = QtWidgets.QLineEdit("0")
        self.region_x_edit.setValidator(validator)
        self.region_x_edit.setFixedWidth(70)
        xy_layout.addWidget(self.region_x_edit)

        xy_layout.addWidget(QtWidgets.QLabel("Y:"))
        self.region_y_edit = QtWidgets.QLineEdit("0")
        self.region_y_edit.setValidator(validator)
        self.region_y_edit.setFixedWidth(70)
        xy_layout.addWidget(self.region_y_edit)

        layout.addLayout(xy_layout, row, 1)
        row += 1

        # サイズ
        layout.addWidget(QtWidgets.QLabel("サイズ"), row, 0)

        wh_layout = QtWidgets.QHBoxLayout()
        wh_layout.setSpacing(5)

        wh_layout.addWidget(QtWidgets.QLabel("幅:"))
        self.region_w_edit = QtWidgets.QLineEdit("0")
        self.region_w_edit.setValidator(validator)
        self.region_w_edit.setFixedWidth(70)
        wh_layout.addWidget(self.region_w_edit)

        wh_layout.addWidget(QtWidgets.QLabel("高さ:"))
        self.region_h_edit = QtWidgets.QLineEdit("0")
        self.region_h_edit.setValidator(validator)
        self.region_h_edit.setFixedWidth(70)
        wh_layout.addWidget(self.region_h_edit)

        layout.addLayout(wh_layout, row, 1)

        # チェックボックス連動
        self.use_burst_checkbox.stateChanged.connect(self.update_burst_state)
        self.use_timestamp_checkbox.stateChanged.connect(self.update_timestamp_state)
        self.use_serial_checkbox.stateChanged.connect(self.update_serial_state)
        self.fullscreen_checkbox.stateChanged.connect(self.update_fullscreen_state)

        # 初期状態反映
        self.update_burst_state()
        self.update_timestamp_state()
        self.update_serial_state()
        self.update_fullscreen_state()

        self.timestamp_format_edit.textChanged.connect(self.update_timestamp_example)
        self.update_timestamp_example()

        layout.setColumnStretch(1, 1)
        self.setLayout(layout)

    def get_settings(self) -> SettingsModel:
        return SettingsModel(
            save_dir=self.save_dir_edit.text(),
            filename=self.filename_edit.text(),
            use_timestamp=self.use_timestamp_checkbox.isChecked(),
            timestamp_format=self.timestamp_format_edit.text(),
            use_serial=self.use_serial_checkbox.isChecked(),
            serial_start=self.serial_start_spinbox.value(),
            use_burst=self.use_burst_checkbox.isChecked(),
            burst_count=self.burst_count_spinbox.value(),
            interval=self.interval_spinbox.value(),
            image_format=self.image_format_combo.currentText(),
            use_fullscreen=self.fullscreen_checkbox.isChecked(),
            region_x=int(self.region_x_edit.text() or 0),      # バグ修正: QLineEdit → int()
            region_y=int(self.region_y_edit.text() or 0),
            region_width=int(self.region_w_edit.text() or 0),
            region_height=int(self.region_h_edit.text() or 0),
        )

    def update_burst_state(self):
        enabled = self.use_burst_checkbox.isChecked()
        self.burst_count_spinbox.setEnabled(enabled)
        self.interval_spinbox.setEnabled(enabled)

    def update_timestamp_state(self):
        enabled = self.use_timestamp_checkbox.isChecked()
        self.timestamp_format_edit.setEnabled(enabled)
        self.timestamp_example_label.setEnabled(enabled)

    def update_serial_state(self):
        enabled = self.use_serial_checkbox.isChecked()
        self.serial_start_spinbox.setEnabled(enabled)

    def update_timestamp_example(self):
        fmt = self.timestamp_format_edit.text()
        try:
            example = datetime.now().strftime(fmt)
            self.timestamp_example_label.setText(f"例: {example}")
        except Exception:
            self.timestamp_example_label.setText("無効なフォーマットです")

    def update_fullscreen_state(self):
        enabled = not self.fullscreen_checkbox.isChecked()
        self.select_region_button.setEnabled(enabled)
        self.region_x_edit.setEnabled(enabled)
        self.region_y_edit.setEnabled(enabled)
        self.region_w_edit.setEnabled(enabled)
        self.region_h_edit.setEnabled(enabled)
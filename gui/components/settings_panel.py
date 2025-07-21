import os
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog
from models.settings_model import SettingsModel

class SettingsPanel(QtWidgets.QWidget):
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
            save_dir="",
            filename="screenshot",
            use_timestamp=False,
            timestamp_format="%Y%m%d_%H%M%S",
            use_serial=True,
            serial_start=1,
            use_burst=False,
            burst_count=2,
            interval=1
        )

    def create_widgets(self):
        layout = QtWidgets.QGridLayout(self)

        # 保存場所
        layout.addWidget(QtWidgets.QLabel("保存場所："), 0, 0)
        self.save_dir_edit = QtWidgets.QLineEdit(self.settings.save_dir)
        layout.addWidget(self.save_dir_edit, 0, 1)
        self.save_dir_button = QtWidgets.QPushButton("参照")
        self.save_dir_button.clicked.connect(self.dirdialog_clicked)
        layout.addWidget(self.save_dir_button, 0, 2)

        # ファイル名
        layout.addWidget(QtWidgets.QLabel("保存ファイル名："), 1, 0)
        self.filename_edit = QtWidgets.QLineEdit(self.settings.filename)
        layout.addWidget(self.filename_edit, 1, 1)

        # タイムスタンプ使用
        self.use_timestamp_checkbox = QtWidgets.QCheckBox("タイムスタンプ")
        self.use_timestamp_checkbox.setChecked(self.settings.use_timestamp)
        layout.addWidget(self.use_timestamp_checkbox, 2, 0, 1, 2)

        # タイムスタンプ形式
        layout.addWidget(QtWidgets.QLabel("タイムスタンプ形式："), 3, 0)
        self.timestamp_format_edit = QtWidgets.QLineEdit(self.settings.timestamp_format)
        layout.addWidget(self.timestamp_format_edit, 3, 1)

        # 連番使用
        self.use_serial_checkbox = QtWidgets.QCheckBox("連番")
        self.use_serial_checkbox.setChecked(self.settings.use_serial)
        layout.addWidget(self.use_serial_checkbox, 4, 0, 1, 2)

        # 開始番号
        layout.addWidget(QtWidgets.QLabel("開始番号:"), 5, 0)
        self.serial_start_spinbox = QtWidgets.QSpinBox()
        self.serial_start_spinbox.setMinimum(1)
        self.serial_start_spinbox.setValue(self.settings.serial_start)
        layout.addWidget(self.serial_start_spinbox, 5, 1)

        # 連続撮影
        self.use_burst_checkbox = QtWidgets.QCheckBox("連続撮影")
        self.use_burst_checkbox.setChecked(self.settings.use_burst)
        layout.addWidget(self.use_burst_checkbox, 6, 0, 1, 2)

        # 連続撮影枚数
        layout.addWidget(QtWidgets.QLabel("連続撮影枚数:"), 6, 2)
        self.burst_count_spinbox = QtWidgets.QSpinBox()
        self.burst_count_spinbox.setMinimum(1)
        self.burst_count_spinbox.setValue(self.settings.burst_count)
        layout.addWidget(self.burst_count_spinbox, 6, 3)

        # 撮影間隔
        layout.addWidget(QtWidgets.QLabel("撮影間隔 (秒):"), 7, 0)
        self.interval_spinbox = QtWidgets.QSpinBox()
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setValue(self.settings.interval)
        layout.addWidget(self.interval_spinbox, 7, 1)

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
            interval=self.interval_spinbox.value()
        )

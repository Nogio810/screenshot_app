from pathlib import Path
from datetime import datetime
from models.settings_model import SettingsModel


class FilenameGenerator:
    def __init__(self, settings: SettingsModel):
        self.settings = settings
        self.serial = settings.serial_start

    def generate_filename(self) -> str:
        # ファイル名と拡張子を設定
        base_name = self.settings.filename
        ext = ".png"

        name_parts = [base_name]

        # タイムスタンプを追加（オプション）
        if self.settings.use_timestamp:
            # 現在の日時をYYYYMMDD_HHMMSS形式で取得
            timestamp = datetime.now().strftime(self.settings.timestamp_format)

            name_parts.append(timestamp)

        if self.settings.use_serial:
            serial = f"{self.serial:03d}"
            name_parts.append(serial)

        return "_".join(name_parts) + ext

    def get_absolute_path(self) -> Path:
        base_path = Path(self.settings.save_dir)
        if self.settings.use_serial:
            while True:
                filename = self.generate_filename()
                full_path = base_path / filename
                if not full_path.exists():
                    break
                self.serial += 1  # ファイルが存在する限り連番を増やす
            return full_path
        else:
            # 連番を使わないなら一度だけ生成
            filename = self.generate_filename()
        return base_path / filename

# services/filename_generator.py

from pathlib import Path
from datetime import datetime
from models.settings_model import SettingsModel


class FilenameGenerator:
    def __init__(self, settings: SettingsModel):
        self.settings = settings
        self.serial = settings.serial_start

    def _build_name(self) -> str:
        base_name = self.settings.filename
        ext = f".{self.settings.image_format.lower()}"

        name_parts = [base_name]

        if self.settings.use_timestamp:
            timestamp = datetime.now().strftime(self.settings.timestamp_format)
            name_parts.append(timestamp)

        if self.settings.use_serial:
            name_parts.append(f"{self.serial:03d}")

        return "_".join(name_parts) + ext

    def generate_unique_path(self) -> Path:
        base_path = Path(self.settings.save_dir)

        while True:
            filename = self._build_name()
            full_path = base_path / filename

            if not full_path.exists():
                break

            if self.settings.use_serial:
                self.serial += 1
            else:
                break

        if self.settings.use_serial:
            self.serial += 1  # 次回用に進める

        return full_path

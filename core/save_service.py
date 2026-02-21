# core/save_service.py

import mss.tools
from pathlib import Path
from models.settings_model import SettingsModel
from services.filename_generator import FilenameGenerator


class SaveService:
    def __init__(self, settings: SettingsModel):
        self.settings = settings
        self.generator = FilenameGenerator(settings)

    def save_image(self, sct_img) -> Path:
        output_path = self.generator.generate_unique_path()

        mss.tools.to_png(
            sct_img.rgb,
            sct_img.size,
            output=str(output_path)
        )

        return output_path

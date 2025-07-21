import mss
import mss.tools
from models.settings_model import SettingsModel
from pathlib import Path
from gui.tools.generate_filename import FilenameGenerator

def capture_specific_region(settings: SettingsModel) -> Path:
    with mss.mss() as sct:
        # キャプチャする領域を定義
        monitor = {
            "top": settings.y,
            "left": settings.x,
            "width": settings.width,
            "height": settings.height
        }
        
        generator = FilenameGenerator(settings)
        output_path = generator.get_absolute_path()

        # スクリーンショットを撮影
        sct_img = sct.grab(monitor)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(output_path))
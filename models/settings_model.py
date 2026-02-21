from dataclasses import dataclass

@dataclass
class SettingsModel:
    save_dir: str
    filename: str
    use_timestamp: bool
    timestamp_format: str
    use_serial: bool
    serial_start: int
    use_burst: bool
    burst_count: int
    interval: int
    image_format: str = "png"
    use_fullscreen: bool = False
    region_x: int = 0
    region_y: int = 0
    region_width: int = 0
    region_height: int = 0
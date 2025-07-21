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
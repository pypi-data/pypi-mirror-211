import locale
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml

if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = Path(sys._MEIPASS)
else:
    application_path = Path(__file__).parent


@dataclass
class Config:
    theme: Literal["auto", "light", "dark"] = "auto"
    locale: str = locale.getdefaultlocale()[0]
    backend: str = "http://localhost:6844/voiceChangeModel"

    input_device: str | None = None
    output_device: str | None = None

    db_threshold: int = -30
    pitch_shift: int = 0
    sample_duration: int = 1000
    fade_duration: int = 80
    extra_duration: int = 50
    input_denoise: bool = False
    output_denoise: bool = False
    sample_rate: int = 44100
    sola_search_duration: int = 12
    buffer_num: int = 4

    # Plugins
    current_plugin: str | None = None
    plugins: dict[str, dict] = field(default_factory=dict)

    @property
    def sample_frames(self):
        return self.sample_duration * self.sample_rate // 1000

    @property
    def fade_frames(self):
        return self.fade_duration * self.sample_rate // 1000

    @property
    def extra_frames(self):
        return self.extra_duration * self.sample_rate // 1000

    @property
    def sola_search_frames(self):
        return self.sola_search_duration * self.sample_rate // 1000


default_config_path = str((Path.home() / ".rtvc" / "config.yaml").absolute())
config = Config()


def load_config(path: Path | str = default_config_path) -> Config:
    global config

    path = Path(path)

    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = Config(**yaml.safe_load(f.read()))
        except Exception:
            config = Config()
            print("Failed to load config file, use default config instead.")

    return config


def save_config(path: Path | str = default_config_path) -> None:
    path = Path(path)

    if not path.parent.exists():
        path.parent.mkdir(parents=True)

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config.__dict__, f)


# Auto load config
load_config()
save_config()

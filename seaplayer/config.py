import properties
from pathlib import Path
from typing import Dict, Any, Optional, TypeVar, Union

T = TypeVar("T")

DEFAULT_CONFIG_DATA = {
    "sound": {
        "sound_font_path": None
    },
    "playback": {
        "volume_change_percent": 0.01,
        "rewind_count_seconds": 1,
        "max_volume_percent": 2.0
    },
    "playlist": {
        "recursive_search": False
    },
    "keys": {
        "quit": "q,й",
        "rewind_forward": "*",
        "rewind_back": "/",
        "volume_up": "+",
        "volume_down": "-"
    }
}

class SeaPlayerConfig:
    @staticmethod
    def dump(filepath: Path, data: Dict[str, Any]) -> None:
        with open(filepath, "w", encoding="utf-8", errors="ignore") as file:
            properties.dump_tree(data, file)
    
    @staticmethod
    def load(filepath: Path, default: Dict[str, Any]) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            try: return properties.load_tree(file)
            except: pass
        with open(filepath, "w", encoding="utf-8", errors="ignore") as file:
            properties.dump_tree(default, file)
        return default
    
    def refresh(self) -> None: self.dump(self.filepath, self.config)
    
    def __init__(
        self,
        filepath: str,
        *,
        default_data: Dict[str, Any]=DEFAULT_CONFIG_DATA
    ) -> None:
        self.filepath = Path(filepath)
        self.default_data = default_data
        if self.filepath.exists():
            self.config = self.load(self.filepath, self.default_data)
            config_temp = self.default_data.copy()
            config_temp.update(self.config)
            self.config = config_temp.copy()
            del config_temp
        else:
            self.config = default_data.copy()
        self.refresh()
    
    @staticmethod
    def tevey(key_path: str, *, sep: str=".") -> str:
        return "".join([f"[{repr(key)}]" for key in key_path.split(sep)])
    def get(self, key: str, default: T=None) -> Union[Any, T]:
        try: return eval(f"self.config{self.tevey(key)}")
        except: return default
    def set(self, key: str, value: Any) -> None:
        try: exec(f"self.config{self.tevey(key)} = value") ; self.refresh()
        except: pass
    
    # ! Sound
    @property
    def sound_font_path(self) -> Optional[str]: return self.get("sound.sound_font_path")
    @sound_font_path.setter
    def sound_font_path(self, value: Optional[str]): self.set("sound.sound_font_path", value)
    
    # ! Playback
    @property
    def volume_change_percent(self) -> float: return self.get("playback.volume_change_percent")
    @volume_change_percent.setter
    def volume_change_percent(self, value: float): self.set("playback.volume_change_percent", value)
    
    @property
    def rewind_count_seconds(self) -> int: return self.get("playback.rewind_count_seconds")
    @rewind_count_seconds.setter
    def rewind_count_seconds(self, value: int): self.set("playback.rewind_count_seconds", value)
    
    @property
    def max_volume_percent(self) -> float: return self.get("playback.max_volume_percent")
    @max_volume_percent.setter
    def max_volume_percent(self, value: float): self.set("playback.max_volume_percent", value)
    
    # ! Playlist
    @property
    def recursive_search(self) -> bool: return self.get("playlist.recursive_search")
    @recursive_search.setter
    def recursive_search(self, value: bool): self.set("playlist.recursive_search", value)
    
    # ! Keys
    @property
    def key_quit(self) -> str: return self.get("keys.quit")
    @key_quit.setter
    def key_quit(self, value: str): return self.set("keys.quit", value)
    
    @property
    def key_rewind_forward(self) -> str: return self.get("keys.rewind_forward")
    @key_rewind_forward.setter
    def key_rewind_forward(self, value: str): return self.set("keys.rewind_forward", value)
    
    @property
    def key_rewind_back(self) -> str: return self.get("keys.rewind_back")
    @key_rewind_back.setter
    def key_rewind_back(self, value: str): return self.set("keys.rewind_back", value)
    
    @property
    def key_volume_up(self) -> str: return self.get("keys.volume_up")
    @key_volume_up.setter
    def key_volume_up(self, value: str): return self.set("keys.volume_up", value)
    
    @property
    def key_volume_down(self) -> str: return self.get("keys.volume_down")
    @key_volume_down.setter
    def key_volume_down(self, value: str): return self.set("keys.volume_down", value)

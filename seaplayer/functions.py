import os
import aiofiles
from io import BytesIO
from PIL import Image
from playsoundsimple import Sound
# > Typing
from typing import Literal, Tuple, Optional

def get_bar_status() -> Tuple[str, Optional[float], Optional[float]]: return "", None, None

def check_status(sound: Sound) -> Literal["Stoped", "Playing", "Paused"]:
    if sound.playing:
        if sound.paused: return "Paused"
        else: return "Playing"
    return "Stoped"

def image_from_bytes(data: Optional[bytes]) -> Optional[Image.Image]:
    if data is not None: return Image.open(BytesIO(data))

def get_sound_basename(sound: Sound) -> str:
    if sound.title is not None:
        if sound.artist is not None:
            return f"{sound.artist} - {sound.title}"
        return f"{sound.title}"
    return f"{os.path.basename(sound.name)}"

def is_midi_file(filepath: str) -> bool:
    with open(filepath, 'rb') as file:
        return file.read(4) == b"MThd"

async def aio_is_midi_file(filepath: str):
    async with aiofiles.open(filepath, 'rb') as file:
        return (await file.read(4)) == b"MThd"
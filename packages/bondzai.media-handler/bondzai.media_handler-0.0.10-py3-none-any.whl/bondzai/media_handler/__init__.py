from pathlib import Path

from .base import get_file_mime, load_binary, save_binary
from .audio import AUDIO_ALLOWED_MIME, get_audio_metadata, get_audio_raw_data
from .image import IMAGE_ALLOWED_MIME, get_image_metadata, get_image_raw_data
from .video import VIDEO_ALLOWED_MIME, get_video_metadata, get_video_raw_data


VERSION = "0.0.10"


def get_raw_data(file_path: Path) -> list[float]:
    mime = get_file_mime(file_path)
    if mime in AUDIO_ALLOWED_MIME:
        return get_audio_raw_data(file_path)
    elif mime in IMAGE_ALLOWED_MIME:
        return get_image_raw_data(file_path)
    elif mime in VIDEO_ALLOWED_MIME:
        return get_video_raw_data(file_path)
    raise Exception(f"File mime '{mime}' is not supported")


def get_metadata(file_path: Path) -> dict:
    mime = get_file_mime(file_path)
    if mime in AUDIO_ALLOWED_MIME:
        return get_audio_metadata(file_path)
    elif mime in IMAGE_ALLOWED_MIME:
        return get_image_metadata(file_path)
    elif mime in VIDEO_ALLOWED_MIME:
        return get_video_metadata(file_path)
    raise Exception(f"File mime '{mime}' is not supported")

from pathlib import Path
import soundfile as sf
import audio_metadata

from .base import check_mime


AUDIO_ALLOWED_MIME = [
    "audio/x-wav",
    "audio/mpeg"
]


def get_audio_metadata(file_path: Path) -> dict:
    mime = check_mime(file_path, AUDIO_ALLOWED_MIME)
    audio = audio_metadata.load(file_path)

    return {
        "mime": mime,
        "sample_rate": audio["streaminfo"].sample_rate,
        "channels": audio["streaminfo"].channels
    }


def get_audio_raw_data(file_path: Path) -> list[float]:
    check_mime(file_path, AUDIO_ALLOWED_MIME)
    with open(file_path, 'rb') as f:
        data, _ = sf.read(f)
    return data.flatten().tolist()

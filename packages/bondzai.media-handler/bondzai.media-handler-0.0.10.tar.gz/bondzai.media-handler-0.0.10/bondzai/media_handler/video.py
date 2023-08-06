import imageio
from pathlib import Path 
from imageio.v3 import immeta, improps

from .image import process_raw_img_data
from .base import check_mime


VIDEO_ALLOWED_MIME = [
    "video/mp4",
    "video/quicktime",
    "video/webm"
]


def get_video_metadata(file_path: Path) -> dict:
    mime = check_mime(file_path, VIDEO_ALLOWED_MIME)
    img = immeta(file_path)
    props = improps(file_path)
    return {
        "mime": mime,
        "width": img['size'][0],
        "height": img['size'][1],
        "fps": img['fps'],
        "channels": props.shape[-1],
        "dim": props.shape
    }


def get_video_raw_data(file_path: Path) -> list[float]:
    check_mime(file_path, VIDEO_ALLOWED_MIME)
    video = imageio.get_reader(file_path) 
    results = []
    for frame in video.iter_data(): 
        results += process_raw_img_data(frame[0])
    return results

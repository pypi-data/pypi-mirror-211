from pathlib import Path
from imageio.v3 import imread, immeta, improps

from .base import check_mime


IMAGE_ALLOWED_MIME = [
    "image/jpeg",
    "image/png",
    "image/tiff"
]


def get_image_metadata(file_path: Path) -> dict:
    mime = check_mime(file_path, IMAGE_ALLOWED_MIME)
    img = immeta(file_path)
    props = improps(file_path)
    return {
        "mime": mime,
        "width": img['shape'][0],
        "height": img['shape'][1],
        "mode": img['mode'],
        "dim": props.shape
    }


def get_image_raw_data(file_path: Path) -> list[float]:
    check_mime(file_path, IMAGE_ALLOWED_MIME)
    return process_raw_img_data(imread(file_path))


def process_raw_img_data(data) -> list[float]:
    data = data.astype("float32")\
        .flatten()\
        .tolist()
    return data

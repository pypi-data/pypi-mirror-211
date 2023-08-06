import mimetypes
import struct as st
from pathlib import Path


def check_mime(file_path: Path, allowed_mime: list):
    mime = get_file_mime(file_path)
    if mime not in allowed_mime:
        raise Exception(f"'{mime}' not supported")
    return mime


def get_file_mime(file_path: Path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime


def load_binary(file_path: Path) -> tuple[float]:
    with open(file_path, "rb") as f:
        d = f.read() 
    return st.unpack(f"{int(len(d)/4)}f", d)


def save_binary(file_path: Path, data: list[float]):
    d = st.pack(f"{len(data)}f", *data)
    with open(file_path, "+wb") as f:
        f.write(d)

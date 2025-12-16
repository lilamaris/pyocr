from typing import Any

import datetime
import csv
import pathlib

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def iter_image(dir: pathlib.Path):
    return [path for path in dir.iterdir() if path.suffix.lower() in IMG_EXTS]


def get_format_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M:%S")


def save_dict(path: pathlib.Path, row: dict[str, Any]):
    file_exists = path.exists()

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())

        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

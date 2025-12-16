from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from module.io_helper import get_format_time, iter_image, save_dict
from module.ocr import ocr_by_rois
from module.pos import recipe_roi_rect

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--dry",
    action=argparse.BooleanOptionalAction,
    help="for test. will be not save to output.",
)

args = parser.parse_args()
is_dry = args.dry


def run():
    from dotenv import load_dotenv
    import os

    load_dotenv()

    INPUT_DIR = Path(os.environ.get("INPUT_DIR") or "inputImage")
    OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR") or "output")

    max_workers = max(1, os.cpu_count() or 1)

    images = iter_image(INPUT_DIR)
    rois = recipe_roi_rect

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(ocr_by_rois, path, rois) for path in images]

        for future in as_completed(futures):
            _, data = future.result()
            if not is_dry:
                save_dict(OUTPUT_DIR / f"{get_format_time()}.csv", data)


if __name__ == "__main__":
    run()

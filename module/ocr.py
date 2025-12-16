from pathlib import Path
import cv2
import numpy as np
import pytesseract

from .pos import Rectangle


def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    gray = cv2.filter2D(gray, -1, kernel)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bw = cv2.medianBlur(bw, 3)
    return bw


def ocr_by_rois(path: Path, rois: dict[str, Rectangle]) -> tuple[str, dict[str, str]]:
    img = cv2.imread(str(path))
    if img is None:
        return path.name, {}
    res = {}

    for k, rect in rois.items():
        y1, y2 = sorted([rect.top, rect.bottom])
        x1, x2 = sorted([rect.left, rect.right])
        roi = img[y1:y2, x1:x2]
        roi = preprocess(roi)

        tesseract_result = pytesseract.image_to_string(
            roi, lang="kor+eng", config="--psm 6 -c preserve_interword_spaces=1"
        )

        res[k] = str(tesseract_result).replace("\n", "")

    print(f"OCR Worker: {path}: {res}")

    return path.name, res

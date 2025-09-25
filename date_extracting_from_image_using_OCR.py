import os
import warnings
from typing import Optional
from PIL import Image
import cv2
import numpy as np
import easyocr
from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning, module="torch.utils.data")

# Initialize EasyOCR once
reader = easyocr.Reader(["en"], gpu=False)


def normalize_date(day: int, month: int, year: int) -> Optional[str]:
    """Validate date and return in dd-mm-yyyy format."""
    try:
        return datetime(year, month, day).strftime("%d-%m-%Y")
    except ValueError:
        return None


def extract_date_from_image(img: Image.Image) -> Optional[str]:
    """Extract date from a single PIL image."""

    import re  # move regex inside function for portability

    DATE_REGEX = re.compile(
        r'(\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b|\b\d{4}[./-]\d{1,2}[./-]\d{1,2}\b)'
    )
    YEAR_REGEX = re.compile(r"(20\d{2})")

    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    results = reader.readtext(img_cv, detail=0, paragraph=False)

    # 1. Try normal regex first
    for text in results:
        match = DATE_REGEX.search(text)
        if match:
            raw = match.group(0).replace("-", "/").replace(".", "/")
            parts = raw.split("/")
            try:
                if len(parts) == 3:
                    day, month, year = map(int, parts)
                    return normalize_date(day, month, year)
            except ValueError:
                continue

    # 2. Fallback: detect year and reconstruct
    for text in results:
        year_match = YEAR_REGEX.search(text)
        if year_match:
            year = int(year_match.group(1))
            idx = text.find(str(year))
            prefix = text[max(0, idx - 10):idx]
            cleaned = re.sub(r"[^0-9]", "", prefix)

            candidates = []
            if len(cleaned) >= 4:
                candidates.append((cleaned[:-2], cleaned[-2:], year))
            if len(cleaned) >= 3:
                candidates.append((cleaned[0], cleaned[1:], year))

            sep_digits = [d for d in re.split(r"[./-]", prefix.strip()) if d.isdigit()]
            if len(sep_digits) >= 2:
                candidates.append((sep_digits[-2], sep_digits[-1], year))

            for cand in candidates:
                try:
                    day, month, yr = map(int, cand)
                    norm = normalize_date(day, month, yr)
                    if norm:
                        return norm
                except Exception:
                    continue

    return None


if __name__ == "__main__":
    base = "/mnt/c/Users/KW/Desktop"
    test_images = [f"test_image_{i}" for i in range(1, 6)]  # test_image_1 to test_image_5

    for name in test_images:
        found_path = None
        for ext in [".jpg", ".png"]:
            path = os.path.join(base, name + ext)
            if os.path.exists(path):
                found_path = path
                break

        if not found_path:
            print(f"{name} not found with .jpg or .png!")
            continue

        img = Image.open(found_path)
        date = extract_date_from_image(img)
        print(f"{os.path.basename(found_path)} -> {date}")

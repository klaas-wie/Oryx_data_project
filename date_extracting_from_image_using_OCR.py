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
    """Extract date from a single PIL image with debug output."""

    import re  # move regex inside function for portability

    DATE_REGEX = re.compile(
        r'(\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b|\b\d{4}[./-]\d{1,2}[./-]\d{1,2}\b)'
    )
    YEAR_REGEX = re.compile(r"(20\d{2})")

    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    results = reader.readtext(img_cv, detail=0, paragraph=False)

    print("DEBUG: OCR results:", results)  # Show what text was detected

    # 1. Try normal regex first
    for text in results:
        match = DATE_REGEX.search(text)
        if match:
            raw = match.group(0).replace("-", "/").replace(".", "/")
            parts = raw.split("/")
            print(f"DEBUG: Regex match found: {raw} -> parts: {parts}")
            try:
                if len(parts) == 3:
                    day, month, year = map(int, parts)
                    norm = normalize_date(day, month, year)
                    print(f"DEBUG: Normalized date: {norm}")
                    return norm
            except ValueError:
                print(f"DEBUG: ValueError for parts: {parts}")
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

            print(f"DEBUG: Year fallback - text: '{text}', year: {year}, prefix: '{prefix}', candidates: {candidates}")

            for cand in candidates:
                try:
                    day, month, yr = map(int, cand)
                    norm = normalize_date(day, month, yr)
                    print(f"DEBUG: Trying candidate: {cand} -> normalized: {norm}")
                    if norm:
                        return norm
                except Exception as e:
                    print(f"DEBUG: Failed candidate {cand}: {e}")
                    continue

    print("DEBUG: No date found in this image")
    return None



if __name__ == "__main__":
    base = "/mnt/c/Users/KW/Desktop/test_sample_hard/slashes"
    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

    for filename in os.listdir(base):
        if any(filename.lower().endswith(ext) for ext in valid_extensions):
            path = os.path.join(base, filename)
            img = Image.open(path)
            date = extract_date_from_image(img)
            print(f"{filename} -> {date}")


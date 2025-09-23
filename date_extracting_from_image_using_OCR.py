import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from datetime import datetime

def extract_date_from_image(img: Image.Image) -> str:
    """
    Hybrid OCR approach to extract a date from an image.
    Tries multiple regions and preprocessing strategies.
    """
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    h, w = img_cv.shape[:2]

    # Regions: top 15%, corners, fallback full image
    regions = [
        img_cv[0:int(0.15*h), :],                  # Top strip
        img_cv[0:int(0.15*h), 0:int(0.15*w)],     # Top-left
        img_cv[0:int(0.15*h), int(0.85*w):],      # Top-right
        img_cv[int(0.85*h):, 0:int(0.15*w)],      # Bottom-left
        img_cv[int(0.85*h):, int(0.85*w):],       # Bottom-right
        img_cv                                     # Full image fallback
    ]

    # Preprocessing strategies
    def preprocess(region, method='adaptive_inv'):
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        if method == 'adaptive_inv':
            return cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )
        elif method == 'adaptive':
            return cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif method == 'otsu':
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return thresh
        elif method == 'otsu_inv':
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            return thresh
        else:
            return gray

    # Try each region with each preprocessing method
    methods = ['adaptive_inv', 'adaptive', 'otsu', 'otsu_inv']
    for region in regions:
        for method in methods:
            processed = preprocess(region, method)
            text = pytesseract.image_to_string(processed)
            date_matches = re.findall(r'\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})\b', text)
            for dm in date_matches:
                parts = re.split(r'[-/.]', dm)
                if len(parts) != 3:
                    continue
                day, month, year = parts
                if len(year) == 2:
                    year = '20' + year
                try:
                    date_obj = datetime(int(year), int(month), int(day))
                    return date_obj.strftime("%d-%m-%Y")
                except ValueError:
                    continue

    return None





if __name__ == "__main__":
    from PIL import Image
    import os

    # Update with your desktop path
    base_path = "/mnt/c/Users/KW/Desktop"

    test_files = ["test_image_1.jpg", "test_image_2.jpg", "test_image_3.jpg", "test_image_4.jpg", "test_image_5.png"]

    for i, file in enumerate(test_files, 1):
        file_path = os.path.join(base_path, file)
        img = Image.open(file_path)
        date = extract_date_from_image(img)
        print(f"Test image {i}: {file} -> Date found: {date}")

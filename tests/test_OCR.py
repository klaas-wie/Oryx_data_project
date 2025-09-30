import unittest
from pathlib import Path
from PIL import Image
from date_extracting_from_image_using_OCR import extract_date_from_image


class TestEasyDates(unittest.TestCase):
    def setUp(self):
        self.base = Path(__file__).parent / "test_samples_OCR" / "samples_easy"
        self.test_cases = {
            "test_image_1.jpg": "14-06-2022"
        }

    def test_dates(self):
        for filename, expected_date in self.test_cases.items():
            path = self.base / filename
            img = Image.open(path)
            result = extract_date_from_image(img)
            self.assertEqual(result, expected_date, msg=f"Failed for {filename}")

class TestSlashes(unittest.TestCase):
    def setUp(self):
        # Folder with test images
        self.base = Path(__file__).parent / "test_samples_OCR" / "slashes"

        # Map filename -> expected date (in dd-mm-yyyy format)
        self.test_cases = {
            "slashes_1.png": "24-02-2022"
        }

    def test_dates(self):
        for filename, expected_date in self.test_cases.items():
            path = self.base / filename
            img = Image.open(path)
            result = extract_date_from_image(img)
            self.assertEqual(result, expected_date, msg=f"Failed for {filename}")


if __name__ == "__main__":
    unittest.main()

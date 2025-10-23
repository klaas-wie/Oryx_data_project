import os
import re

def extract_date_from_postimg_with_date_in_link_string(link: str) -> str | None:
    filename = os.path.splitext(os.path.basename(link))[0]

    matches = re.findall(r'(\d{2,4}-\d{2}-\d{2,4})', filename)
    if not matches:
        return None

    date_str = matches[-1]  # last triple

    parts = date_str.split('-')
    if len(parts) != 3:
        return None

    try:
        a, b, c = int(parts[0]), int(parts[1]), int(parts[2])
    except Exception:
        return None

    # Helper to check if day and month are plausible
    def valid_day_month(day: int, month: int) -> bool:
        return 1 <= day <= 31 and 1 <= month <= 12

    # --- dd-mm-yyyy ---
    if c >= 2022 and c <= 2026 and valid_day_month(a, b):
        return f"{a:02d}-{b:02d}-{c}"

    # --- yyyy-mm-dd ---
    if a >= 2022 and a <= 2026 and valid_day_month(c, b):
        return f"{c:02d}-{b:02d}-{a}"

    # --- dd-mm-yy (2-digit year at end) ---
    if 0 <= c <= 99 and valid_day_month(a, b):
        if 22 <= c <= 26:
            year = 2000 + c
            return f"{a:02d}-{b:02d}-{year}"

    return None

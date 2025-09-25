import re

def extract_date_from_postimg_with_date_in_link_string(link: str) -> str | None:
    """
    Extract date in format dd-mm-yyyy from a postimg link.
    Supports formats in the filename like:
      - dd-mm-yyyy
      - yyyy-mm-dd
    Only considers years >= 2022.
    Returns None if no valid date is found.
    """
    # Look for dd-mm-yyyy or yyyy-mm-dd anywhere in the filename
    date_patterns = [
        r"(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>20\d{2})",
        r"(?P<year>20\d{2})-(?P<month>\d{2})-(?P<day>\d{2})"
    ]

    for pattern in date_patterns:
        match = re.search(pattern, link)
        if match:
            try:
                day = int(match.group("day"))
                month = int(match.group("month"))
                year = int(match.group("year"))

                # Basic validation
                if 1 <= day <= 31 and 1 <= month <= 12 and year >= 2022:
                    return f"{day:02d}-{month:02d}-{year}"
            except Exception:
                continue

    return None

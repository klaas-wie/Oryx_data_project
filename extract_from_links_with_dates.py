import pandas as pd
import re

def extract_date_from_postimg_with_date_in_link_string(link: str) -> str | None:
    """
    Extract date in format dd-mm-yyyy from a postimg link.
    many postimg links have a date embedded in the filename, e.g.: 
    "https://i.postimg.cc/cC76JVMC/1002-unkn-T-62-destr-18-11-24.jpg"
    Returns None if no date is found.
    """
    # Match something like -18-11-24.jpg at the end of the link
    match = re.search(r"-(\d{2}-\d{2}-\d{2})\.jpg$", link)
    if match:
        dd_mm_yy = match.group(1)  # e.g., "18-11-24"
        dd, mm, yy = dd_mm_yy.split("-")
        yyyy = "20" + yy  # assume 2000s
        return f"{dd}-{mm}-{yyyy}"
    return None

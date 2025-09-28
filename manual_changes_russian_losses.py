"""
Manual changes for Russian losses dataset.

Use this file to manually correct rows where OCR or automatic extraction
produced invalid dates. All manual fixes are keyed by the 'link' column,
so they are safe even if row numbers change after merging new losses.

The following corrections were necessary in the Russian dataset:

Found invalid dates:
Row 7368: 24-04-2003 -> Invalid year: 2003 | Link: https://i.postimg.cc/BQvvTDWx/1028-bmp1am-destr-24-04-03.jpg
Row 17174: 18-13-2023 -> Invalid month: 13 | Link: https://i.postimg.cc/gJZhvdV5/1020-tor-m2-dam-18-13-23.jpg
Row 17677: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17678: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17680: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17717: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg

Twitter posts missing dates:
[12094] No date found for https://pic.twitter.com/a9BoN1E03K

All these corrections have already been applied in the current Russian dataset. The commented-out code below shows how to apply them if needed.
"""

import pandas as pd

# Load the Russian losses CSV
losses_with_dates = pd.read_csv("russian_losses_with_dates.csv")

# Ensure 'manually_changed' column exists
if "manually_changed" not in losses_with_dates.columns:
    losses_with_dates["manually_changed"] = False

# -------------------------------
# Manual fixes (already applied)
# -------------------------------

# Example of fixing a single row by link:
# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/BQvvTDWx/1028-bmp1am-destr-24-04-03.jpg",
#     ["date", "manually_changed"]
# ] = ["24-04-2023", True]

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/gJZhvdV5/1020-tor-m2-dam-18-13-23.jpg",
#     ["date", "manually_changed"]
# ] = ["18-03-2023", True]

# Multiple rows at once (all share same date fix)
# links_to_fix = [
#     "https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg"
# ]
# losses_with_dates.loc[
#     losses_with_dates["link"].isin(links_to_fix),
#     ["date", "manually_changed"]
# ] = ["24-06-2023", True]

# Fixing a Twitter post where no date was found
# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://pic.twitter.com/a9BoN1E03K",
#     ["date", "manually_changed"]
# ] = ["04-10-2022", True]

# -------------------------------
# Save the updated CSV
# -------------------------------
losses_with_dates.to_csv("russian_losses_with_dates.csv", index=False)

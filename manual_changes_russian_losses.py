"""
Manual changes for Russian losses dataset.

Use this file to manually correct rows where OCR or automatic extraction
produced invalid dates. All manual fixes are keyed by the 'link' column,
so they are safe even if row numbers change after merging new losses.

The following corrections were necessary in the Russian dataset:
All these corrections have already been applied in the current Russian dataset. The commented-out code below shows how to apply them if needed.

Found invalid dates:
Row 7368: 24-04-2003 -> Invalid year: 2003 | Link: https://i.postimg.cc/BQvvTDWx/1028-bmp1am-destr-24-04-03.jpg
Row 17174: 18-13-2023 -> Invalid month: 13 | Link: https://i.postimg.cc/gJZhvdV5/1020-tor-m2-dam-18-13-23.jpg
Row 17677: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17678: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17680: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17717: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg

Twitter posts missing dates:
[12094] No date found for https://pic.twitter.com/a9BoN1E03K

"""

"""
SECOND ROUND OF MANUAL CHANGES
Row 896: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/sfJXpGgd/kd0uOIzH.jpg
Row 1107: 19-07-7023 -> Invalid year: 7023 | Link: https://i.postimg.cc/K8KNkcMC/3260.png
Row 2024: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/fRfBsKwq/kd0uOIzH.jpg
Row 2025: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/fRfBsKwq/kd0uOIzH.jpg
Row 3223: 01-06-202 -> Invalid format | Link: https://i.postimg.cc/Ls5fcmpp/332.png
Row 4231: 30-03-3022 -> Invalid year: 3022 | Link: https://postimg.cc/XrpSy7x7
Row 5604: 14-10-202 -> Invalid format | Link: https://i.postimg.cc/NfBNk5S5/1049-mtlb-capt.jpg
Row 5682: 22-11-2072 -> Invalid year: 2072 | Link: https://i.postimg.cc/9FD9K8GH/1009-MT-LBVMK-destr.jpg
Row 6164: 22-03-2032 -> Invalid year: 2032 | Link: https://i.postimg.cc/9MBF1VTg/3360.png
Row 6340: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/RhRQ6vSr/dd2.jpg
Row 6392: 21-02-2051 -> Invalid year: 2051 | Link: https://i.postimg.cc/wxPDR4Dr/n7.jpg
Row 6393: 21-02-2051 -> Invalid year: 2051 | Link: https://i.postimg.cc/wxPDR4Dr/n7.jpg
Row 6394: 21-02-2051 -> Invalid year: 2051 | Link: https://i.postimg.cc/wxPDR4Dr/n7.jpg
Row 6404: 17-02-2051 -> Invalid year: 2051 | Link: https://i.postimg.cc/FsYSfSFr/y1.jpg
Row 7125: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/pXwSB7s7/441.jpg
Row 7221: 25-02-2051 -> Invalid year: 2051 | Link: https://i.postimg.cc/d3MG7nfd/dr.jpg
Row 7648: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/wMprp4rM/4433.jpg
Row 7649: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/wMprp4rM/4433.jpg
Row 7650: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/wMprp4rM/4433.jpg
Row 7651: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/wMprp4rM/4433.jpg
Row 7652: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/wMprp4rM/4433.jpg
Row 8844: 08-10-2027 -> Invalid year: 2027 | Link: https://i.postimg.cc/g2yWPyV2/1004-bmp2-capt.jpg
Row 9911: 08-08-202 -> Invalid format | Link: https://i.postimg.cc/5t9tSpNV/1000-bmp3.jpg
Row 13193: 01-02-2036 -> Invalid year: 2036 | Link: https://i.postimg.cc/g0gcjCG4/1005-Kam-AZ-63968-Typhoon.jpg
Row 13637: 14-02-2051 -> Invalid year: 2051 | Link: https://i.postimg.cc/3Rwy43kG/g52.jpg
Row 14174: 10-08-2027 -> Invalid year: 2027 | Link: https://i.postimg.cc/gktrF01S/1001-REM-KL-Kamaz-6x6.jpg
Row 16376: 23-03-2032 -> Invalid year: 2032 | Link: https://i.postimg.cc/R0NhTqLP/4437.png
Row 16950: 28-02-2020 -> Invalid year: 2020 | Link: https://i.postimg.cc/ncXNZ3Yr/zx3.png
Row 20006: 19-02-2043 -> Invalid year: 2043 | Link: https://i.postimg.cc/8CmmLsRF/1114_Ural-4320_captured.jpg
Row 20118: 01-04-3022 -> Invalid year: 3022 | Link: https://i.postimg.cc/CxstkhF4/1.png
Row 21642: 10-08-2027 -> Invalid year: 2027 | Link: https://i.postimg.cc/gktrF01S/1001-REM-KL-Kamaz-6x6.jpg
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

# fixes = {
#     "https://i.postimg.cc/sfJXpGgd/kd0uOIzH.jpg": "28-02-2023",
#     "https://i.postimg.cc/K8KNkcMC/3260.png": "19-07-2023",
#     "https://i.postimg.cc/fRfBsKwq/kd0uOIzH.jpg": "28-02-2023",
#     "https://i.postimg.cc/Ls5fcmpp/332.png": "01-06-2022",
#     "https://postimg.cc/XrpSy7x7": "30-03-2022",
#     "https://i.postimg.cc/NfBNk5S5/1049-mtlb-capt.jpg": "14-10-2022",
#     "https://i.postimg.cc/9FD9K8GH/1009-MT-LBVMK-destr.jpg": "22-11-2022",
#     "https://i.postimg.cc/9MBF1VTg/3360.png": "22-03-2022",
#     "https://i.postimg.cc/RhRQ6vSr/dd2.jpg": "15-05-2022",
#     "https://i.postimg.cc/wxPDR4Dr/n7.jpg": "12-05-2022",
#     "https://i.postimg.cc/FsYSfSFr/y1.jpg": "12-05-2022",
#     "https://i.postimg.cc/pXwSB7s7/441.jpg": "12-05-2022",
#     "https://i.postimg.cc/d3MG7nfd/dr.jpg": "12-05-2022",
#     "https://i.postimg.cc/wMprp4rM/4433.jpg": "12-05-2022",
#     "https://i.postimg.cc/g2yWPyV2/1004-bmp2-capt.jpg": "08-10-2022",
#     "https://i.postimg.cc/5t9tSpNV/1000-bmp3.jpg": "08-08-2022",
#     "https://i.postimg.cc/jdQL4n85/v5.jpg": "01-04-2022",
#     "https://i.postimg.cc/85xLYVny/887.png": "06-08-2023",
#     "https://i.postimg.cc/g0gcjCG4/1005-Kam-AZ-63968-Typhoon.jpg": "15-02-2022",
#     "https://i.postimg.cc/3Rwy43kG/g52.jpg": "15-02-2022",
#     "https://i.postimg.cc/gktrF01S/1001-REM-KL-Kamaz-6x6.jpg": "10-08-2022",
#     "https://i.postimg.cc/R0NhTqLP/4437.png": "23-03-2022",
#     "https://i.postimg.cc/ncXNZ3Yr/zx3.png": "28-02-2022",
#     "https://i.postimg.cc/8CmmLsRF/1114_Ural-4320_captured.jpg": "NO_DATE_FOUND",
#     "https://i.postimg.cc/CxstkhF4/1.png": "01-04-2022",
# }

# # Apply fixes
# for link, set_date in fixes.items():
#     mask = losses_with_dates["link"] == link
#     if mask.any():
#         losses_with_dates.loc[mask, ["date", "manually_changed"]] = [set_date, True]

# -------------------------------------------
# Apply changes for OCR rows that resulted in NO_DATE_FOUND, manually checked
# -------------------------------------------

# Ensure 'manually_changed' column exists
# if "manually_changed" not in losses_with_dates.columns:
#     losses_with_dates["manually_changed"] = False

# # -------------------------------------------
# # Apply changes for OCR rows that resulted in NO_DATE_FOUND, manually checked
# # -------------------------------------------

# no_date_df = pd.read_csv("NO_DATE_FOUND_manual_changes.csv")

# # Filter out rows that actually have a valid date
# valid_dates_df = no_date_df[no_date_df["date"] != "NO_DATE_FOUND"]

# # Create a dictionary mapping link -> date (only valid ones)
# link_to_date = dict(zip(valid_dates_df["link"], valid_dates_df["date"]))

# # Track how many rows are updated
# updated_count = 0

# # Apply updates
# def update_row(row):
#     global updated_count
#     if row["link"] in link_to_date:
#         new_date = link_to_date[row["link"]]
#         if row["date"] != new_date:
#             updated_count += 1
#             row["date"] = new_date
#             row["manually_changed"] = True
#     return row

# # Apply the function row by row
# losses_with_dates = losses_with_dates.apply(update_row, axis=1)

# print(f"🔄 {updated_count} rows were updated and marked as manually changed.")

# -------------------------------
# Save the updated CSV
# -------------------------------

losses_with_dates.to_csv("russian_losses_with_dates.csv", index=False)

print(f"✅ Updated CSV")





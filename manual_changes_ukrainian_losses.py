"""
Manual changes for Ukrainian losses dataset.

Use this file to manually correct rows where OCR or automatic extraction
produced invalid dates. All manual fixes should be keyed by the 'link' column,
so they are safe even if row numbers change after merging new losses.

"""

import pandas as pd

# Load the Ukrainian losses CSV
losses_with_dates = pd.read_csv("ukrainian_losses_with_dates.csv")

# Ensure 'manually_changed' column exists
if "manually_changed" not in losses_with_dates.columns:
    losses_with_dates["manually_changed"] = False

# -------------------------------
# Manual fixes
# -------------------------------

"""
Found invalid dates:
Row 25: 13-03-207 -> Invalid format | Link: https://i.postimg.cc/MpP3ydft/35.png
Row 459: 28-06-2027 -> Invalid year: 2027 | Link: https://postimg.cc/w7DpP5bY
Row 3517: 19-04-2020 -> Invalid year: 2020 | Link: https://i.postimg.cc/dQSWMY46/b2.png
Row 9470: 10-04-2028 -> Invalid year: 2028 | Link: https://i.postimg.cc/HWX759J4/9l.png
Row 9484: 25-03-2028 -> Invalid year: 2028 | Link: https://i.postimg.cc/WbPHkRJz/651.png
Row 9570: 01-10-2020 -> Invalid year: 2020 | Link: https://i.postimg.cc/Nj2txW1y/d4.png
Row 10066: 19-05-2020 -> Invalid year: 2020 | Link: https://i.postimg.cc/x8sypSG9/5g2.png
"""

manual_changes_before = (losses_with_dates["manually_changed"] == True).sum()

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/MpP3ydft/35.png",
#     ["date", "manually_changed"]
# ] = ["13-03-2022", True]

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://postimg.cc/w7DpP5bY",
#     ["date", "manually_changed"]
# ] = ["28-06-2022", True]

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/dQSWMY46/b2.png",
#     ["date", "manually_changed"]
# ] = ["19-04-2022", True]

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/HWX759J4/9l.png",
#     ["date", "manually_changed"]
# ] = ["10-04-2023", True]

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/WbPHkRJz/651.png",
#     ["date", "manually_changed"]
# ] = ["25-03-2023", True]

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/Nj2txW1y/d4.png",
#     ["date", "manually_changed"]
# ] = ["07-03-2022", True]

# losses_with_dates.loc[
#     losses_with_dates["link"] == "https://i.postimg.cc/x8sypSG9/5g2.png",
#     ["date", "manually_changed"]
# ] = ["19-05-2022", True]


# Example: fixing multiple rows sharing same date:
# links_to_fix = [
#     "LINK1_HERE",
#     "LINK2_HERE",
#     ...
# ]
# losses_with_dates.loc[
#     losses_with_dates["link"].isin(links_to_fix),
#     ["date", "manually_changed"]
# ] = ["DD-MM-YYYY", True]

# -------------------------------
# Save the updated CSV
# -------------------------------



losses_with_dates.to_csv("ukrainian_losses_with_dates.csv", index=False)
manual_changes_after = (losses_with_dates["manually_changed"] == True).sum()
print(f"Applied manual changes to {manual_changes_after - manual_changes_before} rows.")

"""
Manual changes for Ukrainian losses dataset.

Use this file to manually correct rows where OCR or automatic extraction
produced invalid dates. All manual fixes should be keyed by the 'link' column,
so they are safe even if row numbers change after merging new losses.

Currently, there are no manual corrections applied for the Ukrainian dataset.
You can add them below following the examples.
"""

import pandas as pd

# Load the Ukrainian losses CSV
losses_with_dates = pd.read_csv("ukrainian_losses_with_dates.csv")

# Ensure 'manually_changed' column exists
if "manually_changed" not in losses_with_dates.columns:
    losses_with_dates["manually_changed"] = False

# -------------------------------
# Manual fixes (examples/template)
# -------------------------------

# Example: fixing a single row by link:
# losses_with_dates.loc[
#     losses_with_dates["link"] == "LINK_HERE",
#     ["date", "manually_changed"]
# ] = ["DD-MM-YYYY", True]

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

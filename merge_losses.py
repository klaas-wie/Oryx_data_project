import pandas as pd
import os

def merge_with_most_recent(existing_csv, recent_csv="most_recent_losses.csv", logger=None):
    """
    Merge new rows from `recent_csv` into `existing_csv`, using 'link' as key.

    Rules:
    - Keep ALL rows from the existing CSV.
    - Add rows from the recent CSV if their 'link' is not already present.
    - If multiple rows in recent CSV share the same link, all are added.
    - After merging, overwrite the existing CSV and delete the recent CSV.

    caveat:
    if Oryx changes an entry with an old link, the change will NOT be reflected.
    If you want to be sure to get all changes, delete the existing CSV first.
    However, running the OCR on the entire csv can take a long time (hours) depending on your hardware.
    REDO manual changes if you delete the existing CSV.
    """
    # Load both datasets
    df_existing = pd.read_csv(existing_csv)
    df_new = pd.read_csv(recent_csv)

    # Ensure 'link' column exists
    if "link" not in df_existing.columns or "link" not in df_new.columns:
        raise ValueError("Both CSV files must contain a 'link' column")

    # Find new rows by link
    new_rows = df_new[~df_new["link"].isin(df_existing["link"])]

    # Merge: always keep all old rows, add only truly new rows
    df_merged = pd.concat([df_existing, new_rows], ignore_index=True)

    # Save back to the original CSV
    df_merged.to_csv(existing_csv, index=False)

    # Remove the most recent file since it's no longer needed
    os.remove(recent_csv)

    # Logging
    msg = (
        f"Merged into {existing_csv} | "
        f"Added {len(new_rows)} new rows | "
        f"Updated total: {len(df_merged)} rows | "
        f"Removed {recent_csv}"
    )
    if logger:
        logger.info(msg)
    else:
        print(msg)

if __name__ == "__main__":
    # Example usage → update the file you want to merge into:
    merge_with_most_recent("russian_losses_with_dates.csv")


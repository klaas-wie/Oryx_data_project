import pandas as pd

def merge_new_losses(df_new, csv_path, logger=None):
    """
    Merge new losses into existing CSV without overwriting existing dates.
    Preserves 'date' and 'manually_changed' columns.
    
    Args:
        df_new: DataFrame containing new losses.
        csv_path: Path to the existing CSV file.
        logger: Optional logger for progress messages.
        
    Returns:
        df_merged: Merged DataFrame.
    """
    # Load existing CSV if it exists
    try:
        df_existing = pd.read_csv(csv_path)
        if logger:
            logger.info(f"Loaded {len(df_existing)} existing rows from {csv_path}")
    except FileNotFoundError:
        df_existing = pd.DataFrame(columns=df_new.columns)
        if logger:
            logger.info(f"No existing CSV found. Creating new file: {csv_path}")

    # Ensure essential columns exist
    for col in ["link", "date", "manually_changed"]:
        if col not in df_existing.columns:
            df_existing[col] = None if col == "date" else False
        if col not in df_new.columns:
            df_new[col] = None if col == "date" else False

    # Preserve existing dates and manually_changed flags
    df_new = df_new.merge(
        df_existing[["link", "date", "manually_changed"]],
        on="link",
        how="left",
        suffixes=("", "_existing")
    )

    df_new["date"] = df_new["date_existing"].combine_first(df_new["date"])
    df_new["manually_changed"] = df_new["manually_changed_existing"].combine_first(df_new["manually_changed"])

    df_new.drop(columns=["date_existing", "manually_changed_existing"], inplace=True)

    # Concatenate old and new to capture any rows not in new HTML
    df_merged = pd.concat([df_existing, df_new], ignore_index=True)

    # Drop duplicates by 'link', keeping first occurrence
    before_drop = len(df_merged)
    df_merged.drop_duplicates(subset=["link"], keep="first", inplace=True)
    dropped = before_drop - len(df_merged)

    # Save merged CSV
    df_merged.to_csv(csv_path, index=False, encoding="utf-8")

    if logger:
        added_rows = len(df_merged) - len(df_existing)
        logger.info(f"Merged {added_rows} new rows. Dropped {dropped} duplicates. CSV now has {len(df_merged)} rows.")

    return df_merged

# Optional standalone usage
if __name__ == "__main__":
    import pandas as pd

    csv_path = input("Enter path to existing CSV: ").strip()
    new_csv_path = input("Enter path to new CSV (or leave blank to skip): ").strip()

    if new_csv_path:
        df_new = pd.read_csv(new_csv_path)
        merge_new_losses(df_new, csv_path)
        print(f"Merged {new_csv_path} into {csv_path}")

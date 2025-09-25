import pandas as pd
from extract_from_links_with_dates import extract_date_from_postimg_with_date_in_link_string
from extract_dates_from_twitter import extract_dates_from_twitter

def load_losses_csv(csv_path="losses_with_dates.csv") -> pd.DataFrame:
    """Load losses.csv into a pandas DataFrame."""
    return pd.read_csv(csv_path)

if __name__ == "__main__":
    # Load CSV
    df = load_losses_csv()

    # Ensure 'manually_changed' exists
    if "manually_changed" not in df.columns:
        df["manually_changed"] = False

    # Ensure 'date' column can hold strings
    df["date"] = df["date"].astype(object)

    # --- Postimg links ---
    mask_postimg = (
        df["link"].str.contains("postimg|i.postimg|postlmg", regex=True, na=False)
        & df["date"].isna()
        & ~df["manually_changed"]
    )
    df.loc[mask_postimg, "date"] = df.loc[mask_postimg, "link"].apply(
        extract_date_from_postimg_with_date_in_link_string
    )

    # --- Twitter/X links ---
    # Only process rows without date and not manually changed
    mask_twitter = (
        df["link"].str.contains("twitter.com|x.com", regex=True, na=False)
        & df["date"].isna()
        & ~df["manually_changed"]
    )
    if mask_twitter.any():
        # Subset to these rows before passing to the function
        df_twitter = df[mask_twitter].copy()
        df_twitter = extract_dates_from_twitter(df_twitter)
        # Merge results back into main dataframe
        df.loc[mask_twitter, "date"] = df_twitter["date"]

    # Save updated CSV
    df.to_csv("losses_with_dates.csv", index=False, encoding="utf-8")
    print("Date extraction completed for postimg and Twitter/X links.")

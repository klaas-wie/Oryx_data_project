import pandas as pd
from extract_from_links_with_dates import extract_date_from_postimg_with_date_in_link_string
from extract_dates_from_twitter import extract_dates_from_twitter

def load_losses_csv(csv_path="losses.csv") -> pd.DataFrame:
    """Load losses.csv into a pandas DataFrame."""
    return pd.read_csv(csv_path)

if __name__ == "__main__":
    # Load CSV
    df = load_losses_csv()

    # Ensure 'manually_changed' exists
    if "manually_changed" not in df.columns:
        df["manually_changed"] = False

    # Extract dates from postimg links for rows without a date and not manually changed
    mask_postimg = (
        df["link"].str.contains("postimg|i.postimg|postlmg", regex=True)
        & df["date"].isna()
        & ~df["manually_changed"]
    )
    df.loc[mask_postimg, "date"] = df.loc[mask_postimg, "link"].apply(
        extract_date_from_postimg_with_date_in_link_string
    )

    # Extract dates from Twitter/X links for rows without a date and not manually changed
    mask_twitter = (
        df["link"].str.contains("twitter.com|x.com", regex=True)
        & df["date"].isna()
        & ~df["manually_changed"]
    )
    df = extract_dates_from_twitter(df, mask=mask_twitter)

    # Save updated CSV
    df.to_csv("losses_with_dates.csv", index=False, encoding="utf-8")

    print("Date extraction completed for postimg and Twitter/X links.")

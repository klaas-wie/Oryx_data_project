import pandas as pd
from extract_from_links_with_dates import extract_date_from_postimg_with_date_in_link_string
from extract_dates_from_twitter import extract_dates_from_twitter

def load_losses_csv(csv_path="losses.csv") -> pd.DataFrame:
    """Load losses.csv into a pandas DataFrame."""
    return pd.read_csv(csv_path)

if __name__ == "__main__":
    # Load CSV
    df = load_losses_csv()

    # Extract dates from postimg links
    df["date"] = df["link"].apply(extract_date_from_postimg_with_date_in_link_string)

    # Extract dates from Twitter/X links
    df = extract_dates_from_twitter(df)

    # Save everything to the same CSV
    df.to_csv("losses_with_dates.csv", index=False, encoding="utf-8")

    print("Date extraction completed for postimg and Twitter/X links.")

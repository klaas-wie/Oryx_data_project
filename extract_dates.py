import pandas as pd
import re

from extract_from_links_with_dates import extract_date_from_postimg_with_date_in_link_string

def load_losses_csv(csv_path="losses.csv"):
    """Load losses.csv into a pandas DataFrame."""
    df = pd.read_csv(csv_path)
    return df

if __name__ == "__main__":
    df = load_losses_csv()

    # Extract dates from links with dates, rows without a dd-mm-yy at the end of the link are None
    df["date"] = df["link"].apply(extract_date_from_postimg_with_date_in_link_string)




    df.to_csv("losses_with_dates.csv", index=False, encoding="utf-8")
    
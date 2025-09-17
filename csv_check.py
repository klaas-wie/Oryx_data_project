import csv
import pandas as pd
import re

#df = pd.read_csv("losses.csv")
df = pd.read_csv("losses_with_dates.csv")

def list_unique_loss_types():
    # Count number of rows per unique loss_type
    loss_type_counts = df['loss_type'].value_counts()

    print(loss_type_counts)

def count_category(categoryname):
    category_count = df[df["category"] == categoryname].shape[0]

    print(f"Number of {categoryname} entries: {category_count}")

def count_link_types():
    link_type_counts = df['link_type'].value_counts()

    print(link_type_counts)

def count_link_types_no_date():
    # Filter rows where date is missing or empty string
    missing_date = df['date'].isna() | (df['date'] == "")
    
    # Count link types only for those rows
    link_type_counts = df.loc[missing_date, 'link_type'].value_counts()
    
    print(link_type_counts)

def count_dates():
    """
    Count how many rows have dates filled and how many do not.
    """

    # Drop NA and empty strings for safety
    has_date = df["date"].notna() & (df["date"].astype(str).str.strip() != "")

    count_with_date = has_date.sum()
    count_without_date = (~has_date).sum()

    print(f"Rows with date: {count_with_date}")
    print(f"Rows without date: {count_without_date}")
    print(f"Total rows: {len(df)}")

import pandas as pd
import re

def validate_dates(df: pd.DataFrame):
    """
    Validate that all non-empty dates are in dd-mm-yyyy format,
    with 01 <= day <= 31, 01 <= month <= 12,
    and 2022 <= year <= 2025.
    Returns a list of (row_index, date_str, reason, link).
    """
    results = []

    for idx, date_str in df["date"].dropna().items():
        date_str = str(date_str).strip()

        if not date_str:
            continue

        # Regex for dd-mm-yyyy
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
            results.append((idx, date_str, "Invalid format", df.loc[idx, "link"]))
            continue

        day, month, year = map(int, date_str.split("-"))

        if not (1 <= day <= 31):
            results.append((idx, date_str, f"Invalid day: {day}", df.loc[idx, "link"]))
        elif not (1 <= month <= 12):
            results.append((idx, date_str, f"Invalid month: {month}", df.loc[idx, "link"]))
        elif not (2022 <= year <= 2025):
            results.append((idx, date_str, f"Invalid year: {year}", df.loc[idx, "link"]))

    return results


if __name__ == "__main__":
    # list_unique_loss_types()

    # for category in df["category"].unique():
    #     count_category(category)

    #count_link_types()

    count_link_types_no_date()
    # other_links = df[df['link_type'] == 'other']['link'].tolist()

    # # Print all the links
    # for link in other_links:
    #     print(link)


    bad_dates = validate_dates(df)

    if bad_dates:
        print("Found invalid dates:")
        for idx, val, reason, link in bad_dates:
            print(f"Row {idx}: {val} -> {reason} | Link: {link}")
    else:
        print("✅ All dates look valid!")



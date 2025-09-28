import pandas as pd
import re

# Define datasets
DATASETS = {
    "1": {"name": "Russian losses", "csv": "russian_losses_with_dates.csv"},
    "2": {"name": "Ukrainian losses", "csv": "ukrainian_losses_with_dates.csv"}
}

def date_year_distribution(df):
    """Compute percentage of rows for each year based on 'date' column (dd-mm-yyyy).  
    Ignores empty dates, 'NO_DATE_FOUND', and any invalid formats.
    """
    # Keep only valid dd-mm-yyyy dates with years 2022–2025
    valid_dates = []
    for date_str in df['date'].dropna().astype(str):
        date_str = date_str.strip()
        if not date_str or date_str.upper() == "NO_DATE_FOUND":
            continue
        if re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
            day, month, year = map(int, date_str.split("-"))
            if 1 <= day <= 31 and 1 <= month <= 12 and 2022 <= year <= 2025:
                valid_dates.append(year)

    if not valid_dates:
        print("\nNo valid dates found for year distribution.")
        return

    year_counts = pd.Series(valid_dates).value_counts().sort_index()
    total = len(valid_dates)
    year_percentages = (year_counts / total * 100).round(2)

    print("\nDate distribution by year (percentage of valid rows with date):")
    for year, pct in year_percentages.items():
        print(f"{year}: {pct}% ({year_counts[year]} rows)")


def list_unique_loss_types(df):
    """Print all unique loss types and their counts."""
    print("\nUnique loss types:")
    print(df['loss_type'].value_counts())

def count_category(df, categoryname):
    """Count how many entries belong to a given category."""
    count = df[df["category"] == categoryname].shape[0]
    print(f"\nNumber of {categoryname} entries: {count}")

def count_link_types(df):
    """Count number of rows per link type."""
    print("\nLink type counts:")
    print(df['link_type'].value_counts())

def count_link_types_no_date(df):
    """Count link types only for rows with missing or empty dates."""
    missing_date = df['date'].isna() | (df['date'].astype(str).str.strip() == "") | (df['date'].astype(str).str.upper() == "NO_DATE_FOUND")
    print("\nLink types for rows with missing dates:")
    print(df.loc[missing_date, 'link_type'].value_counts())

def count_dates(df):
    """Count rows with dates and without dates."""
    has_date = df['date'].notna() & (df['date'].astype(str).str.strip() != "") & (df['date'].astype(str).str.upper() != "NO_DATE_FOUND")
    print(f"\nRows with date: {has_date.sum()}")
    print(f"Rows without date: {(~has_date).sum()}")
    print(f"Total rows: {len(df)}")

def validate_dates(df):
    """Validate date format and logical range. Returns list of invalid entries."""
    results = []
    for idx, date_str in df["date"].dropna().items():
        date_str = str(date_str).strip()
        if not date_str or date_str.upper() == "NO_DATE_FOUND":
            continue
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

def show_menu(df):
    """Interactive menu for inspections."""
    while True:
        print("\nSelect inspection to run:")
        print("1: Date distribution by year")
        print("2: List unique loss types")
        print("3: Count entries per category")
        print("4: Count link types")
        print("5: Count link types with missing date")
        print("6: Count rows with/without date")
        print("7: Validate date format")
        print("0: Exit")
        option = input("Enter option number: ").strip()
        
        if option == "1":
            date_year_distribution(df)
        elif option == "2":
            list_unique_loss_types(df)
        elif option == "3":
            print("Available categories:", df["category"].unique().tolist())
            cat = input("Enter category name: ").strip()
            count_category(df, cat)
        elif option == "4":
            count_link_types(df)
        elif option == "5":
            count_link_types_no_date(df)
        elif option == "6":
            count_dates(df)
        elif option == "7":
            bad_dates = validate_dates(df)
            if bad_dates:
                print("\nFound invalid dates:")
                for idx, val, reason, link in bad_dates:
                    print(f"Row {idx}: {val} -> {reason} | Link: {link}")
            else:
                print("\n✅ All dates look valid!")
        elif option == "0":
            print("Exiting inspection menu.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    # 1️⃣ Choose dataset
    print("Select dataset to inspect:")
    for key, ds in DATASETS.items():
        print(f"{key}: {ds['name']}")
    choice = input("Enter 1 or 2: ").strip()
    if choice not in DATASETS:
        print("Invalid choice. Exiting.")
        exit(1)
    
    dataset = DATASETS[choice]
    csv_path = dataset["csv"]

    try:
        df = pd.read_csv(csv_path)
        print(f"\nLoaded {len(df)} rows from '{csv_path}'")
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        exit(1)

    # Launch interactive menu
    show_menu(df)

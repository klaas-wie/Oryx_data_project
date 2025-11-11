import pandas as pd
import re
import os

def date_year_distribution(df):
    """Compute percentage of rows for each year based on 'date' column (dd-mm-yyyy).  
    Ignores empty dates, 'NO_DATE_FOUND', and any invalid formats.
    """
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
    missing_date = (
        df['date'].isna()
        | (df['date'].astype(str).str.strip() == "")
        | (df['date'].astype(str).str.upper() == "NO_DATE_FOUND")
    )
    print("\nLink types for rows with missing dates:")
    print(df.loc[missing_date, 'link_type'].value_counts())


def count_no_date_found(df):
    """Count rows where date equals exactly 'NO_DATE_FOUND'."""
    count = (df["date"].astype(str).str.upper() == "NO_DATE_FOUND").sum()
    print(f"\nRows where date = 'NO_DATE_FOUND': {count}")


def inspect_manually_changed(df):
    """
    Inspect the 'manually_changed' column in a CSV file.
    Prints unique types of entries and their counts.
    """

    if "manually_changed" not in df.columns:
        print(f"⚠️ Column 'manually_changed' not found")
        return

    print(f"\nInspecting 'manually_changed' column in")

    # Show counts of exact values
    print("\nValue counts:")
    print(df["manually_changed"].value_counts(dropna=False))

    # Show the datatypes of values (if mixed types exist)
    print("\nTypes of entries:")
    types = df["manually_changed"].apply(lambda x: type(x).__name__)
    print(types.value_counts())
    
def list_no_date_found_entries(df):
    """
    Print index and link of rows where date == 'NO_DATE_FOUND'.
    Ask user if they want to save these rows to NO_DATE_FOUND.csv.
    """
    mask = df["date"].astype(str).str.upper() == "NO_DATE_FOUND"
    no_date_rows = df.loc[mask, ["link"]]

    if no_date_rows.empty:
        print("\nNo rows with date = 'NO_DATE_FOUND'.")
        return

    print(f"\nRows with date = 'NO_DATE_FOUND' ({len(no_date_rows)} rows):")
    for idx, row in no_date_rows.iterrows():
        print(f"Row {idx}: Link = {row['link']}")

    # Ask user if they want to save to CSV
    if "russian" in csv_path:
        dataset = "russian"
    elif "ukrainian" in csv_path:
        dataset = "ukraine"
    save_input = input(f"\nDo you want to save these rows to 'NO_DATE_FOUND_{dataset}.csv'? (y/n): ").strip().lower()
    if save_input == "y":
        export_df = no_date_rows.copy()
        export_df["date"] = "NO_DATE_FOUND"
        csv_filename = f"NO_DATE_FOUND_{dataset}.csv"
        export_df.to_csv(csv_filename, index=False)
        print(f"\nSaved {len(export_df)} rows to '{csv_filename}'")
    else:
        print("\nCSV not saved.")



def count_dates(df):
    """Count rows with dates and without dates."""
    has_date = (
        df['date'].notna()
        & (df['date'].astype(str).str.strip() != "")
        & (df['date'].astype(str).str.upper() != "NO_DATE_FOUND")
    )
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

def equipment_per_category(df):
    """Show number of rows per equipment type within a selected category."""
    if "category" not in df.columns or "equipment_type" not in df.columns:
        print("⚠️ Required columns ('category' and 'equipment_type') not found.")
        return

    categories = df["category"].dropna().unique().tolist()
    print("\nAvailable categories:", categories)
    cat = input("Enter category name: ").strip()

    if cat not in categories:
        print(f"Category '{cat}' not found in data.")
        return

    subset = df[df["category"] == cat]
    if subset.empty:
        print(f"No rows found for category '{cat}'.")
        return

    print(f"\nEquipment type counts for category '{cat}':")
    print(subset["equipment_type"].value_counts())
    print(f"Total rows in category '{cat}': {len(subset)}")

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
        print("8: Inspect 'manually_changed' column")
        print("9: Count rows where date = 'NO_DATE_FOUND'")
        print("10: List all rows where date = 'NO_DATE_FOUND'")
        print("11: Show equipment type counts per category")
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
        elif option == "8":
            inspect_manually_changed(df)
        elif option == "9":
            count_no_date_found(df)
        elif option == "10":
            list_no_date_found_entries(df)
        elif option == "11":
            equipment_per_category(df)
        elif option == "0":
            print("Exiting inspection menu.")
            break
        else:
            print("Invalid option, try again.")





if __name__ == "__main__":
    # 🔍 Scan for CSV files in current folder
    csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in current directory.")
        exit(1)

    print("Select CSV to inspect:")
    for i, f in enumerate(csv_files, 1):
        print(f"{i}: {f}")
    choice = input("Enter number: ").strip()

    try:
        csv_path = csv_files[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid choice. Exiting.")
        exit(1)

    try:
        df = pd.read_csv(csv_path)
        print(f"\nLoaded {len(df)} rows from '{csv_path}'")
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        exit(1)

    # Launch interactive menu
    show_menu(df)

import pandas as pd
import logging
import os
from html_parser import parse_oryx_html
from write_csv import write_losses_csv
from merge_losses import merge_with_most_recent
from extract_dates import extract_dates
from download_html import download_html

DATASETS = {
    "1": {
        "name": "Russian losses",
        "url": "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html",
        "csv": "russian_losses_with_dates.csv",
        "html_file": "russian_losses.html"
    },
    "2": {
        "name": "Ukrainian losses",
        "url": "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html",
        "csv": "ukrainian_losses_with_dates.csv",
        "html_file": "ukrainian_losses.html"
    }
}

def main():
    # 1️⃣ Ask user which dataset to process
    print("Select dataset to process:")
    for key, val in DATASETS.items():
        print(f"{key}: {val['name']}")
    choice = input("Enter choice: ").strip()
    if choice not in DATASETS:
        print("Invalid choice. Exiting.")
        return

    dataset = DATASETS[choice]
    print(f"Processing {dataset['name']}")

    # --- Logging setup ---
    logging.basicConfig(
        filename=f"{dataset['name'].replace(' ', '_')}.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)
    logger = logging.getLogger()

    # 2️⃣ Download HTML
    logger.info(f"Downloading HTML from {dataset['url']}")
    download_html(dataset["url"], dataset["html_file"])
    logger.info(f"Saved HTML to {dataset['html_file']}")

    # 3️⃣ Parse HTML
    logger.info("Parsing HTML and copying most recently updated Oryx data to csv")
    losses = parse_oryx_html(file_path=dataset["html_file"])
    write_losses_csv(losses)

    # 4️⃣ Merge with existing CSV if exists
    if not os.path.exists(dataset["csv"]):
        logger.info(f"No existing CSV found at {dataset['csv']}, creating new one.")
        os.rename("most_recent_losses.csv", dataset["csv"])
    else:
        logger.info(f"Merging most recent losses into {dataset['csv']}")
        merge_with_most_recent(dataset["csv"], "most_recent_losses.csv", logger=logger)
        logger.info("Merge completed")

    # 5️⃣ Run date extraction (existing dates preserved)
    logger.info("Running date extraction...")
    extract_dates(dataset["csv"], logger=logger)
    logger.info("Date extraction completed")


if __name__ == "__main__":
    main()

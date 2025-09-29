import os
import pandas as pd
import logging
from extract_images_from_postimg import load_postimg_image
from date_extracting_from_image_using_OCR import extract_date_from_image
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="torch.utils.data")


def load_images_from_csv(df: pd.DataFrame):
    """
    Generator yielding (index, url, image) for rows needing OCR.
    """
    rows_to_process = df[
        df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
        df["date"].isna()
    ]
    for idx, row in rows_to_process.iterrows():
        yield idx, row["link"], load_postimg_image(row["link"])


def process_single_row(idx_url_img):
    """
    Process a single image row: run OCR and return (index, date_str)
    """
    idx, url, img = idx_url_img
    if not img:
        return idx, "NO_DATE_FOUND"
    date_str = extract_date_from_image(img)
    return idx, date_str if date_str else "NO_DATE_FOUND"


def extract_dates_from_images(
    df: pd.DataFrame,
    csv_path: str,
    batch_size: int = 10,
    logger=None,
):
    """
    Core OCR function with mandatory CSV saving and optional logging.

    Args:
        df: DataFrame to process.
        csv_path: Path to save the CSV after each batch and at the end.
        batch_size: Number of rows per save batch (default 10).
        logger: Optional logger for progress messages (default None = no logging).

    Returns:
        Updated dataframe with extracted dates (also saved to CSV).
    """
    processed_count = 0

    for idx, url, img in load_images_from_csv(df):
        remaining = df[
            df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
            df["date"].isna()
        ].shape[0] - 1

        if img:
            if logger:
                logger.info(f"[{idx}] Loaded image from {url}: size={img.size}, format={img.format}")
            date_str = extract_date_from_image(img)
            if date_str:
                df.at[idx, "date"] = date_str
                if logger:
                    logger.info(f"[{idx}] Extracted date: {date_str} ({remaining} remaining)")
            else:
                df.at[idx, "date"] = "NO_DATE_FOUND"
                if logger:
                    logger.info(f"[{idx}] No date found in image. ({remaining} remaining)")
        else:
            df.at[idx, "date"] = "NO_DATE_FOUND"
            if logger:
                logger.info(f"[{idx}] Failed to load image from {url} ({remaining} remaining)")

        processed_count += 1
        # Always save CSV after each batch
        if processed_count % batch_size == 0:
            df.to_csv(csv_path, index=False)
            if logger:
                logger.info(f"Saved progress after {processed_count} processed rows.")

    # Final save at the end
    df.to_csv(csv_path, index=False)
    if logger:
        logger.info("Final CSV save completed.")

    return df

if __name__ == "__main__":

    # 🔍 Scan for CSV files in current folder
    csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in current directory.")
        exit(1)

    print("Select CSV run OCR on:")
    for i, f in enumerate(csv_files, 1):
        print(f"{i}: {f}")
    choice = input("Enter number: ").strip()

    try:
        csv_path = csv_files[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid choice. Exiting.")
        exit(1)

    # --- Logging setup ---
    log_file = csv_path.replace(".csv", "_ocr.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    console = logging.StreamHandler()    # Also log to console
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)

    logger = logging.getLogger()         # Get the root logger

    df = pd.read_csv(csv_path)

    # Run the OCR function with logging enabled
    extract_dates_from_images(
        df,
        csv_path=csv_path,
        logger=logger
    )

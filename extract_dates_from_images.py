import os
import pandas as pd
import logging
from extract_images_from_postimg import load_postimg_image
from date_extracting_from_image_using_OCR import extract_date_from_image
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="torch.utils.data")


def load_images_from_csv(df: pd.DataFrame, retry_only_no_date=False):
    """
    Generator yielding (index, url, image) for rows needing OCR.
    If retry_only_no_date=True, only processes rows where date == 'NO_DATE_FOUND'.
    """
    if retry_only_no_date:
        rows_to_process = df[
            df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
            (df["date"].astype(str).str.upper() == "NO_DATE_FOUND")
        ]
    else:
        rows_to_process = df[
            df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
            (df["date"].isna() | (df["date"].astype(str).str.strip() == ""))
        ]

    for idx, row in rows_to_process.iterrows():
        yield idx, row["link"], load_postimg_image(row["link"])


def extract_dates_from_images(
    df: pd.DataFrame,
    csv_path: str,
    batch_size: int = 10,
    logger=None,
    retry_only_no_date=False,
):
    processed_count = 0

    # ✅ Compute the rows we are actually processing
    rows_to_process = df[
        df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
        ((df["date"].astype(str).str.upper() == "NO_DATE_FOUND") if retry_only_no_date
         else (df["date"].isna() | (df["date"].astype(str).str.strip() == "")))
    ]

    for idx, url, img in load_images_from_csv(df, retry_only_no_date=retry_only_no_date):
        # ✅ Use rows_to_process length instead of all df
        remaining = len(rows_to_process) - processed_count - 1

        if img:
            if logger:
                logger.info(f"[{idx}] Loaded image from {url}: size={img.size}, format={img.format}")
            date_str = extract_date_from_image(img)
            if date_str:
                df.at[idx, "date"] = date_str
                if logger:
                    logger.info(f"[{idx}] ✅ Extracted date: {date_str} ({remaining} remaining)")
            else:
                df.at[idx, "date"] = "NO_DATE_FOUND"
                if logger:
                    logger.info(f"[{idx}] ❌ No date found in image ({remaining} remaining)")
        else:
            df.at[idx, "date"] = "NO_DATE_FOUND"
            if logger:
                logger.info(f"[{idx}] ⚠️ Failed to load image from {url} ({remaining} remaining)")

        processed_count += 1

        if processed_count % batch_size == 0:
            df.to_csv(csv_path, index=False)
            if logger:
                logger.info(f"💾 Saved progress after {processed_count} processed rows.")

    df.to_csv(csv_path, index=False)
    if logger:
        logger.info("✅ Final CSV save completed.")

    return df



if __name__ == "__main__":

    # 🔍 Scan for CSV files in current folder
    csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in current directory.")
        exit(1)

    print("Select CSV to run OCR on:")
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
    logger = logging.getLogger()

    # --- Load CSV ---
    df = pd.read_csv(csv_path)
    no_date_rows = df[df["date"].astype(str).str.upper() == "NO_DATE_FOUND"]
    count_no_date = len(no_date_rows)

    # --- Ask user if they want to retry ---
    if count_no_date > 0:
        print(f"\n🕵️ {count_no_date} rows found with NO_DATE_FOUND.")
        retry_choice = input("Would you like to retry OCR for these rows? (y/n): ").strip().lower()

        if retry_choice == "y":
            logger.info(f"Retrying OCR for {count_no_date} rows with NO_DATE_FOUND.")
            extract_dates_from_images(
                df,
                csv_path=csv_path,
                logger=logger,
                retry_only_no_date=True
            )
            print("\n✅ Retry completed. CSV updated and saved.")
        else:
            print("\nSkipping retry. Running normal OCR for missing dates instead...")
            extract_dates_from_images(
                df,
                csv_path=csv_path,
                logger=logger,
                retry_only_no_date=False
            )
    else:
        print("\nNo rows with NO_DATE_FOUND. Running OCR for missing date entries only...")
        extract_dates_from_images(
            df,
            csv_path=csv_path,
            logger=logger,
            retry_only_no_date=False
        )

    print("\n✅ All done! Results saved to:", csv_path)

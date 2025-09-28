import pandas as pd
import warnings
import logging
from extract_images_from_postimg import load_postimg_image
from date_extracting_from_image_using_OCR import extract_date_from_image

warnings.filterwarnings("ignore", category=UserWarning, module="torch.utils.data")

# --- Logging setup ---
logging.basicConfig(
    filename="ocr_log.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)


def load_images_from_csv(df: pd.DataFrame):
    """
    Generator yielding (index, url, image) for rows in the dataframe
    where the link_type is i.postimg, postimg, or postlmg
    and date is empty (NaN).
    Skips rows already processed or flagged as NO_DATE_FOUND.
    """
    rows_to_process = df[
        df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
        df["date"].isna()
    ]

    for idx, row in rows_to_process.iterrows():
        url = row["link"]
        image = load_postimg_image(url)
        yield idx, url, image


if __name__ == "__main__":
    input_csv = "losses_with_dates.csv"
    df = pd.read_csv(input_csv)

    total_to_process = df[
        df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
        df["date"].isna()
    ].shape[0]
    logging.info(f"Total rows needing processing: {total_to_process}")

    batch_size = 10  # Save CSV after every 10 rows
    processed_count = 0

    for idx, url, img in load_images_from_csv(df):
        remaining = df[
            df["link_type"].isin(["i.postimg", "postimg", "postlmg"]) &
            df["date"].isna()
        ].shape[0] - 1

        if img:
            logging.info(f"[{idx}] Loaded image from {url}: size={img.size}, format={img.format}")
            date_str = extract_date_from_image(img)
            if date_str:
                df.at[idx, "date"] = date_str
                logging.info(f"[{idx}] Extracted date: {date_str} ({remaining} remaining)")
            else:
                # Mark row as attempted but no date found
                df.at[idx, "date"] = "NO_DATE_FOUND"
                logging.info(f"[{idx}] No date found in image. ({remaining} remaining)")
        else:
            logging.info(f"[{idx}] Failed to load image from {url} ({remaining} remaining)")

        processed_count += 1
        if processed_count % batch_size == 0:
            df.to_csv(input_csv, index=False)
            logging.info(f"Saved progress after {processed_count} processed rows.")

    # Final save
    df.to_csv(input_csv, index=False)
    logging.info("OCR processing completed for all rows.")

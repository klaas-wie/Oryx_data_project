import pandas as pd
from extract_from_links_with_dates import extract_date_from_postimg_with_date_in_link_string
from extract_dates_from_twitter import extract_dates_from_twitter
from extract_dates_from_images import extract_dates_from_images

def extract_dates(csv_path, logger=None):
    df = pd.read_csv(csv_path)

    # Ensure columns
    if "manually_changed" not in df.columns:
        df["manually_changed"] = False
    df["date"] = df["date"].astype(object)

    # Helper: missing date mask (NaN or empty string)
    missing_date = df["date"].isna() | (df["date"].astype(str).str.strip() == "")

    # --- Postimg links (from link string)
    mask_postimg = (
        df["link"].str.contains("postimg|i.postimg|postlmg", regex=True, na=False)
        & missing_date
        & ~df["manually_changed"]
    )
    df.loc[mask_postimg, "date"] = df.loc[mask_postimg, "link"].apply(
        extract_date_from_postimg_with_date_in_link_string
    )

    # --- Twitter/X links ---
    mask_twitter = (
        df["link"].str.contains("twitter.com|x.com", regex=True, na=False)
        & missing_date
        & ~df["manually_changed"]
    )
    if mask_twitter.any():
        df_twitter = df[mask_twitter].copy()
        df_twitter = extract_dates_from_twitter(df_twitter)
        df.loc[mask_twitter, "date"] = df_twitter["date"]

    # --- Postimg images ---
    mask_postimg_missing = (
        df["link"].str.contains("postimg|i.postimg|postlmg", regex=True, na=False)
        & missing_date
        & ~df["manually_changed"]
    )
    if mask_postimg_missing.any():
        df_postimg_missing = df[mask_postimg_missing].copy()
        df_postimg_missing = extract_dates_from_images(
            df_postimg_missing,
            csv_path=csv_path,
            logger=logger
        )
        df.loc[mask_postimg_missing, "date"] = df_postimg_missing["date"]

    # Save back
    df.to_csv(csv_path, index=False, encoding="utf-8")
    if logger:
        logger.info("Date extraction completed")
    else:
        print("Date extraction completed")


if __name__ == "__main__":
    import logging

    csv_path = input("Enter path to CSV to extract dates for: ").strip()

    logging.basicConfig(
        filename="ocr_log.txt",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)
    logger = logging.getLogger()

    extract_dates(csv_path, logger=logger)

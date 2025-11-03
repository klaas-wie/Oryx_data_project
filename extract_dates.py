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

    total_rows = len(df)
    missing_date = df["date"].isna() | (df["date"].astype(str).str.strip() == "")
    total_missing_initial = missing_date.sum()

    log = lambda msg: logger.info(msg) if logger else print(msg)

    log(f"📄 Total rows in file: {total_rows}")
    log(f"❌ New rows missing date: {total_missing_initial}")

    # --- Postimg links (from link string) ---
    mask_postimg = (
        df["link"].str.contains("postimg|i.postimg|postlmg", regex=True, na=False)
        & missing_date
        & ~df["manually_changed"]
    )
    count_postimg = mask_postimg.sum()
    log(f"🔍 Processing Postimg links with missing date: {count_postimg}")

    if count_postimg > 0:
        before_count = df["date"].notna().sum()
        df.loc[mask_postimg, "date"] = df.loc[mask_postimg, "link"].apply(
            extract_date_from_postimg_with_date_in_link_string
        )
        after_count = df["date"].notna().sum()
        log(f"✅ Dates found from Postimg link strings: {after_count - before_count}")

    # --- Twitter/X links ---
    mask_twitter = (
        df["link"].str.contains("twitter.com|x.com", regex=True, na=False)
        & ((df["date"].isna()) | (df["date"].astype(str).str.strip() == ""))
        & ~df["manually_changed"]
    )
    count_twitter = mask_twitter.sum()
    log(f"🐦 Processing Twitter/X links with missing date: {count_twitter}")

    if count_twitter > 0:
        before_count = df["date"].notna().sum()
        df_twitter = df[mask_twitter].copy()
        df_twitter = extract_dates_from_twitter(df_twitter)
        df.loc[mask_twitter, "date"] = df_twitter["date"]
        after_count = df["date"].notna().sum()
        log(f"✅ Dates found from Twitter extraction: {after_count - before_count}")

    # --- SAVE RESULTS BEFORE OCR ---
    df.to_csv(csv_path, index=False, encoding="utf-8")
    saved_count = df["date"].notna().sum() - (total_rows - total_missing_initial)
    log(f"💾 CSV saved with Postimg + Twitter dates before starting OCR | New rows saved: {saved_count}")

    # --- Postimg images (OCR fallback) ---
    mask_postimg_missing = (
        df["link"].str.contains("postimg|i.postimg|postlmg", regex=True, na=False)
        & ((df["date"].isna()) | (df["date"].astype(str).str.strip() == ""))
        & ~df["manually_changed"]
    )
    count_postimg_missing = mask_postimg_missing.sum()
    log(f"🖼️ Processing Postimg images with missing date (OCR): {count_postimg_missing}")

    if count_postimg_missing > 0:
        before_count = df["date"].notna().sum()
        # ✅ Pass the full DataFrame to preserve previously filled rows
        df = extract_dates_from_images(
            df,
            csv_path=csv_path,
            logger=logger
        )
        after_count = df["date"].notna().sum()
        found_ocr = after_count - before_count
        log(f"✅ Dates found via image OCR: {found_ocr}")

    # --- Final summary ---
    total_missing_final = df["date"].isna().sum() + (df["date"].astype(str).str.strip() == "").sum()
    log(f"🏁 Extraction complete.")
    log(f"🧮 Total rows processed: {total_rows}")
    log(f"🕵️ Found dates - Postimg link: {count_postimg}, Twitter: {count_twitter}, OCR: {count_postimg_missing}")
    log(f"📊 Remaining new rows missing dates: {total_missing_final}")

    # Save back
    df.to_csv(csv_path, index=False, encoding="utf-8")
    log("💾 CSV file saved with updated dates.")


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

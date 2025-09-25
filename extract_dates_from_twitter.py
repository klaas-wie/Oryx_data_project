import pandas as pd
from datetime import datetime, timezone

def snowflake_to_date(snowflake_id: str) -> str:
    """Convert a Twitter/X snowflake ID to dd-mm-yyyy (UTC)."""
    twitter_epoch = 1288834974657  # 2010-11-04 01:42:54 UTC
    try:
        timestamp_ms = (int(snowflake_id) >> 22) + twitter_epoch
        dt = datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return None

def extract_dates_from_twitter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Update 'date' column for rows with link_type 'twitter' using snowflake IDs.
    Only updates rows where 'date' is missing or empty and 'manually_changed' is not True.
    """
    # Ensure column exists
    if "manually_changed" not in df.columns:
        df["manually_changed"] = False

    twitter_rows = (
        (df['link_type'] == 'twitter') &
        (df['date'].isna() | (df['date'] == "")) &
        (~df['manually_changed'])
    )
    
    for idx, row in df[twitter_rows].iterrows():
        try:
            tweet_id = row['link'].rstrip('/').split('/')[-1]
            date_str = snowflake_to_date(tweet_id)
            if date_str:
                df.at[idx, 'date'] = date_str
            else:
                print(f"[{idx}] No date found for {row['link']}")
        except Exception as e:
            print(f"[{idx}] Failed {row['link']}: {e}")
    
    return df

if __name__ == "__main__":
    # Load CSV
    df = pd.read_csv("losses_with_dates.csv")

    # Only update missing dates
    df = extract_dates_from_twitter(df)

    # Save back to same file
    df.to_csv("losses_with_dates.csv", index=False)

    print("Twitter/X date extraction completed.")

import pandas as pd
import warnings

from extract_images_from_postimg import load_postimg_image
from date_extracting_from_image_using_OCR import extract_date_from_image

warnings.filterwarnings("ignore", category=UserWarning, module="torch.utils.data")

def load_images_from_csv(df: pd.DataFrame, sample_size=5):
    """
    Generator that yields (index, url, image) for a random sample of rows 
    in the dataframe where the link_type is i.postimg, postimg, or postlmg
    and date is empty.
    """
    rows_to_process = df[df['link_type'].isin(['i.postimg', 'postimg', 'postlmg']) & df['date'].isna()]
    
    # Take a random sample of rows
    sample_rows = rows_to_process.sample(n=min(sample_size, len(rows_to_process)))
    
    for idx, row in sample_rows.iterrows():
        url = row['link']
        image = load_postimg_image(url)
        yield idx, url, image

if __name__ == "__main__":

    input_csv = "losses_with_dates.csv"  # <-- set your CSV here
    df = pd.read_csv(input_csv)

    count = 0
    max_images = 5  # limit sample size
    for idx, url, img in load_images_from_csv(df, sample_size=5):
        if img:
            print(f"[{idx}] Loaded image from {url}: size={img.size}, format={img.format}")
            date_str = extract_date_from_image(img)
            if date_str:
                print(f"[{idx}] Extracted date: {date_str}")
            else:
                print(f"[{idx}] No date found in image.")
        else:
            print(f"[{idx}] Failed to load image from {url}")
        count += 1
        if count >= max_images:
            break




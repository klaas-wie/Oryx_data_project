import pandas as pd
from extract_images_from_postimg import load_postimg_image

def load_images_from_csv(df: pd.DataFrame):
    """
    Generator that yields (index, url, image) for each row in the dataframe
    where the link_type is i.postimg, postimg, or postlmg and date is empty.
    The image is loaded into memory but not stored permanently.
    """
    for idx, row in df.iterrows():
        if pd.isna(row['date']) and row['link_type'] in ['i.postimg', 'postimg', 'postlmg']:
            url = row['link']
            image = load_postimg_image(url)
            yield idx, url, image

if __name__ == "__main__":

    input_csv = "losses_with_dates.csv"  # <-- set your CSV here
    df = pd.read_csv(input_csv)

    count = 0
    max_images = 5  # limit sample size
    for idx, url, img in load_images_from_csv(df):
        if img:
            print(f"[{idx}] Loaded image from {url}: size={img.size}, format={img.format}")
        else:
            print(f"[{idx}] Failed to load image from {url}")
        count += 1
        if count >= max_images:
            break




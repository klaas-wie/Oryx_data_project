import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/126.0 Safari/537.36"
}

def load_postimg_image(url: str) -> Image.Image | None:
    """
    Load an image from a direct URL or a Postimg page URL.
    Returns a PIL Image object in memory, or None if it fails.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")

        # If the response is an image, open directly
        if "image" in content_type:
            img = Image.open(BytesIO(response.content))
            return img

        # Otherwise, treat it as an HTML page and parse for the real image
        soup = BeautifulSoup(response.text, "html.parser")
        download_link = soup.find("a", id="download")
        main_img = soup.find("img", id="main-image")

        img_url = None
        if download_link and download_link.get("href"):
            img_url = download_link["href"]
        elif main_img and main_img.get("src"):
            img_url = main_img["src"]

        if img_url:
            img_resp = requests.get(img_url, headers=HEADERS, timeout=10)
            img_resp.raise_for_status()
            img = Image.open(BytesIO(img_resp.content))
            return img

        print(f"[WARN] No download link found for {url}")
        return None

    except Exception as e:
        print(f"Failed to load image from {url}: {e}")
        return None

# --- Test ---
if __name__ == "__main__":
    test_urls = [
        "https://i.postimg.cc/Y95mK6D2/o2.jpg",   # direct image
        "https://postimg.cc/vx1b9B1H"             # page URL
    ]

    for idx, url in enumerate(test_urls, start=1):
        print(f"\nProcessing URL: {url}")
        img = load_postimg_image(url)
        if img:
            save_path = f"/mnt/c/Users/KW/Desktop/test_image_{idx}.jpg"
            img.save(save_path)
            print(f"Saved image to: {save_path}")
        else:
            print("Image not loaded.")

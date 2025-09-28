import requests

def download_html(url, filename):
    """Download HTML from a URL and save locally."""
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request fails
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

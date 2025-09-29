from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

from urllib.parse import urlparse

def classify_link(link: str) -> str:
    """
    Classify a URL as one of the known link types.
    Returns 'twitter', 'postimg', 'postlmg', 'imgur', or 'other'.
    """
    domain = urlparse(link).netloc.lower()  # lowercase for consistency

    if "twitter.com" in domain or "x.com" in domain:
        return "twitter"
    elif domain.endswith("postimg.cc"):
        return "postimg"
    elif domain.endswith("postlmg.cc"):
        return "postlmg"
    elif "imgur.com" in domain:
        return "imgur"
    else:
        return "other"


def load_html(file_path="oryx.html"):
    """Load the HTML file and return a BeautifulSoup object."""
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return BeautifulSoup(html_content, "lxml")


def get_category_h3_tags(soup, start_category="Tanks"):
    """Return all <h3> tags starting from a given category."""
    h3_tags = soup.find_all("h3")
    start_collecting = False
    for h in h3_tags:
        text = h.get_text(strip=True)
        if text.startswith(start_category):
            start_collecting = True
        if start_collecting:
            yield h

def parse_li_item(li, category):
    """Parse a single <li> element into multiple loss entries."""
    li_text = li.get_text(" ", strip=True)
    
    # Extract equipment type (ignore number in front)
    equip_match = re.match(r"^\d*\s*(.*?):", li_text)
    if not equip_match:
        return []

    equipment_type = equip_match.group(1).strip()
    losses = []

    for a in li.find_all("a"):
        link = a["href"]
        link_type = classify_link(link)

        bracket_text = a.get_text(strip=True).strip("()")

        # Find the last number in the bracket text
        all_numbers = list(re.finditer(r"\d+", bracket_text))
        if all_numbers:
            last_num_match = all_numbers[-1]
            # Everything after the last number is the loss type
            loss_type = bracket_text[last_num_match.end():].strip(" ,")
            num_text = bracket_text[:last_num_match.end()]
        else:
            # If no number, just take the whole bracket as loss type
            loss_type = bracket_text.strip()
            num_text = ""

        # Find all numbers in num_text
        numbers = re.findall(r"\d+", num_text)
        if not numbers:
            numbers = ["1"]

        for _ in numbers:
            losses.append({
                "equipment_type": equipment_type,
                "category": category,
                "loss_type": loss_type,
                "link_type": link_type,
                "link": link,
                "date": ""  # placeholder
            })

    return losses



def parse_category(h3_tag):
    """Parse all <li> items under a given <h3> category tag."""
    category = h3_tag.get_text(strip=True).split("(")[0].strip()
    category_losses = []

    for sib in h3_tag.find_next_siblings():
        if sib.name == "h3":
            break
        for li in BeautifulSoup(str(sib), "lxml").find_all("li"):
            category_losses.extend(parse_li_item(li, category))

    return category_losses


def parse_oryx_html(file_path, start_category="Tanks"):
    """Main function: parse HTML and return all losses starting from a category."""
    soup = load_html(file_path)
    all_losses = []
    for h3_tag in get_category_h3_tags(soup, start_category=start_category):
        # Stop if h3 doesn't look like a real category
        if not re.search(r"\(\d", h3_tag.get_text(strip=True)):
            break
        all_losses.extend(parse_category(h3_tag))
    return all_losses

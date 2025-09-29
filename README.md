# Oryx Data Project

Scrapes data on Russo-Ukrainian war from Oryx. Assumes starting category is "Tanks". 1 single piece of equipment loss for one row! See html_parser.py for how I did this. 

Importantly, it adds dates to the losses so losses can be tracked over time. For some cases dates could not be found, and there might be cases where human error led to the wrong date. Some typo errors I have edited manually. Overal I believe the dataset is a very close approximation to reality. 

It does that using three methods:
1. Using regex to extract the date from a link.
postimg links often times have dates in their links.
example: https://i.postimg.cc/jdFBJdQb/1027-t55-dam-05-08-23.jpg

2. for Twitter/X links, it uses snowflake ID to extract the post date from a link.
(https://en.wikipedia.org/wiki/Snowflake_ID)

3. It uses Optical Character Recognition for cases where the date was pasted onto the image.
From the data it seems like this was only done in 2022 and 2023. This was by far the hardest part to code. Takes a long time to run on the clean scrape. That's why I added the csv for which I already did the OCR, and the newly scraped Oryx data is compared with the old as to not have to redo the OCR bit.

csv merge flow:
 Merge new rows from `recent_csv` into `existing_csv`, using 'link' as key.

    Rules:
    - Keep ALL rows from the existing CSV.
    - Add rows from the recent CSV if their 'link' is not already present.
    - If multiple rows in recent CSV share the same link, all are added.
    - After merging, overwrite the existing CSV and delete the recent CSV.

    caveat:
    if Oryx changes an entry with an old link, the change will NOT be reflected.
    If you want to be sure to get all changes, delete the existing CSV first.
    You have to completely rerun the OCR. 
    REDO manual changes if you delete the existing CSV, I've tracked them and commented them out.
    """

use check_csv.py to inspect the csv.

## Installation

Steps to install dependencies:
```bash
pip install -r requirements.txt

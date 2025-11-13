# Oryx Data Project

Scrapes data on Russo-Ukrainian war from Oryx. Assumes starting category is "Tanks". 1 single piece of equipment loss for one row! See html_parser.py for how I did this. 

Importantly, it adds dates to the losses so losses can be tracked over time. For some cases dates could not be found, and there might be cases where human error led to the wrong date. Some typo errors I have edited manually. The dataset obviously assumes that the dates listed on Oryx are the actual loss dates, and for twitter assumes that the post date is the loss date. Analysis-wise, the data is best suited for per-month analysis since actual loss dates might be slightly different from the dates listed on Oryx. Overal I believe the dataset is a very close approximation of reality.

## My personal analysis of the data

# Russian dataset
One thing that can be observed is the downtrend of monthly losses overall. For Tanks, IFV's, AFV's, APC's this trend is the clearest. This is consistent with reports and videos of the Russian Army's increased use of other means of troop transportation like motorcycles, buggies, cars, quads and the like. Also it matches with a change of tactic for gaining ground, where the use of small infantry squads is prefered over the use of concentrations of armour. The transparant battlefield makes focussing firepower on these concentrations of troops and vehicles easier than ever, which could explain why we see fewer losses of armoured vehicles. Another explanation could be that Russia simply does not have as many armoured vehicles as before.

Another observation is the high losses for almost all categories during the opening months of the invasion, especially march and april of 2022, after which the Russian army withdrew from the Kyiv and Chernihiv areas.

Also very clearly visible is the increase in aircraft losses for June 2025, when Operation Spider Web took place. 

# Ukrainian dataset
An interesting observation is the spike in losses for march 2025, mainly APC's, IFV's and IMV's. This was the month of the Ukrainian retreat from Kursk. Ukrainian high command suggested this was an orderly withdrawal. The data suggests otherwise.

The general increase and/or sustained amount in losses of APC's, IMV's and 'Ambush Protected Mine Resistant' is also interesting to note, and could be matched with Ukraine's focus on preserving its manpower as well as the support from European countries in providing these types of vehicles.  

Also noticeable is the spike in losses for distinct categories (mainly armour) in june, july and august of 2023 when Ukrainians launched a counter-offensive, mainly in Zaporizhzhia, which was blunted by subborn Russian defense and well prepared defensive lines. 

Expected is the increase in losses for the category 'Unmanned Ground Vehicles' for both sides, confirming the idea that this war is increasingly relying on unmanned equipment. 

The fact that the data can be matched so well with different phases of the war suggests that the dates that I coupled to the visually confirmed losses on Oryx are certainly a close approximation of reality. 

## About the code

Date extraction is done using three methods:
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

use check_csv.py to inspect the csv. If you check the NO_DATE_FOUND rows, it asks if you want to save the csv. You can manually check the dates for certain losses and merge them later if you want. I have done this myself already, but there might be new rows without a date with new runs. There are a couple hundred rows where the date is unknown to me.

On possibility of wrong dates using the OCR:
- When there's a youtube clip used as visual confirmation, it's possible that the timestamp of the youtube bar is seen as a correct date if it falls within the > 2022 range. I have manually corrected the ones that give year >2025, but it's possible that some timestamps look like a 2022-2025 date. This number is probably very small.
- OCR is not perfect. It might see a black 2 as a seven, or a 3 as an 8 if the background is the same color as the number. I've tried to make it as robust as possible but it is possible some errors have gone unnoticed.

some images may have xx.08.2022, or february 2022 on them. For these cases I have manually chosen day 15 for date. The dataset is thus best suited for monthly analysis rather than daily. 

Other things I have discovered:
The number listed on Oryx behind the category name does not always correspond with what is actually listed in terms of losses. 2 cases in the Ukrainian dataset where this makes a big difference: Armoured Personel Cariers, Engineering Vehicles and Equipment and to a lesser extend Radars and Communications equipment.

the csv's NO_DATE_FOUND_[...]_manual_changes list the entries where no date could be found by my code, and that I have checked for dates manually. For some cases I could not find a date so these rows are not represented in the dashboard. If you want a clean sheet of NO_DATE_FOUND entries use csv_check.py option #10. 

## Installation

Steps to install dependencies:
```bash
pip install -r requirements.txt
run python3 main.py

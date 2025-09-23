# Use check_csv to find rows with bad dates. Manually check links to spot human error.

import pandas as pd

# Load your existing file
losses_with_dates = pd.read_csv("losses_with_dates.csv")

# Add manually_changed column
#losses_with_dates["manually_changed"] = False

# Example of manually fixing a row:
# losses_with_dates.at[10, "date"] = "15-03-2023"
# losses_with_dates.at[10, "manually_changed"] = True

# Manual changes:
'''
Found invalid dates:
Row 7368: 24-04-2003 -> Invalid year: 2003 | Link: https://i.postimg.cc/BQvvTDWx/1028-bmp1am-destr-24-04-03.jpg
Row 17174: 18-13-2023 -> Invalid month: 13 | Link: https://i.postimg.cc/gJZhvdV5/1020-tor-m2-dam-18-13-23.jpg
Row 17677: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17678: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17680: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg
Row 17717: 24-26-2023 -> Invalid month: 26 | Link: https://i.postimg.cc/PJLqFSGF/1062-3x-Mi8-MTPR-1x-destr-2x-dam-1x-mi35-destr-1x-mi28-dam-24-26-23.jpg

[12094] No date found for https://pic.twitter.com/a9BoN1E03K
'''

# losses_with_dates.at[7368, "date"] = "24-04-2023"
# losses_with_dates.at[7368, "manually_changed"] = True

# losses_with_dates.at[17174, "date"] = "18-03-2023"
# losses_with_dates.at[17174, "manually_changed"] = True

# rows_to_fix = [17677, 17678, 17680, 17717]
# losses_with_dates.loc[rows_to_fix, "date"] = ["24-06-2023", "24-06-2023", "24-06-2023", "24-06-2023"]
# losses_with_dates.loc[rows_to_fix, "manually_changed"] = True

# losses_with_dates.at[12094, "date"] = "04-10-2022"
# losses_with_dates.at[12094, "manually_changed"] = True

#save the updated file
losses_with_dates.to_csv("losses_with_dates.csv", index=False)

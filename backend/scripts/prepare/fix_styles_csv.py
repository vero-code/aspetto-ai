# backend/scripts/prepare/fix_styles_csv.py

import csv

input_path = "data/styles.csv"
output_path = "data/styles_clean.csv"

"""
This script cleans the styles.csv file from formatting errors — for example, if
the productDisplayName column contains commas without quotes.
It saves a new file named styles_clean.csv.
"""
with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)
    writer.writerow(header)

    for row in reader:
        if len(row) > len(header):
            fixed_row = row[:9]
            title = ",".join(row[9:]).strip()
            fixed_row.append(title)
            writer.writerow(fixed_row)
        else:
            writer.writerow(row)

print("✅ The corrected file is saved as styles_clean.csv")
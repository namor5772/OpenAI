import pandas as pd
import csv, re

infile  = r"C:\Users\grobl\OneDrive\Python\OpenAI\Nutrient.xlsx"
outfile = r"C:\Users\grobl\OneDrive\Python\OpenAI\Nutrient.csv"

# Read first sheet; dtype=str preserves things like leading zeros
df = pd.read_excel(infile, sheet_name=0, dtype=str)

# Clean headers: remove embedded newlines/tabs and trim
clean_cols = []
for c in df.columns:
    s = str(c) if c is not None else ""
    s = re.sub(r'[\r\n\t]+', ' ', s).strip()
    clean_cols.append(s)
df.columns = clean_cols

# (Optional) also strip newlines inside data cells:
df = df.map(lambda x: re.sub(r'[\r\n\t]+', ' ', str(x)) if x is not None else x)

# Write CSV with UTF-8 and quote ALL fields (safest when commas exist in headers)
df.to_csv(outfile, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

import pandas as pd

from src.load import load_data

# calling load data function
# take file path
file = "/home/callum/projects/sno_analysis/data/raw/SNO_combined.txt"

df = load_data(file)
print(df.shape)

# cleaning data by removing rows that have NA in protein column

from src.clean import remove_nas

df_no_nas = remove_nas(df, "position")

from src.clean import remove_duplicates

df_no_duplicates = remove_duplicates(df_no_nas)

import pandas as pd

from src.load import load_data

from src.clean import remove_nas
from src.clean import remove_duplicates
from src.clean import resolve_label_conflicts

# calling load data function
# take file path
file = "/home/callum/projects/sno_analysis/data/raw/SNO_combined.txt"

df = load_data(file)
print(df.shape)

# cleaning data by removing rows that have NA in protein column

df_no_nas = remove_nas(df, "position")

df_no_duplicates = remove_duplicates(df_no_nas)

df_clean = resolve_label_conflicts(df_no_duplicates, group_cols=["id", "position"], label_col="modified", keep_value=1)
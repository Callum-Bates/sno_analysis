import pandas as pd

from src.load import load_data

from src.clean import remove_nas
from src.clean import remove_duplicates
from src.clean import resolve_label_conflicts

from src.analyse import get_pos_and_neg_sites
from src.analyse import get_highly_modified_proteins
from src.analyse import get_top_n_proteins
from src.analyse import create_protein_summary_table

from src.export import df_to_csv


PROCESSED_DIR = "/home/callum/projects/sno_analysis/data/processed"


# calling load data function
# take file path
file = "/home/callum/projects/sno_analysis/data/raw/SNO_combined.txt"

df = load_data(file)
print(df.shape)

# cleaning data by removing rows that have NA in protein column

df_no_nas = remove_nas(df, "position")

df_no_duplicates = remove_duplicates(df_no_nas)

df_clean = resolve_label_conflicts(df_no_duplicates, group_cols=["id", "position"], label_col="modified", keep_value=1)
df_to_csv(df_clean, f"{PROCESSED_DIR}/df_clean.csv", False)



# creating summary tables / new data
positive_sites, negative_sites = get_pos_and_neg_sites(df_clean, "modified")

highly_mod_protein_df = get_highly_modified_proteins(df_clean, "id", 40)
df_to_csv(highly_mod_protein_df, f"{PROCESSED_DIR}/highly_modified.csv", False)

top_20 = get_top_n_proteins(df_clean, 20, "id")

summary = create_protein_summary_table(df_clean, "id")

# saving files
df_to_csv(summary, f"{PROCESSED_DIR}/protein_summary.csv", False)

df_to_csv(top_20, f"{PROCESSED_DIR}/top20_proteins.csv", False)


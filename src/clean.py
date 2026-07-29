import pandas as pd


def remove_nas(df, column):
    
    df_no_na = df.dropna(subset=[column])
    
    rows_before = df.shape[0]
    rows_after = df_no_na.shape[0]
    
    print(f"number of NA rows: {rows_before - rows_after}")
    
    # reset index for export
    df_no_na = df_no_na.reset_index(drop = True)
    
    return df_no_na
    

def remove_duplicates(df):

    # remove duplicates of same row
    df_no_duplicates = df.drop_duplicates()
    
    rows_before = df.shape[0]
    rows_after = df_no_duplicates.shape[0]
    
    print(f"number of duplicate rows: {rows_before - rows_after}")
    
    # reset index for export
    df_no_duplicates = df_no_duplicates.reset_index(drop = True)
    
    return df_no_duplicates



def resolve_label_conflicts(df, group_cols, label_col, keep_value=1):
    """
    For rows sharing the same group_cols (e.g. id + position), where label_col
    has more than one distinct value, keep only the row where label_col == keep_value.
    Rows with no conflict are left untouched.
    """
    # count distinct label values per group
    label_counts = df.groupby(group_cols)[label_col].nunique()
    conflicting_groups = label_counts[label_counts > 1].reset_index()
    conflicting_groups = conflicting_groups.rename(columns={label_col: "n_unique_labels"})

    # flag which rows belong to a conflicting group
    merged = pd.merge(df, conflicting_groups, on=group_cols, how="left", indicator=True)

    # keep: non-conflicting rows, plus only the "keep_value" row within conflicting groups
    no_conflict = merged["_merge"] == "left_only"
    resolved_conflict = (merged["_merge"] == "both") & (merged[label_col] == keep_value)

    result = merged[no_conflict | resolved_conflict].drop(columns=["_merge", "n_unique_labels"])
    return result.reset_index(drop=True)
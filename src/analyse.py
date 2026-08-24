import pandas as pd


def get_pos_and_neg_sites(df, label_col):
    
    positive_condition = df[label_col] == 1
    negative_condition = df[label_col] == 0 

    positive_sites = df[positive_condition]
    negative_sites = df[negative_condition]

    both = df.shape[0]
    print(f"no. sites in original dataframe: {both}")

    positive = positive_sites.shape[0]
    negative = negative_sites.shape[0]
    
    print(f"no. positive sites: {positive}\nno. negative sites: {negative}")
    
    return positive_sites, negative_sites


# returning dataset that has only proteins with x or more registered sites - positive or negative 
# counting / filtering for proteins based on how many sites they have - can identify highly modified proteins

def get_highly_modified_proteins(df, id_col_name, threshold_number):
    series = df.groupby([id_col_name]).size()

    #filter based on x modifications 
    mask = series >= threshold_number
    excluded_mask = series < threshold_number
    # apply the mask
    series_filtered = series[mask]
    series_filtered = series_filtered.reset_index()

    excluded = series[excluded_mask]
    excluded = excluded.reset_index()

    # # check how many proteins appear x or more times

    print(f"proteins > {threshold_number}:{series_filtered.shape}")

    # merge using array of protein ids 

    df_merged = pd.merge(df, series_filtered, on = "id", how = "inner", indicator = False)

    excluded_rows = pd.merge(df, excluded, on="id", how="inner")

    print("================##===============")
    print(f"proteins > {threshold_number}:{series_filtered.shape}")
    print(f"original df:{df.shape}")
    print(f"new dataframe: {df_merged.shape}")
    print(f"ecluded: {excluded.shape}")
    print("================##===============")

    # sanity check

    print(f"{df_merged.shape[0] + excluded_rows.shape[0] == df.shape[0]}")
    
    return df_merged






def get_top_n_proteins(df, n, colname):
    series = df.groupby(colname).size()
    
    # turn into df so we can use it 
    series = series.reset_index()
    series = series.rename(columns={0: "occurrences"})

    # now applying .nlargest - this sorts AND selects in one
    top = series.nlargest(n = n, columns = "occurrences")

    # merging dataframe to create master table of top 20 proteins
    top_merged = pd.merge(df, top, on = "id", how = "inner", indicator= False)

    # sanity check - should be 20 proteins
    print(f"number of unique proteins in final df: {top_merged["id"].nunique()}")
    
    return top_merged



def create_protein_summary_table(df, colname):
    table = df.groupby(colname)["position"].agg(['mean', 'median', 'std'])
    table = table.reset_index()
    
    return table

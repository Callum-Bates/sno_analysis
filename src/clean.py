import pandas as pd


def remove_nas(df, column):
    
    df_no_na = df.dropna(subset=[column])
    
    # reset index 
    df_cleaned = df_no_na.reset_index(drop = True)
    
    return df_cleaned
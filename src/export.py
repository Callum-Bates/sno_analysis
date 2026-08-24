import pandas as pd





def df_to_csv(df, file_path, index_flag):
    
    df.to_csv(file_path, index=index_flag)
    
    print(f"Saved {df.shape[0]} rows to {file_path}")
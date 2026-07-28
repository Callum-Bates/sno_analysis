import pandas as pd
# function for loading file and changing column names
def load_data(file_path):
    df = pd.read_csv(file_path, header = None, sep = "\t")
    
    df = df.rename(columns={
    0: "id",
    1: "modified",
    2: "sequence",
    3: "position"
})
    df["position"] = df["position"].astype("Int64")
    return df

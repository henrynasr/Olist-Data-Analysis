import glob
import pandas as pd

# Find all CSV files in the data directory
for file in glob.glob("data/*.csv"):
    df = pd.read_csv(file)

    print(f"--- File: {file} ---")
    print(f"Shape: {df.shape}")
    #print(f"Columns: {list(df.columns)}")
    #print("First 2 rows:")
    #print(df.head(2))
    print(f"Missing values:\n{df.isnull().sum()}")
    print("\n")

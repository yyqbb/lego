import pandas as pd
import glob
import os

dir_path = '/Users/Downloads/data'  

print(f"Searching for CSV files in: {dir_path}")

csv_files = glob.glob(os.path.join(dir_path, '*.csv'))

if len(csv_files) == 0:
    print("No CSV files found. Please check the directory path.")
else:
    print(f"Found {len(csv_files)} CSV files:")
    for file in csv_files:
        print(file)

combined_df = pd.DataFrame()

for file in csv_files:
    try:
        df = pd.read_csv(file)
        if df.empty:
            print(f"Warning: {file} is empty or has no data rows.")
        else:
            print(f"Reading {file} with {len(df)} rows")
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    except Exception as e:
        print(f"Error reading {file}: {str(e)}")

print(f"Combined DataFrame has {len(combined_df)} rows")

output_path = os.path.join(os.getcwd(), 'combined_sets.csv')

combined_df.to_csv(output_path, index=False)
print(f"Combined CSV file saved to: {output_path}")

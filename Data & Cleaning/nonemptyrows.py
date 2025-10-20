import pandas as pd

file_path = '/Users/combined_sets.csv'
combined_df = pd.read_csv(file_path)

both_non_empty = combined_df[['RRP (USD)', 'Value new (USD)']].notna().all(axis=1).sum()

only_rrp_non_empty = combined_df['RRP (USD)'].notna() & combined_df['Value new (USD)'].isna()
only_rrp_count = only_rrp_non_empty.sum()

only_resale_non_empty = combined_df['Value new (USD)'].notna() & combined_df['RRP (USD)'].isna()
only_resale_count = only_resale_non_empty.sum()

only_used_non_empty = combined_df['Value used (USD)'].notna() & combined_df[['RRP (USD)', 'Value new (USD)']].isna().all(axis=1)
only_used_count = only_used_non_empty.sum()

all_three_non_empty = combined_df[['RRP (USD)', 'Value new (USD)', 'Value used (USD)']].notna().all(axis=1).sum()

print(f"Number of rows with non-empty 'RRP (USD)' and 'Value new (USD)': {both_non_empty}")
print(f"Number of rows with only non-empty 'RRP (USD)': {only_rrp_count}")
print(f"Number of rows with only non-empty 'Value new (USD)': {only_resale_count}")
print(f"Number of rows with only non-empty 'Value used (USD)': {only_used_count}")
print(f"Number of rows with non-empty 'RRP (USD)', 'Value new (USD)', and 'Value used (USD)': {all_three_non_empty}")

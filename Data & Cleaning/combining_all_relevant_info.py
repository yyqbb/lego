import pandas as pd

file_path = '/Users/data/combined_sets.csv'
combined_df = pd.read_csv(file_path)

combined_df = combined_df.rename(columns={'Exit date': 'Retired Date'})

rrp_new_df = combined_df[['Number', 'Theme', 'Subtheme', 'Year', 'RRP (USD)', 'Value new (USD)', 'Minifigs', 'Pieces', 'Launch date', 'Retired Date']].dropna(subset=['RRP (USD)', 'Value new (USD)'])

rrp_used_df = combined_df[['Number', 'Theme', 'Subtheme', 'Year', 'RRP (USD)', 'Value used (USD)', 'Minifigs', 'Pieces', 'Launch date', 'Retired Date']].dropna(subset=['RRP (USD)', 'Value used (USD)'])

rrp_new_used_df = combined_df[['Number', 'Theme', 'Subtheme', 'Year', 'RRP (USD)', 'Value new (USD)', 'Value used (USD)', 'Minifigs', 'Pieces', 'Launch date', 'Retired Date']].dropna(subset=['RRP (USD)', 'Value new (USD)', 'Value used (USD)'])

rrp_new_basic_df = combined_df[['Number', 'Theme', 'Subtheme', 'Year', 'RRP (USD)', 'Value new (USD)']].dropna(subset=['RRP (USD)', 'Value new (USD)'])

rrp_used_basic_df = combined_df[['Number', 'Theme', 'Subtheme', 'Year', 'RRP (USD)', 'Value used (USD)']].dropna(subset=['RRP (USD)', 'Value used (USD)'])

rrp_new_used_basic_df = combined_df[['Number', 'Theme', 'Subtheme', 'Year', 'RRP (USD)', 'Value new (USD)', 'Value used (USD)']].dropna(subset=['RRP (USD)', 'Value new (USD)', 'Value used (USD)'])

rrp_new_df.to_csv('rrp_new_details.csv', index=False)
rrp_used_df.to_csv('rrp_used_details.csv', index=False)
rrp_new_used_df.to_csv('rrp_new_used_details.csv', index=False)
rrp_new_basic_df.to_csv('rrp_new.csv', index=False)
rrp_used_basic_df.to_csv('rrp_used.csv', index=False)
rrp_new_used_basic_df.to_csv('rrp_new_used.csv', index=False)
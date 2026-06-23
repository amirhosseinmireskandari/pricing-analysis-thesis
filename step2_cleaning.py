import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# PHASE 1: Load Your Data into Python
file_name = 'Scraping_Project.csv' 
df = pd.read_csv(file_name)

print("Original Dimensions:", df.shape)  
print(df.head())                         
print(df.dtypes)                         
print(df.isnull().sum())                 

# PHASE 2: Check and Fix Data Types
df['RRP'] = df['RRP'].astype(str).str.replace('€', '').str.replace(' ', '').str.replace(',', '.')
df['RRP'] = pd.to_numeric(df['RRP'], errors='coerce')

df['Sold Products (Numeric)'] = df['Sold Products (Numeric)'].astype(str).str.replace(',', '')
df['Sold Products (Numeric)'] = pd.to_numeric(df['Sold Products (Numeric)'], errors='coerce')

df['number of ratings'] = df['number of ratings'].astype(str).str.replace(',', '')
df['number of ratings'] = pd.to_numeric(df['number of ratings'], errors='coerce')
# Clean and convert the RRP column
df['RRP'] = df['RRP'].astype(str).str.replace('€', '').str.replace(' ', '').str.replace(',', '.')
df['RRP'] = pd.to_numeric(df['RRP'], errors='coerce')
# NOTE: RRP has 378 missing values — this is expected and acceptable
# RRP is not used in any regression specification — missing values in this column are not a concern

# Clean and convert the Sold Products column
df['Sold Products (Numeric)'] = df['Sold Products (Numeric)'].astype(str).str.replace(',', '')
df['Sold Products (Numeric)'] = pd.to_numeric(df['Sold Products (Numeric)'], errors='coerce')
# NOTE: Sold Products column cleaned for completeness — not used in regression specifications
# PHASE 3: Handle Missing Values
# Added Title_URL to the subset to ensure we have valid links to check for duplicates!
df = df.dropna(subset=['Title', 'Title_URL', 'Full Price', 'ratings', 'number of ratings'])
print(f"Rows after dropping missing values: {len(df)}")

# PHASE 4: Apply the Price Range Filter
print(f'Rows before price filter: {len(df)}')
df = df[(df['Full Price'] >= 1.0) & (df['Full Price'] <= 35.0)]
print(f'Rows after price filter: {len(df)}')

# PHASE 5: Remove Duplicates (UPDATED TO CHECK URLs)
print(f'Exact duplicate rows across all columns: {df.duplicated().sum()}')
df = df.drop_duplicates()

# Check for duplicate product links within the same platform
duplicates_by_url = df[df.duplicated(subset=['Platform', 'Title_URL'], keep=False)]
print(f'Products with duplicate URLs on same platform: {len(duplicates_by_url)}')

# For duplicate URLs on the same platform — keep the first occurrence
df = df.drop_duplicates(subset=['Platform', 'Title_URL'], keep='first')

# ============================================================
# Phase 6 — Check for Suspicious Values
# ============================================================

print(f'Rows before suspicious value check: {len(df)}')

# Step 1 — Remove impossible rating values
df = df[(df['ratings'] >= 1.0) & (df['ratings'] <= 5.0)]

# Step 2 — Remove negative review counts
df = df[df['number of ratings'] >= 0]

# Step 3 — Remove perfect 5.0 ratings with 2 or fewer reviews
# These are likely placeholder or fake listings with no genuine consumer feedback
suspicious_perfect = df[(df['ratings'] == 5.0) & (df['number of ratings'] <= 2)]
print(f'Suspicious listings — perfect 5.0 with ≤2 reviews: {len(suspicious_perfect)}')
print(f'  Temu: {len(suspicious_perfect[suspicious_perfect["Platform"] == "Temu"])}')
print(f'  Amazon: {len(suspicious_perfect[suspicious_perfect["Platform"] == "Amazon"])}')

df = df[~((df['ratings'] == 5.0) & (df['number of ratings'] <= 2))]

# Step 4 — Remove extreme review counts above 50,000
suspicious_reviews = df[df['number of ratings'] > 50000]
print(f'Suspicious listings — review count > 50,000: {len(suspicious_reviews)}')

df = df[df['number of ratings'] <= 50000]

print(f'Rows after suspicious value check: {len(df)}')

# ============================================================
# Phase 7 — Create Platform Dummy Variable
# ============================================================

df['platform_dummy'] = df['Platform'].map({'Amazon': 0, 'Temu': 1})
print(f'Missing values in platform_dummy: {df["platform_dummy"].isnull().sum()}')

# ============================================================
# Phase 8 — Create Log Price Variable
# ============================================================

df['log_price'] = np.log(df['Full Price'])
print(f'Missing values in log_price: {df["log_price"].isnull().sum()}')
print(f'Minimum value of log_price: {df["log_price"].min():.4f}')
print(f'Maximum value of log_price: {df["log_price"].max():.4f}')

# ============================================================
# Phase 9 — Check Platform Balance Before Sampling
# ============================================================

print('\nPlatform counts before balancing:')
print(df['Platform'].value_counts())

amazon_count = len(df[df['Platform'] == 'Amazon'])
temu_count = len(df[df['Platform'] == 'Temu'])
target_size = min(amazon_count, temu_count)

print(f'\nAmazon available: {amazon_count}')
print(f'Temu available:   {temu_count}')
print(f'Target size per platform: {target_size}')

# ============================================================
# Phase 9b — Balance the Dataset
# ============================================================

# Randomly undersample the larger platform to match the smaller one
# random_state=42 ensures reproducibility — same result every time you run the script
df_amazon = df[df['Platform'] == 'Amazon'].sample(n=target_size, random_state=42)
df_temu = df[df['Platform'] == 'Temu'].sample(n=target_size, random_state=42)

df_balanced = pd.concat([df_amazon, df_temu]).reset_index(drop=True)

print('\nPlatform counts after balancing:')
print(df_balanced['Platform'].value_counts())
print(f'Total observations: {len(df_balanced)}')

# Verify balance is exactly equal
assert len(df_balanced[df_balanced['Platform'] == 'Amazon']) == \
       len(df_balanced[df_balanced['Platform'] == 'Temu']), \
       "ERROR: Platforms are not balanced — check sampling code"

print('\nBalance check passed — platforms are equal')

# ============================================================
# Phase 12 — Save Clean Dataset
# ============================================================

# Rename columns for Python compatibility before saving
df_balanced = df_balanced.rename(columns={
    'number of ratings': 'number_of_ratings',
    'Full Price': 'full_price',
    'Sold Products (Numeric)': 'sold_products'
})

# Save as Excel for manual spot-checking
df_balanced.to_excel('Thesis_Data_Clean.xlsx', index=False)

# Save as CSV for Python regression pipeline
df_balanced.to_csv('Thesis_Data_Clean.csv', index=False)

# Final confirmation
print('Files saved successfully')
print(f'Excel: Thesis_Data_Clean.xlsx')
print(f'CSV:   Thesis_Data_Clean.csv')
print(f'\nFinal dataset summary:')
print(df_balanced[['full_price', 'log_price', 'ratings', 'number_of_ratings', 'platform_dummy']].describe().round(3))
print(f'\nPlatform balance:')
print(df_balanced['Platform'].value_counts())
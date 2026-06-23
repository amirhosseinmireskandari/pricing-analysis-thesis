import pandas as pd
import numpy as np

# 1. Load the locked, clean dataset generated from the cleaning pipeline
df = pd.read_csv('Thesis_Data_Clean.csv')

print("Dataset loaded successfully. Commencing Chapter 4 Analysis...\n")
print("="*60)
print("          PHASE 1: SUMMARY STATISTICS TABLES")
print("="*60)

# ---------------------------------------------------------
# TABLE 1: RAW PRICE SUMMARY
# ---------------------------------------------------------
summary_price = df.groupby('Platform')['full_price'].agg(
    Mean='mean',
    Median='median',
    Std_Dev='std',
    Min='min',
    Max='max',
    Observations='count'
).round(2)

print("\n--- TABLE 1: RAW PRICE SUMMARY (€) ---")
print(summary_price)

# ---------------------------------------------------------
# TABLE 2: LOG PRICE SUMMARY
# ---------------------------------------------------------
summary_log = df.groupby('Platform')['log_price'].agg(
    Mean='mean',
    Median='median',
    Std_Dev='std',
    Min='min',
    Max='max'
).round(3)

print("\n--- TABLE 2: LOG PRICE SUMMARY ---")
print(summary_log)

# ---------------------------------------------------------
# TABLE 3: FULL VARIABLE SUMMARY (Price, Ratings, Reviews)
# ---------------------------------------------------------
# This generates a wide, multi-column academic table
summary_full = df.groupby('Platform')[['full_price', 'ratings', 'number_of_ratings']].agg(
    ['mean', 'median', 'std', 'min', 'max', 'count']
).round(2)

print("\n--- TABLE 3: COMPLETE DESCRIPTIVE STATISTICS ---")
print(summary_full)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------------------------------------------------
# FIGURE 1: DUAL PRICE DISTRIBUTION HISTOGRAMS
# ---------------------------------------------------------
print("\nGenerating Figure 1: Price Distribution Histograms...")
print(">>> IMPORTANT: Close the pop-up chart window to continue running the script (if applicable) <<<")

# Create the figure with a shared Y-axis
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Filter the data using the exact column names from your clean CSV
amazon_prices = df[df['Platform'] == 'Amazon']['full_price']
temu_prices = df[df['Platform'] == 'Temu']['full_price']

# Plot Amazon (Left side)
axes[0].hist(amazon_prices, bins=25, color='navy', alpha=0.8, edgecolor='white')
axes[0].set_title('Amazon — Price Distribution', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Price (€)', fontsize=11)
axes[0].set_ylabel('Number of Products', fontsize=11)
axes[0].set_xlim(0, 36)
axes[0].grid(axis='y', linestyle='--', alpha=0.7) # Added a grid for academic readability

# Plot Temu (Right side)
axes[1].hist(temu_prices, bins=25, color='steelblue', alpha=0.8, edgecolor='white')
axes[1].set_title('Temu — Price Distribution', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Price (€)', fontsize=11)
axes[1].set_xlim(0, 36)
axes[1].grid(axis='y', linestyle='--', alpha=0.7) # Added a grid for academic readability

# Add main title and format
plt.suptitle('Price Distributions: Amazon vs Temu (Women\'s Tank Tops)', fontsize=14, y=1.02)
plt.tight_layout()

# Save the figure in high resolution for your Word/PDF thesis document
plt.savefig('Figure_1_Histogram_Prices.png', dpi=300, bbox_inches='tight')
print("SUCCESS: Saved -> Figure_1_Histogram_Prices.png")

# Display the chart
plt.show()

# ---------------------------------------------------------
# FIGURE 2: DUAL LOG-PRICE DISTRIBUTION HISTOGRAMS
# ---------------------------------------------------------
print("\nGenerating Figure 2: Log-Price Distribution Histograms...")
print(">>> IMPORTANT: Close the pop-up chart window to continue running the script <<<")

# Create the figure with a shared Y-axis
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Plot Amazon (Left side) - Note the capitalized 'Platform'
axes[0].hist(df[df['Platform'] == 'Amazon']['log_price'], bins=25, 
             color='navy', alpha=0.8, edgecolor='white')
axes[0].set_title('Amazon — ln(Price) Distribution', fontsize=13, fontweight='bold')
axes[0].set_xlabel('ln(Price)', fontsize=11)
axes[0].set_ylabel('Number of Products', fontsize=11)
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# Plot Temu (Right side) - Note the capitalized 'Platform'
axes[1].hist(df[df['Platform'] == 'Temu']['log_price'], bins=25,
             color='steelblue', alpha=0.8, edgecolor='white')
axes[1].set_title('Temu — ln(Price) Distribution', fontsize=13, fontweight='bold')
axes[1].set_xlabel('ln(Price)', fontsize=11)
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

# Add main title and format
plt.suptitle("Price Distributions: Amazon vs Temu\nWomen's Tank Tops (n=550, 275 per platform)", fontsize=13, y=1.02)
plt.tight_layout()

# Save the figure in high resolution for your thesis document
plt.savefig('Figure_2_Histogram_LogPrices.png', dpi=300, bbox_inches='tight')
print("SUCCESS: Saved -> Figure_2_Histogram_LogPrices.png")

# Display the chart
plt.show()

# ---------------------------------------------------------
# FIGURE 3: BOXPLOT OF PRICE DISTRIBUTIONS
# ---------------------------------------------------------
print("\nGenerating Figure 3: Price Boxplots...")
print(">>> IMPORTANT: Close the pop-up chart window to continue running the script <<<")

fig, ax = plt.subplots(figsize=(8, 6))

# Filter the data using the exact column names
data_to_plot = [
    df[df['Platform'] == 'Amazon']['full_price'],
    df[df['Platform'] == 'Temu']['full_price']
]

# Create the boxplot
bp = ax.boxplot(data_to_plot, 
                labels=['Amazon', 'Temu'],
                patch_artist=True,
                medianprops=dict(color='white', linewidth=2))

# Apply platform-specific colors
bp['boxes'][0].set_facecolor('navy')
bp['boxes'][1].set_facecolor('steelblue')

# Formatting for academic standards
ax.set_title('Price Distribution by Platform: Amazon vs Temu', fontsize=13, fontweight='bold')
ax.set_ylabel('Price (€)', fontsize=11)
ax.set_xlabel('Platform', fontsize=11)
ax.set_ylim(0, 40)
ax.grid(axis='y', linestyle='--', alpha=0.7) # Grid helps identify exact percentile values

plt.tight_layout()

# Save the figure in high resolution for your thesis document
plt.savefig('Figure_3_Boxplot_Prices.png', dpi=300, bbox_inches='tight')
print("SUCCESS: Saved -> Figure_3_Boxplot_Prices.png")

# Display the chart
plt.show()

# ---------------------------------------------------------
# PHASE 5: ADDITIONAL DESCRIPTIVE CHECKS
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 5: ADDITIONAL DESCRIPTIVE CHECKS")
print("="*60)

# 1. Headline Price Difference Calculation
amazon_mean = df[df['Platform'] == 'Amazon']['full_price'].mean()
temu_mean = df[df['Platform'] == 'Temu']['full_price'].mean()

absolute_diff = amazon_mean - temu_mean
percentage_diff = ((amazon_mean - temu_mean) / amazon_mean) * 100

print(f'\n--- PRICE DIFFERENCE METRICS ---')
print(f'Amazon mean price: €{amazon_mean:.2f}')
print(f'Temu mean price: €{temu_mean:.2f}')
print(f'Absolute difference: €{absolute_diff:.2f}')
print(f'Percentage difference (Amazon Premium): {percentage_diff:.1f}%')

# 2. Rating Comparison (Quality Proxy)
print(f'\n--- RATING COMPARISON ---')
print(df.groupby('Platform')['ratings'].describe().round(2))

# 3. Reviews Comparison (Market Maturity Proxy)
print(f'\n--- REVIEWS COMPARISON ---')
print(df.groupby('Platform')['number_of_ratings'].describe().round(0))

# 4. Psychological Pricing Check (9-Ending Prevalence)
print(f'\n--- PSYCHOLOGICAL PRICING (.99, .95) ---')
# Isolate the decimal cents (e.g., 14.99 becomes 0.99)
df['decimal_ending'] = df['full_price'].apply(lambda x: round(x % 1, 2))

# Calculate the percentage of items using psychological endings
psych_endings = [0.99, 0.98, 0.97, 0.95]
nine_endings = df.groupby('Platform')['decimal_ending'].apply(
    lambda x: x.isin(psych_endings).mean() * 100
).round(1)

print('Percentage of psychological price endings by platform:')
print(nine_endings.astype(str) + '%')

# ---------------------------------------------------------
# PHASE 6: EXPORT FINAL TABLES & VERIFY FILES
# ---------------------------------------------------------
import os

print("\n" + "="*60)
print("          PHASE 6: EXPORT & FILE VERIFICATION")
print("="*60)

# 1. Export the Master Summary Table to Excel
# This allows you to easily format the table in Excel before pasting into Word
summary_full.to_excel('Table_3_Descriptive_Stats.xlsx')
print("SUCCESS: Saved -> Table_3_Descriptive_Stats.xlsx")

# 2. Verify all required thesis files exist in the folder
print("\nChecking project folder for Chapter 4 assets...")

# The exact names of the files your script generated today
expected_files = [
    'Table_3_Descriptive_Stats.xlsx',
    'Figure_1_Histogram_Prices.png',
    'Figure_2_Histogram_LogPrices.png',
    'Figure_3_Boxplot_Prices.png'
]

current_files = os.listdir('.')
missing_files = []

for file in expected_files:
    if file in current_files:
        print(f"[OK] Secured: {file}")
    else:
        missing_files.append(file)
        print(f"[MISSING] Could not find: {file}")

if len(missing_files) == 0:
    print("\n>>> ALL CHAPTER 4 DESCRIPTIVE ASSETS SECURED! <<<")
    print(">>> YOU ARE OFFICIALLY READY TO RUN THE REGRESSIONS. <<<")
else:
    print("\nWarning: Some files are missing. Check your previous code blocks.")
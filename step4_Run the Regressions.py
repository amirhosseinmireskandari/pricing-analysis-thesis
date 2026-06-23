import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore') # Keeps the terminal clean for your thesis screenshots

# 1. Load the locked, clean dataset
df = pd.read_csv('Thesis_Data_Clean.csv')

print("\n" + "="*60)
print("          PHASE 1: REGRESSION ENVIRONMENT SETUP")
print("="*60)

# Quick structural check
print(f"Dataset Shape: {df.shape}")

# Verify critical regression variables
print("\n--- Summary of Regression Variables ---")
print(df[['log_price', 'platform_dummy', 'ratings', 'number_of_ratings']].describe().round(3))

# Confirm the binary variable is perfectly balanced (0 = Amazon, 1 = Temu)
print("\n--- Platform Dummy Balance ---")
print(df['platform_dummy'].value_counts())

# ============================================================
# PHASE 1B — STANDARDIZE REVIEWS TO FIX CONDITION NUMBER
# ============================================================
# number_of_ratings ranges from 1 to 49,225 while other variables
# range from 1 to 5. This scale difference causes a high condition
# number in Model 1. Standardizing resolves this without affecting
# any substantive findings.

df['number_of_ratings_std'] = (df['number_of_ratings'] - 
                                df['number_of_ratings'].mean()) / \
                                df['number_of_ratings'].std()

print("\n--- Standardized Reviews Variable Check ---")
print(f"Original mean: {df['number_of_ratings'].mean():.1f}, std: {df['number_of_ratings'].std():.1f}")
print(f"Standardized mean: {df['number_of_ratings_std'].mean():.4f}")
print(f"Standardized std:  {df['number_of_ratings_std'].std():.4f}")
print("(Mean should be ~0.0000, Std should be ~1.0000)")

# ---------------------------------------------------------
# PHASE 2: MODEL 1 - BASELINE OLS REGRESSION
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 2: RUNNING MODEL 1 (BASELINE)")
print("="*60)

# Define the hedonic pricing formula using the STANDARDIZED review variable
formula_1 = 'log_price ~ platform_dummy + ratings + number_of_ratings_std'

# Fit the model
model1 = smf.ols(formula_1, data=df).fit()

# Print the dense academic summary
print(model1.summary())

# ---------------------------------------------------------
# PHASE 3: CONVERT COEFFICIENT TO PERCENTAGE
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 3: PLATFORM PREMIUM CALCULATION")
print("="*60)

# Extract the platform_dummy coefficient directly from the model
beta1_model1 = model1.params['platform_dummy']

# Convert log-coefficient to an exact percentage difference
pct_diff_model1 = (np.exp(beta1_model1) - 1) * 100

print(f'β₁ Model 1 (Log units): {beta1_model1:.4f}')
print(f'Percentage price difference: {pct_diff_model1:.1f}%')

# ---------------------------------------------------------
# PHASE 4: MODEL 2 - WITHOUT REVIEWS (ENDOGENEITY CHECK)
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 4: RUNNING MODEL 2 (ENDOGENEITY CHECK)")
print("="*60)

# Model 2 — dropping reviews entirely to check for omitted variable bias
formula_2 = 'log_price ~ platform_dummy + ratings'
model2 = smf.ols(formula_2, data=df).fit()

# Print the dense academic summary
print(model2.summary())

# Extract and convert β₁ from Model 2
beta1_model2 = model2.params['platform_dummy']
pct_diff_model2 = (np.exp(beta1_model2) - 1) * 100

print(f'\n--- PLATFORM PREMIUM (MODEL 2) ---')
print(f'β₁ Model 2 (Log units): {beta1_model2:.4f}')
print(f'Percentage price difference: {pct_diff_model2:.1f}%')

# Compare the two models side-by-side
print(f'\n--- ROBUSTNESS COMPARISON (MODEL 1 vs MODEL 2) ---')
print(f'Model 1 (with reviews):    {beta1_model1:.4f} ({pct_diff_model1:.1f}%)')
print(f'Model 2 (without reviews): {beta1_model2:.4f} ({pct_diff_model2:.1f}%)')
print(f'Absolute Difference in β₁: {abs(beta1_model1 - beta1_model2):.4f}')

# ---------------------------------------------------------
# PHASE 5: AUTOMATED REGRESSION RESULTS EXTRACTION
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 5: BUILDING THE MASTER RESULTS TABLE")
print("="*60)

def extract_results(model, model_name):
    # Extract core metrics using the exact variable names
    results = {
        'Model': model_name,
        'β₁ (Platform)': round(model.params['platform_dummy'], 4),
        'SE (Platform)': round(model.bse['platform_dummy'], 4),
        'p-value (Platform)': '<0.001' if model.pvalues['platform_dummy'] < 0.001 else round(model.pvalues['platform_dummy'], 4),
        
        'β₂ (Rating)': round(model.params['ratings'], 4),
        'SE (Rating)': round(model.bse['ratings'], 4),
        'p-value (Rating)': '<0.001' if model.pvalues['ratings'] < 0.001 else round(model.pvalues['ratings'], 4),
        
        'R²': round(model.rsquared, 4),
        'Adj R²': round(model.rsquared_adj, 4),
        'N': int(model.nobs),
        '% Price Diff': f"{round((np.exp(model.params['platform_dummy']) - 1) * 100, 2)}%"
    }
    
    # Check for the standardized review variable
    if 'number_of_ratings_std' in model.params:
        # Changed to 4 decimal places since standardized vars produce larger coefficients
        results['β₃ (Reviews)'] = round(model.params['number_of_ratings_std'], 4)
        results['p-value (Reviews)'] = '<0.001' if model.pvalues['number_of_ratings_std'] < 0.001 else round(model.pvalues['number_of_ratings_std'], 4)
    else:
        results['β₃ (Reviews)'] = 'Excluded'
        results['p-value (Reviews)'] = '—'
    
    return results

# Run the extraction on both our models
r1 = extract_results(model1, 'Model 1 (With Reviews)')
r2 = extract_results(model2, 'Model 2 (Without Reviews)')

# Combine into a pandas DataFrame and transpose (.T) for typical academic formatting
results_df = pd.DataFrame([r1, r2]).set_index('Model').T
print(results_df)

# Save to Excel for easy copy/pasting into Chapter 4
results_df.to_excel('Table_4_Regression_Results.xlsx')
print("\nSUCCESS: Saved -> Table_4_Regression_Results.xlsx")

# ---------------------------------------------------------
# PHASE 6: CHECK R² AND MODEL FIT
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 6: CHECK R² AND MODEL FIT")
print("="*60)

print(f'Model 1 (With Reviews) R²:         {model1.rsquared:.4f}')
print(f'Model 1 (With Reviews) Adj R²:     {model1.rsquared_adj:.4f}')
print("-" * 40)
print(f'Model 2 (Without Reviews) R²:      {model2.rsquared:.4f}')
print(f'Model 2 (Without Reviews) Adj R²:  {model2.rsquared_adj:.4f}')

# ---------------------------------------------------------
# PHASE 7: PRODUCE ACADEMIC REGRESSION RESULTS TABLE
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 7: ACADEMIC FORMATTING EXPORT")
print("="*60)

# Helper function to assign significance stars dynamically
def get_stars(p_value):
    if p_value < 0.01: return '***'
    if p_value < 0.05: return '**'
    if p_value < 0.10: return '*'
    return ''

table_data = {
    'Variable': [
        'Platform (1 = Temu)', '', 
        'Ratings (1-5 Stars)', '', 
        'Review Volume (Standardized)', '', # Updated Label
        'Constant', '', 
        'R²', 'Adj. R²', 'Observations', 'Platform Premium (%)'
    ],
    'Model 1 (With Reviews)': [
        f'{model1.params["platform_dummy"]:.4f}{get_stars(model1.pvalues["platform_dummy"])}',
        f'({model1.bse["platform_dummy"]:.4f})',
        f'{model1.params["ratings"]:.4f}{get_stars(model1.pvalues["ratings"])}',
        f'({model1.bse["ratings"]:.4f})',
        # Updated to extract the _std variable
        f'{model1.params["number_of_ratings_std"]:.4f}{get_stars(model1.pvalues["number_of_ratings_std"])}',
        f'({model1.bse["number_of_ratings_std"]:.4f})',
        f'{model1.params["Intercept"]:.4f}{get_stars(model1.pvalues["Intercept"])}',
        f'({model1.bse["Intercept"]:.4f})',
        f'{model1.rsquared:.4f}',
        f'{model1.rsquared_adj:.4f}',
        f'{int(model1.nobs)}',
        f'{(np.exp(model1.params["platform_dummy"]) - 1) * 100:.1f}%'
    ],
    'Model 2 (Without Reviews)': [
        f'{model2.params["platform_dummy"]:.4f}{get_stars(model2.pvalues["platform_dummy"])}',
        f'({model2.bse["platform_dummy"]:.4f})',
        f'{model2.params["ratings"]:.4f}{get_stars(model2.pvalues["ratings"])}',
        f'({model2.bse["ratings"]:.4f})',
        '—',
        '—',
        f'{model2.params["Intercept"]:.4f}{get_stars(model2.pvalues["Intercept"])}',
        f'({model2.bse["Intercept"]:.4f})',
        f'{model2.rsquared:.4f}',
        f'{model2.rsquared_adj:.4f}',
        f'{int(model2.nobs)}',
        f'{(np.exp(model2.params["platform_dummy"]) - 1) * 100:.1f}%'
    ]
}

table_df = pd.DataFrame(table_data).set_index('Variable')
print(table_df)

# Save to Excel for perfect copy-pasting into Word
table_df.to_excel('Table_5_Academic_Regression_Results.xlsx')
print("\nSUCCESS: Saved -> Table_5_Academic_Regression_Results.xlsx")

# ---------------------------------------------------------
# PHASE 8: VISUALIZE THE REGRESSION RESULTS
# ---------------------------------------------------------
print("\n" + "="*60)
print("          PHASE 8: VISUALIZING COEFFICIENT STABILITY")
print("="*60)
print("Generating Figure 4: Coefficient Plot...")
print(">>> IMPORTANT: Close the pop-up chart window to finish the script <<<")

fig, ax = plt.subplots(figsize=(8, 5))

models = ['Model 1\n(With Reviews)', 'Model 2\n(Without Reviews)']
betas = [model1.params['platform_dummy'], model2.params['platform_dummy']]

# Extract the 95% Confidence Intervals (0 = lower bound, 1 = upper bound)
ci_low = [model1.conf_int().loc['platform_dummy', 0], 
          model2.conf_int().loc['platform_dummy', 0]]
ci_high = [model1.conf_int().loc['platform_dummy', 1],
           model2.conf_int().loc['platform_dummy', 1]]

colors = ['navy', 'steelblue']

# Plot the dots and the vertical confidence interval lines
for i, (model_name, beta, low, high, color) in enumerate(zip(models, betas, ci_low, ci_high, colors)):
    ax.scatter(i, beta, color=color, s=100, zorder=5)
    ax.vlines(i, low, high, color=color, linewidth=2.5)

# Add a red zero-line to easily visualize statistical significance
ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)

# Formatting for academic standards
ax.set_xticks([0, 1])
ax.set_xticklabels(models, fontsize=11, fontweight='bold')
ax.set_ylabel('β₁ Coefficient (Platform Effect)', fontsize=11)
ax.set_title('Platform Coefficient (β₁) with 95% Confidence Intervals\nDependent variable: ln(Price)', fontsize=13, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust the Y-axis so the -1.19 coefficient sits nicely in the frame
ax.set_ylim(-1.5, 0.5)

plt.tight_layout()

# Save the figure in high resolution for your presentation
plt.savefig('Figure_4_Coefficient_Plot.png', dpi=300, bbox_inches='tight')
print("SUCCESS: Saved -> Figure_4_Coefficient_Plot.png")

# Display the chart
plt.show()

# ============================================================
# STEP 5: ROBUSTNESS CHECK — MEDIAN REGRESSION (QUANTILE)
# ============================================================
print("\n" + "="*60)
print("          STEP 5: MEDIAN REGRESSION (ROBUSTNESS CHECK)")
print("="*60)

# We use the exact same formula as our optimized Model 1
formula_1 = 'log_price ~ platform_dummy + ratings + number_of_ratings_std'

# Fit the Quantile Regression model at q=0.5 (The Median)
# We set max_iter=2000 to ensure the optimization algorithm has enough time to converge
model_qr = smf.quantreg(formula_1, data=df).fit(q=0.5, max_iter=2000)

# Extract and convert the β₁ coefficient from the Median model
beta1_qr = model_qr.params['platform_dummy']
pct_diff_qr = (np.exp(beta1_qr) - 1) * 100

# Extract the previously saved OLS baseline coefficient for comparison
beta1_ols = model1.params['platform_dummy']
pct_diff_ols = (np.exp(beta1_ols) - 1) * 100

print("\n--- QUANTILE REGRESSION (q=0.5) RESULTS ---")
print(model_qr.summary())

print(f'\n--- ROBUSTNESS COMPARISON (OLS MEAN vs QUANTILE MEDIAN) ---')
print(f'OLS Baseline (Mean) β₁:  {beta1_ols:.4f} ({pct_diff_ols:.1f}%)')
print(f'Median Regression β₁:    {beta1_qr:.4f} ({pct_diff_qr:.1f}%)')
print(f'Absolute Difference:     {abs(beta1_ols - beta1_qr):.4f}')

if abs(beta1_ols - beta1_qr) < 0.1:
    print(">>> CONCLUSION: HIGHLY ROBUST. Outliers are not driving your results. <<<")
else:
    print(">>> CONCLUSION: SENSITIVE. Outliers are influencing your OLS mean. <<<")
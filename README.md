# Pricing Patterns in Online Fashion Marketplaces: Evidence from Amazon and Temu

**Master's Thesis — Marketing and Digital Transformation**  
**University of Padova | Supervisor: Professor Leonardo Madio**  
**Expected Defence: September 2026**

---

## Overview

This repository contains the full empirical pipeline for the thesis *"Pricing Patterns in Online Fashion Marketplaces: Evidence from Amazon and Temu."*

The study empirically compares product-level pricing between Amazon and Temu within the women's tank tops category using a cross-sectional dataset of 550 observations (275 per platform). The analysis employs OLS hedonic regression to estimate the platform price differential after controlling for observable product quality characteristics.

**Central Research Question:**  
How do pricing patterns and price distributions differ across online marketplaces such as Amazon and Temu in a cross-border e-commerce environment within a comparable product category?

**Main Finding:**  
After controlling for product rating and review volume, Temu products are associated with prices approximately **69.8–70.1% lower** than comparable Amazon products. This finding is statistically significant at the 1% level and robust across all specifications.

---

## Repository Structure

```
├── data/
│   ├── Scraping_Project.csv          # Raw collected dataset (678 observations)
│   └── Thesis_Data_Clean.csv         # Final cleaned and balanced dataset (550 observations)
│
├── scripts/
│   ├── step2_cleaning.py             # Data cleaning pipeline
│   ├── step3_descriptive.py          # Descriptive statistics and visualizations
│   ├── step4_regression.py           # OLS regression analysis and robustness checks
│
├── outputs/
│   ├── tables/
│   │   ├── Table_3_Descriptive_Stats.xlsx
│   │   ├── Table_4_Regression_Results.xlsx
│   │   └── Table_5_Academic_Regression_Results.xlsx
│   └── figures/
│       ├── Figure_1_Histogram_Prices.png
│       ├── Figure_2_Histogram_LogPrices.png
│       ├── Figure_3_Boxplot_Prices.png
│       └── Figure_4_Coefficient_Plot.png
│
└── README.md
```

---

## Data

### Collection
Data were collected manually and via Octoparse from Amazon.it and Temu.com within a single collection window in May 2026. The product category is restricted to women's tank tops (single-item listings only — bundle and multi-pack listings excluded) within a price range of €1–€35.

**Variables collected:**

| Variable | Description |
|---|---|
| Title | Product listing title |
| Title_URL | Direct URL to product page |
| Full Price | Base/original listed price in euros |
| Number of Ratings | Total review count |
| Ratings | Average star rating (1.0–5.0) |
| Platform | Amazon or Temu |

### Cleaning Pipeline (step2_cleaning.py)
The raw dataset of 678 observations was processed through the following steps:

| Decision | Rows Affected | Reason |
|---|---|---|
| Raw data | 678 | Starting point |
| Dropped — missing core metrics | 2 | Ghost rows |
| Dropped — outside €1–35 range | 0 | Passed by design |
| Dropped — suspicious listings | 35 | Perfect 5.0 rating with ≤2 reviews (33) or >50,000 reviews (2) |
| Remaining before balancing | 641 | Clean unbalanced dataset |
| Dropped — random undersampling | 91 | Amazon downsampled from 366 to match Temu (275) |
| **Final clean dataset** | **550** | **275 per platform** |

Random undersampling used `random_state=42` for reproducibility.

---

## Methodology

### Econometric Specifications

All models use the natural log of price as the dependent variable to address right-skew and enable percentage interpretation of coefficients.

**Model 1 (Full specification):**
```
ln(Price) = β₀ + β₁·Platform + β₂·Ratings + β₃·Reviews_std + ε
```

**Model 2 (Restricted — endogeneity check):**
```
ln(Price) = β₀ + β₁·Platform + β₂·Ratings + ε
```

- `Platform`: binary indicator (Amazon = 0, Temu = 1)
- `Ratings`: average star rating (1.0–5.0)
- `Reviews_std`: standardized review count (z-score transformation applied to resolve matrix conditioning issue — condition number reduced from 6.66×10⁴ to 66.9)

The platform effect is recovered as: **(e^β₁ − 1) × 100**

The two-specification design addresses the potential endogeneity of review volume. Stability of β₁ across both models provides a partial robustness check.

**Robustness check:** Median regression (quantile regression at q=0.5) confirms findings are not driven by extreme price observations.

> **Important:** All results are interpreted as conditional associations, not causal effects. The cross-sectional design does not permit causal identification.

---

## Results

### Descriptive Statistics

| Statistic | Amazon | Temu |
|---|---|---|
| Mean price | €17.51 | €5.88 |
| Median price | €14.99 | €5.70 |
| Std deviation | €6.14 | €1.30 |
| Min | €4.69 | €3.40 |
| Max | €34.95 | €12.27 |
| Observations | 275 | 275 |

Raw price gap: **€11.63 (66.4% Amazon premium)**  
Psychological pricing (9-endings): **70.5% Amazon vs 5.1% Temu**

### Regression Results

| | Model 1 (Full) | Model 2 (Restricted) |
|---|---|---|
| Platform (β₁) | −1.1983*** (0.0329) | −1.2089*** (0.0336) |
| Rating (β₂) | 0.2264*** (0.0371) | 0.2356*** (0.0378) |
| Reviews std (β₃) | 0.0569*** (0.0113) | — |
| Constant | 1.8561*** (0.1560) | 1.8203*** (0.1592) |
| R² | 0.8053 | 0.7963 |
| Adj. R² | 0.8042 | 0.7955 |
| N | 550 | 550 |
| **Platform premium** | **−69.8%** | **−70.1%** |

*Standard errors in parentheses. \* p<0.10, \*\* p<0.05, \*\*\* p<0.01*

### Robustness Check

| Specification | β₁ | Platform Premium |
|---|---|---|
| OLS Model 1 | −1.1983 | −69.8% |
| OLS Model 2 | −1.2089 | −70.1% |
| Median Regression | −1.1478 | −68.3% |

Difference between OLS and median regression: 0.0505 — confirms finding is not driven by outliers.

---

## Requirements

```
pandas
numpy
statsmodels
matplotlib
scipy
openpyxl
```

Install with:
```bash
pip install pandas numpy statsmodels matplotlib scipy openpyxl
```

---

## How to Reproduce

Run scripts in order:

```bash
python step2_cleaning.py       # Produces Thesis_Data_Clean.csv
python step3_descriptive.py    # Produces Tables 1–3 and Figures 1–3
python step4_regression.py     # Produces Tables 4–5 and Figure 4
```

Each script loads from the output of the previous step. Place `Scraping_Project.csv` in the same directory before running.

---

## Limitations

- Cross-sectional snapshot — dynamic pricing not captured
- Base price measure may not reflect actual transaction prices given Temu's promotional intensity
- Unobserved quality differences between platforms not fully controlled
- Findings specific to women's tank tops — generalizability to other categories requires further research
- Temu's penetration pricing strategy may reflect a temporary market position rather than long-run equilibrium

---

## Author

**Amir** — Master's student, Marketing and Digital Transformation, University of Padova  
Thesis supervised by Professor Leonardo Madio# pricing-analysis-thesis
Amazon vs Temu pricing analysis using regression models

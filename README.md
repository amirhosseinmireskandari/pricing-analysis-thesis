# Pricing Patterns in Online Fashion Marketplaces: Evidence from Amazon and Temu

**Master's thesis, MSc in Management for Sustainable Firms (track: Marketing and Digital Transformation)**
**University of Padova, Department of Economics and Management "Marco Fanno"**
**Supervisor: Prof. Leonardo Madio | Defended: October 2026**

---

## At a glance

![Regression coefficients](outputs/figures/Figure_4_Coefficient_Plot.png)

- Temu's mean listed price is **66% lower** than Amazon's (€5.88 vs €17.51).
- After controlling for rating and review volume, the gap is about **70%** (β = −1.1983), stable across three specifications.
- **70.5%** of Amazon listings have a price ending in .99 or .95, against **5.1%** on Temu.

---

## Overview

This repository contains the data and the analysis pipeline for the thesis *"Pricing Patterns in Online Fashion Marketplaces: Evidence from Amazon and Temu."*

The study compares **listed prices** at product level on Amazon Italy and Temu Italy within one fashion category (women's tank tops). It uses a cross-sectional dataset of 550 listings (275 per platform) and log-linear OLS regressions of price on a platform indicator, controlling for product rating and standardized review volume.

**Central research question:**
How do pricing patterns and price distributions differ across online marketplaces such as Amazon and Temu in a cross-border e-commerce environment within a comparable product category?

**Main findings:**

- Mean listed price: **€5.88 on Temu vs €17.51 on Amazon**, an unconditional difference of about **66%**.
- After controlling for rating and review volume, listed prices on Temu are about **70% lower** (β = −1.1983, p < 0.01; −69.8%).
- The estimate is stable without the review control (β = −1.2089, −70.1%) and under median regression (β = −1.1478, −68.3%).

> **Important:** all results are **conditional associations, not causal effects**. The listings are comparable but not matched products, the data are a single cross-section, and unobserved differences in material, quality or brand may contribute to the gap. See [Limitations](#limitations).

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

There is no `step1` script: data collection (step 1) was done with Octoparse and manually, as described below.

---

## Data

### Collection

- **Sources:** Amazon Italy (amazon.it) and Temu Italy (temu.com/it-en). The Italian storefronts hold the national market and currency constant.
- **Search term:** "women tank top", results in default relevance order, no additional filters.
- **Method:** Amazon listings were extracted with **Octoparse** (23 May 2026). Temu listings were collected **manually** (24–26 May 2026), because Temu's anti-scraping mechanisms made automated extraction impractical.
- **Scope:** women's tank tops priced between **€1 and €35**. The €1 floor is needed for the log transformation, and the €35 ceiling excludes a small number of atypical outliers (for example branded items and multi-piece bundles).

**Variables collected:**

| Variable | Description |
|---|---|
| Title | Product listing title |
| Title_URL | Direct URL to product page |
| Full Price | Listed base price in euros |
| Number of Ratings | Total review count |
| Ratings | Average star rating (1.0–5.0) |
| Platform | Amazon or Temu |

### Cleaning pipeline (`step2_cleaning.py`)

| Step | Rows affected | Reason |
|---|---|---|
| Raw data | 678 | Starting point |
| Dropped: missing values | 2 | Missing values in required variables |
| Dropped: outside €1–€35 | 0 | All observations satisfied the predefined range |
| Dropped: duplicates | 0 | No exact duplicate records or duplicate URLs within a platform |
| Dropped: suspicious listings | 35 | Perfect 5.0 rating with ≤2 reviews (33), or more than 50,000 reviews (2) |
| Remaining before balancing | 641 | 366 Amazon + 275 Temu |
| Dropped: random undersampling | 91 | Amazon reduced from 366 to 275 to match Temu |
| **Final dataset** | **550** | **275 per platform** |

Random undersampling used `random_state=42` for reproducibility.

> **Data note:** the raw file contains listing titles and URLs that were publicly displayed when collected, for academic research. Check the platforms' terms of service before reusing or redistributing it.

---

## Methodology

### Econometric specifications

All models use the natural log of price as the dependent variable. This addresses right-skewed prices and lets coefficients be read as percentage differences.

**Model 1 (full specification):**
```
ln(Price) = β₀ + β₁·Platform + β₂·Rating + β₃·Reviews_std + ε
```

**Model 2 (without reviews, sensitivity check):**
```
ln(Price) = β₀ + β₁·Platform + β₂·Rating + ε
```

- `Platform`: binary indicator (Amazon = 0, Temu = 1)
- `Rating`: average star rating, kept in raw form (1.0–5.0)
- `Reviews_std`: review count standardized to a z-score, because counts range from under 10 to over 49,000. Standardization changes the scale, not the substance. In the regression script it also reduced the condition number of the design matrix from 6.66×10⁴ to 66.9.

The percentage price difference is recovered as **(e^β₁ − 1) × 100**.

**Expected signs:** Platform negative (H1), Rating positive (H2); no directional prediction for Reviews_std, because review volume is endogenous.

### Endogeneity and robustness

- **Two-specification design.** Review volume is plausibly endogenous: unobserved quality, seller reputation and marketing effort may affect both reviews and price. Comparing Models 1 and 2 shows that the platform coefficient is **not sensitive to including review volume**. This does **not** establish that review volume is exogenous. A causal estimate would need an instrumental-variable strategy or matched products, which is outside the scope of the thesis.
- **Median regression** (quantile regression at q = 0.5) checks that the result is not driven mainly by extreme price observations.

### Standard errors

The reported standard errors (in parentheses) are conventional, non-robust OLS standard errors. Price dispersion differs strongly between platforms (standard deviation €6.14 on Amazon vs €1.30 on Temu), so the errors are unlikely to have constant variance. Heteroskedasticity-robust (HC) standard errors are listed under [extensions](#possible-extensions). They would change the standard errors and p-values, not the coefficients.

---

## Results

### Descriptive statistics (N = 275 per platform)

| Statistic | Amazon | Temu |
|---|---|---|
| Mean price | €17.51 | €5.88 |
| Median price | €14.99 | €5.70 |
| Std deviation | €6.14 | €1.30 |
| Min | €4.69 | €3.40 |
| Max | €34.95 | €12.27 |
| Mean rating | 4.18 | 4.83 |
| Rating std deviation | 0.42 | 0.11 |
| Mean / median review count | 1,145 / 111 | 766 / 134 |

- Mean listed price difference: **€11.63**, i.e. Temu's mean listed price is **66.4% lower**.
- Share of listings with a price ending in .99 or .95: **70.5% on Amazon vs 5.1% on Temu**.
- 56 Amazon listings have a rating below 4.0 stars, against none on Temu.

### Regression results (dependent variable: ln(Price), N = 550)

| | (1) OLS, Model 1 | (2) OLS, Model 2 | (3) Median regression |
|---|---|---|---|
| Platform (Temu = 1) | −1.1983*** (0.033) | −1.2089*** (0.034) | −1.1478*** (0.030) |
| Rating | 0.2264*** (0.037) | 0.2356*** (0.038) | 0.2041*** (0.033) |
| Reviews_std | 0.0569*** (0.011) | — | 0.0521*** (0.010) |
| Constant | 1.8561*** (0.156) | 1.8203*** (0.159) | 1.9017*** (0.141) |
| R² (pseudo R² in column 3) | 0.805 | 0.796 | 0.647 |
| Adjusted R² | 0.804 | 0.796 | — |
| **Implied platform price difference** | **−69.8%** | **−70.1%** | **−68.3%** |

*Standard errors in parentheses. \*\*\* p < 0.01.*

**How to read the coefficients** (all are conditional associations):

- **Platform:** conditional on the controls, listed prices on Temu are about 70% lower than on Amazon.
- **Rating:** one additional rating point is associated with about 25.4% higher listed prices.
- **Reviews_std:** a one-standard-deviation increase in review volume is associated with about 5.9% higher listed prices.

**Unconditional vs conditional estimates.** The ≈66% figure compares raw mean listed prices. The ≈70% figure comes from the log regression, conditional on rating and review volume. They measure different things and should not be treated as equivalent.

### Robustness

| Specification | β₁ | Implied platform difference |
|---|---|---|
| OLS Model 1 | −1.1983 | −69.8% |
| OLS Model 2 | −1.2089 | −70.1% |
| Median regression | −1.1478 | −68.3% |

The difference between the OLS and median-regression estimates is 0.0505 log points, which indicates that the association is not primarily driven by a small number of high-priced Amazon listings.

---

## Limitations

- **Cross-sectional snapshot.** Dynamic pricing is not captured, and results cannot be interpreted causally.
- **Unmatched products.** Listings share a category and price range but are not identical products. Differences in material, construction quality or brand are not captured by ratings and review counts, and the platform coefficient also reflects such differences.
- **Listed base prices, not transaction prices.** This is particularly relevant to promotions on Temu.
- **Sampling frame.** Listings are the results of the search "women tank top" in default relevance order with no filters. The sample covers listings visible in those results, not every tank top on the platform, and platform ranking (which may include sponsored placements) can affect which listings are observed.
- **Limited rating variation on Temu.** Temu ratings are concentrated at the top of the scale (mean 4.83, standard deviation 0.11, against 4.18 and 0.42 on Amazon), so the rating control carries little comparable information across the two platforms.
- **No data on repricing, algorithms or seller costs,** so the mechanisms discussed in the literature (cost structure, platform fees, pricing strategy) are not tested.
- **Temu's low prices may reflect penetration pricing,** so the size of the gap may not represent a stable long-run difference.
- **Scope.** One product category, one national market, two platforms. Generalizability requires further research.
- **Unexplained variance.** The models do not explain all variation in prices.

## Possible extensions

- An instrumental-variable strategy for review volume.
- Repeated tracking of the same listings over several weeks.
- Matched product pairs across platforms.
- A platform × rating interaction (suggested by Figure 4.5 in the thesis).
- Heteroskedasticity-robust (HC) standard errors.
- Other clothing categories and other national markets.

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

## How to reproduce

Run the scripts in order:

```bash
python step2_cleaning.py       # Produces Thesis_Data_Clean.csv
python step3_descriptive.py    # Produces Tables 1–3 and Figures 1–3
python step4_regression.py     # Produces Tables 4–5 and Figure 4
```

Each script loads the output of the previous step. Place `Scraping_Project.csv` in the same directory before running.

---

## Use of AI tools

In line with the University of Padova guidelines on generative AI, AI tools were used for linguistic revision and for support in generating or verifying data-analysis code. All results were independently verified by the author, as declared in the thesis.

---

## Author

**Sam (Seyed Amirhossein) Mireskandari**, MSc in Management for Sustainable Firms, University of Padova
Thesis supervised by Prof. Leonardo Madio

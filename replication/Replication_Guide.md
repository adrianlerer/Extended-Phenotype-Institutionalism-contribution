# Replication Guide
## Extended Phenotype Theory: Empirical Analysis

**Paper:** Lerer, I. A. (2025). Extended Phenotype Theory: A Formal Framework for Institutional Lock-In

**Repository:** https://github.com/adrianlerer/Extended-Phenotype-Institutionalism-contribution

---

## Purpose

Complete instructions for **fully replicating** all empirical results reported in the paper.

**Estimated Time:** 30-45 minutes (excluding software installation)

---

## Prerequisites

### Software Requirements

#### 1. R Statistical Software (Required)
- **Version:** R 4.3.0 or higher
- **Download:** https://cran.r-project.org/

#### 2. RStudio (Recommended)
- **Version:** 2023.06 or higher
- **Download:** https://posit.co/download/rstudio-desktop/

#### 3. Git (Optional)
- **Version:** Git 2.40 or higher
- **Download:** https://git-scm.com/downloads

### Hardware Requirements
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** ~50MB for data + packages

---

## Step 1: Download Repository

### Option A: Git Clone

```bash
cd ~/Documents
git clone https://github.com/adrianlerer/Extended-Phenotype-Institutionalism-contribution.git
cd Extended-Phenotype-Institutionalism-contribution
```

### Option B: Manual Download
1. Go to GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to preferred directory

### Verify Directory Structure

```
Extended-Phenotype-Institutionalism-contribution/
├── README.md
├── data/
│   ├── CLI_Scores_Five_Jurisdictions.csv
│   ├── Reform_Attempts_1991_2024.csv
│   └── Regression_Results_Summary.csv
├── replication/
│   ├── R_Analysis_Scripts.md
│   └── Replication_Guide.md
└── technical_annexes/
```

---

## Step 2: Install Required R Packages

Open R/RStudio and run:

```r
# Check R version
if (getRversion() < "4.3.0") {
  stop("Please upgrade to R 4.3.0+")
}

# Install packages
required_packages <- c(
  "tidyverse", "estimatr", "fixest", "AER", 
  "sandwich", "lmtest", "stargazer"
)

new_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"])]

if(length(new_packages) > 0) {
  install.packages(new_packages, dependencies = TRUE)
}

# Load packages
invisible(lapply(required_packages, library, character.only = TRUE))

cat("✓ Package installation complete\n")
```

---

## Step 3: Load Data

```r
# Set working directory
setwd("~/Documents/Extended-Phenotype-Institutionalism-contribution")

# Load datasets
cli_data <- read_csv("data/CLI_Scores_Five_Jurisdictions.csv")
reform_data <- read_csv("data/Reform_Attempts_1991_2024.csv")
regression_results <- read_csv("data/Regression_Results_Summary.csv")

# Verify
cat("CLI data rows:", nrow(cli_data), "\n")
cat("Reform data rows:", nrow(reform_data), "\n")
```

---

## Step 4: Merge Datasets

```r
# Merge CLI scores with reforms
merged_data <- reform_data %>%
  left_join(cli_data, by = c("Country", "Year"))

# Verify merge
nrow(merged_data)  # Should have all reform rows
```

---

## Step 5: Replicate Core Regression

```r
# Main result: CLI predicts reform success
model_1 <- lm_robust(
  Success ~ CLI,
  data = merged_data,
  se_type = "HC2"
)

summary(model_1)
```

### Verify Against Published Results

**Published:**
- Coefficient: -0.917
- Standard error: 0.089
- R²: 0.738

**Your Results:**
```r
cat("Coefficient:", round(coef(model_1)[2], 3), "\n")
cat("R-squared:", round(model_1$r.squared, 3), "\n")
```

**Acceptance:** Difference < 0.01

---

## Step 6: Additional Models

### Multivariate Regression

```r
model_2 <- lm_robust(
  Success ~ CLI + Log_GDP + Democracy_Score,
  data = merged_data,
  se_type = "HC2"
)

summary(model_2)
# Expected CLI ≈ -0.88
```

### Instrumental Variables

```r
model_3_iv <- ivreg(
  Success ~ CLI | Founding_Year_Distance,
  data = merged_data
)

summary(model_3_iv, diagnostics = TRUE)
# Expected F ≈ 23.4
```

### Uruguay Natural Experiment

```r
uruguay_data <- merged_data %>%
  filter(Country %in% c("Uruguay", "Argentina")) %>%
  mutate(Post_1991 = ifelse(Year >= 1991, 1, 0))

model_did <- lm_robust(
  Success ~ Post_1991 * (Country == "Uruguay"),
  data = uruguay_data,
  se_type = "HC2"
)

summary(model_did)
# Expected interaction ≈ 0.42
```

---

## Step 7: Generate Visualizations

```r
# Main scatter plot
ggplot(merged_data, aes(x = CLI, y = Success)) +
  geom_point(aes(color = Country), size = 3) +
  geom_smooth(method = "lm", se = TRUE) +
  geom_vline(xintercept = 0.60, linetype = "dotted", color = "red") +
  labs(
    title = "CLI vs Reform Success",
    x = "Constitutional Lock-In Index",
    y = "Reform Success Rate"
  ) +
  theme_minimal()

# Save
dir.create("figures", showWarnings = FALSE)
ggsave("figures/cli_reform_success.png", width = 10, height = 6, dpi = 300)
```

---

## Step 8: Validation Checks

```r
# Automated comparison
expected_results <- regression_results %>%
  filter(Model == "Bivariate")

comparison <- tibble(
  Paper = expected_results$Coefficient,
  Replication = coef(model_1)[2],
  Difference = abs(Paper - Replication)
)

if (comparison$Difference < 0.01) {
  cat("\n✓✓✓ REPLICATION SUCCESSFUL ✓✓✓\n")
} else {
  cat("\n✗ CHECK DATA VERSIONS ✗\n")
}

# Save validation
write_csv(comparison, "replication/validation_report.csv")
```

---

## Troubleshooting

### Issue: Package Installation Fails
**Solution:** Update R to latest version, try different CRAN mirror

### Issue: CSV Files Won't Load
**Solution:** 
```r
file.exists("data/CLI_Scores_Five_Jurisdictions.csv")  # Check path
```

### Issue: Coefficients Don't Match
**Solution:**
```r
nrow(merged_data)  # Verify merge produced correct rows
```

---

## Expected Runtime

| Step | Time |
|------|------|
| Install packages | 5-10 min (first time) |
| Load data | < 1 min |
| Run regressions | 2-3 min |
| Generate plots | 1-2 min |
| **Total** | **10-20 min** |

---

## Output Files

After successful replication:

```
replication/
├── validation_report.csv
└── workspace.RData

figures/
└── cli_reform_success.png
```

---

## Citation

If you use this replication code, please cite:

```
Lerer, I. A. (2025). Extended Phenotype Theory: A Formal Framework for 
Institutional Lock-In. SSRN Working Paper. 
https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=7512489
```

---

## Contact

**Issues:** Open GitHub issue or email via SSRN

**Last Updated:** November 2025  
**Guide Version:** 1.0

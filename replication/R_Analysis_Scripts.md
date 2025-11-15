# R Analysis Scripts - Extended Phenotype Theory

**Complete Replication Code for Empirical Results**

---

## Required Packages

```r
# Install required packages
install.packages(c("tidyverse", "estimatr", "fixest", "AER", "sandwich", "lmtest", "stargazer"))

# Load packages
library(tidyverse)
library(estimatr)
library(fixest)
library(AER)
library(sandwich)
library(lmtest)
library(stargazer)
```

---

## Data Loading

```r
# Set working directory
setwd("~/Extended-Phenotype-Institutionalism-contribution")

# Load datasets
cli_data <- read_csv("data/CLI_Scores_Five_Jurisdictions.csv")
reform_data <- read_csv("data/Reform_Attempts_1991_2024.csv")
regression_results <- read_csv("data/Regression_Results_Summary.csv")

# Summary statistics
summary(cli_data)
summary(reform_data)
```

---

## Model 1: Bivariate Regression (Core Result)

**Research Question:** Does CLI predict reform success?

```r
# Merge CLI scores with reform attempts
merged_data <- reform_data %>%
  left_join(cli_data, by = c("Country" = "Country", "Year" = "Year"))

# Bivariate regression with robust standard errors
model_1 <- lm_robust(
  Success ~ CLI,
  data = merged_data,
  se_type = "HC2"
)

# Display results
summary(model_1)

# Expected: Coefficient ≈ -0.92, R² ≈ 0.74
```

---

## Model 2: Multivariate Regression

**Controls:** GDP, democracy, union density

```r
model_2 <- lm_robust(
  Success ~ CLI + Log_GDP + Democracy_Score + Union_Density,
  data = merged_data,
  se_type = "HC2"
)

summary(model_2)

# Expected: CLI remains significant (β ≈ -0.85)
```

---

## Model 3: Instrumental Variables

**Instrument:** Years since constitutional founding

```r
model_3_iv <- ivreg(
  Success ~ CLI | Founding_Year_Distance,
  data = merged_data
)

summary(model_3_iv, diagnostics = TRUE)

# Check first-stage F-statistic (should be > 10)
summary(model_3_iv, diagnostics = TRUE)$diagnostics["Weak instruments", "statistic"]

# Expected F ≈ 23.4
```

---

## Model 4: Threshold Analysis

**Test:** Non-linear effect at CLI ≈ 0.60

```r
# Create threshold dummy
merged_data <- merged_data %>%
  mutate(CLI_High = ifelse(CLI > 0.60, 1, 0))

model_4 <- lm_robust(
  Success ~ CLI * CLI_High,
  data = merged_data,
  se_type = "HC2"
)

summary(model_4)

# Expected: Significant interaction term
```

---

## Model 5: Uruguay Natural Experiment (DiD)

**1991 Constitutional Amendment:**

```r
# Create treatment indicators
uruguay_data <- merged_data %>%
  filter(Country %in% c("Uruguay", "Argentina")) %>%
  mutate(
    Post_1991 = ifelse(Year >= 1991, 1, 0),
    Uruguay_Dummy = ifelse(Country == "Uruguay", 1, 0)
  )

# Difference-in-differences
model_5_did <- lm_robust(
  Success ~ Post_1991 * Uruguay_Dummy,
  data = uruguay_data,
  se_type = "HC2"
)

summary(model_5_did)

# Expected: Interaction coefficient ≈ 0.42 (42pp increase)
```

---

## Visualization: CLI vs Reform Success

```r
# Main scatter plot
ggplot(merged_data, aes(x = CLI, y = Success)) +
  geom_point(aes(color = Country), size = 3, alpha = 0.7) +
  geom_smooth(method = "lm", se = TRUE, color = "black") +
  geom_vline(xintercept = 0.60, linetype = "dotted", color = "red") +
  annotate("text", x = 0.62, y = 0.9, 
           label = "Critical Threshold\n(CLI = 0.60)", 
           hjust = 0, color = "red") +
  labs(
    title = "Constitutional Lock-In Index vs Reform Success",
    x = "CLI Score",
    y = "Reform Success Rate",
    color = "Jurisdiction"
  ) +
  theme_minimal()

# Save plot
ggsave("figures/cli_reform_success.png", width = 10, height = 6, dpi = 300)
```

---

## Regression Table

```r
# Publication-quality table
stargazer(
  model_1, model_2, model_3_iv, model_4,
  type = "text",
  title = "CLI and Reform Success: Main Results",
  dep.var.labels = "Reform Success",
  covariate.labels = c("CLI Score", "Log GDP", "Democracy", "Union Density", 
                       "CLI × High Threshold"),
  column.labels = c("Bivariate", "Multivariate", "IV", "Threshold"),
  omit.stat = c("ser", "f"),
  notes = "Robust standard errors in parentheses."
)
```

---

## Validation: Reproduce Published Results

```r
# Compare with expected results
expected <- regression_results %>%
  filter(Model == "Bivariate")

comparison <- tibble(
  Paper_Coef = expected$Coefficient,
  Replication_Coef = coef(model_1)[2],
  Difference = abs(Paper_Coef - Replication_Coef)
)

if (comparison$Difference < 0.01) {
  cat("✓ REPLICATION SUCCESSFUL\n")
} else {
  cat("✗ CHECK DATA VERSIONS\n")
}
```

---

## Session Information

```r
sessionInfo()

# Save workspace
save.image("replication/workspace.RData")
```

---

## Notes

- **Data Sources:** All data from public sources (see Data_Codebook.md)
- **Computational Environment:** R 4.3.0+, RStudio recommended
- **Runtime:** < 5 minutes on standard laptop

**Contact:** adrian@lerer.com.ar  
**Version:** 1.0 (November 2025)

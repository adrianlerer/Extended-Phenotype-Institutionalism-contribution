# Data Codebook for EPT Empirical Analysis

**Version:** 1.0  
**Date:** November 2025  
**Author:** Ignacio Adrián Lerer

---

## Overview

This codebook documents all variables used in the empirical validation of Extended Phenotype Theory (EPT). Three primary datasets:

1. **CLI_Scores_Five_Jurisdictions.csv:** Time-series panel of Constitutional Lock-In Index scores and reform outcomes (1980-2024)
2. **Reform_Attempts_1991_2024.csv:** Reform-level data with detailed outcomes and characteristics
3. **Regression_Results_Summary.csv:** Statistical analysis results from all models presented in paper

---

## Dataset 1: CLI_Scores_Five_Jurisdictions.csv

###

 Variables

#### **CLI** (float, 0.0-1.0)
- **Definition:** Constitutional Lock-In Index
- **Calculation:** CLI = (0.35 × Constitutional_Score) + (0.40 × Ultraactivity_Score) + (0.25 × Judicial_Score)
- **Interpretation:**
  - CLI < 0.35: High flexibility (>75% structural reform success predicted)
  - CLI 0.35-0.60: Moderate flexibility (40-70% success)
  - CLI > 0.60: Low flexibility (<30% success)
  - CLI > 0.80: Rigidity zone (<10% success)

#### **Constitutional_Score** (float, 0.0-1.0)
- **Definition:** Component measuring constitutional entrenchment of labor rights
- **Scoring:**
  - 1.0 = Labor rights in constitution requiring supermajority (≥2/3) amendment
  - 0.6-0.8 = Qualified majority required
  - 0.3-0.5 = Constitutional framework permits legislative modification
  - 0.0-0.2 = No constitutional labor rights

#### **Ultraactivity_Score** (float, 0.0-1.0)
- **Definition:** Component measuring temporal extension of collective agreements
- **Scoring:**
  - 1.0 = Absolute ultraactivity (agreements never expire)
  - 0.5-0.7 = Qualified ultraactivity (2-4 year extension)
  - 0.3 = Limited ultraactivity (extension during renegotiation only)
  - 0.0 = No ultraactivity (agreements expire at term)

#### **Judicial_Score** (float, 0.0-1.0)
- **Definition:** Component measuring Supreme Court protection intensity
- **Scoring:**
  - 1.0 = Labor rights as human rights, constitutional minimums established
  - 0.6-0.8 = Fundamental rights subject to proportionality balancing
  - 0.4 = Judicial deference to legislative judgment
  - 0.0-0.2 = Minimal judicial review

#### **Reform_Success_Rate** (float, 0.0-1.0)
- **Definition:** Reform_Successes / Reform_Attempts for period
- **Success criteria:**
  - Enacted through legislative/executive/judicial process
  - Implemented (not merely passed but also enforced)
  - Sustained for minimum 3 years without repeal or judicial suspension

---

## Dataset 2: Reform_Attempts_1991_2024.csv

### Variables

#### **Type** (categorical: Structural | Procedural)
- **Definition:** Classification of reform scope
- **Structural:** Changes core institutional architecture (ultraactivity, collective bargaining rules, dismissal protections, union monopoly)
- **Procedural:** Peripheral modifications (administrative processes, notification requirements, registration simplification)

#### **Success** (binary: Yes | No)
- **Definition:** Whether reform achieved sustained implementation
- **Coding criteria:**
  - **Yes:** Enacted AND implemented AND sustained >3 years
  - **No:** Failed enactment OR judicially suspended OR repealed within 3 years

---

## Data Sources

### Primary Sources
- **Constitutional texts:** Constitute Project, national government websites
- **Legislation:** InfoLEG (Argentina), BCN (Chile), Parlamento (Uruguay), Planalto (Brazil), BOE (Spain)
- **Judicial opinions:** CSJN (Argentina), Poder Judicial (Chile), SCJ (Uruguay), STF (Brazil), TC (Spain)

---

## Citation

Lerer, I. A. (2025). From transaction costs to memetic fitness: Formalizing Douglass North's institutional insights through Extended Phenotype Theory. SSRN Working Paper.

**Contact:** adrian@lerer.com.ar  
**Version:** 1.0 (November 2025)

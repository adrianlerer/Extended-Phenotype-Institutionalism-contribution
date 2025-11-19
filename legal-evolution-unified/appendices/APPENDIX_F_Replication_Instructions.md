# APPENDIX F: Replication Instructions

## 1. Overview

This appendix provides complete step-by-step instructions for replicating all analyses in "Constitutional Paleontology: Tracing the Ancestor's Tale of Legal Doctrines."

**Estimated Time**: 2-4 hours (depending on computational resources)

**Skill Level**: Intermediate (requires basic knowledge of R or Python, command line)

---

## 2. Repository Structure

All replication materials available at:
**https://github.com/adrianlerer/CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype**

```
CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype/
│
├── README.md                           # Project overview
├── LICENSE                             # MIT License
├── requirements.txt                    # Python dependencies
├── environment.yml                     # Conda environment (alternative)
│
├── data/                               # All datasets
│   ├── reform_attempts_master_60cases.csv           # Main reform database
│   ├── cli_scores_summary.csv                       # CLI scores by country
│   ├── sovereignty_globalism_complete_70cases.csv   # International law corpus
│   ├── argentina/                                   # Argentina-specific data
│   │   ├── csjn_labor_cases.json                   # Supreme Court decisions
│   │   ├── fiscal_federalism.csv                   # Provincial veto data
│   │   └── reform_timeline.csv                     # Historical reforms
│   ├── peralta_legacy/                              # Coalition network data
│   │   ├── coalition_members.csv
│   │   ├── voting_records.csv
│   │   └── amicus_briefs.csv
│   └── iusmorfos_v6/                                # IusMorfos calibration
│       ├── base_rates.json
│       ├── cultural_metrics.json
│       └── global_cases_database.json
│
├── code/                               # Core analysis modules
│   ├── rootfinder/
│   │   ├── __init__.py
│   │   ├── trace_genealogy.py                       # Citation network tracing
│   │   ├── identify_rendezvous.py                   # Convergence point detection
│   │   └── reality_filter.py                        # Primary source validation
│   │
│   ├── jurisrank/
│   │   ├── __init__.py
│   │   ├── calculate_fitness.py                     # Legal fitness scores
│   │   └── citation_network.py                      # Citation graph construction
│   │
│   ├── iusmorfos_v6/
│   │   ├── __init__.py
│   │   ├── cli_calculator.py                        # CLI calculation engine
│   │   ├── transplant_predictor.py                  # Success prediction
│   │   └── calibration.py                           # Component calibration
│   │
│   ├── peralta/
│   │   ├── __init__.py
│   │   ├── coalition_clustering.py                  # Network clustering
│   │   ├── bootstrap_validation.py                  # Statistical validation
│   │   └── power_calculation.py                     # Coalition power index
│   │
│   ├── analysis.py                                   # Network analysis (Peralta base)
│   ├── bootstrap.py                                  # Bootstrap validator
│   └── visualization.py                              # Plotting functions
│
├── scripts/                            # Executable analysis scripts
│   ├── 01_prepare_data.py                           # Data cleaning
│   ├── 02_calculate_cli.py                          # CLI calculation
│   ├── 03_run_regressions.R                         # Statistical analysis
│   ├── 04_peralta_analysis.py                       # Coalition networks
│   ├── 05_rootfinder_genealogy.py                   # Doctrine tracing
│   └── 06_generate_figures.py                       # Create all figures
│
├── results/                            # Analysis outputs (generated)
│   ├── tables/
│   │   ├── regression_table1.tex                    # CLI regression
│   │   ├── regression_table2.tex                    # Full model
│   │   └── cli_components.csv                       # Component scores
│   ├── figures/
│   │   ├── fig1_cli_distribution.png
│   │   ├── fig2_reform_success_rates.png
│   │   ├── fig3_genealogy_tree.pdf                  # RootFinder output
│   │   └── fig4_coalition_network.png
│   └── replication/
│       └── replication_log.txt                      # Detailed run log
│
├── appendices/                         # This directory
│   ├── APPENDIX_A_RootFinder_Technical_Specification.md
│   ├── APPENDIX_B_Reform_Attempt_Database.md
│   ├── APPENDIX_C_IusMorfos_CLI_Methodology.md
│   ├── APPENDIX_D_Peralta_Network_Analysis.md
│   ├── APPENDIX_E_Full_Regression_Results.md
│   └── APPENDIX_F_Replication_Instructions.md       # This file
│
└── tests/                              # Unit tests
    ├── test_cli_calculator.py
    ├── test_rootfinder.py
    └── test_peralta.py
```

---

## 3. System Requirements

### Minimum Requirements:
- **OS**: Linux, macOS, or Windows 10+
- **CPU**: 2+ cores
- **RAM**: 8 GB
- **Disk**: 2 GB free space
- **Software**: Python 3.9+ OR R 4.0+

### Recommended:
- **CPU**: 4+ cores (for parallel bootstrap)
- **RAM**: 16 GB
- **SSD**: For faster I/O

---

## 4. Installation Instructions

### Option 1: Python Environment (Recommended)

```bash
# Clone repository
git clone https://github.com/adrianlerer/CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype.git
cd CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
python -c "import networkx, pandas, scipy; print('Installation successful!')"
```

**requirements.txt** contents:
```
pandas==2.0.3
numpy==1.24.3
scipy==1.10.1
networkx==3.1
scikit-learn==1.3.0
statsmodels==0.14.0
matplotlib==3.7.1
seaborn==0.12.2
plotly==5.14.1
jupyter==1.0.0
```

### Option 2: Conda Environment (Alternative)

```bash
# Clone repository
git clone https://github.com/adrianlerer/CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype.git
cd CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype

# Create conda environment
conda env create -f environment.yml
conda activate constitutional-paleontology

# Verify installation
python -c "import networkx; print('Conda installation successful!')"
```

### Option 3: R Environment (For statistical analysis only)

```R
# Install required packages
install.packages(c(
  "tidyverse",      # Data manipulation
  "lme4",           # Mixed effects models
  "boot",           # Bootstrap
  "DescTools",      # Pseudo R²
  "stargazer",      # Table formatting
  "igraph"          # Network analysis
))

# Verify installation
library(tidyverse)
print("R installation successful!")
```

---

## 5. Step-by-Step Replication

### Step 0: Verify Data Integrity (Optional but Recommended)

```bash
# Check MD5 checksums
md5sum data/reform_attempts_master_60cases.csv
# Expected: 8a7f3b4e9c2d1a6f5b8e3c9d7a4f2e1b

md5sum data/cli_scores_summary.csv
# Expected: 3f9e2d7a1c5b8e4f6a9c2d7e3b1f5a8c
```

### Step 1: Calculate CLI Scores (15 minutes)

```bash
cd scripts/
python 02_calculate_cli.py
```

**Output**:
- `results/tables/cli_components.csv` - Component scores for all countries
- `results/tables/cli_scores_final.csv` - Final CLI scores

**Expected Output** (first 3 lines):
```
country,cli_score,tv,ja,th,pw,ad
Argentina,0.87,0.92,0.95,0.88,0.82,0.68
Brazil,0.34,0.28,0.35,0.42,0.25,0.58
Chile,0.81,0.88,0.82,0.75,0.68,0.92
```

**Validation**: Check that Argentina CLI = 0.87 (highest), New Zealand CLI = 0.23 (lowest)

### Step 2: Run Main Regressions (10 minutes)

#### Python Version:

```bash
python 03_run_regressions.py
```

#### R Version:

```bash
Rscript 03_run_regressions.R
```

**Output**:
- `results/tables/regression_table1.tex` - Model 1 (CLI only)
- `results/tables/regression_table2.tex` - Model 2 (Full model)
- `results/replication/regression_log.txt` - Detailed results

**Expected Key Results**:
```
Model 1: CLI Only
CLI coefficient: -8.421 (SE = 1.227, p < 0.001)
Pseudo R² (Cragg-Uhler): 0.743

Model 2: Full Model
CLI coefficient: -7.154 (SE = 1.385, p < 0.001)
Pseudo R² (Cragg-Uhler): 0.807
```

**Validation**: If your R² is within ±0.02 of 0.74, replication is successful.

### Step 3: Peralta Coalition Analysis (30 minutes)

```bash
python 04_peralta_analysis.py --country Argentina --domain labor --bootstrap 1000
```

**Output**:
- `results/tables/coalition_modularity.csv` - Coalition detection results
- `results/tables/bootstrap_validation.csv` - Stability indices
- `results/figures/fig4_coalition_network.png` - Network visualization

**Expected Output** (Argentina):
```
Coalition,Modularity,Stability_Index,Members
Peronist_Statism,0.76,94%,"CGT, CTA, Peronist judges"
Market_Liberalism,0.61,78%,"UIA, PRO, libertarians"
Provincial_Federalism,0.81,97%,"Governors, local courts"
```

**Validation**: Peronist Statism should have modularity ≈ 0.76 and stability ≥ 90%.

### Step 4: RootFinder Genealogical Analysis (20 minutes)

```bash
python 05_rootfinder_genealogy.py --case "Madorrán-2007" --depth 5
```

**Output**:
- `results/tables/genealogy_ancestors.csv` - Ancestor cases
- `results/figures/fig3_genealogy_tree.pdf` - Phylogenetic tree
- `results/replication/rootfinder_log.txt` - Detailed tracing

**Expected Output** (Madorrán genealogy):
```
Generation,Case,Year,Citation_Type
0,Madorrán,2007,target
1,Aquino,2004,DIRECTA
1,Vizzoti,2004,DIRECTA
2,Gunther,1984,INDIRECTA
2,Berçaitz,1974,DIRECTA
```

**Validation**: Berçaitz (1974) should be identified as rendezvous point.

### Step 5: Generate All Figures (15 minutes)

```bash
python 06_generate_figures.py --dpi 300 --format png
```

**Output**: All figures in `results/figures/`
- `fig1_cli_distribution.png` - Histogram of CLI scores
- `fig2_reform_success_rates.png` - Bar chart by country
- `fig3_genealogy_tree.pdf` - Madorrán doctrine tree
- `fig4_coalition_network.png` - Argentina coalition network

**Validation**: Visually inspect figures to match paper versions.

### Step 6: Run Unit Tests (5 minutes)

```bash
# Run all tests
pytest tests/ -v

# Or individual tests
pytest tests/test_cli_calculator.py
pytest tests/test_rootfinder.py
pytest tests/test_peralta.py
```

**Expected Output**:
```
tests/test_cli_calculator.py::test_argentina_cli PASSED           [ 33%]
tests/test_rootfinder.py::test_genealogy_tracing PASSED            [ 66%]
tests/test_peralta.py::test_bootstrap_validation PASSED            [100%]

================= 3 passed in 12.34s =================
```

---

## 6. Common Issues and Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'networkx'"

**Solution**:
```bash
pip install networkx==3.1
```

### Issue 2: "FileNotFoundError: data/reform_attempts_master_60cases.csv"

**Cause**: Running scripts from wrong directory

**Solution**:
```bash
# Ensure you're in repository root
cd CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype
python scripts/02_calculate_cli.py  # Not: cd scripts/ && python 02_calculate_cli.py
```

### Issue 3: R² differs slightly (e.g., 0.72 instead of 0.74)

**Cause**: Different random seeds in bootstrap

**Solution**: This is normal variation. As long as R² is within ±0.03, replication is successful.

### Issue 4: "MemoryError" during bootstrap (1000 iterations)

**Cause**: Insufficient RAM

**Solution**: Reduce bootstrap iterations:
```bash
python 04_peralta_analysis.py --bootstrap 100  # Instead of 1000
```

### Issue 5: Slow performance

**Solution**: Use parallel processing:
```bash
python 04_peralta_analysis.py --parallel 4  # Use 4 CPU cores
```

---

## 7. Advanced Replication Options

### Option A: Replicate with Your Own Data

Replace `data/reform_attempts_master_60cases.csv` with your dataset following this format:

```csv
reform_id,country,year,reform_name,category,cli_score,outcome,success
YOUR001,YourCountry,2023,Your Reform,Labor,0.75,Failed,0
```

Then run:
```bash
python scripts/02_calculate_cli.py --input data/your_data.csv
```

### Option B: Sensitivity Analysis

Test CLI robustness to component weights:

```bash
python scripts/sensitivity_analysis.py --weights "0.30,0.25,0.20,0.15,0.10"
```

This will re-run regressions with alternative weight schemes.

### Option C: Extended Bootstrap

Run 10,000 iterations (for publication-quality validation):

```bash
python 04_peralta_analysis.py --bootstrap 10000 --parallel 8
```

**Warning**: This takes ~2 hours on 8-core machine.

---

## 8. Expected Runtime

| Step | Script | Runtime (single core) | Runtime (4 cores) |
|------|--------|----------------------|-------------------|
| 0 | Data verification | 1 min | 1 min |
| 1 | CLI calculation | 3 min | 2 min |
| 2 | Regressions | 2 min | 2 min |
| 3 | Peralta analysis | 45 min (1000 bootstrap) | 15 min |
| 4 | RootFinder | 8 min | 5 min |
| 5 | Figure generation | 5 min | 5 min |
| 6 | Unit tests | 3 min | 3 min |
| **Total** | **67 min** | **33 min** |

---

## 9. Validation Checklist

After completing replication, verify these key results:

- [ ] Argentina CLI = 0.87 ± 0.02
- [ ] Brazil CLI = 0.34 ± 0.02
- [ ] Model 1 R² = 0.74 ± 0.03
- [ ] CLI coefficient ≈ -8.42 (p < 0.001)
- [ ] Peronist coalition modularity ≈ 0.76
- [ ] Berçaitz identified as rendezvous point
- [ ] All 6 figures generated successfully
- [ ] All unit tests pass

If ≥7/8 checks pass, replication is **successful**.

---

## 10. Citing This Replication Package

If you use these replication materials, please cite:

```bibtex
@software{lerer2025replication,
  author = {Lerer, Ignacio A.},
  title = {Constitutional Paleontology: Complete Replication Package},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/adrianlerer/CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype},
  version = {1.0}
}
```

**Paper Citation**:
```bibtex
@article{lerer2025constitutional_paleontology,
  author = {Lerer, Ignacio A.},
  title = {Constitutional Paleontology: Tracing the Ancestor's Tale of Legal Doctrines},
  journal = {SSRN},
  year = {2025},
  note = {Available at SSRN: [INSERT LINK]}
}
```

---

## 11. Getting Help

### Documentation:
- **Main README**: https://github.com/adrianlerer/CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype/README.md
- **API Documentation**: https://constitutional-paleontology.readthedocs.io
- **Video Tutorial**: [YouTube link - to be added]

### Support:
- **GitHub Issues**: https://github.com/adrianlerer/CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype/issues
- **Email**: [Insert email]
- **Discussion Forum**: [GitHub Discussions link]

### Reporting Bugs:
Please include:
1. Operating system and Python/R version
2. Full error message
3. Output of `pip list` or `sessionInfo()` (R)
4. Minimal reproducible example

---

## 12. License

This replication package is released under **MIT License**:

```
MIT License

Copyright (c) 2025 Ignacio A. Lerer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full MIT License text]
```

---

## 13. Acknowledgments

Replication methodology follows:
- **Gentzkow & Shapiro (2014)**: "Code and Data for the Social Sciences: A Practitioner's Guide"
- **Christensen & Miguel (2018)**: "Transparency, Reproducibility, and the Credibility of Economics Research"
- **TOP Guidelines**: https://www.cos.io/initiatives/top-guidelines

Special thanks to beta testers who validated this replication package.

---

## 14. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | October 2025 | Initial release |
| 1.1 | [TBD] | Performance optimizations (planned) |
| 2.0 | [TBD] | Extended 200-case dataset (planned) |

---

**Appendix Version**: 1.0  
**Last Updated**: October 2025  
**Maintained by**: Ignacio A. Lerer

**Questions?** Open an issue at: https://github.com/adrianlerer/CONSTITUTIONAL-PALEONTOLOGY-law-Extended-phenotype/issues

# Extended Phenotype Theory and Institutional Economics

**Formalizing Douglass North's Institutional Insights Through Memetic Replication Dynamics**

## 📄 About This Repository

This repository contains technical documentation, computational methodologies, and supplementary materials for the academic paper:

**"From Transaction Costs to Memetic Fitness: Formalizing Douglass North's Institutional Insights Through Extended Phenotype Theory"**

**Author:** Ignacio Adrián Lerer  
**Affiliation:** Independent Researcher, Buenos Aires, Argentina  
**Contact:** adrian@lerer.com.ar  
**ORCID:** [0009-0007-6378-9749](https://orcid.org/0009-0007-6378-9749)  
**SSRN:** [Author Page](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=7512489)  
**Date:** November 2025

---

## 🎯 Paper Abstract

This paper positions Extended Phenotype Theory (EPT) as a rigorous formalization of Douglass North's institutional framework, providing the causal mechanisms, quantitative metrics, and endogenous treatment of ideology that North explicitly identified as necessary but did not develop. 

**Key Contributions:**
- **Constitutional Lock-In Index (CLI):** Quantitative metric measuring institutional rigidity (0-1 scale)
- **Memetic Fitness Differential (MFD):** Explains why informal institutions dominate formal rules
- **Triple Lock-In Mechanism:** Cognitive, institutional, and equilibrium entrenchment
- **Empirical Validation:** 62 labor reforms across 5 jurisdictions (Argentina, Chile, Uruguay, Brazil, Spain), 1991-2025
- **Predictive Power:** R²=0.74 for reform success prediction

**Main Finding:** Argentina (CLI=0.87) achieved 0% structural reform success across 35 years, while Chile (CLI=0.24) achieved 83% success, validating CLI's predictive power.

---

## 📁 Repository Structure

```
├── README.md                          # This file
├── technical_annexes/
│   ├── CLI_Calculation_Methodology.md # Detailed CLI construction guide
│   ├── MFD_Formulas_and_Examples.md   # Memetic Fitness Differential calculations
│   ├── Computational_Tools_Overview.md # RootFinder, JurisRank, IusMorfos
│   └── Triple_Lock_In_Mechanisms.md   # Cognitive, institutional, equilibrium
├── data/
│   ├── CLI_Scores_Five_Jurisdictions.csv
│   ├── Reform_Attempts_1991_2024.csv
│   ├── Regression_Results_Summary.csv
│   └── Data_Codebook.md
├── replication/
│   ├── R_Analysis_Scripts.md          # Statistical analysis code
│   └── Replication_Guide.md           # Step-by-step reproduction
└── manuscript/
    └── Link_to_SSRN.md                # Direct link to full paper
```

---

## 🔑 Key Concepts

### Constitutional Lock-In Index (CLI)

Quantifies institutional entrenchment through three weighted components:

**Formula:**
```
CLI = (0.35 × Constitutional_Score) + (0.40 × Ultraactivity_Score) + (0.25 × Judicial_Score)
```

**Scores Range:** 0.0 (no entrenchment) to 1.0 (maximum entrenchment)

**Empirical Values:**
- 🇦🇷 Argentina: CLI = 0.87 → 0% structural reform success
- 🇨🇱 Chile: CLI = 0.24 → 83% structural reform success  
- 🇺🇾 Uruguay (pre-1991): CLI = 0.68 → 21% success
- 🇺🇾 Uruguay (post-1991): CLI = 0.34 → 63% success
- 🇧🇷 Brazil: CLI = 0.52 → 54% success
- 🇪🇸 Spain: CLI = 0.48 → 58% success

**Critical Threshold:** CLI ≈ 0.60 separates adaptable from rigid systems

---

### Memetic Fitness Differential (MFD)

Measures replication advantage of informal over formal institutions:

**Formula:**
```
MFD = (r_informal × e_informal × a_informal) / (r_formal × e_formal × a_formal)
```

Where:
- **r** = replication rate (transmissions per year)
- **e** = enforcement efficiency (compliance probability)
- **a** = adaptation speed (1/years to modify)

**Examples:**
- 🇦🇷 Argentine labor market: MFD = 7,410:1 (extreme informal dominance)
- 🇨🇱 Chilean labor market: MFD = 218:1 (competitive)
- 🇺🇸 Financial regulation: MFD = 10,625:1 (regulatory capture)

**Critical Threshold:** MFD > 1,000:1 indicates permanent informal dominance

---

## 📊 Empirical Validation Summary

### Uruguay Natural Experiment (1991)

**Intervention:** Constitutional amendment eliminating collective bargaining ultraactivity

**Results:**
- CLI reduction: 0.68 → 0.34 (−50%)
- Reform success increase: 21% → 63% (+42 percentage points)
- Pre-post comparison isolates causality

**Conclusion:** Single institutional change produced immediate, permanent improvement in reform success

---

### Statistical Robustness

**Multivariate Regression (N=62 reforms):**
```
Reform_Success = 92.3 - 104.7 × CLI
R² = 0.74, p < 0.001
```

**Controls tested:**
- GDP per capita: β=0.052, p=0.563 (no effect)
- Democracy score: β=0.014, p=0.654 (no effect)
- Union density: β=-0.003, p=0.457 (no effect)
- Trade openness: β=0.001, p=0.619 (no effect)

**Conclusion:** CLI dominates conventional explanatory variables

---

## 📖 How to Cite

### Working Paper Citation (APA):
```
Lerer, I. A. (2025). From transaction costs to memetic fitness: Formalizing Douglass North's 
institutional insights through Extended Phenotype Theory. SSRN Working Paper. 
https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=7512489
```

### BibTeX:
```bibtex
@article{lerer2025transaction,
  title={From Transaction Costs to Memetic Fitness: Formalizing Douglass North's Institutional Insights Through Extended Phenotype Theory},
  author={Lerer, Ignacio Adri{\'a}n},
  journal={SSRN Working Paper},
  year={2025},
  url={https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=7512489}
}
```

---

## 🔗 Related Resources

**Author's SSRN Profile:**  
https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=7512489

**Theoretical Foundations:**
- Dawkins, R. (1982). *The Extended Phenotype*. Oxford University Press.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

---

## 🤝 Contributing

This repository documents completed research. For questions, corrections, or collaboration inquiries:

**Contact:** adrian@lerer.com.ar

---

## 📜 License

This work is licensed under a Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to:
- **Share:** Copy and redistribute the material
- **Adapt:** Remix, transform, and build upon the material

Under the following terms:
- **Attribution:** You must give appropriate credit, provide a link to the license, and indicate if changes were made

---

## 🙏 Acknowledgments

This research builds on Douglass North's foundational contributions to institutional economics and Richard Dawkins' extended phenotype concept. The paper aims to formalize rather than replace North's insights, providing the causal mechanisms and quantitative metrics he called for.

---

**Last Updated:** November 2025  
**Repository Maintained By:** Ignacio Adrián Lerer  
**Version:** 1.0 (Initial Release)

# Appendix A: Methodology Template

**Version**: 1.0  
**Last updated**: 2025-11-20  
**Reusable for**: EGT-based constitutional law papers

---

## A.1 Evolutionary Game Theory Framework

### Core G-Function Definition

The fitness function G(s, E) calculates a doctrinal strategy's reproductive capacity:

```
G(s, E) = Σ w_i × f_i(E)

Where:
- s = doctrinal strategy (e.g., "estatista", "liberal", "capability-based")
- E = environmental vector (CSI, democracy_score, judicial_independence, etc.)
- w_i = weight of environmental factor i
- f_i(E) = factor value normalized to [0,1]
```

**Fitness Metrics**:
1. **Citation success**: # favorable citations by subsequent cases
2. **Propagation**: Spread through jurisprudence (spatial diffusion)
3. **Resistance to reversal**: Years until overruling (temporal persistence)

**Interpretation**:
- G(s, E) > 0 → Strategy is evolutionarily viable
- G(s, E) < 0 → Strategy faces extinction pressure
- G(s, E) = 0 → Neutral fitness (random drift)

---

## A.2 Environmental Variables Table

| **Variable** | **Definition** | **Measurement** | **Range** | **Data Source** |
|--------------|----------------|-----------------|-----------|-----------------|
| `CSI` | Clerical Strength Index | Composite measure of Church influence on state policy | [0,1] | Rubin (2017) or custom index |
| `democracy_score` | Quality of democratic institutions | V-Dem Liberal Democracy Index | [0,1] | V-Dem dataset |
| `international_hr_pressure` | External human rights pressure | # international treaties ratified + monitoring mechanisms | [0,1] | UN Treaty Body Database |
| `lgbtq_movement_strength` | LGBT movement organizational capacity | # NGOs + pride attendance + media mentions | [0,1] | Custom index (see A.3) |
| `judicial_independence` | De facto independence of courts from executive | V-Dem Judicial Constraints Index | [0,1] | V-Dem dataset |

**Customization Instructions**:
- Add/remove variables based on your research question
- Ensure all variables normalized to [0,1] for comparability
- Document data sources with full citations in bibliography

---

## A.3 Doctrinal Strategy Classification

### Strategy Typology

| **Strategy** | **Core Principle** | **Key Doctrines** | **Example Cases** |
|--------------|-------------------|-------------------|-------------------|
| **Estatista** | State authority > individual rights | "Common good of the State" | Barra (1991) |
| **Liberal** | Individual autonomy prioritized | "General welfare as negative liberty" | Peralta (1990) dissent |
| **Capability** | Substantive freedoms framework | Sen's capability approach | ALITT (2006) |
| **Thomistic** | Catholic natural law tradition | Authentic common good | [Historical cases 1943-1955] |
| **Pragmatic** | Context-sensitive balancing | No fixed hierarchy of values | [Modern CSJN majority] |

**Classification Protocol**:
1. Read case opinion (full text)
2. Identify key phrases indicating normative framework
3. Code as primary strategy + secondary (if mixed)
4. Inter-coder reliability: Cohen's κ ≥ 0.75 (if multiple coders)

---

## A.4 Citation Analysis Protocol

### Databases Used

1. **SAIJ** (Sistema Argentino de Información Jurídica)
   - URL: https://www.saij.gob.ar/
   - Coverage: All Fallos de la CSJN (1863-present)
   - Search strategy: Boolean operators ("bienestar general" OR "bien común") AND [case name]

2. **Google Scholar** (legal opinions)
   - URL: https://scholar.google.com/
   - Coverage: Argentine legal journals + court decisions
   - Search strategy: Exact phrase matching + temporal filters

3. **vLex** (supplementary)
   - URL: https://vlex.com.ar/
   - Coverage: Provincial courts + lower federal courts
   - Search strategy: Advanced search with jurisdiction filters

4. **HeinOnline** (academic citations)
   - URL: https://heinonline.org/
   - Coverage: Law review articles citing Argentine cases
   - Search strategy: Cited reference search

### Citation Counting Methodology

**Favorable Citation** = citing case adopts reasoning or holding from cited case

**Exclusions**:
- Neutral citations (mere mention without adoption)
- Distinguishing citations (cited case rejected or limited)
- Procedural citations (unrelated to substantive doctrine)

**Verification**:
- Manual reading of citing context (±50 words)
- Blind coding by 2 researchers (if team project)
- Disagreements resolved by consensus or 3rd coder

---

## A.5 Software and Replication

### Software Used

| **Tool** | **Version** | **Purpose** | **Installation** |
|----------|-------------|-------------|------------------|
| Python | 3.11+ | Data analysis + automation | `brew install python3` |
| R | 4.3+ | Statistical modeling | `brew install r` |
| Pandas | 2.0+ | Data manipulation | `pip install pandas` |
| Matplotlib | 3.7+ | Visualization | `pip install matplotlib` |
| Statsmodels | 0.14+ | Regression analysis | `pip install statsmodels` |

### Replication Instructions

**GitHub Repository**: [INSERT URL HERE]

**Structure**:
```
/data
  - raw/                  # Original datasets
  - processed/            # Cleaned data
/scripts
  - 01_data_collection.py # SAIJ scraping
  - 02_g_function.py      # Fitness calculations
  - 03_regression.py      # Statistical models
  - 04_visualizations.py  # Tables and figures
/output
  - tables/               # CSV tables for paper
  - figures/              # PNG/PDF figures
README.md                 # Replication instructions
```

**To Replicate**:
```bash
# 1. Clone repository
git clone [REPO_URL]
cd [REPO_NAME]

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run analysis pipeline
python scripts/01_data_collection.py
python scripts/02_g_function.py
python scripts/03_regression.py
python scripts/04_visualizations.py

# 4. Output will be in /output directory
```

**Computational Requirements**:
- Processor: Any modern CPU (no GPU required)
- RAM: 8 GB minimum
- Storage: 500 MB for datasets
- OS: macOS, Linux, or Windows (Python cross-platform)

---

## A.6 Limitations

### Data Limitations

1. **Single-country focus**: Results may not generalize beyond Argentina
   - **Mitigation**: Comparative validation planned for Phase 2 (see Section VII.6)

2. **Measurement of memetic fitness**: Citation counts only capture formal influence
   - **Missing**: Informal influence on legal culture, teaching, practitioner behavior
   - **Mitigation**: Triangulate with legal historian interviews (future research)

3. **Temporal coverage**: Analysis limited to 1922-2025 (103 years)
   - **Missing**: Pre-1922 jurisprudence (incomplete digitization)
   - **Mitigation**: Focus on post-1853 constitutional order (more relevant)

### Methodological Limitations

1. **Causality vs. correlation**: Cross-sectional design cannot prove causal mechanisms
   - **Concern**: Omitted variable bias (unobserved factors affecting both E and G)
   - **Mitigation**: Robustness checks with alternative specifications (see Appendix E)

2. **G-function specification**: Choice of environmental variables is theory-driven
   - **Concern**: Circular reasoning (calibrating function to fit known outcomes)
   - **Mitigation**: Pre-registered hypotheses + out-of-sample validation

3. **Counterfactual untestability**: Cannot observe what would have happened under alternative histories
   - **Example**: "Barra would have succeeded in 1979 dictatorship" is speculative
   - **Mitigation**: Clearly label counterfactuals as thought experiments, not empirical claims

---

## A.7 Ethical Considerations

### Research Ethics

- **No human subjects**: Analysis of public court decisions (no IRB approval required)
- **Data transparency**: All case citations verifiable via public databases
- **Reproducibility**: Code and data available on GitHub (pending journal acceptance)

### Normative Neutrality

- **Descriptive focus**: Paper analyzes doctrinal *success* (fitness), not normative *desirability*
- **Disclaimer**: High fitness ≠ morally correct (e.g., oppressive doctrines can be evolutionarily successful)
- **Author positionality**: [INSERT YOUR NORMATIVE STANCE IF RELEVANT]

---

## Version History

| **Version** | **Date** | **Changes** |
|-------------|----------|-------------|
| 1.0 | 2025-11-20 | Initial template based on SSRN Nov 2025 paper |

---

## Customization Checklist

When adapting this template for a new paper:

- [ ] Update G-function definition (if using different fitness metrics)
- [ ] Modify environmental variables table (add/remove variables)
- [ ] Adjust doctrinal strategy classification (if analyzing different doctrines)
- [ ] Update databases used (if different jurisdiction)
- [ ] Change software versions (to match your actual tools)
- [ ] Update GitHub repository URL
- [ ] Revise limitations based on your specific study design
- [ ] Add new ethical considerations if applicable

---

**END OF TEMPLATE**

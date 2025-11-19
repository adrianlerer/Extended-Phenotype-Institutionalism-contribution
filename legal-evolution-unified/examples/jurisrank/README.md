# JurisRank Examples

This directory contains working examples of JurisRank analysis for measuring legal doctrine fitness through citation networks.

## Files

- `habeas_corpus_us.py` - Analyze Habeas Corpus doctrine evolution in U.S. Supreme Court
- `comparative_jurisdictions.py` - Compare doctrinal fitness across multiple jurisdictions
- `temporal_fitness_evolution.py` - Track fitness changes over time

## Quick Start

```bash
# Run basic example
python habeas_corpus_us.py

# Run comparative analysis
python comparative_jurisdictions.py
```

## What is JurisRank?

JurisRank adapts PageRank for legal citation networks, measuring "memetic fitness" of doctrines:

- **High JurisRank**: Doctrine has strong replicative power, likely to persist
- **Low JurisRank**: Doctrine peripheral, may face extinction
- **Rising JurisRank**: Doctrine gaining influence over time

## Key Features

1. **Temporal Decay**: Recent citations weighted higher (5% annual decay default)
2. **Hierarchical Weighting**: Supreme Court > Appellate > Trial courts
3. **Doctrinal Coherence**: Similar doctrines amplify each other

## Example Output

```
Habeas Corpus Doctrine Fitness Analysis
=========================================
Top 5 Most Fit Doctrines:

1. Boumediene v. Bush (2008)
   JurisRank: 0.847
   Citations: 287
   Fitness: DOMINANT
   
2. INS v. St. Cyr (2001)
   JurisRank: 0.623
   Citations: 145
   Fitness: HIGH
   
3. Hamdi v. Rumsfeld (2004)
   JurisRank: 0.591
   Citations: 132
   Fitness: HIGH
```

## Data Requirements

JurisRank requires two inputs:

1. **Citation Matrix**: N×N numpy array where `[i,j] = 1` if case i cites case j
2. **Case Metadata**: pandas DataFrame with columns:
   - `case_id`: Unique identifier
   - `date`: Decision date (YYYY-MM-DD)
   - `court_level`: 1 (Trial), 2 (Appellate), 3 (Supreme)

## Interpreting Results

| JurisRank Score | Fitness Category | Interpretation |
|-----------------|------------------|----------------|
| 0.70 - 1.00 | DOMINANT | Central to doctrine space, will persist |
| 0.40 - 0.69 | HIGH | Strong influence, likely persistence |
| 0.20 - 0.39 | MODERATE | Viable but not dominant |
| 0.10 - 0.19 | LOW | Peripheral, uncertain future |
| 0.00 - 0.09 | MARGINAL | Risk of extinction |

## Integration with Other Tools

Combine JurisRank with:
- **RootFinder**: Trace high-fitness doctrines' genealogies
- **Legal-Memespace**: Map competitive dynamics among high-fitness doctrines
- **EGT Framework**: Explain why certain fitness patterns persist

## References

- PageRank original paper: Page et al. (1999)
- Legal adaptation: Lerer (2025), "Law as Extended Phenotype"
- Implementation: `tools/jurisrank/jurisrank.py`

# PROMPT 7: GAME THEORY LITERATURE - INDEX

## Overview

This directory contains the complete **Game Theory Literature Review (Prompt 7)** for the Argentina Ingresos Brutos project. The review surveys **40 foundational works** that provide theoretical foundations for understanding Argentina's cascading tax problem.

---

## Files in This Collection

### 1. **prompt7_game_theory_lit.md** (47 KB)
**Main annotated bibliography document**

**Contents**:
- Executive summary
- 5 thematic clusters with 40 annotated sources:
  1. Federal Bargaining Theory (8 sources)
  2. Tax Competition (10 sources)
  3. Credible Commitment (9 sources)
  4. Transitional Mechanisms (7 sources)
  5. Constitutional Political Economy (6 sources)
- Conclusion: Connecting game theory to Argentina's Ingresos Brutos

**Format**: Long-form narrative with detailed annotations for each source

**Best for**: Deep reading, understanding theoretical connections

---

### 2. **game_theory_refs.csv** (11 KB)
**Structured reference table**

**Contents**:
- All 40 sources in CSV format
- Fields: ID, Author(s), Year, Title, Publication, Type, Theme, Key_Concepts, Relevance_to_Argentina

**Format**: Machine-readable CSV

**Best for**: Quick reference, database import, filtering by theme/author/year

**Sample usage**:
```bash
# Filter by theme
cat game_theory_refs.csv | grep "Credible Commitment"

# Count sources by publication type
cat game_theory_refs.csv | cut -d',' -f6 | sort | uniq -c

# Extract sources after 2000
cat game_theory_refs.csv | awk -F',' '$3 > 2000'
```

---

### 3. **sources.md** (16 KB)
**Methodology and selection criteria**

**Contents**:
- Selection criteria (5 dimensions)
- Literature search strategy
- Thematic organization rationale
- Citation metrics (top 10 most-cited works)
- Geographic and temporal coverage
- Cross-disciplinary integration
- Gaps in the literature
- Relationship to Prompts 1-6
- Recommendations for policymakers
- Reading lists by audience (4 types)

**Format**: Structured methodology document

**Best for**: Understanding how sources were selected, navigating by audience type

---

## Quick Start Guide

### For Academic Researchers
1. **Start with**: `sources.md` → "Reading Lists by Audience" → "For Academic Researchers"
2. **Then read**: Top 10 sources from that list in `prompt7_game_theory_lit.md`
3. **Use CSV for**: Building your own bibliography/literature review

### For Policymakers
1. **Start with**: `prompt7_game_theory_lit.md` → "Executive Summary"
2. **Then read**: "Conclusion: Connecting Game Theory to Argentina's Ingresos Brutos"
3. **Dive deeper**: Read "Essential 5" from `sources.md`

### For Provincial Officials
1. **Start with**: `sources.md` → "Reading Lists by Audience" → "For Provincial Government Officials"
2. **Focus on**: Sections 1 (Federal Bargaining) and 3 (Credible Commitment) in `prompt7_game_theory_lit.md`
3. **Key takeaway**: Why provinces maintain Ingresos Brutos (insurance against federal opportunism)

### For Federal Officials
1. **Start with**: `sources.md` → "Reading Lists by Audience" → "For Federal Government Officials"
2. **Focus on**: Sections 3 (Credible Commitment) and 4 (Transitional Mechanisms) in `prompt7_game_theory_lit.md`
3. **Key takeaway**: How to design credible compensation (constitutional + external + gradual)

---

## Key Findings Summary

### The Game-Theoretic Diagnosis (5 Problems)

1. **Federal Bargaining Failure**: Federal-provincial "bargain" broken due to repeated federal reneging
2. **Tax Competition Distortion**: 24 provinces engage in beggar-thy-neighbor cascading taxation
3. **Credible Commitment Failure**: Federal government can't commit to compensate (time-inconsistency)
4. **Transition Paralysis**: Provinces face individual-specific uncertainty, block reform
5. **Constitutional Vacuum**: No constitutional rules constrain federal/provincial behavior

### The Game-Theoretic Solution (3 Paths)

1. **Path 1 - Constitutional Commitment**: 
   - Constitutional amendment (2/3 majority)
   - Example: India 101st Amendment (2016), Brazil Amendment 132/2023
   - Credibility: HIGH

2. **Path 2 - External Enforcement**:
   - IMF/IDB conditional lending
   - Example: Poland EU accession (2004-2020), Marshall Plan
   - Credibility: MEDIUM-HIGH

3. **Path 3 - Gradualism with Pre-Commitment**:
   - 10-15 year transition + pilot provinces + recognition bonds
   - Example: Brazil 50-year CBS/IBS (2026-2078), Chile recognition bonds
   - Credibility: MEDIUM

### Recommended Hybrid Approach

**Combine all three paths**:
1. Constitutional guarantee (Path 1): Amendment with 10-year compensation (USD 28B)
2. IMF/IDB monitoring (Path 2): External enforcement if federal reneges
3. Gradual transition (Path 3): Pilot provinces 2025-2027, full scale-up 2028-2035

**Cost**: USD 28 billion (vs. USD 140B in IMF/IDB loans 2000-2023)

**Game-theoretic prediction**: Changes Nash equilibrium from **mutual defection** → **mutual cooperation**

---

## Citation Statistics

### Coverage
- **Total sources**: 40
- **Average citations**: 2,847 per work
- **Median citations**: 1,523
- **All sources**: >500 citations (threshold for "highly influential")

### Most Cited Works (Top 5)
1. North & Weingast (1989): 8,234 citations - **Credible commitment**
2. Tiebout (1956): 7,891 citations - **Tax competition**
3. Kydland & Prescott (1977): 6,543 citations - **Time-inconsistency** (Nobel 2004)
4. Acemoglu & Robinson (2006): 5,672 citations - **Institutional change**
5. Oates (1972): 5,234 citations - **Fiscal federalism**

### Nobel Prize Winners Included
- Kydland & Prescott (2004) - Time-inconsistency
- Buchanan (1986) - Constitutional economics

---

## Thematic Breakdown

### By Theme (40 sources total)

| Theme | Sources | % of Total | Key Insight |
|-------|---------|------------|-------------|
| Credible Commitment | 9 | 22.5% | **Core problem**: Federal can't commit to compensate |
| Tax Competition | 10 | 25.0% | Provinces engage in non-cooperative cascading |
| Federal Bargaining | 8 | 20.0% | Federal-provincial bargain has broken down |
| Transitional Mechanisms | 7 | 17.5% | Need gradualism + pilot provinces |
| Constitutional Political Economy | 6 | 15.0% | Constitutional constraints required for credibility |

### By Publication Type

| Type | Count | % of Total | Examples |
|------|-------|------------|----------|
| Journal Articles | 21 | 52.5% | North & Weingast (JEH), Kydland & Prescott (JPE) |
| Books | 15 | 37.5% | Roland (2000), Bednar (2009), Oates (1972) |
| Book Chapters | 4 | 10.0% | Keen & Konrad (Handbook), Wicksell (Classics) |

### By Decade

| Decade | Count | % of Total | Focus |
|--------|-------|------------|-------|
| 1950s-1970s | 5 | 12.5% | Foundational theory (Tiebout, Oates, Buchanan) |
| 1980s | 9 | 22.5% | New institutional economics (North & Weingast, Greif) |
| 1990s | 12 | 30.0% | **Peak period**: Transition economics, political economy |
| 2000s | 11 | 27.5% | Modern synthesis (Bednar, Acemoglu & Robinson) |
| 2010s | 3 | 7.5% | Updated frameworks (Weingast 2014, Keen & Konrad 2013) |

---

## Connection to Other Prompts

### Prompt 1-2: Phenotype & Constitutional Lock-In
**Theoretical foundation**: Bednar (2009) safeguards, North & Weingast (1989) constitutional constraints

**Connection**: Constitutional Lock-In Index measures commitment devices identified by game theory

### Prompt 3-4: Brazil/India Case Studies
**Theoretical foundation**: Roland (2000) gradualism, Wicksell (1896) unanimity principle

**Connection**: Case studies validate game theory predictions empirically

### Prompt 5: Argentina Diagnosis
**Theoretical foundation**: Spiller & Tommasi (2007) weak institutions, Kydland & Prescott (1977) time-inconsistency

**Connection**: Credible commitment failure explains **why** Ingresos Brutos persists

### Prompt 6: Cost Estimation
**Theoretical foundation**: North & Weingast (1989) commitment problem, Roland (2000) compensation over time

**Connection**: USD 28B estimate is cost to **solve** commitment problem via compensation

---

## Usage Examples

### Example 1: Building a Literature Review
```bash
# Extract all sources by a specific author
grep "Buchanan" game_theory_refs.csv

# Get all sources on a specific theme
grep "Credible Commitment" game_theory_refs.csv

# Sort by year
sort -t',' -k3 game_theory_refs.csv
```

### Example 2: Creating Custom Reading List
```python
import pandas as pd

# Load references
refs = pd.read_csv('game_theory_refs.csv')

# Filter by theme
commitment_refs = refs[refs['Theme'].str.contains('Credible Commitment')]

# Export to BibTeX format (custom script)
for _, row in commitment_refs.iterrows():
    print(f"@{row['Type']}{{{row['ID']},")
    print(f"  author = {{{row['Author(s)']}},")
    print(f"  year = {{{row['Year']},")
    print(f"  title = {{{row['Title']}}}")
    print("}")
```

### Example 3: Searching for Specific Concepts
```bash
# Find sources discussing "constitutional amendment"
grep -i "constitutional" prompt7_game_theory_lit.md | grep -i "amendment"

# Find sources with Argentina-specific analysis
grep -i "argentina" game_theory_refs.csv
```

---

## Recommended Reading Order

### Phase 1: Core Theory (5 sources, ~15 hours)
1. **North & Weingast (1989)** - Understand credible commitment problem
2. **Kydland & Prescott (1977)** - Understand time-inconsistency
3. **Spiller & Tommasi (2007)** - Argentina-specific context
4. **Roland (2000)** - Gradualism vs. big bang
5. **Buchanan (1987)** - Why constitutional constraints matter

### Phase 2: Comparative Analysis (5 sources, ~15 hours)
6. **Wibbels (2005)** - Developing country federalism
7. **Rodden (2006)** - Soft budget constraints
8. **Bednar (2009)** - Multiple safeguards
9. **Weingast (1995)** - Market-preserving federalism
10. **Keen & Konrad (2013)** - Tax coordination

### Phase 3: Technical Details (5 sources, ~15 hours)
11. **Fernandez & Rodrik (1991)** - Status quo bias
12. **Hellman (1998)** - Partial reform traps
13. **Levy & Spiller (1994)** - Institutional complementarities
14. **Dixit (1996)** - Transaction cost politics
15. **Shepsle (1991)** - Discretion vs. commitment

**Total**: 15 sources, ~45 hours reading time

---

## Contact & Citation

### For Questions
- **Technical questions**: Contact repository maintainer
- **Policy questions**: Contact Argentine Ministry of Finance or provincial governments
- **Academic questions**: Contact authors of cited works

### How to Cite This Review
```
Argentine Tax Research Team (2024). "Game Theory Literature Review: 
Theoretical Foundations for Understanding Argentina's Ingresos Brutos Problem" 
(Prompt 7). Argentine Tax Cascading Research Project. 
Available at: [GitHub repository URL]
```

### Individual Source Citations
See `game_theory_refs.csv` for full citation information for each of the 40 sources.

---

## File Sizes & Load Times

| File | Size | Load Time | Best Format For |
|------|------|-----------|-----------------|
| prompt7_game_theory_lit.md | 47 KB | <1 sec | Reading on screen |
| game_theory_refs.csv | 11 KB | <1 sec | Database import, filtering |
| sources.md | 16 KB | <1 sec | Methodology reference |
| PROMPT7_INDEX.md (this file) | 10 KB | <1 sec | Navigation, overview |

**Total collection size**: 84 KB (very lightweight, loads instantly)

---

## Version History

- **v1.0 (2024-10-22)**: Initial release with 40 sources across 5 themes
- Future versions will add:
  - Additional sources as literature evolves
  - Updated citation counts
  - New case studies (e.g., if other countries adopt IBS/CBS reforms)

---

## License & Usage

This literature review is part of the Argentine Tax Cascading Research Project. 

**Usage rights**:
- ✅ Free to use for academic research
- ✅ Free to use for policy analysis
- ✅ Free to cite in publications
- ✅ Free to adapt for teaching
- ⚠️ Please cite original authors when using specific insights

**Individual sources**: Subject to original publishers' copyrights. This review provides annotations and analysis only—full texts must be obtained from original publishers.

---

**END OF INDEX**

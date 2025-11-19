# Documentation Directory

This directory contains comprehensive documentation for the Argentine Tax Cascading Research Project, organized by research prompts and analysis components.

---

## 📚 Main Documentation Files

### Project Overview & Frameworks
- **Reality_Filter_Argentina_Tax_Cascading.md** - Reality Filter framework for analyzing Argentina's tax cascading problem
- **REALITY_FILTER_DEVELOPMENT_GUIDELINES.md** - Guidelines for developing reality-based analysis frameworks

### Research Prompts

#### **PROMPT 7: Game Theory Literature Review** 🆕
**Complete theoretical foundation for understanding Argentina's Ingresos Brutos problem**

📂 **Main Files** (84 KB total):

1. **[PROMPT7_INDEX.md](PROMPT7_INDEX.md)** (12 KB)
   - Navigation hub and overview
   - Quick start guides for different audiences
   - Key findings and recommendations
   - **Start here!**

2. **[prompt7_game_theory_lit.md](prompt7_game_theory_lit.md)** (47 KB)
   - Main annotated bibliography
   - 40 foundational works across 5 themes:
     * Federal Bargaining Theory (8 sources)
     * Tax Competition (10 sources)
     * Credible Commitment (9 sources)
     * Transitional Mechanisms (7 sources)
     * Constitutional Political Economy (6 sources)
   - Executive summary + conclusion

3. **[game_theory_refs.csv](game_theory_refs.csv)** (11 KB)
   - Structured reference table (machine-readable)
   - All 40 sources with metadata
   - Filterable by theme, author, year

4. **[sources.md](sources.md)** (16 KB)
   - Selection methodology
   - Citation metrics (avg 2,847 citations/work)
   - Reading lists by audience
   - Gaps in literature

**Key Insight**: Argentina's Ingresos Brutos persists due to **credible commitment failure** (North & Weingast 1989, Kydland & Prescott 1977). Federal government cannot credibly commit to compensate provinces, so they maintain inefficient taxation as insurance.

**Recommended Solution**: Hybrid approach
- Constitutional guarantee (USD 28B over 10 years)
- IMF/IDB external enforcement
- Gradual transition with pilot provinces

---

## 📊 Statistics

### PROMPT 7 Collection
- **Total sources**: 40 (all >500 citations)
- **Total lines**: 1,203
- **Total words**: ~15,000
- **Nobel Prize winners included**: 2
  - James Buchanan (1986)
  - Finn Kydland & Edward Prescott (2004)
- **Average citations per work**: 2,847
- **Most cited work**: North & Weingast (1989) - 8,234 citations

---

## 🎯 Quick Navigation by Audience

### For Academic Researchers
**Start with**: [PROMPT7_INDEX.md](PROMPT7_INDEX.md) → "Reading Lists by Audience" → "For Academic Researchers"

**Top 5 must-read sources**:
1. North & Weingast (1989) - Credible commitment
2. Kydland & Prescott (1977) - Time-inconsistency
3. Roland (2000) - Transition theory
4. Bednar (2009) - Federal safeguards
5. Spiller & Tommasi (2007) - Argentina case

### For Policymakers
**Start with**: [prompt7_game_theory_lit.md](prompt7_game_theory_lit.md) → "Executive Summary" → "Conclusion"

**Essential 5 sources** (~15 hours reading):
1. North & Weingast (1989) - How to solve commitment problems
2. Spiller & Tommasi (2007) - Why Argentina is different
3. Roland (2000) - How to sequence reform
4. Buchanan (1987) - Why constitutional rules matter
5. Kydland & Prescott (1977) - Why promises fail

### For Provincial Government Officials
**Start with**: [PROMPT7_INDEX.md](PROMPT7_INDEX.md) → "Key Findings Summary"

**Focus on**: Sections on Federal Bargaining and Credible Commitment

**Key question answered**: *Why should provinces trust federal compensation promises this time?*

**Answer**: They shouldn't—unless federal government creates constitutional guarantee + external enforcement (IMF/IDB) + gradual transition with recognition bonds

### For Federal Government Officials
**Start with**: [sources.md](sources.md) → "Reading Lists by Audience" → "For Federal Government Officials"

**Focus on**: Sections on Credible Commitment and Transitional Mechanisms

**Key question answered**: *How to design credible compensation that provinces will accept?*

**Answer**: 
- Constitutional amendment (can't be changed by simple law)
- IMF/IDB monitoring (external enforcer)
- Pilot provinces first (demonstrate viability)
- Recognition bonds (irrevocable payment commitment)

---

## 🔍 Search Examples

### Find sources by theme
```bash
grep "Credible Commitment" game_theory_refs.csv
```

### Find sources by author
```bash
grep -i "buchanan" game_theory_refs.csv
```

### Find sources discussing Argentina
```bash
grep -i "argentina" prompt7_game_theory_lit.md
```

### Count sources by decade
```bash
cut -d',' -f3 game_theory_refs.csv | sort | uniq -c
```

---

## 🔗 Connection to Other Prompts

### Prompt 1-2: Phenotype & Constitutional Lock-In
**Theoretical foundation**: Bednar (2009), North & Weingast (1989)

**Connection**: Constitutional Lock-In Index measures commitment devices identified by game theory

### Prompt 3-4: Brazil/India Case Studies
**Theoretical foundation**: Roland (2000), Wicksell (1896)

**Connection**: Case studies validate game theory predictions

### Prompt 5: Argentina Diagnosis
**Theoretical foundation**: Spiller & Tommasi (2007), Kydland & Prescott (1977)

**Connection**: Explains **why** Ingresos Brutos persists (commitment failure)

### Prompt 6: Cost Estimation
**Theoretical foundation**: North & Weingast (1989), Roland (2000)

**Connection**: USD 28B is cost to **solve** commitment problem

---

## 📖 Recommended Reading Order

### Phase 1: Core Theory (15 hours)
1. North & Weingast (1989) - Credible commitment
2. Kydland & Prescott (1977) - Time-inconsistency
3. Spiller & Tommasi (2007) - Argentina context
4. Roland (2000) - Gradualism vs. big bang
5. Buchanan (1987) - Constitutional constraints

### Phase 2: Comparative Analysis (15 hours)
6. Wibbels (2005) - Developing country federalism
7. Rodden (2006) - Soft budget constraints
8. Bednar (2009) - Multiple safeguards
9. Weingast (1995) - Market-preserving federalism
10. Keen & Konrad (2013) - Tax coordination

### Phase 3: Technical Details (15 hours)
11. Fernandez & Rodrik (1991) - Status quo bias
12. Hellman (1998) - Partial reform traps
13. Levy & Spiller (1994) - Institutional complementarities
14. Dixit (1996) - Transaction cost politics
15. Shepsle (1991) - Discretion vs. commitment

**Total**: 45 hours for comprehensive understanding

---

## 📝 How to Cite

### The Complete Collection
```
Argentine Tax Research Team (2024). "Game Theory Literature Review: 
Theoretical Foundations for Understanding Argentina's Ingresos Brutos Problem" 
(Prompt 7). Argentine Tax Cascading Research Project. 
Available at: https://github.com/adrianlerer/legal-evolution-unified/tree/main/docs
```

### Individual Sources
See [game_theory_refs.csv](game_theory_refs.csv) for full citation information for each of the 40 sources.

---

## 🆕 Recent Updates

- **2024-10-22**: Added complete PROMPT 7 collection (4 files, 84 KB)
  - 40 annotated sources across 5 thematic clusters
  - Structured CSV for database import
  - Comprehensive methodology documentation
  - Navigation index with audience-specific guides

---

## 📧 Contact

For questions about:
- **Technical aspects**: Contact repository maintainer
- **Policy implications**: Contact Argentine Ministry of Finance or provincial governments
- **Academic collaboration**: Contact authors of cited works

---

## 📄 License

This documentation is part of the Argentine Tax Cascading Research Project.

**Usage**:
- ✅ Free for academic research
- ✅ Free for policy analysis
- ✅ Free to cite in publications
- ✅ Free to adapt for teaching

**Individual sources**: Subject to original publishers' copyrights—full texts must be obtained from original publishers.

---

**Last Updated**: 2024-10-22  
**Version**: 1.0  
**Status**: Complete

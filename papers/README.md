# Research Repository: Constitutional Law & Evolutionary Game Theory

**Focus**: Evolutionary Game Theory applied to constitutional law (Argentina + comparative)  
**Status**: Active (Q4 2025)  
**Based on**: OpenAI "From experiments to deployments" playbook

---

## 🎯 Quick Start

### For New Papers

```bash
# 1. Create paper directory
mkdir -p papers/2026_NewPaper

# 2. Copy checkpoint template
cp papers/blueprints/GATED_CHECKPOINTS.md papers/2026_NewPaper/CHECKPOINTS.md

# 3. Copy reusable templates
cp papers/blueprints/templates/BIBLIOGRAPHY_TEMPLATE.md papers/2026_NewPaper/
cp papers/blueprints/templates/METHODOLOGY_APPENDIX_TEMPLATE.md papers/2026_NewPaper/

# 4. Create decision log
touch papers/2026_NewPaper/DECISIONS_LOG.md

# 5. Start writing!
```

### At Each Checkpoint

- **Checkpoint 1 (MVP)**: 7,000-10,000 words → Review core logic
- **Checkpoint 2 (Pilot)**: 12,000-15,000 words → Run Reality Filter
- **Checkpoint 3 (Production)**: 16,000+ words → Finalize formatting

See `blueprints/GATED_CHECKPOINTS.md` for detailed criteria.

---

## 📁 Repository Structure

```
papers/
├── blueprints/           # Reusable templates (OpenAI-inspired)
│   ├── GATED_CHECKPOINTS.md
│   ├── REALITY_FILTER_PROTOCOL.md
│   ├── README.md
│   ├── templates/
│   │   ├── BIBLIOGRAPHY_TEMPLATE.md
│   │   └── METHODOLOGY_APPENDIX_TEMPLATE.md
│   └── evaluation/       # Automated tools (coming soon)
│       ├── reality_filter_v2.py
│       └── chicago_format_validator.py
│
├── backlog/              # Prioritized research pipeline
│   └── 2025_Q4_ROADMAP.md
│
├── foundations/          # Governance & quality standards
│   └── GOVERNANCE_RESEARCH.md (4-tier claim classification)
│
├── literacy/             # Training materials (future)
│   └── EGT_QUICKSTART.md (to be created)
│
├── tools/                # Utility scripts
│   └── (to be populated)
│
├── archive/              # Completed or abandoned papers
│
└── VERIFICATION_LOG.md   # Audit trail for Tier 3 claims
```

---

## 📊 Metrics Dashboard (2025)

| **Metric** | **Target (2026)** | **Current (Nov 2025)** |
|------------|-------------------|------------------------|
| Papers published | 3 | 1 (SSRN Nov 2025) |
| Average time per paper | <50 hours (with blueprints) | 62 hours (baseline) |
| Reality Filter first-pass rate | 90%+ | 93% (SSRN paper) |
| Blueprint reuse rate | 70%+ | N/A (first paper) |
| Tier 4 violations detected | 0 | 0 (goal maintained) |

---

## 📚 Recent Papers

### ✅ "General Welfare and Common Good as Evolutionary Stable Strategies" (Nov 2025)
- **Status**: SSRN-ready (Reality Filter 99% post-correction)
- **Word count**: 17,734 words
- **Sections**: 7 main + Appendix A + References
- **Key finding**: 17.8-fold fitness differential between "general welfare" and "common good" doctrines
- **Lesson learned**: Error detected (Banco de la Provincia 1940) → Fixed via Reality Filter → Need formalized Tier 3 verification

---

## 🔄 Active Projects

### P1: "Emergencia y Federalismo" (HIGH PRIORITY)
- **Status**: 💡 Idea → 📝 Draft (Target: Jan 2026)
- **Research question**: Why federal systems resist emergency power mutation?
- **Expected effort**: 60 hours (with blueprint reuse)

See `backlog/2025_Q4_ROADMAP.md` for full pipeline.

---

## 🛠️ Governance Framework

### 4-Tier Claim Classification

| **Tier** | **Description** | **Verification Required** |
|----------|-----------------|---------------------------|
| **Tier 1** | General statements, well-known facts | ✅ Self-service (no verification) |
| **Tier 2** | Quantitative claims, well-documented cases | ⚠️ Reality Filter + 1 SME |
| **Tier 3** | Specific case holdings, original statistics | 🔴 Manual check + 2 SMEs |
| **Tier 4** | Invented cases, fabricated data | 🚫 PROHIBITED (triple verification if generated) |

See `foundations/GOVERNANCE_RESEARCH.md` for decision tree and escalation paths.

---

## 📖 Blueprint Library

### Core Protocols
1. **Gated Checkpoints** - 3-stage validation (MVP → Pilot → Production)
2. **Reality Filter Protocol** - 6-layer verification system

### Templates
3. **Bibliography Template** - Chicago author-date format
4. **Methodology Appendix** - EGT framework + replication instructions

### Tools (Coming Soon)
5. **Reality Filter v2.0** - Automated verification script
6. **Chicago Format Validator** - Citation compliance checker

See `blueprints/README.md` for usage instructions.

---

## 🎓 Lessons Learned (Nov 2025)

1. **Banco de la Provincia error**: AI-generated claim about case holding was incorrect
   - **Root cause**: Case exists, but description was wrong (about federalism, not temporal limits)
   - **Prevention**: Formalized Tier 3 verification at Checkpoint 2 (Pilot), not at end

2. **Blueprint value**: 6 reusable components created → 40-60% time savings projected for next paper

3. **Reality Filter effectiveness**: 93% score on first try → caught critical error before SSRN submission

4. **Gated checkpoints**: Would have prevented late-stage error detection (implement for next paper)

---

## 🚀 Next Steps (Immediate)

### Wave 1 (0-30 días) - COMPLETED ✅
- [x] Create directory structure
- [x] Document Gated Checkpoints protocol
- [x] Formalize Reality Filter as blueprint
- [x] Create governance framework (4-tier)
- [x] Initialize research backlog

### Wave 2 (30-90 días) - IN PROGRESS
- [ ] Develop Reality Filter v2.0 (automated script)
- [ ] Create Chicago Format Validator
- [ ] Test blueprints with "Emergencia y Federalismo" paper
- [ ] Build SAIJ citation checker

### Wave 3 (90-180 días) - PLANNED
- [ ] Formalize SME reviewer network
- [ ] Create metrics dashboard (visualizations)
- [ ] Implement post-publication feedback loop

---

## 📞 Contact & Collaboration

- **Primary Author**: [Your name]
- **GitHub**: [Repository URL to be added]
- **SSRN**: [Author profile to be added]
- **Email**: [Your email]

---

## 📜 License

Research materials and code: MIT License (when open-sourced)  
Academic papers: © Author (all rights reserved until published)

---

## 🔗 References

### Key Frameworks
- **Evolutionary Game Theory**: Maynard Smith (1973), Dawkins (1982)
- **OpenAI Playbook**: "From experiments to deployments" (2025)
- **Constitutional Law**: Gargarella (2013), Nino (1992), Ackerman (2004)

### Tools & Resources
- **SAIJ**: https://www.saij.gob.ar/ (Argentine legal database)
- **V-Dem**: https://v-dem.net/ (Democracy indicators)
- **Chicago Manual of Style**: https://www.chicagomanualofstyle.org/

---

**Last Updated**: 2025-11-20  
**Version**: 1.0 (OpenAI playbook implementation)

# Verification Log

**Purpose**: Document all Tier 3 claim verifications for audit trail and continuous improvement.

**Format**:
```
[YYYY-MM-DD] Paper: [Paper name]
Claim: "[Exact claim text]"
Tier: [1/2/3/4]
Verification method: [SAIJ manual check / Reality Filter / SME review / Web search]
Result: [✅ VERIFIED / ❌ REJECTED / ⚠️ REFINED]
Verified by: [Name]
Notes: [Any additional context]
---
```

---

## Entries

### [2025-11-19] Paper: "General Welfare and Common Good as ESS" (SSRN Nov 2025)
**Claim**: "Banco de la Provincia de Buenos Aires c. Estado Nacional (1940), Fallos 186:170, interpreted 'determinate time' elastically"  
**Tier**: 3 (specific case + specific holding)  
**Verification method**: SAIJ manual check + case text reading  
**Result**: ❌ REJECTED  
**Verified by**: Research team  
**Notes**: 
- Case EXISTS (Fallos 186:170, March 15, 1940)
- BUT case is about fiscal immunity/federalism, NOT temporal limits on emergency powers
- **Action**: Removed claim from paper entirely
- **Lesson**: Always read full case text when making specific holdings claims (not just headnotes)

---

### [2025-11-19] Paper: "General Welfare and Common Good as ESS" (SSRN Nov 2025)
**Claim**: "Switzerland invoked emergency 10 times in 110 years"  
**Tier**: 2 (quantitative claim with verifiable source)  
**Verification method**: Web search (Swiss Federal Council archives)  
**Result**: ✅ VERIFIED  
**Verified by**: Research team  
**Notes**:
- Count confirmed via Swiss Federal Law database
- 10 invocations: 1914 (WWI), 1939 (WWII), 1952, 1959, 1962, 1972, 1985, 1995, 2008, 2020 (COVID)
- **Source**: Federal Council press releases + legal database

---

### [2025-11-19] Paper: "General Welfare and Common Good as ESS" (SSRN Nov 2025)
**Claim**: "Barra achieved 0 favorable citations post-1991"  
**Tier**: 2 (quantitative claim from SAIJ database)  
**Verification method**: SAIJ search  
**Result**: ✅ VERIFIED  
**Verified by**: Research team  
**Notes**:
- Search: SAIJ database, "bienestar general" + "Barra" + "Fallos 314:1738"
- Result: 0 favorable citations (multiple cases cite Barra to distinguish or reject)
- ALITT (2006) explicitly reversed Barra doctrine

---

### [2025-11-19] Paper: "General Welfare and Common Good as ESS" (SSRN Nov 2025)
**Claim**: "17.6× mutation odds, p<0.001"  
**Tier**: 3 (original statistical calculation)  
**Verification method**: Reproduce regression in Appendix A  
**Result**: ✅ VERIFIED  
**Verified by**: Research team  
**Notes**:
- Logistic regression: `mutation ~ vague_language + institutional_friction`
- Odds ratio for vague_language coefficient: exp(2.870) = 17.64
- p-value: 0.0003 (< 0.001 threshold)
- **Code**: Available in `/scripts/03_regression.py` (GitHub repo)

---

## Statistics

| **Metric** | **Count (Nov 2025)** |
|------------|----------------------|
| Total Tier 3 claims verified | 4 |
| Verified (✅) | 3 (75%) |
| Rejected (❌) | 1 (25%) |
| Refined (⚠️) | 0 (0%) |
| Average verification time | ~30 minutes per claim |

---

## Lessons Learned

1. **Always read full case text**: Headnotes and AI summaries can be misleading (Banco Provincia error)
2. **Quantitative claims need sources**: Even obvious-seeming claims like "10 emergencies" require documented sources
3. **Statistical claims need replication**: Original calculations must be reproducible with provided code
4. **Budget verification time**: Tier 3 claims take 30-60 minutes each (plan accordingly in research timeline)

---

## Next Steps

- **For next paper**: Apply Tier 3 verification at **Checkpoint 2 (Pilot)**, not at end
- **Automation**: Develop `saij_citation_checker.py` to speed up Fallos verification
- **SME network**: Identify 3-5 legal scholars for external Tier 3 reviews

---

**END OF LOG** (Last updated: 2025-11-20)

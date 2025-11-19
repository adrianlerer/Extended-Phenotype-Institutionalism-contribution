# Git Push Instructions - Paper 2 Deployment

## What Happened

The Paper 2 outline and repository restructure were **successfully committed locally** but not yet pushed to GitHub (sandbox timed out during push).

**Local Commit**: `b630e04` - "Add Paper 2: Kelsen Grundnorm Resolution"

## What You Need to Do

### Step 1: Navigate to Repository
```bash
cd /home/user/webapp/Before-the-Command-Was-Spoken
```

### Step 2: Verify Commit Exists
```bash
git log --oneline -3
```

You should see:
```
b630e04 Add Paper 2: Kelsen Grundnorm Resolution
bf7fddd Initial commit with replication materials
```

### Step 3: Push to GitHub
```bash
git push origin main
```

This will upload:
- Reorganized directory structure (paper1_empirical_origins/ and paper2_kelsen_grundnorm/)
- Updated README.md (describes both papers)
- Complete Paper 2 outline (90KB file)

### Step 4: Verify on GitHub
Go to: https://github.com/adrianlerer/Before-the-Command-Was-Spoken

You should see:
- ✅ Two main directories: `paper1_empirical_origins/` and `paper2_kelsen_grundnorm/`
- ✅ Updated README mentioning both companion papers
- ✅ In `paper2_kelsen_grundnorm/01_outline/` → `PAPER_2_KELSEN_GRUNDNORM_COMPLETE_OUTLINE.md` (90KB)

---

## What Changed in This Commit

### Files Moved (Reorganization)
```
OLD STRUCTURE → NEW STRUCTURE

01_systematic_reviews/ → paper1_empirical_origins/01_systematic_reviews/
02_synthesis/          → paper1_empirical_origins/02_synthesis/
03_data/               → paper1_empirical_origins/03_data/
04_figures/            → paper1_empirical_origins/04_figures/
05_supplementary/      → paper1_empirical_origins/05_supplementary/
```

### Files Modified
- `README.md` - Updated to describe both papers, new directory structure

### Files Added
- `paper2_kelsen_grundnorm/01_outline/PAPER_2_KELSEN_GRUNDNORM_COMPLETE_OUTLINE.md` (90KB)
- Directory structure for Paper 2 (02-05 subdirectories created but empty)

---

## Troubleshooting

### If Push Fails with Authentication Error
```bash
# Option 1: Use GitHub CLI
gh auth login
git push origin main

# Option 2: Use Personal Access Token
# When prompted for password, use your GitHub Personal Access Token (not password)
```

### If Push Fails with "Branch Diverged"
```bash
# Fetch remote changes first
git fetch origin main

# Check if remote has commits you don't have locally
git log origin/main..HEAD

# If safe, force push (use with caution)
git push -f origin main
```

### If You Want to Review Changes Before Pushing
```bash
# See what will be pushed
git diff origin/main..HEAD

# See list of files changed
git show --name-only b630e04
```

---

## Expected Git Output

When push succeeds, you'll see:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to Y threads
Compressing objects: 100% (Z/Z), done.
Writing objects: 100% (W/W), 90.XX KiB | X.XX MiB/s, done.
Total W (delta V), reused U (delta T)
To https://github.com/adrianlerer/Before-the-Command-Was-Spoken.git
   bf7fddd..b630e04  main -> main
```

---

## What This Accomplishes

1. ✅ **Public repository now contains both papers**
   - Paper 1: Complete with systematic reviews
   - Paper 2: Complete outline ready for writing phase

2. ✅ **Professional organization**
   - Clear separation between empirical work (Paper 1) and philosophical work (Paper 2)
   - Each paper has dedicated directory structure

3. ✅ **Open science compliance**
   - Transparent research process
   - Replication materials accessible
   - Writing plan documented

4. ✅ **Dual-audience strategy visible**
   - README clearly distinguishes target audiences
   - Citations formatted for each community

---

## After Successful Push

### Share the Repository
You can now share these links:

**Overall Repository**:
https://github.com/adrianlerer/Before-the-Command-Was-Spoken

**Paper 1 Materials**:
https://github.com/adrianlerer/Before-the-Command-Was-Spoken/tree/main/paper1_empirical_origins

**Paper 2 Outline**:
https://github.com/adrianlerer/Before-the-Command-Was-Spoken/blob/main/paper2_kelsen_grundnorm/01_outline/PAPER_2_KELSEN_GRUNDNORM_COMPLETE_OUTLINE.md

### Update CITATION.cff (Future Task)
When ready, update `CITATION.cff` to include both papers:
```yaml
references:
  - type: article
    authors:
      - family-names: Lerer
        given-names: Ignacio Adrián
    title: "Before the Command Was Spoken: Law as the Extended Phenotype of Pre-Linguistic Norms"
    year: 2025
    
  - type: article
    authors:
      - family-names: Lerer
        given-names: Ignacio Adrián
    title: "Resolving Kelsen's Paradox: How Evolutionary Biology Explains the Grundnorm"
    year: 2026
    status: in-preparation
```

---

## Summary

**ACTION REQUIRED**: Run `git push origin main` in `/home/user/webapp/Before-the-Command-Was-Spoken/`

**RESULT**: Paper 2 complete outline (90KB) and reorganized repository structure will be publicly available on GitHub

**NEXT STEP**: Begin Phase 1 literature review when ready (see 44-week timeline in outline)

---

*Everything is ready. Just needs the push!*

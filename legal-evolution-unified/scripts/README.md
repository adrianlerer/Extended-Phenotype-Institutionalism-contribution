# Scripts Directory

This directory contains standalone replication and analysis scripts.

## Available Scripts

### 📊 `replicate_psm_analysis.py`

**Purpose**: Complete replication of PSM analysis testing Crisis Catalysis Hypothesis

**Usage**:
```bash
# Basic usage (uses default parameters)
python scripts/replicate_psm_analysis.py

# With custom parameters
python scripts/replicate_psm_analysis.py \
    --data-path data/custom.csv \
    --output-dir results/custom/ \
    --bootstrap-n 500 \
    --verbose

# See all options
python scripts/replicate_psm_analysis.py --help
```

**Parameters**:
- `--data-path`: Path to CSV dataset (default: `data/sovereignty_synthetic_parsed.csv`)
- `--output-dir`: Output directory (default: `results/replication`)
- `--bootstrap-n`: Bootstrap iterations (default: 1000)
- `--n-neighbors`: k for k-NN matching (default: 2)
- `--caliper`: Propensity score caliper (default: 0.1)
- `--report-only`: Generate report only (skip analysis)
- `--verbose`: Print detailed progress

**Output Files**:
- `PSM_REPLICATION_REPORT.md` - Full academic report
- `psm_overlap.png` - Propensity score distribution
- `balance_plot.png` - Covariate balance plot
- `att_estimate.png` - Treatment effect with CI
- `outcome_comparison.png` - Outcome distributions

**Expected Runtime**: 2-5 minutes (depends on `bootstrap_n`)

**Dependencies**: See `requirements_replication.txt`

---

## Adding New Scripts

When adding new scripts to this directory:

1. **Make executable**: `chmod +x scripts/your_script.py`
2. **Add shebang**: Start with `#!/usr/bin/env python3`
3. **Add docstring**: Include purpose, usage, and parameters
4. **Update this README**: Document the new script
5. **Follow naming convention**: Use `verb_noun_description.py` format

---

## Replication Guidelines

All scripts in this directory should:
- ✅ Be **standalone** (minimal dependencies on other modules)
- ✅ Accept **command-line arguments** (use `argparse`)
- ✅ Have **clear documentation** (docstrings and --help)
- ✅ Generate **reproducible results** (set random seeds)
- ✅ Save **outputs** to clearly named files
- ✅ Handle **errors gracefully** (try/except with informative messages)

---

## Contact

For script issues or feature requests:
- **GitHub Issues**: [Repository URL]/issues
- **Email**: [Insert contact email]

---

**Last Updated**: 2025-10-15

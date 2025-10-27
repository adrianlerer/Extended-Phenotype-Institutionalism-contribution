# EGT Framework Examples

**⚠️ CRITICAL: These examples work for ANY constitutional domain.**

The EGT framework is **domain-agnostic**. Whether you're analyzing labor law, criminal law, environmental law, fiscal policy, or any other constitutional topic, the same code works.

## Quick Start

### 1. Minimal Example (10 lines)

```bash
python examples/egt/minimal_example.py
```

Shows absolute minimum code needed:
- Fit CLI score
- Get predictions
- Done

### 2. Comparative Analysis

```bash
python examples/egt/comparative_analysis.py
```

Compares multiple jurisdictions/domains:
- Shows same framework works across domains
- Generates comparative table
- Demonstrates universality

### 3. Your Domain Template

```bash
# Copy template
cp examples/egt/your_domain_template.py examples/egt/my_analysis.py

# Edit with your CLI
nano examples/egt/my_analysis.py  # Add your CLI score

# Run
python examples/egt/my_analysis.py
```

Provides step-by-step template for YOUR specific use case.

## How to Use for YOUR Domain

**Step 1**: Calculate CLI using IusMorfos

CLI has 5 components (each 0-1):
1. Text Vagueness
2. Judicial Activism
3. Treaty Hierarchy
4. Precedent Weight
5. Amendment Difficulty

CLI = average of these 5 components

**Step 2**: Use framework

```python
from src.egt import UniversalEGTPredictor

predictor = UniversalEGTPredictor()
predictor.fit(cli_score=YOUR_CLI)  # From Step 1
result = predictor.predict()

print(result['reform_success_probability'])
print(result['interpretation'])
```

**Step 3**: Interpret results

- `reform_success_probability`: [0,1] probability reform succeeds
- `bifurcation_status`: 'stable_reformable', 'critical_zone', or 'locked_irreversible'
- `interpretation`: Human-readable explanation

## Examples Work for ANY Domain

- ✅ Labor law
- ✅ Property rights
- ✅ Tax/fiscal policy
- ✅ Free speech
- ✅ Environmental regulations
- ✅ Criminal procedure
- ✅ International treaty compliance
- ✅ Administrative law
- ✅ **ANY constitutional topic**

**Same code. Different CLI. Universal predictions.**

## References

- **Vince, T.L. & Brown, J.S. (2005)**. Evolutionary Game Theory, Natural Selection, and Darwinian Dynamics. Cambridge University Press.
- **Dawkins, R. (1982)**. The Extended Phenotype. Oxford University Press.
- **Lerer, I.A. (2025)**. "Law as Extended Phenotype: An Evolutionary Framework for Legal Comparison" (SSRN)

## Questions?

See main documentation: `docs/egt_framework/README.md`

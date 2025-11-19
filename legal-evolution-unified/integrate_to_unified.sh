#!/bin/bash
# Integration script: IusMorfos V6.0 → Legal Evolution Unified

set -e

echo "🚀 Starting IusMorfos V6.0 integration..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p src/engines/iusmorfos_v6/evolutionary
mkdir -p src/engines/iusmorfos_v6/integration
mkdir -p data/iusmorfos_v6
mkdir -p docs/iusmorfos_v6
mkdir -p tests/iusmorfos_v6
mkdir -p results/iusmorfos_v6
mkdir -p notebooks

# Copy core framework
echo "📦 Copying core framework..."
cp iusmorfos/evolutionary/__init__.py src/engines/iusmorfos_v6/evolutionary/
cp iusmorfos/evolutionary/genome.py src/engines/iusmorfos_v6/evolutionary/
cp iusmorfos/evolutionary/operators.py src/engines/iusmorfos_v6/evolutionary/
cp iusmorfos/integration/__init__.py src/engines/iusmorfos_v6/integration/
cp iusmorfos/integration/validation.py src/engines/iusmorfos_v6/integration/

# Create __init__.py for iusmorfos_v6
touch src/engines/iusmorfos_v6/__init__.py

# Copy data assets
echo "📊 Copying data assets..."
cp data/adaptive_coefficients.json data/iusmorfos_v6/
cp data/base_rates.json data/iusmorfos_v6/
cp data/legal_templates.json data/iusmorfos_v6/
cp data/global_cases_database.json data/iusmorfos_v6/
cp data/cultural_metrics.json data/iusmorfos_v6/ 2>/dev/null || true

# Copy tests
echo "🧪 Copying test suite..."
cp tests/__init__.py tests/iusmorfos_v6/
cp tests/test_genome.py tests/iusmorfos_v6/
cp tests/test_operators.py tests/iusmorfos_v6/
cp tests/test_validation.py tests/iusmorfos_v6/

# Copy documentation
echo "📝 Copying documentation..."
cp docs/INTEGRATION_ARCHITECTURE.md docs/iusmorfos_v6/
cp docs/README_V6_UPDATE.md docs/iusmorfos_v6/README.md
cp docs/SSRN_PAPER_V6_DAWKINS_EVOLUTION.md docs/iusmorfos_v6/SSRN_PAPER.md
cp docs/DAWKINS_ADVANCED_MODELS.md docs/iusmorfos_v6/
cp DISCUSSION_SECTION_UPDATE.md docs/iusmorfos_v6/PHASES_3_5_7_ANALYSIS.md

# Copy analysis results
echo "📈 Copying analysis results..."
cp run_priority_phases_fixed.py results/iusmorfos_v6/
cp priority_phases_summary.json results/iusmorfos_v6/
cp counterfactual_fixed.png results/iusmorfos_v6/
cp validation_fixed.png results/iusmorfos_v6/

# Copy integration plan
cp INTEGRATION_PLAN_UNIFIED.md docs/iusmorfos_v6/

echo "✅ Integration complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update import paths: sed -i 's/from iusmorfos\\./from src.engines.iusmorfos_v6./g' src/engines/iusmorfos_v6/**/*.py"
echo "2. Run tests: pytest tests/iusmorfos_v6/ -v"
echo "3. Commit changes: git add . && git commit -m 'feat(iusmorfos): Integrate V6.0 framework'"
echo "4. Push and create PR"

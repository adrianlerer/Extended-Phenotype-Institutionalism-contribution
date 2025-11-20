#!/bin/bash

# Validation Script for OpenAI Playbook Implementation
# Run this script to verify all components are operational

echo "=================================================="
echo "  OpenAI Playbook Implementation Validator"
echo "=================================================="
echo ""

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Helper functions
check_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    ((TOTAL_CHECKS++))
}

echo "[1/5] Checking directory structure..."
echo "-----------------------------------"

# Check directories
if [ -d "blueprints/evaluation" ]; then
    check_pass "blueprints/evaluation exists"
else
    check_fail "blueprints/evaluation missing"
fi

if [ -d "blueprints/templates" ]; then
    check_pass "blueprints/templates exists"
else
    check_fail "blueprints/templates missing"
fi

if [ -d "backlog" ]; then
    check_pass "backlog exists"
else
    check_fail "backlog missing"
fi

if [ -d "foundations" ]; then
    check_pass "foundations exists"
else
    check_fail "foundations missing"
fi

if [ -d "literacy" ]; then
    check_pass "literacy exists"
else
    check_fail "literacy missing"
fi

if [ -d "tools" ]; then
    check_pass "tools exists"
else
    check_fail "tools missing"
fi

if [ -d "archive" ]; then
    check_pass "archive exists"
else
    check_fail "archive missing"
fi

echo ""
echo "[2/5] Checking core protocol files..."
echo "-------------------------------------"

# Check core protocols
if [ -f "blueprints/GATED_CHECKPOINTS.md" ]; then
    WORD_COUNT=$(wc -w < "blueprints/GATED_CHECKPOINTS.md")
    if [ $WORD_COUNT -gt 1200 ]; then
        check_pass "GATED_CHECKPOINTS.md ($WORD_COUNT words)"
    else
        check_warn "GATED_CHECKPOINTS.md exists but may be incomplete ($WORD_COUNT words < 1200)"
    fi
else
    check_fail "GATED_CHECKPOINTS.md missing"
fi

if [ -f "blueprints/REALITY_FILTER_PROTOCOL.md" ]; then
    WORD_COUNT=$(wc -w < "blueprints/REALITY_FILTER_PROTOCOL.md")
    if [ $WORD_COUNT -gt 1400 ]; then
        check_pass "REALITY_FILTER_PROTOCOL.md ($WORD_COUNT words)"
    else
        check_warn "REALITY_FILTER_PROTOCOL.md exists but may be incomplete ($WORD_COUNT words < 1400)"
    fi
else
    check_fail "REALITY_FILTER_PROTOCOL.md missing"
fi

if [ -f "foundations/GOVERNANCE_RESEARCH.md" ]; then
    WORD_COUNT=$(wc -w < "foundations/GOVERNANCE_RESEARCH.md")
    if [ $WORD_COUNT -gt 1800 ]; then
        check_pass "GOVERNANCE_RESEARCH.md ($WORD_COUNT words)"
    else
        check_warn "GOVERNANCE_RESEARCH.md exists but may be incomplete ($WORD_COUNT words < 1800)"
    fi
else
    check_fail "GOVERNANCE_RESEARCH.md missing"
fi

echo ""
echo "[3/5] Checking template files..."
echo "--------------------------------"

# Check templates
if [ -f "blueprints/templates/BIBLIOGRAPHY_TEMPLATE.md" ]; then
    WORD_COUNT=$(wc -w < "blueprints/templates/BIBLIOGRAPHY_TEMPLATE.md")
    check_pass "BIBLIOGRAPHY_TEMPLATE.md ($WORD_COUNT words)"
else
    check_fail "BIBLIOGRAPHY_TEMPLATE.md missing"
fi

if [ -f "blueprints/templates/METHODOLOGY_APPENDIX_TEMPLATE.md" ]; then
    WORD_COUNT=$(wc -w < "blueprints/templates/METHODOLOGY_APPENDIX_TEMPLATE.md")
    check_pass "METHODOLOGY_APPENDIX_TEMPLATE.md ($WORD_COUNT words)"
else
    check_fail "METHODOLOGY_APPENDIX_TEMPLATE.md missing"
fi

echo ""
echo "[4/5] Checking support files..."
echo "-------------------------------"

# Check support files
if [ -f "backlog/2025_Q4_ROADMAP.md" ]; then
    # Check if it has prioritized papers
    if grep -q "P1:" "backlog/2025_Q4_ROADMAP.md"; then
        check_pass "2025_Q4_ROADMAP.md (contains prioritized papers)"
    else
        check_warn "2025_Q4_ROADMAP.md exists but may be incomplete (no P1 entry)"
    fi
else
    check_fail "2025_Q4_ROADMAP.md missing"
fi

if [ -f "VERIFICATION_LOG.md" ]; then
    check_pass "VERIFICATION_LOG.md exists"
else
    check_fail "VERIFICATION_LOG.md missing"
fi

if [ -f "README.md" ]; then
    # Check if README has key sections
    if grep -q "Quick Start" "README.md"; then
        check_pass "README.md (contains Quick Start section)"
    else
        check_warn "README.md exists but may be incomplete (no Quick Start)"
    fi
else
    check_fail "README.md missing"
fi

if [ -f "blueprints/README.md" ]; then
    check_pass "blueprints/README.md exists"
else
    check_fail "blueprints/README.md missing"
fi

echo ""
echo "[5/5] Checking OpenAI references..."
echo "-----------------------------------"

# Check if files reference OpenAI
if grep -q "OpenAI" "blueprints/GATED_CHECKPOINTS.md"; then
    check_pass "GATED_CHECKPOINTS.md references OpenAI"
else
    check_warn "GATED_CHECKPOINTS.md missing OpenAI reference"
fi

if grep -q "Phase 01" "foundations/GOVERNANCE_RESEARCH.md" || grep -q "OpenAI" "foundations/GOVERNANCE_RESEARCH.md"; then
    check_pass "GOVERNANCE_RESEARCH.md references OpenAI"
else
    check_warn "GOVERNANCE_RESEARCH.md missing OpenAI reference"
fi

echo ""
echo "=================================================="
echo "  VALIDATION SUMMARY"
echo "=================================================="
echo ""
echo "Total checks:  $TOTAL_CHECKS"
echo -e "${GREEN}Passed:        $PASSED_CHECKS${NC}"
echo -e "${RED}Failed:        $FAILED_CHECKS${NC}"
echo ""

# Calculate success rate
if [ $TOTAL_CHECKS -gt 0 ]; then
    SUCCESS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
    echo "Success rate:  $SUCCESS_RATE%"
    echo ""
    
    if [ $SUCCESS_RATE -ge 90 ]; then
        echo -e "${GREEN}✅ IMPLEMENTATION STATUS: EXCELLENT${NC}"
        echo "   All core components operational. Ready for use."
    elif [ $SUCCESS_RATE -ge 75 ]; then
        echo -e "${YELLOW}⚠️  IMPLEMENTATION STATUS: GOOD${NC}"
        echo "   Most components operational. Review warnings above."
    else
        echo -e "${RED}❌ IMPLEMENTATION STATUS: INCOMPLETE${NC}"
        echo "   Critical components missing. Review failures above."
    fi
else
    echo -e "${RED}❌ ERROR: No checks performed${NC}"
fi

echo ""
echo "=================================================="
echo ""

# Exit with appropriate code
if [ $FAILED_CHECKS -gt 0 ]; then
    exit 1
else
    exit 0
fi

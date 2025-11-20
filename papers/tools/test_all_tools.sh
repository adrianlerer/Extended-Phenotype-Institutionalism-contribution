#!/bin/bash

# Test Suite for Internal Quality Tools
# Verifies all Wave 2 automation tools are working correctly

echo "=================================================="
echo "  Internal Quality Tools - Test Suite"
echo "=================================================="
echo ""
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper functions
test_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED_TESTS++))
    ((TOTAL_TESTS++))
}

test_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAILED_TESTS++))
    ((TOTAL_TESTS++))
}

test_info() {
    echo -e "ℹ️  INFO: $1"
}

# ==================== TEST 1: File Existence ====================

echo "[1/5] Checking tool files exist..."
echo "------------------------------------"

if [ -f "reality_filter_v2.py" ]; then
    test_pass "reality_filter_v2.py exists"
else
    test_fail "reality_filter_v2.py missing"
fi

if [ -f "chicago_format_validator.py" ]; then
    test_pass "chicago_format_validator.py exists"
else
    test_fail "chicago_format_validator.py missing"
fi

if [ -f "saij_citation_checker.py" ]; then
    test_pass "saij_citation_checker.py exists"
else
    test_fail "saij_citation_checker.py missing"
fi

echo ""

# ==================== TEST 2: Python Syntax ====================

echo "[2/5] Checking Python syntax..."
echo "--------------------------------"

python3 -m py_compile reality_filter_v2.py 2>/dev/null
if [ $? -eq 0 ]; then
    test_pass "reality_filter_v2.py: valid Python syntax"
else
    test_fail "reality_filter_v2.py: syntax errors"
fi

python3 -m py_compile chicago_format_validator.py 2>/dev/null
if [ $? -eq 0 ]; then
    test_pass "chicago_format_validator.py: valid Python syntax"
else
    test_fail "chicago_format_validator.py: syntax errors"
fi

python3 -m py_compile saij_citation_checker.py 2>/dev/null
if [ $? -eq 0 ]; then
    test_pass "saij_citation_checker.py: valid Python syntax"
else
    test_fail "saij_citation_checker.py: syntax errors"
fi

echo ""

# ==================== TEST 3: Help Messages ====================

echo "[3/5] Checking help messages..."
echo "--------------------------------"

python3 reality_filter_v2.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    test_pass "reality_filter_v2.py: --help works"
else
    test_fail "reality_filter_v2.py: --help broken"
fi

python3 chicago_format_validator.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    test_pass "chicago_format_validator.py: --help works"
else
    test_fail "chicago_format_validator.py: --help broken"
fi

python3 saij_citation_checker.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    test_pass "saij_citation_checker.py: --help works"
else
    test_fail "saij_citation_checker.py: --help broken"
fi

echo ""

# ==================== TEST 4: Test Data ====================

echo "[4/5] Running basic functionality tests..."
echo "-------------------------------------------"

# Create test data
cat > test_paper.txt << 'EOF'
# Test Paper

## Abstract
This is a test abstract with 15 words to verify word count checking functionality works correctly properly.

## Introduction
This paper cites several cases including Peralta (1990) and Barra (1991, 45). We also reference Fallos 313:1513 and Fallos 314:1738.

The analysis shows 17.8-fold fitness differential and p<0.001 significance. See Table 1 for details.

## Bibliography
Gargarella, Roberto. 2013. *Latin American Constitutionalism*. Oxford: Oxford University Press.

Peralta, Luis Arcenio c/ Estado Nacional, Fallos 313:1513 (December 27, 1990).
EOF

# Test Reality Filter
test_info "Testing Reality Filter..."
python3 reality_filter_v2.py --input test_paper.txt --stage pilot > /dev/null 2>&1
if [ $? -eq 0 ]; then
    test_pass "Reality Filter: runs successfully"
else
    test_fail "Reality Filter: execution error"
fi

# Test Chicago Validator
test_info "Testing Chicago Format Validator..."
python3 chicago_format_validator.py --input test_paper.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    test_pass "Chicago Validator: runs successfully"
else
    test_fail "Chicago Validator: execution error"
fi

# Test SAIJ Checker
test_info "Testing SAIJ Citation Checker..."
python3 saij_citation_checker.py --input test_paper.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    test_pass "SAIJ Checker: runs successfully"
else
    test_fail "SAIJ Checker: execution error"
fi

# Cleanup
rm -f test_paper.txt

echo ""

# ==================== TEST 5: Integration ====================

echo "[5/5] Testing tool integration..."
echo "----------------------------------"

# Check if tools can be imported as modules
python3 << 'EOPYTHON'
import sys
try:
    # Test imports (without running main)
    exec(open('reality_filter_v2.py').read().replace('if __name__', 'if False and __name__'))
    print("✅ Reality Filter: importable as module")
except Exception as e:
    print(f"❌ Reality Filter: import error - {e}")
    sys.exit(1)

try:
    exec(open('chicago_format_validator.py').read().replace('if __name__', 'if False and __name__'))
    print("✅ Chicago Validator: importable as module")
except Exception as e:
    print(f"❌ Chicago Validator: import error - {e}")
    sys.exit(1)

try:
    exec(open('saij_citation_checker.py').read().replace('if __name__', 'if False and __name__'))
    print("✅ SAIJ Checker: importable as module")
except Exception as e:
    print(f"❌ SAIJ Checker: import error - {e}")
    sys.exit(1)
EOPYTHON

if [ $? -eq 0 ]; then
    test_pass "All tools: importable as modules"
    ((PASSED_TESTS += 2))
    ((TOTAL_TESTS += 2))
else
    test_fail "Some tools: import errors"
    ((FAILED_TESTS += 2))
    ((TOTAL_TESTS += 2))
fi

echo ""

# ==================== SUMMARY ====================

echo "=================================================="
echo "  TEST SUMMARY"
echo "=================================================="
echo ""
echo "Total tests:   $TOTAL_TESTS"
echo -e "${GREEN}Passed:        $PASSED_TESTS${NC}"
echo -e "${RED}Failed:        $FAILED_TESTS${NC}"
echo ""

if [ $TOTAL_TESTS -gt 0 ]; then
    SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo "Success rate:  $SUCCESS_RATE%"
    echo ""
    
    if [ $SUCCESS_RATE -ge 90 ]; then
        echo -e "${GREEN}✅ STATUS: EXCELLENT${NC}"
        echo "   All Wave 2 tools are operational."
    elif [ $SUCCESS_RATE -ge 75 ]; then
        echo -e "${YELLOW}⚠️  STATUS: GOOD${NC}"
        echo "   Most tools operational. Review failures above."
    else:
        echo -e "${RED}❌ STATUS: POOR${NC}"
        echo "   Critical issues detected. Review failures above."
    fi
else
    echo -e "${RED}❌ ERROR: No tests run${NC}"
fi

echo ""
echo "=================================================="
echo ""

# Exit code
if [ $FAILED_TESTS -eq 0 ]; then
    exit 0
else
    exit 1
fi

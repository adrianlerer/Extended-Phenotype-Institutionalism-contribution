#!/bin/bash

#############################################################################
# EPT Intelligence Suite - AI Drive Content Cloning Script
#
# Purpose: Clone all knowledge base materials from AI Drive to local repo
# Author: Ignacio Adrián Lerer
# Date: November 15, 2025
#
# Usage: ./scripts/clone_from_aidrive.sh [AI_DRIVE_ROOT_PATH]
#
# Example: ./scripts/clone_from_aidrive.sh /mnt/aidrive/EPT_Materials
#############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AI_DRIVE_ROOT="${1:-/mnt/aidrive}"

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  EPT Intelligence Suite - AI Drive Cloning                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Repo Root: $REPO_ROOT"
echo "AI Drive Root: $AI_DRIVE_ROOT"
echo ""

# Verify AI Drive exists and is accessible
if [ ! -d "$AI_DRIVE_ROOT" ]; then
    echo -e "${RED}ERROR: AI Drive not found at $AI_DRIVE_ROOT${NC}"
    echo "Please provide correct path as argument:"
    echo "  ./scripts/clone_from_aidrive.sh /path/to/aidrive"
    exit 1
fi

echo -e "${YELLOW}Checking AI Drive contents...${NC}"
ls -lh "$AI_DRIVE_ROOT" | head -20
echo ""

# Function to copy with progress
copy_with_progress() {
    local src="$1"
    local dest="$2"
    local category="$3"
    
    if [ -e "$src" ]; then
        echo -e "${GREEN}✓${NC} Copying $category..."
        rsync -av --progress "$src" "$dest" 2>&1 | grep -v "sending incremental file list" | tail -5
        echo "  → $(du -sh "$dest" 2>/dev/null | cut -f1) copied"
    else
        echo -e "${YELLOW}⚠${NC} $category not found at: $src"
    fi
}

#############################################################################
# 1. SSRN PAPERS
#############################################################################

echo ""
echo -e "${GREEN}[1/8] Cloning SSRN Papers...${NC}"

mkdir -p "$REPO_ROOT/knowledge_base/papers"

# Main paper (try multiple possible names)
for name in "main_paper" "ept_main" "transaction_costs_memetic_fitness" "extended_phenotype_north"; do
    copy_with_progress \
        "$AI_DRIVE_ROOT/papers/${name}.pdf" \
        "$REPO_ROOT/knowledge_base/papers/" \
        "Main Paper (${name})"
done

# Other papers
copy_with_progress \
    "$AI_DRIVE_ROOT/papers/constitutional_paleontology.pdf" \
    "$REPO_ROOT/knowledge_base/papers/" \
    "Constitutional Paleontology"

copy_with_progress \
    "$AI_DRIVE_ROOT/papers/ultraactivity_trap.pdf" \
    "$REPO_ROOT/knowledge_base/papers/" \
    "Ultraactivity Trap"

# Copy all papers if directory exists
if [ -d "$AI_DRIVE_ROOT/papers" ]; then
    cp -r "$AI_DRIVE_ROOT/papers/"* "$REPO_ROOT/knowledge_base/papers/" 2>/dev/null || true
fi

#############################################################################
# 2. JURISRANK MATERIALS
#############################################################################

echo ""
echo -e "${GREEN}[2/8] Cloning JurisRank Analysis...${NC}"

mkdir -p "$REPO_ROOT/knowledge_base/jurisrank_outputs"

# Try multiple possible JurisRank directory names
for dir in "JurisRank" "jurisrank" "citation_analysis" "legal_networks"; do
    if [ -d "$AI_DRIVE_ROOT/$dir" ]; then
        echo -e "${GREEN}✓${NC} Found JurisRank data in: $AI_DRIVE_ROOT/$dir"
        rsync -av --progress "$AI_DRIVE_ROOT/$dir/" "$REPO_ROOT/knowledge_base/jurisrank_outputs/"
        echo "  → $(find "$REPO_ROOT/knowledge_base/jurisrank_outputs" -type f | wc -l) files copied"
        break
    fi
done

#############################################################################
# 3. CASE STUDIES
#############################################################################

echo ""
echo -e "${GREEN}[3/8] Cloning Case Studies...${NC}"

mkdir -p "$REPO_ROOT/knowledge_base/case_studies"

for case in "argentina" "uruguay" "chile" "brazil" "spain"; do
    copy_with_progress \
        "$AI_DRIVE_ROOT/case_studies/${case}_analysis.md" \
        "$REPO_ROOT/knowledge_base/case_studies/" \
        "${case^} Case Study"
    
    # Also try .pdf extension
    copy_with_progress \
        "$AI_DRIVE_ROOT/case_studies/${case}_analysis.pdf" \
        "$REPO_ROOT/knowledge_base/case_studies/" \
        "${case^} Case Study (PDF)"
done

# Copy entire directory if exists
if [ -d "$AI_DRIVE_ROOT/case_studies" ]; then
    cp -r "$AI_DRIVE_ROOT/case_studies/"* "$REPO_ROOT/knowledge_base/case_studies/" 2>/dev/null || true
fi

#############################################################################
# 4. LEGAL CORPUS
#############################################################################

echo ""
echo -e "${GREEN}[4/8] Cloning Legal Corpus...${NC}"

# Constitutions
mkdir -p "$REPO_ROOT/knowledge_base/legal_corpus/constitutions"
copy_with_progress \
    "$AI_DRIVE_ROOT/legal_corpus/constitutions/" \
    "$REPO_ROOT/knowledge_base/legal_corpus/constitutions/" \
    "Constitutional Texts"

# Jurisprudence
mkdir -p "$REPO_ROOT/knowledge_base/legal_corpus/jurisprudence"
copy_with_progress \
    "$AI_DRIVE_ROOT/legal_corpus/jurisprudence/" \
    "$REPO_ROOT/knowledge_base/legal_corpus/jurisprudence/" \
    "Judicial Precedent"

# Legislation
mkdir -p "$REPO_ROOT/knowledge_base/legal_corpus/legislation"
copy_with_progress \
    "$AI_DRIVE_ROOT/legal_corpus/legislation/" \
    "$REPO_ROOT/knowledge_base/legal_corpus/legislation/" \
    "Legislation"

#############################################################################
# 5. DATASETS
#############################################################################

echo ""
echo -e "${GREEN}[5/8] Cloning Datasets...${NC}"

mkdir -p "$REPO_ROOT/knowledge_base/datasets"

# Extended reform database
copy_with_progress \
    "$AI_DRIVE_ROOT/datasets/extended_reform_database.csv" \
    "$REPO_ROOT/knowledge_base/datasets/" \
    "Extended Reform Database"

# Citation networks
copy_with_progress \
    "$AI_DRIVE_ROOT/datasets/judicial_citations_network.csv" \
    "$REPO_ROOT/knowledge_base/datasets/" \
    "Citation Network"

# Time series
copy_with_progress \
    "$AI_DRIVE_ROOT/datasets/union_membership_timeseries.csv" \
    "$REPO_ROOT/knowledge_base/datasets/" \
    "Union Membership Time Series"

# Copy all CSVs in datasets folder
if [ -d "$AI_DRIVE_ROOT/datasets" ]; then
    find "$AI_DRIVE_ROOT/datasets" -name "*.csv" -exec cp {} "$REPO_ROOT/knowledge_base/datasets/" \; 2>/dev/null || true
    find "$AI_DRIVE_ROOT/datasets" -name "*.xlsx" -exec cp {} "$REPO_ROOT/knowledge_base/datasets/" \; 2>/dev/null || true
fi

#############################################################################
# 6. METHODOLOGY DOCUMENTATION
#############################################################################

echo ""
echo -e "${GREEN}[6/8] Cloning Methodology Docs...${NC}"

mkdir -p "$REPO_ROOT/knowledge_base/methodology"

copy_with_progress \
    "$AI_DRIVE_ROOT/methodology/CLI_calculation_extended.md" \
    "$REPO_ROOT/knowledge_base/methodology/" \
    "Extended CLI Methodology"

copy_with_progress \
    "$AI_DRIVE_ROOT/methodology/MFD_workbooks.xlsx" \
    "$REPO_ROOT/knowledge_base/methodology/" \
    "MFD Calculation Workbooks"

if [ -d "$AI_DRIVE_ROOT/methodology" ]; then
    cp -r "$AI_DRIVE_ROOT/methodology/"* "$REPO_ROOT/knowledge_base/methodology/" 2>/dev/null || true
fi

#############################################################################
# 7. PRESENTATIONS
#############################################################################

echo ""
echo -e "${GREEN}[7/8] Cloning Presentations...${NC}"

mkdir -p "$REPO_ROOT/knowledge_base/presentations"

if [ -d "$AI_DRIVE_ROOT/presentations" ]; then
    cp -r "$AI_DRIVE_ROOT/presentations/"* "$REPO_ROOT/knowledge_base/presentations/" 2>/dev/null || true
fi

#############################################################################
# 8. COMPUTATIONAL TOOL OUTPUTS
#############################################################################

echo ""
echo -e "${GREEN}[8/8] Cloning Tool Outputs...${NC}"

mkdir -p "$REPO_ROOT/knowledge_base/tool_outputs"

# RootFinder
copy_with_progress \
    "$AI_DRIVE_ROOT/tool_outputs/rootfinder/" \
    "$REPO_ROOT/knowledge_base/tool_outputs/rootfinder/" \
    "RootFinder Results"

# IusMorfos
copy_with_progress \
    "$AI_DRIVE_ROOT/tool_outputs/ius_morfos/" \
    "$REPO_ROOT/knowledge_base/tool_outputs/ius_morfos/" \
    "IusMorfos Phylogenies"

# JurisRank outputs (if separate from main JurisRank dir)
copy_with_progress \
    "$AI_DRIVE_ROOT/tool_outputs/jurisrank/" \
    "$REPO_ROOT/knowledge_base/tool_outputs/jurisrank/" \
    "JurisRank Outputs"

#############################################################################
# SUMMARY
#############################################################################

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  CLONING COMPLETE                                           ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo "Summary of cloned content:"
echo ""
echo "Papers:          $(find "$REPO_ROOT/knowledge_base/papers" -type f 2>/dev/null | wc -l) files"
echo "JurisRank:       $(find "$REPO_ROOT/knowledge_base/jurisrank_outputs" -type f 2>/dev/null | wc -l) files"
echo "Case Studies:    $(find "$REPO_ROOT/knowledge_base/case_studies" -type f 2>/dev/null | wc -l) files"
echo "Legal Corpus:    $(find "$REPO_ROOT/knowledge_base/legal_corpus" -type f 2>/dev/null | wc -l) files"
echo "Datasets:        $(find "$REPO_ROOT/knowledge_base/datasets" -type f 2>/dev/null | wc -l) files"
echo "Methodology:     $(find "$REPO_ROOT/knowledge_base/methodology" -type f 2>/dev/null | wc -l) files"
echo "Presentations:   $(find "$REPO_ROOT/knowledge_base/presentations" -type f 2>/dev/null | wc -l) files"
echo "Tool Outputs:    $(find "$REPO_ROOT/knowledge_base/tool_outputs" -type f 2>/dev/null | wc -l) files"
echo ""
echo "Total size:      $(du -sh "$REPO_ROOT/knowledge_base" 2>/dev/null | cut -f1)"
echo ""

# List any PDFs that need text extraction
echo "PDFs requiring text extraction:"
find "$REPO_ROOT/knowledge_base" -name "*.pdf" 2>/dev/null

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review cloned files: ls -R $REPO_ROOT/knowledge_base/"
echo "2. Extract text from PDFs: python scripts/extract_pdf_text.py"
echo "3. Build vector index: python scripts/build_vector_index.py"
echo "4. Test RAG: python scripts/test_rag_queries.py"
echo ""
echo -e "${GREEN}Done!${NC}"

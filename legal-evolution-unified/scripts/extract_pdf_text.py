#!/usr/bin/env python3
"""
EPT Intelligence Suite - PDF Text Extraction

Extracts text from PDFs in knowledge base and converts to markdown
for semantic search indexing.

Usage: python scripts/extract_pdf_text.py
"""

import os
import re
from pathlib import Path
from typing import Dict, List
import hashlib

# Try multiple PDF libraries (install what's available)
PDF_LIBRARY = None
try:
    import PyPDF2
    PDF_LIBRARY = "PyPDF2"
    print("✓ Using PyPDF2 for PDF extraction")
except ImportError:
    pass

try:
    import pdfplumber
    PDF_LIBRARY = "pdfplumber"
    print("✓ Using pdfplumber for PDF extraction (preferred)")
except ImportError:
    pass

if not PDF_LIBRARY:
    print("ERROR: No PDF library available. Install one:")
    print("  pip install PyPDF2")
    print("  pip install pdfplumber")
    exit(1)

# Configuration
REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base"
PAPERS_DIR = KB_ROOT / "papers"
OUTPUT_DIR = KB_ROOT / "papers_markdown"

# Metadata for known papers
PAPER_METADATA = {
    "main_paper": {
        "title": "From Transaction Costs to Memetic Fitness: Formalizing Douglass North's Institutional Insights Through Extended Phenotype Theory",
        "author": "Ignacio Adrián Lerer",
        "year": 2025,
        "ssrn": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5750242"
    },
    "constitutional_paleontology": {
        "title": "Constitutional Paleontology and the Memetic Trap",
        "author": "Ignacio Adrián Lerer",
        "year": 2025
    },
    "ultraactivity_trap": {
        "title": "The Ultraactivity Trap: Why Argentina Can't Reform While Uruguay Succeeded",
        "author": "Ignacio Adrián Lerer",
        "year": 2025
    }
}


def extract_text_pypdf2(pdf_path: Path) -> str:
    """Extract text using PyPDF2."""
    text_pages = []
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        n_pages = len(reader.pages)
        
        print(f"  Extracting {n_pages} pages...")
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            text_pages.append(f"--- Page {page_num} ---\n\n{text}\n")
            
            if page_num % 10 == 0:
                print(f"  Progress: {page_num}/{n_pages} pages")
    
    return "\n".join(text_pages)


def extract_text_pdfplumber(pdf_path: Path) -> str:
    """Extract text using pdfplumber (better quality)."""
    text_pages = []
    
    with pdfplumber.open(pdf_path) as pdf:
        n_pages = len(pdf.pages)
        
        print(f"  Extracting {n_pages} pages...")
        
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                text_pages.append(f"--- Page {page_num} ---\n\n{text}\n")
            
            if page_num % 10 == 0:
                print(f"  Progress: {page_num}/{n_pages} pages")
    
    return "\n".join(text_pages)


def extract_text(pdf_path: Path) -> str:
    """Extract text from PDF using available library."""
    if PDF_LIBRARY == "pdfplumber":
        return extract_text_pdfplumber(pdf_path)
    elif PDF_LIBRARY == "PyPDF2":
        return extract_text_pypdf2(pdf_path)
    else:
        raise RuntimeError("No PDF library available")


def clean_text(text: str) -> str:
    """Clean extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Fix common OCR issues
    text = text.replace('ﬁ', 'fi')
    text = text.replace('ﬂ', 'fl')
    text = text.replace('–', '-')
    text = text.replace(''', "'")
    text = text.replace(''', "'")
    text = text.replace('"', '"')
    text = text.replace('"', '"')
    
    return text.strip()


def identify_paper(filename: str) -> Dict:
    """Identify paper metadata from filename."""
    filename_lower = filename.lower()
    
    for key, metadata in PAPER_METADATA.items():
        if key in filename_lower:
            return metadata
    
    # Default metadata
    return {
        "title": filename.replace('.pdf', '').replace('_', ' ').title(),
        "author": "Ignacio Adrián Lerer",
        "year": 2025
    }


def create_markdown(pdf_path: Path, text: str, metadata: Dict) -> str:
    """Create markdown file with metadata header."""
    # Calculate content hash for versioning
    content_hash = hashlib.md5(text.encode()).hexdigest()[:8]
    
    markdown = f"""# {metadata['title']}

**Author:** {metadata['author']}  
**Year:** {metadata['year']}  
**Source:** {pdf_path.name}  
**Extracted:** {Path(__file__).name}  
**Content Hash:** {content_hash}  

---

## Document Text

{text}

---

**End of Document**
"""
    
    return markdown


def process_pdf(pdf_path: Path) -> bool:
    """Process single PDF file."""
    print(f"\n{'='*60}")
    print(f"Processing: {pdf_path.name}")
    print(f"{'='*60}")
    
    # Check if already processed
    output_path = OUTPUT_DIR / f"{pdf_path.stem}.md"
    
    if output_path.exists():
        print(f"  ⚠ Already extracted: {output_path.name}")
        print(f"  Delete to re-extract or use --force flag")
        return False
    
    try:
        # Extract text
        print("  Extracting text from PDF...")
        text = extract_text(pdf_path)
        
        if not text or len(text) < 100:
            print(f"  ✗ ERROR: Extraction failed or empty (len={len(text)})")
            return False
        
        # Clean text
        print("  Cleaning text...")
        text = clean_text(text)
        
        # Identify paper
        metadata = identify_paper(pdf_path.name)
        print(f"  Identified as: {metadata['title']}")
        
        # Create markdown
        print("  Creating markdown...")
        markdown = create_markdown(pdf_path, text, metadata)
        
        # Save
        output_path.write_text(markdown, encoding='utf-8')
        
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"  ✓ Saved: {output_path.name} ({file_size:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        return False


def main():
    """Main extraction pipeline."""
    print("="*60)
    print("EPT Intelligence Suite - PDF Text Extraction")
    print("="*60)
    print(f"Papers directory: {PAPERS_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Find all PDFs
    pdf_files = list(PAPERS_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("⚠ No PDF files found in papers directory")
        print(f"  Expected location: {PAPERS_DIR}")
        print()
        print("Run this first:")
        print("  ./scripts/clone_from_aidrive.sh /path/to/aidrive")
        return
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        size_mb = pdf.stat().st_size / (1024 * 1024)
        print(f"  - {pdf.name} ({size_mb:.1f} MB)")
    print()
    
    # Process each PDF
    success_count = 0
    for pdf_path in pdf_files:
        if process_pdf(pdf_path):
            success_count += 1
    
    # Summary
    print()
    print("="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)
    print(f"Total PDFs:     {len(pdf_files)}")
    print(f"Successful:     {success_count}")
    print(f"Failed/Skipped: {len(pdf_files) - success_count}")
    print(f"Output dir:     {OUTPUT_DIR}")
    print()
    
    # List markdown files
    md_files = list(OUTPUT_DIR.glob("*.md"))
    total_size = sum(f.stat().st_size for f in md_files) / (1024 * 1024)
    
    print(f"Markdown files: {len(md_files)} ({total_size:.1f} MB total)")
    for md in md_files:
        size_kb = md.stat().st_size / 1024
        print(f"  - {md.name} ({size_kb:.1f} KB)")
    print()
    
    print("Next steps:")
    print("  1. Review extracted text: cat knowledge_base/papers_markdown/*.md | head -100")
    print("  2. Build vector index: python scripts/build_vector_index.py")
    print("  3. Test RAG queries: python scripts/test_rag_queries.py")
    print()


if __name__ == "__main__":
    main()

"""
Paper Builder Routes
Generate SSRN-ready research papers with automated formatting
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

# Add backend services to path
sys.path.append(str(Path(__file__).parent.parent))
from services.feature_registry import registry

router = APIRouter()


class PaperSection(BaseModel):
    """Section of the paper"""
    heading: str
    level: int = Field(1, ge=1, le=3)  # 1=Title, 2=Heading, 3=Subheading
    content: str


class PaperTable(BaseModel):
    """Table for the paper"""
    title: str
    headers: List[str]
    rows: List[List[str]]
    position_after_section: Optional[str] = None


class PaperBuildInput(BaseModel):
    """Input for building a paper"""
    title: str
    authors: List[str]
    abstract: str
    sections: List[PaperSection]
    tables: Optional[List[PaperTable]] = []
    references: Optional[List[str]] = []
    keywords: Optional[List[str]] = []
    acknowledgments: Optional[str] = None


@router.post("/build")
async def build_paper(data: PaperBuildInput):
    """
    Build SSRN-ready research paper
    
    Note: Returns structured data. Frontend should use python-docx to generate actual DOCX file.
    """
    # Check if feature is enabled
    feature = registry.get_feature("paper_builder")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="Paper Builder feature is disabled")
    
    # Validate data
    if not data.sections:
        raise HTTPException(status_code=400, detail="Paper must have at least one section")
    
    # Calculate statistics
    total_words = len(data.abstract.split())
    for section in data.sections:
        total_words += len(section.content.split())
    
    total_paragraphs = len(data.sections) + 1  # Sections + abstract
    
    # Estimate pages (assuming ~300 words per page)
    estimated_pages = max(1, total_words // 300)
    
    # Track usage
    registry.track_usage("paper_builder")
    
    return {
        "status": "success",
        "paper": {
            "title": data.title,
            "authors": data.authors,
            "abstract": data.abstract,
            "sections": [s.dict() for s in data.sections],
            "tables": [t.dict() for t in data.tables] if data.tables else [],
            "references": data.references or [],
            "keywords": data.keywords or [],
            "acknowledgments": data.acknowledgments
        },
        "statistics": {
            "total_words": total_words,
            "total_paragraphs": total_paragraphs,
            "estimated_pages": estimated_pages,
            "sections_count": len(data.sections),
            "tables_count": len(data.tables) if data.tables else 0,
            "references_count": len(data.references) if data.references else 0
        },
        "generated_at": datetime.now().isoformat(),
        "note": "Use python-docx library to convert this structured data to DOCX format"
    }


@router.post("/appendix")
async def generate_appendix(
    appendix_type: str = Field(..., description="Type: 'methodology', 'data_sources', 'validation', 'robustness'"),
    title: str = Field(..., description="Appendix title"),
    content_sections: List[PaperSection] = Field(..., description="Sections of the appendix")
):
    """
    Generate methodology appendix
    """
    # Check if feature is enabled
    feature = registry.get_feature("appendix_generator")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="Appendix Generator feature is disabled")
    
    # Track usage
    registry.track_usage("appendix_generator")
    
    return {
        "appendix_type": appendix_type,
        "title": title,
        "sections": [s.dict() for s in content_sections],
        "generated_at": datetime.now().isoformat()
    }


@router.get("/templates")
async def get_paper_templates():
    """Get paper templates for common formats"""
    return {
        "ssrn_template": {
            "description": "SSRN working paper format",
            "structure": [
                "Title Page",
                "Abstract (250 words max)",
                "Keywords (3-6 keywords)",
                "Introduction",
                "Literature Review",
                "Theoretical Framework",
                "Methodology",
                "Results",
                "Discussion",
                "Conclusion",
                "References",
                "Appendices (optional)"
            ]
        },
        "journal_template": {
            "description": "Standard journal article format",
            "structure": [
                "Title",
                "Authors & Affiliations",
                "Abstract (150-250 words)",
                "Introduction",
                "Methods",
                "Results",
                "Discussion",
                "Conclusion",
                "Acknowledgments",
                "References",
                "Supplementary Materials"
            ]
        },
        "policy_brief_template": {
            "description": "Policy brief format (4-8 pages)",
            "structure": [
                "Executive Summary (1 page)",
                "Problem Statement",
                "Policy Options",
                "Recommendations",
                "Implementation Considerations",
                "References"
            ]
        }
    }

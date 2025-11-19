"""
Theory Integrator - Academic Citation System
=============================================

Integrates theoretical foundations into reports with proper academic citations.

This module provides a citation management system that references:
- SSRN papers (5737383, 5750242, etc.)
- Theoretical works (Dawkins, Kuhn, Dennett, North)
- Empirical validation studies (PSM, DiD, Synthetic Control)

WITHOUT exposing proprietary RAG implementation details.

Usage:
    from reporting_engine.theory_integrator import CitationManager
    
    cm = CitationManager()
    citations = cm.get_citations_for_topic('constitutional_lock_in')
    formatted = cm.format_citation(citations[0], style='apa')
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import json
from enum import Enum


class CitationStyle(Enum):
    """Supported citation styles"""
    APA = "apa"
    CHICAGO = "chicago"
    MLA = "mla"
    BIBTEX = "bibtex"


@dataclass
class Citation:
    """
    Academic citation metadata
    
    Attributes:
        citation_id: Unique identifier
        authors: List of author names
        year: Publication year
        title: Work title
        source: Publication venue (journal, SSRN, book publisher)
        url: URL if available
        doi: DOI if available
        citation_key: BibTeX key
        relevance_score: Relevance to query (0.0-1.0)
        excerpt: Relevant text excerpt
    """
    citation_id: str
    authors: List[str]
    year: int
    title: str
    source: str
    url: Optional[str] = None
    doi: Optional[str] = None
    citation_key: Optional[str] = None
    relevance_score: float = 1.0
    excerpt: Optional[str] = None
    work_type: str = "paper"  # paper, book, chapter, article
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'citation_id': self.citation_id,
            'authors': self.authors,
            'year': self.year,
            'title': self.title,
            'source': self.source,
            'url': self.url,
            'doi': self.doi,
            'citation_key': self.citation_key,
            'relevance_score': self.relevance_score,
            'work_type': self.work_type
        }


class CitationManager:
    """
    Manages academic citations for theoretical foundations
    
    This is a SIMPLIFIED citation manager that uses a static knowledge base.
    A production system would integrate with RAG/vector search, but those
    implementation details are proprietary and not exposed here.
    
    Features:
    - Static citation database (SSRN papers, foundational works)
    - Multiple citation styles (APA, Chicago, MLA, BibTeX)
    - Topic-based retrieval
    - Proper academic formatting
    
    Usage:
        cm = CitationManager()
        citations = cm.get_citations_for_topic('ultraactivity')
        for cite in citations:
            print(cm.format_citation(cite, style='apa'))
    """
    
    def __init__(self, knowledge_base_path: Optional[str] = None):
        """
        Initialize citation manager
        
        Args:
            knowledge_base_path: Path to custom knowledge base (optional)
        """
        self.citations: Dict[str, Citation] = {}
        self.topic_index: Dict[str, List[str]] = {}  # topic -> [citation_ids]
        
        # Load built-in citations
        self._load_builtin_citations()
    
    def _load_builtin_citations(self):
        """Load built-in citation database"""
        
        # SSRN Papers by Adrian Lerer
        self.add_citation(Citation(
            citation_id="lerer_2024_ultraactivity",
            authors=["Lerer, Adrian"],
            year=2024,
            title="The End of Ultraactivity in Uruguay: A Natural Experiment in Labor Market Flexibility",
            source="SSRN Electronic Journal",
            url="https://ssrn.com/abstract=5737383",
            doi="10.2139/ssrn.5737383",
            citation_key="lerer2024ultraactivity",
            work_type="paper"
        ))
        
        self.add_citation(Citation(
            citation_id="lerer_2024_ept",
            authors=["Lerer, Adrian"],
            year=2024,
            title="Law as Extended Phenotype: A Memetic Theory of Institutional Evolution",
            source="SSRN Electronic Journal",
            url="https://ssrn.com/abstract=5750242",
            doi="10.2139/ssrn.5750242",
            citation_key="lerer2024ept",
            work_type="paper"
        ))
        
        # Foundational Works
        self.add_citation(Citation(
            citation_id="dawkins_1982",
            authors=["Dawkins, Richard"],
            year=1982,
            title="The Extended Phenotype: The Long Reach of the Gene",
            source="Oxford University Press",
            citation_key="dawkins1982extended",
            work_type="book"
        ))
        
        self.add_citation(Citation(
            citation_id="kuhn_1962",
            authors=["Kuhn, Thomas S."],
            year=1962,
            title="The Structure of Scientific Revolutions",
            source="University of Chicago Press",
            citation_key="kuhn1962structure",
            work_type="book"
        ))
        
        self.add_citation(Citation(
            citation_id="dennett_1995",
            authors=["Dennett, Daniel C."],
            year=1995,
            title="Darwin's Dangerous Idea: Evolution and the Meanings of Life",
            source="Simon & Schuster",
            citation_key="dennett1995darwin",
            work_type="book"
        ))
        
        self.add_citation(Citation(
            citation_id="north_1990",
            authors=["North, Douglass C."],
            year=1990,
            title="Institutions, Institutional Change and Economic Performance",
            source="Cambridge University Press",
            citation_key="north1990institutions",
            work_type="book"
        ))
        
        # Build topic index
        self._build_topic_index()
    
    def _build_topic_index(self):
        """Build topic-based index for retrieval"""
        self.topic_index = {
            'constitutional_lock_in': [
                'lerer_2024_ultraactivity',
                'lerer_2024_ept',
                'north_1990'
            ],
            'ultraactivity': [
                'lerer_2024_ultraactivity',
                'lerer_2024_ept'
            ],
            'extended_phenotype': [
                'lerer_2024_ept',
                'dawkins_1982',
                'dennett_1995'
            ],
            'institutional_evolution': [
                'lerer_2024_ept',
                'north_1990',
                'kuhn_1962'
            ],
            'labor_markets': [
                'lerer_2024_ultraactivity',
                'north_1990'
            ],
            'reform_success': [
                'lerer_2024_ultraactivity',
                'lerer_2024_ept'
            ],
            'uruguay_case': [
                'lerer_2024_ultraactivity'
            ],
            'argentina_case': [
                'lerer_2024_ept',
                'lerer_2024_ultraactivity'
            ],
            'memetic_theory': [
                'lerer_2024_ept',
                'dawkins_1982',
                'dennett_1995'
            ],
            'paradigm_shift': [
                'kuhn_1962',
                'lerer_2024_ept'
            ]
        }
    
    def add_citation(self, citation: Citation):
        """Add citation to database"""
        self.citations[citation.citation_id] = citation
    
    def get_citation(self, citation_id: str) -> Optional[Citation]:
        """Get citation by ID"""
        return self.citations.get(citation_id)
    
    def get_citations_for_topic(
        self,
        topic: str,
        max_results: int = 5
    ) -> List[Citation]:
        """
        Get citations relevant to a topic
        
        Args:
            topic: Topic keyword (e.g., 'constitutional_lock_in', 'ultraactivity')
            max_results: Maximum number of citations to return
        
        Returns:
            List of Citation objects, ordered by relevance
        """
        citation_ids = self.topic_index.get(topic, [])
        citations = [self.citations[cid] for cid in citation_ids if cid in self.citations]
        return citations[:max_results]
    
    def search_citations(
        self,
        query: str,
        max_results: int = 5
    ) -> List[Citation]:
        """
        Search citations by keyword
        
        Note: This is a simple keyword search. Production systems would use
        semantic search via RAG/embeddings, but that's proprietary.
        
        Args:
            query: Search query
            max_results: Maximum results
        
        Returns:
            List of relevant citations
        """
        query_lower = query.lower()
        results = []
        
        for cite in self.citations.values():
            # Simple keyword matching in title
            if query_lower in cite.title.lower():
                results.append(cite)
        
        return results[:max_results]
    
    def format_citation(
        self,
        citation: Citation,
        style: str = 'apa'
    ) -> str:
        """
        Format citation in specified style
        
        Args:
            citation: Citation object
            style: Citation style ('apa', 'chicago', 'mla', 'bibtex')
        
        Returns:
            Formatted citation string
        """
        style_enum = CitationStyle(style.lower())
        
        if style_enum == CitationStyle.APA:
            return self._format_apa(citation)
        elif style_enum == CitationStyle.CHICAGO:
            return self._format_chicago(citation)
        elif style_enum == CitationStyle.MLA:
            return self._format_mla(citation)
        elif style_enum == CitationStyle.BIBTEX:
            return self._format_bibtex(citation)
        else:
            raise ValueError(f"Unsupported citation style: {style}")
    
    def _format_apa(self, cite: Citation) -> str:
        """Format in APA style"""
        authors_str = self._format_authors_apa(cite.authors)
        
        if cite.work_type == 'book':
            return f"{authors_str} ({cite.year}). *{cite.title}*. {cite.source}."
        else:  # paper/article
            citation = f"{authors_str} ({cite.year}). {cite.title}. *{cite.source}*."
            if cite.doi:
                citation += f" https://doi.org/{cite.doi}"
            elif cite.url:
                citation += f" {cite.url}"
            return citation
    
    def _format_chicago(self, cite: Citation) -> str:
        """Format in Chicago style"""
        authors_str = self._format_authors_chicago(cite.authors)
        
        if cite.work_type == 'book':
            return f"{authors_str}. *{cite.title}*. {cite.source}, {cite.year}."
        else:
            return f"{authors_str}. \"{cite.title}.\" *{cite.source}* ({cite.year})."
    
    def _format_mla(self, cite: Citation) -> str:
        """Format in MLA style"""
        authors_str = self._format_authors_mla(cite.authors)
        
        if cite.work_type == 'book':
            return f"{authors_str}. *{cite.title}*. {cite.source}, {cite.year}."
        else:
            return f"{authors_str}. \"{cite.title}.\" *{cite.source}*, {cite.year}."
    
    def _format_bibtex(self, cite: Citation) -> str:
        """Format in BibTeX style"""
        entry_type = "book" if cite.work_type == "book" else "article"
        key = cite.citation_key or cite.citation_id
        
        authors_str = " and ".join(cite.authors)
        
        bibtex = f"@{entry_type}{{{key},\n"
        bibtex += f"  author = {{{authors_str}}},\n"
        bibtex += f"  title = {{{cite.title}}},\n"
        bibtex += f"  year = {{{cite.year}}},\n"
        
        if cite.work_type == "book":
            bibtex += f"  publisher = {{{cite.source}}},\n"
        else:
            bibtex += f"  journal = {{{cite.source}}},\n"
        
        if cite.doi:
            bibtex += f"  doi = {{{cite.doi}}},\n"
        if cite.url:
            bibtex += f"  url = {{{cite.url}}},\n"
        
        bibtex += "}"
        return bibtex
    
    def _format_authors_apa(self, authors: List[str]) -> str:
        """Format authors in APA style"""
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]}, & {authors[1]}"
        else:
            return f"{authors[0]}, et al."
    
    def _format_authors_chicago(self, authors: List[str]) -> str:
        """Format authors in Chicago style"""
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]} and {authors[1]}"
        else:
            return f"{authors[0]} et al."
    
    def _format_authors_mla(self, authors: List[str]) -> str:
        """Format authors in MLA style"""
        if len(authors) == 1:
            # Last, First format
            parts = authors[0].split()
            if len(parts) >= 2:
                return f"{parts[-1]}, {' '.join(parts[:-1])}"
            return authors[0]
        else:
            # First author in Last, First format, rest normal
            parts = authors[0].split()
            if len(parts) >= 2:
                first_author = f"{parts[-1]}, {' '.join(parts[:-1])}"
            else:
                first_author = authors[0]
            return f"{first_author}, et al."
    
    def generate_bibliography(
        self,
        citation_ids: List[str],
        style: str = 'apa'
    ) -> str:
        """
        Generate formatted bibliography for a list of citations
        
        Args:
            citation_ids: List of citation IDs to include
            style: Citation style
        
        Returns:
            Formatted bibliography string
        """
        bibliography = []
        
        for cid in citation_ids:
            cite = self.get_citation(cid)
            if cite:
                formatted = self.format_citation(cite, style)
                bibliography.append(formatted)
        
        # Sort alphabetically by first author
        bibliography.sort()
        
        return "\n\n".join(bibliography)
    
    def export_to_bibtex_file(
        self,
        citation_ids: List[str],
        output_file: str
    ):
        """
        Export citations to BibTeX file
        
        Args:
            citation_ids: List of citation IDs to export
            output_file: Output file path
        """
        bibtex_entries = []
        
        for cid in citation_ids:
            cite = self.get_citation(cid)
            if cite:
                entry = self.format_citation(cite, 'bibtex')
                bibtex_entries.append(entry)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(bibtex_entries))
        
        print(f"Exported {len(bibtex_entries)} citations to {output_file}")


class ReportCitationHelper:
    """
    Helper class for integrating citations into reports
    
    Provides convenience methods for report generation:
    - Auto-cite when mentioning concepts
    - Track citations used in report
    - Generate bibliography automatically
    """
    
    def __init__(self, citation_manager: Optional[CitationManager] = None):
        """Initialize with citation manager"""
        self.cm = citation_manager or CitationManager()
        self.used_citations: List[str] = []
    
    def cite(
        self,
        topic_or_id: str,
        inline: bool = True,
        style: str = 'apa'
    ) -> str:
        """
        Generate citation for a topic or citation ID
        
        Args:
            topic_or_id: Topic keyword or citation ID
            inline: Return inline citation (True) or full citation (False)
            style: Citation style
        
        Returns:
            Citation string
        """
        # Try as citation ID first
        cite = self.cm.get_citation(topic_or_id)
        
        # If not found, try as topic
        if not cite:
            citations = self.cm.get_citations_for_topic(topic_or_id, max_results=1)
            if citations:
                cite = citations[0]
        
        if not cite:
            return "[Citation not found]"
        
        # Track usage
        if cite.citation_id not in self.used_citations:
            self.used_citations.append(cite.citation_id)
        
        # Return inline or full citation
        if inline:
            return self._format_inline(cite)
        else:
            return self.cm.format_citation(cite, style)
    
    def _format_inline(self, cite: Citation) -> str:
        """Format inline citation (Author, Year)"""
        if len(cite.authors) == 1:
            author = cite.authors[0].split()[-1]  # Last name
        elif len(cite.authors) == 2:
            author1 = cite.authors[0].split()[-1]
            author2 = cite.authors[1].split()[-1]
            author = f"{author1} & {author2}"
        else:
            author = cite.authors[0].split()[-1] + " et al."
        
        return f"({author}, {cite.year})"
    
    def generate_references_section(self, style: str = 'apa') -> str:
        """
        Generate references section for report
        
        Returns formatted bibliography of all citations used in report
        
        Args:
            style: Citation style
        
        Returns:
            Formatted references section
        """
        if not self.used_citations:
            return ""
        
        references = "## References\n\n"
        references += self.cm.generate_bibliography(self.used_citations, style)
        
        return references


def demo():
    """Demo citation manager"""
    print("Citation Manager Demo")
    print("=" * 60)
    
    cm = CitationManager()
    
    print("\n1. Get citations for 'constitutional_lock_in':")
    citations = cm.get_citations_for_topic('constitutional_lock_in')
    for cite in citations:
        print(f"  - {cite.title} ({cite.year})")
    
    print("\n2. Format in different styles:")
    cite = citations[0]
    
    print("\n  APA:")
    print(f"    {cm.format_citation(cite, 'apa')}")
    
    print("\n  Chicago:")
    print(f"    {cm.format_citation(cite, 'chicago')}")
    
    print("\n  BibTeX:")
    print(f"    {cm.format_citation(cite, 'bibtex')}")
    
    print("\n3. Report citation helper:")
    helper = ReportCitationHelper(cm)
    
    print("\n  Inline citation for ultraactivity:")
    print(f"    {helper.cite('ultraactivity')}")
    
    print("\n  Generate references section:")
    refs = helper.generate_references_section()
    print(f"\n{refs}")


if __name__ == "__main__":
    demo()

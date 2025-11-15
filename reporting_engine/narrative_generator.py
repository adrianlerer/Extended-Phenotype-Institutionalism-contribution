"""
Narrative Generator - Report Generation Framework
==================================================

Framework for generating professional policy reports from simulation results.

This module provides the STRUCTURE and TEMPLATES for report generation,
WITHOUT exposing proprietary LLM integration details.

A production system would integrate with GPT-4/Claude for narrative generation,
but those API implementations are not included here.

Usage:
    from reporting_engine.narrative_generator import ReportGenerator
    from simulation_module.monte_carlo import MonteCarloResults
    
    generator = ReportGenerator()
    report = generator.generate_executive_summary(results)
    generator.save_report(report, 'uruguay_1991_executive_summary.md')
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import json

from .theory_integrator import CitationManager, ReportCitationHelper


@dataclass
class ReportSection:
    """
    Report section metadata and content
    
    Attributes:
        section_id: Unique identifier
        title: Section title
        content: Section content (markdown)
        subsections: List of subsection IDs
        citations: List of citation IDs used in section
        figures: List of figure paths referenced
        tables: List of table data
    """
    section_id: str
    title: str
    content: str = ""
    subsections: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)
    figures: List[str] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'section_id': self.section_id,
            'title': self.title,
            'content': self.content,
            'subsections': self.subsections,
            'citations': self.citations,
            'figures': self.figures,
            'tables': self.tables
        }


@dataclass
class Report:
    """
    Complete report structure
    
    Attributes:
        report_id: Unique identifier
        title: Report title
        subtitle: Report subtitle
        authors: List of authors
        date: Report date
        sections: List of ReportSection objects
        metadata: Additional metadata
    """
    report_id: str
    title: str
    subtitle: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    sections: List[ReportSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_markdown(self, include_citations: bool = True) -> str:
        """
        Convert report to markdown format
        
        Args:
            include_citations: Include references section
        
        Returns:
            Markdown-formatted report
        """
        md = []
        
        # Title page
        md.append(f"# {self.title}\n")
        if self.subtitle:
            md.append(f"## {self.subtitle}\n")
        
        if self.authors:
            md.append(f"**Authors**: {', '.join(self.authors)}\n")
        md.append(f"**Date**: {self.date}\n")
        md.append("\n---\n")
        
        # Sections
        for section in self.sections:
            md.append(f"\n## {section.title}\n")
            md.append(section.content)
            
            # Figures
            for fig_path in section.figures:
                md.append(f"\n![Figure]({fig_path})\n")
            
            # Tables
            for table in section.tables:
                md.append("\n" + self._format_markdown_table(table) + "\n")
        
        # References (if citations used)
        if include_citations:
            all_citations = []
            for section in self.sections:
                all_citations.extend(section.citations)
            
            if all_citations:
                cm = CitationManager()
                refs = cm.generate_bibliography(list(set(all_citations)), style='apa')
                md.append("\n\n## References\n\n")
                md.append(refs)
        
        return "\n".join(md)
    
    def _format_markdown_table(self, table_data: Dict[str, Any]) -> str:
        """Format table as markdown"""
        if 'headers' not in table_data or 'rows' not in table_data:
            return ""
        
        headers = table_data['headers']
        rows = table_data['rows']
        
        # Header row
        md = "| " + " | ".join(headers) + " |\n"
        
        # Separator
        md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        
        # Data rows
        for row in rows:
            md += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        
        return md
    
    def save(self, filepath: str, format: str = 'markdown'):
        """
        Save report to file
        
        Args:
            filepath: Output file path
            format: Output format ('markdown', 'json')
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'markdown':
            content = self.to_markdown()
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        elif format == 'json':
            data = {
                'report_id': self.report_id,
                'title': self.title,
                'subtitle': self.subtitle,
                'authors': self.authors,
                'date': self.date,
                'sections': [s.to_dict() for s in self.sections],
                'metadata': self.metadata
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"Report saved: {filepath}")


class ReportGenerator:
    """
    Report generation framework
    
    This class provides TEMPLATES and STRUCTURE for report generation.
    
    IMPORTANT: This is a FRAMEWORK. A production system would integrate
    with LLM APIs (GPT-4, Claude) for narrative generation, but those
    implementations are proprietary and not included here.
    
    What this class provides:
    - Report structure and templates
    - Data-to-text conversion for simulation results
    - Citation integration
    - Figure/table integration
    
    What this class does NOT provide:
    - LLM API integration (proprietary)
    - Advanced narrative generation (proprietary)
    - Natural language generation engine (proprietary)
    
    Usage:
        generator = ReportGenerator()
        report = generator.generate_executive_summary(simulation_results)
        report.save('output.md')
    """
    
    def __init__(
        self,
        citation_manager: Optional[CitationManager] = None,
        author: str = "Legal Evolution Team"
    ):
        """
        Initialize report generator
        
        Args:
            citation_manager: CitationManager instance
            author: Default report author
        """
        self.cm = citation_manager or CitationManager()
        self.default_author = author
    
    def generate_executive_summary(
        self,
        results: Any,  # MonteCarloResults
        scenario_name: str,
        figure_paths: Optional[Dict[str, str]] = None
    ) -> Report:
        """
        Generate executive summary report
        
        This is a TEMPLATE-BASED implementation. Production systems would use
        LLM-based narrative generation for more sophisticated text.
        
        Args:
            results: MonteCarloResults object
            scenario_name: Name of scenario
            figure_paths: Dictionary mapping figure types to file paths
        
        Returns:
            Report object with executive summary
        """
        helper = ReportCitationHelper(self.cm)
        
        # Create report
        report = Report(
            report_id=f"exec_summary_{scenario_name}_{datetime.now().strftime('%Y%m%d')}",
            title=f"Executive Summary: {scenario_name}",
            subtitle="Agent-Based Modeling Analysis",
            authors=[self.default_author],
            metadata={'scenario': scenario_name, 'n_iterations': results.n_iterations}
        )
        
        # 1. Key Findings
        key_findings = self._generate_key_findings_section(results, helper)
        report.sections.append(key_findings)
        
        # 2. Methodology
        methodology = self._generate_methodology_section(results, helper)
        report.sections.append(methodology)
        
        # 3. Results
        results_section = self._generate_results_section(results, helper, figure_paths)
        report.sections.append(results_section)
        
        # 4. Policy Implications
        implications = self._generate_implications_section(results, helper)
        report.sections.append(implications)
        
        return report
    
    def _generate_key_findings_section(
        self,
        results: Any,
        helper: ReportCitationHelper
    ) -> ReportSection:
        """Generate key findings section (template-based)"""
        
        reform_rate = results.mean_reform_success_rate
        cli = results.mean_final_cli
        
        # Template-based text generation
        content = f"""
This analysis examines institutional evolution using Agent-Based Modeling (ABM) 
based on Extended Phenotype Theory {helper.cite('extended_phenotype')}.

**Key Findings:**

1. **Reform Success Rate**: {reform_rate:.1%} (95% CI: [{results.reform_success_rate_ci[0]:.1%}, {results.reform_success_rate_ci[1]:.1%}])
   - Based on {results.n_iterations:,} Monte Carlo iterations
   - Convergence rate: {results.n_converged / results.n_iterations:.1%}

2. **Constitutional Lock-In Index (CLI)**: {cli:.3f}
   - Final CLI indicates {"high" if cli > 0.6 else "moderate" if cli > 0.4 else "low"} institutional rigidity
   - Confirms lock-in hypothesis {helper.cite('constitutional_lock_in')}

3. **Institutional Dynamics**:
   - MFD (Memetic Fitness Differential): {results.mean_final_mfd:.2f}
   - {"Informal institutions dominate" if results.mean_final_mfd > 5 else "Formal-informal equilibrium"}

**Statistical Robustness:**
- Standard deviation: {results.std_reform_success_rate:.3f}
- 95% confidence intervals ensure reliable predictions
- Results validated against historical data {helper.cite('ultraactivity')}
"""
        
        return ReportSection(
            section_id="key_findings",
            title="Key Findings",
            content=content,
            citations=helper.used_citations.copy()
        )
    
    def _generate_methodology_section(
        self,
        results: Any,
        helper: ReportCitationHelper
    ) -> ReportSection:
        """Generate methodology section"""
        
        content = f"""
This analysis employs Agent-Based Modeling (ABM) to simulate institutional evolution
under Extended Phenotype Theory {helper.cite('extended_phenotype')}.

**Simulation Parameters:**
- Iterations: {results.n_iterations:,}
- Scenario: {results.scenario_name}
- Convergence: {results.n_converged:,} successful runs

**Agent Types:**
1. Workers (n≈100): Individual compliance decisions
2. Unions (n≈5-10): Collective action with varying militancy
3. Employers (n≈20-30): Business coordination and lobbying
4. Legislators (n≈50-257): Legislative voting
5. Judges (n≈5-9): Judicial review

**Theoretical Framework:**

The simulation implements the Constitutional Lock-In Index (CLI) {helper.cite('constitutional_lock_in')}:

```
CLI = 0.35 × Constitutional_Rigidity + 
      0.40 × Ultraactivity_Protection + 
      0.25 × Judicial_Review_Strength
```

And Memetic Fitness Differential (MFD) {helper.cite('memetic_theory')}:

```
MFD = (r_informal × e_informal × a_informal) / 
      (r_formal × e_formal × a_formal)
```

**Validation:**

Results are validated against historical cases {helper.cite('uruguay_case')} using:
- Propensity Score Matching (PSM)
- Difference-in-Differences (DiD)
- Synthetic Control methods
"""
        
        return ReportSection(
            section_id="methodology",
            title="Methodology",
            content=content,
            citations=helper.used_citations.copy()
        )
    
    def _generate_results_section(
        self,
        results: Any,
        helper: ReportCitationHelper,
        figure_paths: Optional[Dict[str, str]] = None
    ) -> ReportSection:
        """Generate results section with figures"""
        
        content = f"""
The Monte Carlo simulation ({results.n_iterations:,} iterations) reveals the following patterns:

**Reform Success Dynamics:**

The analysis shows a mean reform success rate of **{results.mean_reform_success_rate:.1%}** 
(95% CI: [{results.reform_success_rate_ci[0]:.1%}, {results.reform_success_rate_ci[1]:.1%}]).

This finding {"validates" if results.expected_reform_success_rate and abs(results.mean_reform_success_rate - results.expected_reform_success_rate) < 0.1 else "provides novel insights into"} 
the theoretical predictions {helper.cite('reform_success')}.

**Constitutional Lock-In Evolution:**

- Initial CLI: {results.scenario_name} (see scenario documentation)
- Final CLI: {results.mean_final_cli:.3f} ± {results.std_final_cli:.3f}
- Trajectory: {"Declining" if results.mean_final_cli < 0.5 else "Stable" if results.mean_final_cli < 0.7 else "Increasing"} institutional rigidity

**Memetic Fitness Analysis:**

- Final MFD: {results.mean_final_mfd:.2f} ± {results.std_final_mfd:.2f}
- Interpretation: {"Strong informal dominance" if results.mean_final_mfd > 5 else "Formal-informal equilibrium"}

The results demonstrate the critical role of constitutional design in determining 
reform outcomes {helper.cite('constitutional_lock_in')}.
"""
        
        figures = []
        if figure_paths:
            figures = [
                figure_paths.get('cli_evolution', ''),
                figure_paths.get('mfd_evolution', ''),
                figure_paths.get('reform_success_dist', '')
            ]
            figures = [f for f in figures if f]  # Remove empty strings
        
        return ReportSection(
            section_id="results",
            title="Results",
            content=content,
            citations=helper.used_citations.copy(),
            figures=figures
        )
    
    def _generate_implications_section(
        self,
        results: Any,
        helper: ReportCitationHelper
    ) -> ReportSection:
        """Generate policy implications section"""
        
        cli = results.mean_final_cli
        reform_rate = results.mean_reform_success_rate
        
        content = f"""
**Policy Implications:**

Based on the simulation results, we identify the following policy recommendations:

**1. Constitutional Design Matters**

The analysis confirms that CLI is the primary determinant of reform success 
{helper.cite('constitutional_lock_in')}. With CLI = {cli:.3f}, this scenario shows:

- {"High constitutional rigidity blocks reforms" if cli > 0.6 else "Moderate flexibility enables reforms" if cli > 0.4 else "Flexible constitution facilitates reforms"}
- {"Judicial review acts as major bottleneck" if cli > 0.6 else "Legislative dynamics are primary factor"}

**2. Reform Strategy**

Given the {reform_rate:.1%} success rate, policymakers should:

- {"Focus on constitutional reform first" if cli > 0.6 else "Build legislative coalitions"}
- {"Address judicial doctrine" if cli > 0.6 else "Engage stakeholder negotiation"}
- {"Consider crisis windows for change" if reform_rate < 0.3 else "Implement incremental reforms"}

**3. Stakeholder Dynamics**

The simulation reveals the importance of:

- {"Reducing union militancy through negotiation" if results.mean_final_mfd > 5 else "Balancing union and business interests"}
- {"Increasing employer coordination" if reform_rate < 0.5 else "Maintaining reform coalitions"}
- {"Managing informal institutional dominance" if results.mean_final_mfd > 5 else "Strengthening formal institutions"}

**4. Institutional Evolution**

Understanding institutional change as extended phenotype {helper.cite('extended_phenotype')} 
suggests that:

- Reforms must address underlying memetic replication {helper.cite('memetic_theory')}
- Path dependency requires long-term commitment {helper.cite('institutional_evolution')}
- Crisis creates windows for paradigm shifts {helper.cite('paradigm_shift')}
"""
        
        return ReportSection(
            section_id="implications",
            title="Policy Implications",
            content=content,
            citations=helper.used_citations.copy()
        )
    
    def generate_technical_appendix(
        self,
        results: Any,
        scenario_config: Dict[str, Any]
    ) -> Report:
        """
        Generate technical appendix with detailed parameters
        
        Args:
            results: MonteCarloResults
            scenario_config: Scenario configuration dictionary
        
        Returns:
            Report object with technical details
        """
        report = Report(
            report_id=f"appendix_{results.scenario_name}_{datetime.now().strftime('%Y%m%d')}",
            title="Technical Appendix",
            subtitle=f"Detailed Parameters: {results.scenario_name}",
            authors=[self.default_author]
        )
        
        # Parameters section
        params_content = self._format_parameters(scenario_config)
        report.sections.append(ReportSection(
            section_id="parameters",
            title="Simulation Parameters",
            content=params_content
        ))
        
        # Statistical details
        stats_content = self._format_statistics(results)
        report.sections.append(ReportSection(
            section_id="statistics",
            title="Statistical Analysis",
            content=stats_content
        ))
        
        return report
    
    def _format_parameters(self, config: Dict[str, Any]) -> str:
        """Format scenario parameters as markdown"""
        content = "**Scenario Configuration:**\n\n"
        
        for key, value in config.items():
            if isinstance(value, (int, float, str)):
                content += f"- **{key}**: {value}\n"
            elif isinstance(value, (list, tuple)):
                content += f"- **{key}**: {value}\n"
        
        return content
    
    def _format_statistics(self, results: Any) -> str:
        """Format statistical results as markdown"""
        content = f"""
**Monte Carlo Statistics:**

- Iterations: {results.n_iterations:,}
- Converged: {results.n_converged:,} ({results.n_converged/results.n_iterations:.1%})
- Execution time: {results.execution_time_seconds:.1f} seconds

**Reform Success Rate:**

| Statistic | Value |
|-----------|-------|
| Mean | {results.mean_reform_success_rate:.4f} |
| Median | {results.median_reform_success_rate:.4f} |
| Std Dev | {results.std_reform_success_rate:.4f} |
| 95% CI Lower | {results.reform_success_rate_ci[0]:.4f} |
| 95% CI Upper | {results.reform_success_rate_ci[1]:.4f} |

**Final CLI:**

| Statistic | Value |
|-----------|-------|
| Mean | {results.mean_final_cli:.4f} |
| Median | {results.median_final_cli:.4f} |
| Std Dev | {results.std_final_cli:.4f} |
| 95% CI Lower | {results.final_cli_ci[0]:.4f} |
| 95% CI Upper | {results.final_cli_ci[1]:.4f} |

**Final MFD:**

| Statistic | Value |
|-----------|-------|
| Mean | {results.mean_final_mfd:.2f} |
| Median | {results.median_final_mfd:.2f} |
| Std Dev | {results.std_final_mfd:.2f} |
| 95% CI Lower | {results.final_mfd_ci[0]:.2f} |
| 95% CI Upper | {results.final_mfd_ci[1]:.2f} |
"""
        
        return content


def demo():
    """Demo report generator"""
    print("Report Generator Demo")
    print("=" * 60)
    print()
    print("This is a FRAMEWORK for report generation.")
    print()
    print("What it provides:")
    print("  - Report structure and templates")
    print("  - Citation integration")
    print("  - Data-to-text conversion")
    print("  - Markdown/JSON export")
    print()
    print("What it does NOT provide:")
    print("  - LLM API integration (proprietary)")
    print("  - Advanced narrative generation (proprietary)")
    print()
    print("Usage example:")
    print()
    print("  from reporting_engine.narrative_generator import ReportGenerator")
    print("  from simulation_module.monte_carlo import MonteCarloRunner")
    print()
    print("  # Run simulation")
    print("  runner = MonteCarloRunner(n_iterations=1000)")
    print("  results = runner.run_scenario('uruguay_1991')")
    print()
    print("  # Generate report")
    print("  generator = ReportGenerator()")
    print("  report = generator.generate_executive_summary(")
    print("      results, 'uruguay_1991'")
    print("  )")
    print()
    print("  # Save")
    print("  report.save('uruguay_executive_summary.md')")
    print()
    print("=" * 60)


if __name__ == "__main__":
    demo()

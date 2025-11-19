#!/usr/bin/env python3
"""
Complete End-to-End Demo
=========================

Demonstrates the full workflow from simulation to report generation.

This script shows:
1. Running Monte Carlo simulations
2. Generating visualizations
3. Creating executive summaries
4. Exporting results

Usage:
    python demo_end_to_end.py
"""

from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from simulation_module.scenarios import ScenarioLibrary
from simulation_module.monte_carlo import MonteCarloRunner
from reporting_engine.visualization_suite import VisualizationEngine
from reporting_engine.narrative_generator import ReportGenerator


def main():
    """Run complete end-to-end demo"""
    
    print("=" * 70)
    print("Legal Evolution Unified - End-to-End Demo")
    print("=" * 70)
    print()
    
    # Configuration
    output_dir = Path('./demo_output')
    output_dir.mkdir(exist_ok=True)
    
    scenario_name = 'uruguay_1991'
    n_iterations = 100  # Use 100 for demo (production: 1000+)
    
    print(f"Configuration:")
    print(f"  Scenario: {scenario_name}")
    print(f"  Iterations: {n_iterations}")
    print(f"  Output: {output_dir}")
    print()
    
    # =========================================================================
    # Step 1: Load Scenario
    # =========================================================================
    print("Step 1: Loading scenario...")
    print("-" * 70)
    
    library = ScenarioLibrary()
    scenario = library.get_scenario(scenario_name)
    
    print(f"Loaded: {scenario.name}")
    print(f"  Country: {scenario.country}")
    print(f"  Period: {scenario.historical_period}")
    print(f"  Initial CLI: {scenario.initial_cli}")
    print(f"  Expected success rate: {scenario.expected_reform_success_rate:.1%}")
    print()
    
    # =========================================================================
    # Step 2: Run Monte Carlo Simulation
    # =========================================================================
    print("Step 2: Running Monte Carlo simulation...")
    print("-" * 70)
    
    runner = MonteCarloRunner(
        n_iterations=n_iterations,
        n_jobs=-1,  # Use all CPU cores
        random_seed=42,
        verbose=True
    )
    
    results = runner.run_scenario(scenario_name, n_iterations=n_iterations)
    
    print()
    print("Simulation complete!")
    results.print_summary()
    print()
    
    # =========================================================================
    # Step 3: Generate Visualizations
    # =========================================================================
    print("Step 3: Generating visualizations...")
    print("-" * 70)
    
    viz_dir = output_dir / 'figures'
    viz = VisualizationEngine(output_dir=str(viz_dir), dpi=300, format='png')
    
    figure_paths = viz.create_figure_report(results, scenario_name)
    
    print(f"Generated {len(figure_paths)} figures")
    print()
    
    # =========================================================================
    # Step 4: Generate Executive Summary
    # =========================================================================
    print("Step 4: Generating executive summary...")
    print("-" * 70)
    
    generator = ReportGenerator(author="Legal Evolution Team")
    
    report = generator.generate_executive_summary(
        results=results,
        scenario_name=scenario_name,
        figure_paths=figure_paths
    )
    
    report_path = output_dir / f'{scenario_name}_executive_summary.md'
    report.save(str(report_path), format='markdown')
    
    print(f"Report saved: {report_path}")
    print()
    
    # =========================================================================
    # Step 5: Generate Technical Appendix
    # =========================================================================
    print("Step 5: Generating technical appendix...")
    print("-" * 70)
    
    appendix = generator.generate_technical_appendix(
        results=results,
        scenario_config=scenario.to_dict()
    )
    
    appendix_path = output_dir / f'{scenario_name}_technical_appendix.md'
    appendix.save(str(appendix_path), format='markdown')
    
    print(f"Appendix saved: {appendix_path}")
    print()
    
    # =========================================================================
    # Step 6: Save Results as JSON
    # =========================================================================
    print("Step 6: Exporting results...")
    print("-" * 70)
    
    json_path = output_dir / f'{scenario_name}_results.json'
    results.save_json(str(json_path))
    
    print(f"Results JSON saved: {json_path}")
    print()
    
    # =========================================================================
    # Summary
    # =========================================================================
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print()
    print(f"Generated outputs in: {output_dir}")
    print()
    print("Files created:")
    print(f"  1. Executive summary: {report_path.name}")
    print(f"  2. Technical appendix: {appendix_path.name}")
    print(f"  3. Results JSON: {json_path.name}")
    print(f"  4. Figures: {len(figure_paths)} charts in figures/")
    print()
    print("Next steps:")
    print("  - Review the executive summary for policy insights")
    print("  - Examine figures for visual analysis")
    print("  - Compare with other scenarios")
    print("  - Use results for decision-making")
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

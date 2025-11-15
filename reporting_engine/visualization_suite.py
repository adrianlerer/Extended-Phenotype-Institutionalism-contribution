"""
Visualization Suite - Publication-Quality Charts
=================================================

Generate professional charts for reports, papers, and presentations.

Supported visualizations:
1. CLI/MFD Evolution Over Time (line plots with confidence intervals)
2. Monte Carlo Results Distribution (histograms, violin plots)
3. Reform Success Rates by Scenario (bar charts with error bars)
4. Agent Population Dynamics (stacked area charts)
5. Sensitivity Analysis Heatmaps
6. Comparative Analysis (multi-scenario overlays)

Output formats: PNG, SVG, PDF (publication-ready)
Style: Professional, colorblind-friendly palettes

Usage:
    from reporting_engine.visualization_suite import VisualizationEngine
    from simulation_module.monte_carlo import MonteCarloRunner
    
    runner = MonteCarloRunner(n_iterations=1000)
    results = runner.run_scenario('uruguay_1991')
    
    viz = VisualizationEngine(output_dir='./figures')
    viz.plot_cli_evolution(results, save=True)
    viz.plot_reform_success_distribution(results, save=True)
"""

from typing import Dict, Any, List, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter, MaxNLocator
import seaborn as sns
import numpy as np
from pathlib import Path
import json

# Professional style settings
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("colorblind")

# Publication-quality defaults
FIGURE_DPI = 300
FIGURE_FORMAT = 'png'  # Can be 'png', 'svg', 'pdf'
FIGURE_SIZE = (10, 6)
TITLE_FONTSIZE = 14
LABEL_FONTSIZE = 12
TICK_FONTSIZE = 10
LEGEND_FONTSIZE = 10

# Colorblind-friendly palette
COLORS = {
    'primary': '#0173B2',      # Blue
    'secondary': '#DE8F05',    # Orange
    'success': '#029E73',      # Green
    'warning': '#CC78BC',      # Purple
    'danger': '#CA9161',       # Brown
    'neutral': '#949494',      # Gray
    'highlight': '#ECE133'     # Yellow
}


class VisualizationEngine:
    """
    Professional visualization engine for ABM simulation results
    
    Features:
    - Publication-quality charts (matplotlib, seaborn)
    - Colorblind-friendly palettes
    - Multiple output formats (PNG, SVG, PDF)
    - Consistent styling
    - Error bars and confidence intervals
    - Multi-scenario comparisons
    
    Usage:
        viz = VisualizationEngine(output_dir='./figures')
        viz.plot_cli_evolution(results)
        viz.plot_reform_success_distribution(results)
    """
    
    def __init__(
        self,
        output_dir: str = './figures',
        dpi: int = FIGURE_DPI,
        format: str = FIGURE_FORMAT,
        style: str = 'seaborn-v0_8-paper'
    ):
        """
        Initialize visualization engine
        
        Args:
            output_dir: Directory to save figures
            dpi: DPI for raster formats (PNG, JPG)
            format: Output format ('png', 'svg', 'pdf')
            style: Matplotlib style
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.dpi = dpi
        self.format = format
        
        # Set style
        plt.style.use(style)
        sns.set_palette("colorblind")
    
    def plot_cli_evolution(
        self,
        results: Any,  # MonteCarloResults
        title: Optional[str] = None,
        show_ci: bool = True,
        save: bool = True,
        filename: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot CLI evolution over time with confidence intervals
        
        Args:
            results: MonteCarloResults object
            title: Custom title (default: auto-generated)
            show_ci: Show confidence interval shading
            save: Save figure to disk
            filename: Custom filename (default: auto-generated)
        
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        
        # Extract data
        timesteps = range(len(results.mean_cli_trajectory))
        mean_cli = results.mean_cli_trajectory
        std_cli = results.std_cli_trajectory
        
        # Plot mean line
        ax.plot(timesteps, mean_cli, 
                color=COLORS['primary'], linewidth=2.5, 
                label='Mean CLI')
        
        # Plot confidence interval
        if show_ci and std_cli:
            lower = np.array(mean_cli) - 1.96 * np.array(std_cli)
            upper = np.array(mean_cli) + 1.96 * np.array(std_cli)
            ax.fill_between(timesteps, lower, upper, 
                           color=COLORS['primary'], alpha=0.2,
                           label='95% CI')
        
        # Add critical CLI thresholds
        ax.axhline(y=0.60, color=COLORS['warning'], linestyle='--', 
                  linewidth=1.5, alpha=0.7, label='CLI=0.60 (High Lock-In)')
        ax.axhline(y=0.40, color=COLORS['success'], linestyle='--', 
                  linewidth=1.5, alpha=0.7, label='CLI=0.40 (Moderate)')
        
        # Styling
        ax.set_xlabel('Timestep', fontsize=LABEL_FONTSIZE)
        ax.set_ylabel('Constitutional Lock-In Index (CLI)', fontsize=LABEL_FONTSIZE)
        
        if title is None:
            title = f'CLI Evolution: {results.scenario_name}'
        ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold')
        
        ax.legend(fontsize=LEGEND_FONTSIZE, loc='best')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1.0)
        
        plt.tight_layout()
        
        if save:
            if filename is None:
                filename = f"cli_evolution_{results.scenario_name.replace(' ', '_').replace(':', '')}.{self.format}"
            filepath = self.output_dir / filename
            fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        return fig
    
    def plot_mfd_evolution(
        self,
        results: Any,
        title: Optional[str] = None,
        show_ci: bool = True,
        save: bool = True,
        filename: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot MFD (Memetic Fitness Differential) evolution over time
        
        Args:
            results: MonteCarloResults object
            title: Custom title
            show_ci: Show confidence interval
            save: Save figure to disk
            filename: Custom filename
        
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        
        timesteps = range(len(results.mean_mfd_trajectory))
        mean_mfd = results.mean_mfd_trajectory
        std_mfd = results.std_mfd_trajectory
        
        # Plot mean line
        ax.plot(timesteps, mean_mfd, 
                color=COLORS['secondary'], linewidth=2.5, 
                label='Mean MFD')
        
        # Confidence interval
        if show_ci and std_mfd:
            lower = np.array(mean_mfd) - 1.96 * np.array(std_mfd)
            upper = np.array(mean_mfd) + 1.96 * np.array(std_mfd)
            lower = np.maximum(lower, 0)  # MFD can't be negative
            ax.fill_between(timesteps, lower, upper, 
                           color=COLORS['secondary'], alpha=0.2,
                           label='95% CI')
        
        # Critical MFD thresholds
        ax.axhline(y=1.0, color=COLORS['neutral'], linestyle='--', 
                  linewidth=1.5, alpha=0.7, label='MFD=1.0 (Equilibrium)')
        ax.axhline(y=5.0, color=COLORS['danger'], linestyle='--', 
                  linewidth=1.5, alpha=0.7, label='MFD=5.0 (Strong Informal)')
        
        # Styling
        ax.set_xlabel('Timestep', fontsize=LABEL_FONTSIZE)
        ax.set_ylabel('Memetic Fitness Differential (MFD)', fontsize=LABEL_FONTSIZE)
        
        if title is None:
            title = f'MFD Evolution: {results.scenario_name}'
        ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold')
        
        ax.legend(fontsize=LEGEND_FONTSIZE, loc='best')
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')  # Log scale for MFD (can range widely)
        
        plt.tight_layout()
        
        if save:
            if filename is None:
                filename = f"mfd_evolution_{results.scenario_name.replace(' ', '_').replace(':', '')}.{self.format}"
            filepath = self.output_dir / filename
            fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        return fig
    
    def plot_reform_success_distribution(
        self,
        results: Any,
        title: Optional[str] = None,
        bins: int = 30,
        save: bool = True,
        filename: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot distribution of reform success rates across Monte Carlo iterations
        
        Args:
            results: MonteCarloResults object
            title: Custom title
            bins: Number of histogram bins
            save: Save figure
            filename: Custom filename
        
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE)
        
        # Histogram
        ax.hist(results.reform_success_rates, bins=bins,
               color=COLORS['primary'], alpha=0.7, edgecolor='black',
               linewidth=0.5, density=True, label='Distribution')
        
        # Add mean line
        ax.axvline(x=results.mean_reform_success_rate, 
                  color=COLORS['danger'], linestyle='--', linewidth=2.5,
                  label=f'Mean: {results.mean_reform_success_rate:.3f}')
        
        # Add median line
        ax.axvline(x=results.median_reform_success_rate, 
                  color=COLORS['success'], linestyle='--', linewidth=2.5,
                  label=f'Median: {results.median_reform_success_rate:.3f}')
        
        # Add confidence interval
        ci_lower, ci_upper = results.reform_success_rate_ci
        ax.axvspan(ci_lower, ci_upper, alpha=0.2, color=COLORS['highlight'],
                  label=f'95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]')
        
        # Styling
        ax.set_xlabel('Reform Success Rate', fontsize=LABEL_FONTSIZE)
        ax.set_ylabel('Density', fontsize=LABEL_FONTSIZE)
        
        if title is None:
            title = f'Reform Success Distribution: {results.scenario_name}'
        ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold')
        
        ax.legend(fontsize=LEGEND_FONTSIZE, loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xlim(0, 1.0)
        
        plt.tight_layout()
        
        if save:
            if filename is None:
                filename = f"reform_success_dist_{results.scenario_name.replace(' ', '_').replace(':', '')}.{self.format}"
            filepath = self.output_dir / filename
            fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        return fig
    
    def plot_scenario_comparison(
        self,
        results_dict: Dict[str, Any],  # Dict[scenario_name, MonteCarloResults]
        metric: str = 'reform_success_rate',
        title: Optional[str] = None,
        save: bool = True,
        filename: Optional[str] = None
    ) -> plt.Figure:
        """
        Compare multiple scenarios on a single metric
        
        Args:
            results_dict: Dictionary mapping scenario names to MonteCarloResults
            metric: Metric to compare ('reform_success_rate', 'final_cli', 'final_mfd')
            title: Custom title
            save: Save figure
            filename: Custom filename
        
        Returns:
            Matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        scenario_names = list(results_dict.keys())
        
        # Extract metric data
        if metric == 'reform_success_rate':
            means = [results_dict[name].mean_reform_success_rate for name in scenario_names]
            stds = [results_dict[name].std_reform_success_rate for name in scenario_names]
            ylabel = 'Reform Success Rate'
        elif metric == 'final_cli':
            means = [results_dict[name].mean_final_cli for name in scenario_names]
            stds = [results_dict[name].std_final_cli for name in scenario_names]
            ylabel = 'Final CLI'
        elif metric == 'final_mfd':
            means = [results_dict[name].mean_final_mfd for name in scenario_names]
            stds = [results_dict[name].std_final_mfd for name in scenario_names]
            ylabel = 'Final MFD'
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        # Bar chart with error bars
        x_pos = np.arange(len(scenario_names))
        bars = ax.bar(x_pos, means, yerr=stds, 
                     color=COLORS['primary'], alpha=0.7,
                     capsize=5, ecolor='black', linewidth=1.5)
        
        # Color bars based on value
        if metric == 'reform_success_rate':
            for bar, mean in zip(bars, means):
                if mean > 0.7:
                    bar.set_color(COLORS['success'])
                elif mean > 0.3:
                    bar.set_color(COLORS['warning'])
                else:
                    bar.set_color(COLORS['danger'])
        
        # Styling
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenario_names, rotation=45, ha='right', fontsize=TICK_FONTSIZE)
        ax.set_ylabel(ylabel, fontsize=LABEL_FONTSIZE)
        
        if title is None:
            title = f'Scenario Comparison: {ylabel}'
        ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold')
        
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            if filename is None:
                filename = f"scenario_comparison_{metric}.{self.format}"
            filepath = self.output_dir / filename
            fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        return fig
    
    def plot_sensitivity_analysis(
        self,
        sensitivity_results: Dict[str, Any],
        title: Optional[str] = None,
        save: bool = True,
        filename: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot sensitivity analysis results
        
        Args:
            sensitivity_results: Output from MonteCarloRunner.sensitivity_analysis()
            title: Custom title
            save: Save figure
            filename: Custom filename
        
        Returns:
            Matplotlib Figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        parameter = sensitivity_results['parameter']
        values = sensitivity_results['values_tested']
        results = sensitivity_results['results']
        
        # Extract metrics
        param_values = [r['parameter_value'] for r in results]
        reform_means = [r['mean_reform_success_rate'] for r in results]
        reform_stds = [r['std_reform_success_rate'] for r in results]
        cli_means = [r['mean_final_cli'] for r in results]
        cli_stds = [r['std_final_cli'] for r in results]
        
        # Plot 1: Reform success rate
        ax1.plot(param_values, reform_means, 
                color=COLORS['primary'], linewidth=2.5, marker='o', markersize=6)
        ax1.fill_between(param_values, 
                        np.array(reform_means) - np.array(reform_stds),
                        np.array(reform_means) + np.array(reform_stds),
                        color=COLORS['primary'], alpha=0.2)
        
        ax1.set_xlabel(parameter.replace('_', ' ').title(), fontsize=LABEL_FONTSIZE)
        ax1.set_ylabel('Reform Success Rate', fontsize=LABEL_FONTSIZE)
        ax1.set_title(f'Sensitivity: {parameter} → Reform Success', 
                     fontsize=TITLE_FONTSIZE, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 1.0)
        
        # Plot 2: Final CLI
        ax2.plot(param_values, cli_means, 
                color=COLORS['secondary'], linewidth=2.5, marker='s', markersize=6)
        ax2.fill_between(param_values, 
                        np.array(cli_means) - np.array(cli_stds),
                        np.array(cli_means) + np.array(cli_stds),
                        color=COLORS['secondary'], alpha=0.2)
        
        ax2.set_xlabel(parameter.replace('_', ' ').title(), fontsize=LABEL_FONTSIZE)
        ax2.set_ylabel('Final CLI', fontsize=LABEL_FONTSIZE)
        ax2.set_title(f'Sensitivity: {parameter} → Final CLI', 
                     fontsize=TITLE_FONTSIZE, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1.0)
        
        plt.tight_layout()
        
        if save:
            if filename is None:
                filename = f"sensitivity_{parameter}.{self.format}"
            filepath = self.output_dir / filename
            fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        return fig
    
    def plot_cli_mfd_joint(
        self,
        results: Any,
        title: Optional[str] = None,
        save: bool = True,
        filename: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot CLI and MFD evolution on joint axes (two y-axes)
        
        Args:
            results: MonteCarloResults object
            title: Custom title
            save: Save figure
            filename: Custom filename
        
        Returns:
            Matplotlib Figure object
        """
        fig, ax1 = plt.subplots(figsize=FIGURE_SIZE)
        
        timesteps = range(len(results.mean_cli_trajectory))
        
        # Plot CLI on primary y-axis
        ax1.plot(timesteps, results.mean_cli_trajectory,
                color=COLORS['primary'], linewidth=2.5, label='CLI')
        ax1.set_xlabel('Timestep', fontsize=LABEL_FONTSIZE)
        ax1.set_ylabel('CLI', fontsize=LABEL_FONTSIZE, color=COLORS['primary'])
        ax1.tick_params(axis='y', labelcolor=COLORS['primary'])
        ax1.set_ylim(0, 1.0)
        ax1.grid(True, alpha=0.3)
        
        # Create secondary y-axis for MFD
        ax2 = ax1.twinx()
        ax2.plot(timesteps, results.mean_mfd_trajectory,
                color=COLORS['secondary'], linewidth=2.5, label='MFD')
        ax2.set_ylabel('MFD', fontsize=LABEL_FONTSIZE, color=COLORS['secondary'])
        ax2.tick_params(axis='y', labelcolor=COLORS['secondary'])
        ax2.set_yscale('log')
        
        if title is None:
            title = f'CLI & MFD Evolution: {results.scenario_name}'
        ax1.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold')
        
        # Combined legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, 
                  fontsize=LEGEND_FONTSIZE, loc='best')
        
        plt.tight_layout()
        
        if save:
            if filename is None:
                filename = f"cli_mfd_joint_{results.scenario_name.replace(' ', '_').replace(':', '')}.{self.format}"
            filepath = self.output_dir / filename
            fig.savefig(filepath, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved: {filepath}")
        
        return fig
    
    def create_figure_report(
        self,
        results: Any,
        scenario_name: str,
        save_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate complete figure report for a scenario
        
        Creates all standard visualizations:
        1. CLI evolution
        2. MFD evolution
        3. CLI & MFD joint
        4. Reform success distribution
        
        Args:
            results: MonteCarloResults object
            scenario_name: Name of scenario
            save_dir: Directory to save figures (default: self.output_dir/scenario_name)
        
        Returns:
            Dictionary mapping figure type to filepath
        """
        if save_dir is None:
            save_dir = self.output_dir / scenario_name.replace(' ', '_').replace(':', '')
        else:
            save_dir = Path(save_dir)
        
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Temporarily change output dir
        original_output_dir = self.output_dir
        self.output_dir = save_dir
        
        figure_paths = {}
        
        try:
            # Generate all figures
            print(f"\nGenerating figure report for: {scenario_name}")
            print("=" * 60)
            
            fig1 = self.plot_cli_evolution(results, save=True)
            figure_paths['cli_evolution'] = str(save_dir / f"cli_evolution.{self.format}")
            plt.close(fig1)
            
            fig2 = self.plot_mfd_evolution(results, save=True)
            figure_paths['mfd_evolution'] = str(save_dir / f"mfd_evolution.{self.format}")
            plt.close(fig2)
            
            fig3 = self.plot_cli_mfd_joint(results, save=True)
            figure_paths['cli_mfd_joint'] = str(save_dir / f"cli_mfd_joint.{self.format}")
            plt.close(fig3)
            
            fig4 = self.plot_reform_success_distribution(results, save=True)
            figure_paths['reform_success_dist'] = str(save_dir / f"reform_success_dist.{self.format}")
            plt.close(fig4)
            
            print("=" * 60)
            print(f"Figure report complete: {len(figure_paths)} figures generated")
            print(f"Location: {save_dir}")
            
        finally:
            # Restore original output dir
            self.output_dir = original_output_dir
        
        return figure_paths


def demo():
    """Demo visualization suite"""
    print("Visualization Suite Demo")
    print("=" * 60)
    print("To use the visualization suite:")
    print()
    print("1. Run Monte Carlo simulations:")
    print("   from simulation_module.monte_carlo import MonteCarloRunner")
    print("   runner = MonteCarloRunner(n_iterations=1000)")
    print("   results = runner.run_scenario('uruguay_1991')")
    print()
    print("2. Create visualizations:")
    print("   from reporting_engine.visualization_suite import VisualizationEngine")
    print("   viz = VisualizationEngine(output_dir='./figures')")
    print("   viz.create_figure_report(results, 'uruguay_1991')")
    print()
    print("This will generate:")
    print("  - CLI evolution plot")
    print("  - MFD evolution plot")
    print("  - CLI & MFD joint plot")
    print("  - Reform success distribution")
    print()
    print("All figures saved in ./figures/ directory")
    print("=" * 60)


if __name__ == "__main__":
    demo()

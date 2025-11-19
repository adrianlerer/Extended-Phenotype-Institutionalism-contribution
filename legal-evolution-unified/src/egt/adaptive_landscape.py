"""
Adaptive Landscape Visualization and Bifurcation Analysis
==========================================================

Implements visualization tools from Vince (2005) for adaptive landscapes
and bifurcation analysis.

The Adaptive Landscape is the central visual tool in EGT, showing:
- G*(v) = G(v, u, x*) as function of virtual strategy v
- Peaks (ESS), Valleys (CSS/Speciation), Saddles (Unstable)
- Bifurcations as parameters change

Key Insight from Report 4:
---------------------------
"The adaptive landscape is FLEXIBLE - it changes shape rapidly with 
changes in population densities (x) and resident strategies (u)."

CLI as Bifurcation Parameter:
------------------------------
- High CLI (Argentina 0.87) → Narrow niche → Multiple peaks (speciation)
- Low CLI (Chile 0.15) → Wide niche → Single peak (lock-in)

References:
-----------
Vince (2005), Chapter 7: "Adaptive Landscape and ESS Maximum Principle"
Vince (2005), Chapter 8: "Evolutionary Branching and Speciation"
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass

from .g_function import GFunction, LotkaVolterraGFunction
from .ess_solver import ESSResult


@dataclass
class LandscapeData:
    """Data for adaptive landscape plot."""
    v_grid: np.ndarray
    G_star: np.ndarray
    u_ess: np.ndarray
    x_ess: np.ndarray
    cli_score: Optional[float] = None


class AdaptiveLandscape:
    """
    Adaptive landscape G*(v) = G(v, u, x*) construction and analysis.
    """
    
    def __init__(self, g_function: GFunction):
        """
        Initialize adaptive landscape.
        
        Parameters
        ----------
        g_function : GFunction
            G-function defining fitness
        """
        self.g_function = g_function
    
    def compute(self, u: np.ndarray, x: np.ndarray,
                v_range: Optional[Tuple[float, float]] = None,
                n_points: int = 500) -> LandscapeData:
        """
        Compute adaptive landscape G*(v).
        
        Parameters
        ----------
        u : np.ndarray
            Resident strategies
        x : np.ndarray
            Equilibrium densities
        v_range : Tuple[float, float], optional
            Range of v to plot
        n_points : int
            Number of points
            
        Returns
        -------
        LandscapeData
            Landscape data for plotting
        """
        if v_range is None:
            u_flat = u.flatten()
            margin = max(u_flat.max() - u_flat.min(), 2.0)
            v_range = (u_flat.min() - margin, u_flat.max() + margin)
        
        v_grid = np.linspace(v_range[0], v_range[1], n_points)
        G_star = np.array([self.g_function.evaluate(v, u, x) for v in v_grid])
        
        # Extract CLI if available
        cli_score = None
        if isinstance(self.g_function, LotkaVolterraGFunction):
            cli_score = self.g_function.cli_score
        
        return LandscapeData(
            v_grid=v_grid,
            G_star=G_star,
            u_ess=u,
            x_ess=x,
            cli_score=cli_score
        )


class LandscapeVisualizer:
    """
    Publication-ready visualization of adaptive landscapes.
    """
    
    @staticmethod
    def plot_single(landscape: LandscapeData, 
                   ax: Optional[plt.Axes] = None,
                   show_ess: bool = True) -> plt.Axes:
        """
        Plot single adaptive landscape.
        
        Parameters
        ----------
        landscape : LandscapeData
            Landscape data
        ax : plt.Axes, optional
            Axes to plot on
        show_ess : bool
            If True, mark ESS locations
            
        Returns
        -------
        plt.Axes
            Axes with plot
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot G*(v)
        ax.plot(landscape.v_grid, landscape.G_star, 'b-', linewidth=2)
        ax.axhline(0, color='k', linestyle='--', alpha=0.3, label='Fitness = 0')
        
        # Mark ESS
        if show_ess:
            u_flat = landscape.u_ess.flatten()
            for u_i in u_flat:
                G_i = landscape.G_star[np.argmin(np.abs(landscape.v_grid - u_i))]
                ax.plot(u_i, G_i, 'ro', markersize=10, label=f'ESS u={u_i:.3f}')
        
        ax.set_xlabel('Strategy v (Doctrinal Rigidity)', fontsize=12)
        ax.set_ylabel('Fitness G*(v)', fontsize=12)
        
        title = 'Adaptive Landscape'
        if landscape.cli_score is not None:
            title += f' (CLI = {landscape.cli_score:.2f})'
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return ax
    
    @staticmethod
    def plot_bifurcation(landscapes: List[LandscapeData],
                        cli_values: np.ndarray,
                        figsize: Tuple[int, int] = (15, 10)) -> plt.Figure:
        """
        Plot bifurcation diagram as CLI changes.
        
        Shows how adaptive landscape topology changes from
        single peak (low CLI, Chile) to multiple peaks (high CLI, Argentina).
        
        Parameters
        ----------
        landscapes : List[LandscapeData]
            Landscapes at different CLI values
        cli_values : np.ndarray
            CLI values for each landscape
        figsize : Tuple[int, int]
            Figure size
            
        Returns
        -------
        plt.Figure
            Figure with bifurcation plots
        """
        n_plots = len(landscapes)
        fig, axes = plt.subplots(n_plots, 1, figsize=figsize, sharex=True)
        
        if n_plots == 1:
            axes = [axes]
        
        for i, (landscape, cli) in enumerate(zip(landscapes, cli_values)):
            ax = axes[i]
            
            # Plot landscape
            ax.plot(landscape.v_grid, landscape.G_star, 'b-', linewidth=2)
            ax.axhline(0, color='k', linestyle='--', alpha=0.3)
            
            # Mark peaks/valleys
            # Find local maxima (peaks)
            dG = np.diff(landscape.G_star)
            peaks = np.where((dG[:-1] > 0) & (dG[1:] < 0))[0] + 1
            
            for peak in peaks:
                v_peak = landscape.v_grid[peak]
                G_peak = landscape.G_star[peak]
                ax.plot(v_peak, G_peak, 'ro', markersize=8)
            
            # Find local minima (valleys)
            valleys = np.where((dG[:-1] < 0) & (dG[1:] > 0))[0] + 1
            
            for valley in valleys:
                v_valley = landscape.v_grid[valley]
                G_valley = landscape.G_star[valley]
                ax.plot(v_valley, G_valley, 'go', markersize=8)
            
            ax.set_ylabel(f'G*(v)\nCLI={cli:.2f}', fontsize=11)
            ax.grid(True, alpha=0.3)
        
        axes[-1].set_xlabel('Strategy v (Doctrinal Rigidity)', fontsize=12)
        fig.suptitle('Bifurcation Analysis: Adaptive Landscape vs CLI', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig


class BifurcationAnalyzer:
    """
    Bifurcation analysis with CLI as bifurcation parameter.
    
    Critical Hypothesis:
    --------------------
    CLI acts as bifurcation parameter determining regime:
    - Low CLI (Chile 0.15) → Single ESS (doctrinal unity)
    - High CLI (Argentina 0.87) → Multiple ESS (doctrinal pluralism/speciation)
    
    This predicts constitutional lock-in behavior!
    """
    
    def __init__(self, g_function_constructor):
        """
        Initialize bifurcation analyzer.
        
        Parameters
        ----------
        g_function_constructor : callable
            Function that constructs G-function given CLI
            Signature: g_function_constructor(cli) -> GFunction
        """
        self.g_function_constructor = g_function_constructor
    
    def analyze(self, cli_range: np.ndarray, u0: np.ndarray,
                **solver_kwargs) -> Dict:
        """
        Perform bifurcation analysis over CLI range.
        
        Parameters
        ----------
        cli_range : np.ndarray
            Range of CLI values to analyze
        u0 : np.ndarray
            Initial strategy guess
        **solver_kwargs
            Arguments for ESS solver
            
        Returns
        -------
        dict
            Bifurcation data: CLI values, ESS values, stability types
        """
        from .ess_solver import ESSSolver
        from .darwinian_dynamics import TimescaleParams
        
        ess_values = []
        stability_types = []
        n_ess_list = []
        landscapes = []
        
        for cli in cli_range:
            # Construct G-function for this CLI
            g_func = self.g_function_constructor(cli)
            
            # Solve for ESS
            timescale_params = TimescaleParams(sigma_sq=1.0, tau_eco=10.0, tau_evo=1000.0)
            solver = ESSSolver(g_func, timescale_params)
            
            result = solver.solve(u0, verify_cs=False, **solver_kwargs)
            
            ess_values.append(result.u_ess)
            stability_types.append(result.stability_type)
            n_ess_list.append(len(result.u_ess[result.x_ess > 1e-10]))
            
            # Compute landscape
            landscape_obj = AdaptiveLandscape(g_func)
            landscape = landscape_obj.compute(result.u_ess, result.x_ess)
            landscapes.append(landscape)
        
        return {
            'cli_values': cli_range,
            'ess_values': ess_values,
            'stability_types': stability_types,
            'n_ess': np.array(n_ess_list),
            'landscapes': landscapes,
        }
    
    def plot_bifurcation_diagram(self, bifurcation_data: Dict,
                                figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Plot bifurcation diagram: ESS values vs CLI.
        
        This is the KEY plot showing regime transition!
        
        Parameters
        ----------
        bifurcation_data : dict
            Output from analyze()
        figsize : Tuple[int, int]
            Figure size
            
        Returns
        -------
        plt.Figure
            Bifurcation diagram
        """
        fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
        
        cli_values = bifurcation_data['cli_values']
        ess_values = bifurcation_data['ess_values']
        n_ess = bifurcation_data['n_ess']
        
        # Plot 1: ESS values vs CLI
        ax1 = axes[0]
        for i, cli in enumerate(cli_values):
            u_ess = ess_values[i].flatten()
            u_ess = u_ess[u_ess != 0]  # Remove extinct species
            
            for u in u_ess:
                ax1.plot(cli, u, 'bo', markersize=5)
        
        ax1.set_ylabel('ESS Strategy u*', fontsize=12)
        ax1.set_title('Bifurcation Diagram: ESS vs CLI', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Mark empirical cases
        ax1.axvline(0.15, color='g', linestyle='--', label='Chile CLI=0.15 (88% success)')
        ax1.axvline(0.87, color='r', linestyle='--', label='Argentina CLI=0.87 (0% success)')
        ax1.legend()
        
        # Plot 2: Number of coexisting ESS vs CLI
        ax2 = axes[1]
        ax2.plot(cli_values, n_ess, 'b-', linewidth=2)
        ax2.set_xlabel('Constitutional Lock-in Index (CLI)', fontsize=12)
        ax2.set_ylabel('Number of Coexisting Strategies', fontsize=12)
        ax2.set_title('Regime Transition: Unity → Pluralism', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Mark empirical cases
        ax2.axvline(0.15, color='g', linestyle='--')
        ax2.axvline(0.87, color='r', linestyle='--')
        
        plt.tight_layout()
        return fig


# Export main classes
__all__ = [
    'AdaptiveLandscape',
    'LandscapeVisualizer',
    'BifurcationAnalyzer',
    'LandscapeData',
]

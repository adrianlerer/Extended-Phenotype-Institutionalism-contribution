"""
Monte Carlo Simulation Runner
==============================

Parallel execution of multiple simulation runs with statistical analysis.

Features:
- Multi-core parallel processing
- Robust statistical analysis (mean, median, std, confidence intervals)
- Sensitivity analysis for parameter exploration
- Publication-ready results with uncertainty quantification

Usage:
    from simulation_module.monte_carlo import MonteCarloRunner
    from simulation_module.scenarios import ScenarioLibrary
    
    runner = MonteCarloRunner(n_iterations=1000, n_jobs=-1)
    results = runner.run_scenario('uruguay_1991')
    
    print(f"Reform success rate: {results.mean_reform_success_rate:.3f} ± {results.std_reform_success_rate:.3f}")
    print(f"95% CI: [{results.reform_success_rate_ci[0]:.3f}, {results.reform_success_rate_ci[1]:.3f}]")
"""

from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
import numpy as np
from multiprocessing import Pool, cpu_count
from functools import partial
import json
from pathlib import Path
from tqdm import tqdm
import time

from .environment import SimulationEnvironment
from .scenarios import ScenarioLibrary, ScenarioConfig


@dataclass
class MonteCarloResults:
    """
    Results from Monte Carlo simulation runs
    
    Contains:
    - Summary statistics (mean, median, std, CI)
    - Raw results from all iterations
    - Convergence diagnostics
    - Scenario metadata
    """
    scenario_name: str
    n_iterations: int
    n_converged: int
    
    # Reform success statistics
    mean_reform_success_rate: float
    median_reform_success_rate: float
    std_reform_success_rate: float
    reform_success_rate_ci: Tuple[float, float]  # 95% CI
    reform_success_rates: List[float] = field(default_factory=list)
    
    # CLI evolution statistics
    mean_final_cli: float
    median_final_cli: float
    std_final_cli: float
    final_cli_ci: Tuple[float, float]
    final_cli_values: List[float] = field(default_factory=list)
    
    # MFD statistics
    mean_final_mfd: float
    median_final_mfd: float
    std_final_mfd: float
    final_mfd_ci: Tuple[float, float]
    final_mfd_values: List[float] = field(default_factory=list)
    
    # Trajectory statistics (timestep-by-timestep)
    mean_cli_trajectory: List[float] = field(default_factory=list)
    std_cli_trajectory: List[float] = field(default_factory=list)
    mean_mfd_trajectory: List[float] = field(default_factory=list)
    std_mfd_trajectory: List[float] = field(default_factory=list)
    
    # Execution metadata
    execution_time_seconds: float = 0.0
    random_seed: Optional[int] = None
    
    # Raw results for detailed analysis
    all_results: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'scenario_name': self.scenario_name,
            'n_iterations': self.n_iterations,
            'n_converged': self.n_converged,
            'convergence_rate': self.n_converged / self.n_iterations,
            
            'reform_success': {
                'mean': round(self.mean_reform_success_rate, 4),
                'median': round(self.median_reform_success_rate, 4),
                'std': round(self.std_reform_success_rate, 4),
                'ci_95': [round(x, 4) for x in self.reform_success_rate_ci]
            },
            
            'final_cli': {
                'mean': round(self.mean_final_cli, 4),
                'median': round(self.median_final_cli, 4),
                'std': round(self.std_final_cli, 4),
                'ci_95': [round(x, 4) for x in self.final_cli_ci]
            },
            
            'final_mfd': {
                'mean': round(self.mean_final_mfd, 2),
                'median': round(self.median_final_mfd, 2),
                'std': round(self.std_final_mfd, 2),
                'ci_95': [round(x, 2) for x in self.final_mfd_ci]
            },
            
            'execution_time_seconds': round(self.execution_time_seconds, 2)
        }
    
    def save_json(self, filepath: str):
        """Save results to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def print_summary(self):
        """Print human-readable summary"""
        print("=" * 70)
        print(f"Monte Carlo Results: {self.scenario_name}")
        print("=" * 70)
        print(f"Iterations: {self.n_iterations} (converged: {self.n_converged})")
        print(f"Execution time: {self.execution_time_seconds:.1f}s")
        print()
        
        print("Reform Success Rate:")
        print(f"  Mean:   {self.mean_reform_success_rate:.3f}")
        print(f"  Median: {self.median_reform_success_rate:.3f}")
        print(f"  Std:    {self.std_reform_success_rate:.3f}")
        print(f"  95% CI: [{self.reform_success_rate_ci[0]:.3f}, {self.reform_success_rate_ci[1]:.3f}]")
        print()
        
        print("Final CLI:")
        print(f"  Mean:   {self.mean_final_cli:.3f}")
        print(f"  Median: {self.median_final_cli:.3f}")
        print(f"  Std:    {self.std_final_cli:.3f}")
        print(f"  95% CI: [{self.final_cli_ci[0]:.3f}, {self.final_cli_ci[1]:.3f}]")
        print()
        
        print("Final MFD:")
        print(f"  Mean:   {self.mean_final_mfd:.2f}")
        print(f"  Median: {self.median_final_mfd:.2f}")
        print(f"  Std:    {self.std_final_mfd:.2f}")
        print(f"  95% CI: [{self.final_mfd_ci[0]:.2f}, {self.final_mfd_ci[1]:.2f}]")
        print("=" * 70)


def _run_single_simulation(args: Tuple[ScenarioConfig, int, int]) -> Dict[str, Any]:
    """
    Run single simulation (for parallel execution)
    
    Args:
        args: Tuple of (scenario_config, iteration_number, random_seed)
    
    Returns:
        Dictionary with simulation results
    """
    scenario, iteration, seed = args
    
    try:
        # Create environment with triple capture decomposition
        env = SimulationEnvironment(
            n_workers=scenario.n_workers,
            n_unions=scenario.n_unions,
            n_employers=scenario.n_employers,
            n_legislators=scenario.n_legislators,
            n_judges=scenario.n_judges,
            initial_cli=scenario.initial_cli,
            initial_mfd=scenario.initial_mfd,
            # Triple capture components (if provided in scenario)
            initial_cli_memetic=scenario.initial_cli_memetic,
            initial_cli_corporate=scenario.initial_cli_corporate,
            initial_cli_oligarchic=scenario.initial_cli_oligarchic,
            union_militancy_range=scenario.union_militancy_range,
            employer_coordination_range=scenario.employer_coordination_range,
            crisis_probability=scenario.crisis_probability,
            reform_proposal_interval=scenario.reform_proposal_interval,
            random_seed=seed
        )
        
        # Run simulation
        env.run(scenario.n_timesteps)
        
        # Get results
        results = env.get_results()
        
        return {
            'iteration': iteration,
            'success': True,
            'reform_success_rate': results['summary_stats']['reform_success_rate'],
            'final_cli': results['final_state']['cli'],
            'final_mfd': results['final_state']['mfd'],
            'cli_trajectory': results['summary_stats']['cli_trajectory'],
            'mfd_trajectory': results['summary_stats']['mfd_trajectory'],
            'reforms_attempted': results['summary_stats']['reforms_attempted'],
            'reforms_succeeded': results['summary_stats']['reforms_succeeded']
        }
    
    except Exception as e:
        return {
            'iteration': iteration,
            'success': False,
            'error': str(e)
        }


class MonteCarloRunner:
    """
    Monte Carlo simulation runner with parallel processing
    
    Features:
    - Parallel execution across CPU cores
    - Progress tracking
    - Statistical analysis with confidence intervals
    - Convergence diagnostics
    - Sensitivity analysis
    
    Usage:
        runner = MonteCarloRunner(n_iterations=1000, n_jobs=-1)
        results = runner.run_scenario('uruguay_1991')
        results.print_summary()
    """
    
    def __init__(
        self,
        n_iterations: int = 1000,
        n_jobs: int = -1,
        random_seed: Optional[int] = None,
        verbose: bool = True
    ):
        """
        Initialize Monte Carlo runner
        
        Args:
            n_iterations: Number of simulation runs
            n_jobs: Number of parallel jobs (-1 = all CPUs, 1 = sequential)
            random_seed: Random seed for reproducibility
            verbose: Show progress bars and messages
        """
        self.n_iterations = n_iterations
        self.n_jobs = cpu_count() if n_jobs == -1 else n_jobs
        self.random_seed = random_seed
        self.verbose = verbose
        
        self.scenario_library = ScenarioLibrary()
        
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def run_scenario(
        self,
        scenario_name: str,
        n_iterations: Optional[int] = None
    ) -> MonteCarloResults:
        """
        Run Monte Carlo analysis for a scenario
        
        Args:
            scenario_name: Name of scenario from library
            n_iterations: Override default number of iterations
        
        Returns:
            MonteCarloResults with statistical analysis
        """
        scenario = self.scenario_library.get_scenario(scenario_name)
        n_iter = n_iterations if n_iterations is not None else self.n_iterations
        
        if self.verbose:
            print(f"Running Monte Carlo analysis: {scenario_name}")
            print(f"Iterations: {n_iter}, Parallel jobs: {self.n_jobs}")
            print()
        
        start_time = time.time()
        
        # Generate random seeds for each iteration
        if self.random_seed is not None:
            seeds = [self.random_seed + i for i in range(n_iter)]
        else:
            seeds = [None] * n_iter
        
        # Prepare arguments for parallel execution
        args_list = [(scenario, i, seeds[i]) for i in range(n_iter)]
        
        # Run simulations in parallel
        if self.n_jobs > 1:
            with Pool(self.n_jobs) as pool:
                if self.verbose:
                    # With progress bar
                    results_list = list(tqdm(
                        pool.imap(_run_single_simulation, args_list),
                        total=n_iter,
                        desc="Simulations"
                    ))
                else:
                    results_list = pool.map(_run_single_simulation, args_list)
        else:
            # Sequential execution
            if self.verbose:
                results_list = [
                    _run_single_simulation(args)
                    for args in tqdm(args_list, desc="Simulations")
                ]
            else:
                results_list = [_run_single_simulation(args) for args in args_list]
        
        execution_time = time.time() - start_time
        
        # Process results
        return self._process_results(
            scenario_name=scenario_name,
            results_list=results_list,
            execution_time=execution_time
        )
    
    def _process_results(
        self,
        scenario_name: str,
        results_list: List[Dict[str, Any]],
        execution_time: float
    ) -> MonteCarloResults:
        """Process raw results into statistical summary"""
        
        # Filter successful runs
        successful_results = [r for r in results_list if r.get('success', False)]
        n_converged = len(successful_results)
        
        if n_converged == 0:
            raise RuntimeError("All simulations failed!")
        
        if n_converged < len(results_list) and self.verbose:
            print(f"Warning: {len(results_list) - n_converged} simulations failed")
        
        # Extract metrics
        reform_success_rates = [r['reform_success_rate'] for r in successful_results]
        final_cli_values = [r['final_cli'] for r in successful_results]
        final_mfd_values = [r['final_mfd'] for r in successful_results]
        
        # Calculate statistics
        mean_reform = np.mean(reform_success_rates)
        median_reform = np.median(reform_success_rates)
        std_reform = np.std(reform_success_rates)
        ci_reform = self._calculate_confidence_interval(reform_success_rates)
        
        mean_cli = np.mean(final_cli_values)
        median_cli = np.median(final_cli_values)
        std_cli = np.std(final_cli_values)
        ci_cli = self._calculate_confidence_interval(final_cli_values)
        
        mean_mfd = np.mean(final_mfd_values)
        median_mfd = np.median(final_mfd_values)
        std_mfd = np.std(final_mfd_values)
        ci_mfd = self._calculate_confidence_interval(final_mfd_values)
        
        # Calculate trajectory statistics (timestep-by-timestep)
        cli_trajectories = [r['cli_trajectory'] for r in successful_results]
        mfd_trajectories = [r['mfd_trajectory'] for r in successful_results]
        
        # Ensure all trajectories have same length (take minimum)
        min_length = min(len(t) for t in cli_trajectories)
        cli_trajectories_trimmed = [t[:min_length] for t in cli_trajectories]
        mfd_trajectories_trimmed = [t[:min_length] for t in mfd_trajectories]
        
        mean_cli_trajectory = np.mean(cli_trajectories_trimmed, axis=0).tolist()
        std_cli_trajectory = np.std(cli_trajectories_trimmed, axis=0).tolist()
        mean_mfd_trajectory = np.mean(mfd_trajectories_trimmed, axis=0).tolist()
        std_mfd_trajectory = np.std(mfd_trajectories_trimmed, axis=0).tolist()
        
        return MonteCarloResults(
            scenario_name=scenario_name,
            n_iterations=len(results_list),
            n_converged=n_converged,
            
            mean_reform_success_rate=mean_reform,
            median_reform_success_rate=median_reform,
            std_reform_success_rate=std_reform,
            reform_success_rate_ci=ci_reform,
            reform_success_rates=reform_success_rates,
            
            mean_final_cli=mean_cli,
            median_final_cli=median_cli,
            std_final_cli=std_cli,
            final_cli_ci=ci_cli,
            final_cli_values=final_cli_values,
            
            mean_final_mfd=mean_mfd,
            median_final_mfd=median_mfd,
            std_final_mfd=std_mfd,
            final_mfd_ci=ci_mfd,
            final_mfd_values=final_mfd_values,
            
            mean_cli_trajectory=mean_cli_trajectory,
            std_cli_trajectory=std_cli_trajectory,
            mean_mfd_trajectory=mean_mfd_trajectory,
            std_mfd_trajectory=std_mfd_trajectory,
            
            execution_time_seconds=execution_time,
            random_seed=self.random_seed,
            all_results=successful_results
        )
    
    def _calculate_confidence_interval(
        self,
        values: List[float],
        confidence: float = 0.95
    ) -> Tuple[float, float]:
        """Calculate confidence interval using percentile method"""
        alpha = 1 - confidence
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        lower = np.percentile(values, lower_percentile)
        upper = np.percentile(values, upper_percentile)
        
        return (float(lower), float(upper))
    
    def sensitivity_analysis(
        self,
        scenario_name: str,
        parameter: str,
        values: List[float],
        n_iterations_per_value: int = 100
    ) -> Dict[str, Any]:
        """
        Perform sensitivity analysis for a parameter
        
        Args:
            scenario_name: Base scenario name
            parameter: Parameter to vary (e.g., 'initial_cli', 'union_militancy_min')
            values: List of parameter values to test
            n_iterations_per_value: Monte Carlo iterations per value
        
        Returns:
            Dictionary with sensitivity analysis results
        """
        scenario = self.scenario_library.get_scenario(scenario_name)
        results = []
        
        if self.verbose:
            print(f"Sensitivity Analysis: {parameter}")
            print(f"Base scenario: {scenario_name}")
            print(f"Testing {len(values)} values with {n_iterations_per_value} iterations each")
            print()
        
        for value in tqdm(values, desc="Parameter values", disable=not self.verbose):
            # Create modified scenario
            modified_scenario = self._modify_scenario_parameter(scenario, parameter, value)
            
            # Run Monte Carlo
            mc_results = self._run_monte_carlo_direct(
                modified_scenario,
                n_iterations_per_value,
                show_progress=False
            )
            
            results.append({
                'parameter_value': value,
                'mean_reform_success_rate': mc_results.mean_reform_success_rate,
                'std_reform_success_rate': mc_results.std_reform_success_rate,
                'mean_final_cli': mc_results.mean_final_cli,
                'std_final_cli': mc_results.std_final_cli
            })
        
        return {
            'parameter': parameter,
            'base_scenario': scenario_name,
            'values_tested': values,
            'n_iterations_per_value': n_iterations_per_value,
            'results': results
        }
    
    def _modify_scenario_parameter(
        self,
        scenario: ScenarioConfig,
        parameter: str,
        value: float
    ) -> ScenarioConfig:
        """Create modified copy of scenario with parameter changed"""
        import copy
        modified = copy.deepcopy(scenario)
        
        # Handle different parameter types
        if parameter == 'initial_cli':
            modified.initial_cli = value
        elif parameter == 'initial_mfd':
            modified.initial_mfd = value
        elif parameter == 'union_militancy_min':
            modified.union_militancy_range = (int(value), modified.union_militancy_range[1])
        elif parameter == 'union_militancy_max':
            modified.union_militancy_range = (modified.union_militancy_range[0], int(value))
        elif parameter == 'employer_coordination_min':
            modified.employer_coordination_range = (int(value), modified.employer_coordination_range[1])
        elif parameter == 'employer_coordination_max':
            modified.employer_coordination_range = (modified.employer_coordination_range[0], int(value))
        elif parameter == 'crisis_probability':
            modified.crisis_probability = value
        else:
            raise ValueError(f"Unknown parameter: {parameter}")
        
        return modified
    
    def _run_monte_carlo_direct(
        self,
        scenario: ScenarioConfig,
        n_iterations: int,
        show_progress: bool = False
    ) -> MonteCarloResults:
        """Run Monte Carlo directly on scenario object (internal helper)"""
        # Generate random seeds
        if self.random_seed is not None:
            seeds = [self.random_seed + i + 100000 for i in range(n_iterations)]
        else:
            seeds = [None] * n_iterations
        
        args_list = [(scenario, i, seeds[i]) for i in range(n_iterations)]
        
        # Run simulations
        if self.n_jobs > 1:
            with Pool(self.n_jobs) as pool:
                if show_progress:
                    results_list = list(tqdm(
                        pool.imap(_run_single_simulation, args_list),
                        total=n_iterations
                    ))
                else:
                    results_list = pool.map(_run_single_simulation, args_list)
        else:
            results_list = [_run_single_simulation(args) for args in args_list]
        
        return self._process_results(
            scenario_name=scenario.name,
            results_list=results_list,
            execution_time=0.0
        )


def main():
    """
    Demo script showing Monte Carlo usage
    """
    # Initialize runner
    runner = MonteCarloRunner(n_iterations=100, n_jobs=-1, random_seed=42)
    
    # Run Uruguay scenario
    print("Running Uruguay 1991 scenario...")
    uruguay_results = runner.run_scenario('uruguay_1991')
    uruguay_results.print_summary()
    
    # Run Argentina scenario
    print("\n\nRunning Argentina chronic lock-in scenario...")
    argentina_results = runner.run_scenario('argentina_chronic_lockin')
    argentina_results.print_summary()
    
    # Compare
    print("\n\n" + "=" * 70)
    print("Comparison: Uruguay vs Argentina")
    print("=" * 70)
    print(f"Uruguay reform success:   {uruguay_results.mean_reform_success_rate:.3f}")
    print(f"Argentina reform success: {argentina_results.mean_reform_success_rate:.3f}")
    print(f"Ratio: {uruguay_results.mean_reform_success_rate / max(0.001, argentina_results.mean_reform_success_rate):.1f}x")


if __name__ == "__main__":
    main()

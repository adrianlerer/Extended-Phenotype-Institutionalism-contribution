#!/usr/bin/env python3
"""
Crystallization Drivers Model Validation
========================================

Comprehensive statistical validation of the CLI prediction model:
1. Formula-based validation (theory-driven)
2. Linear regression benchmark (ML comparison)
3. Sensitivity analysis (robustness testing)
4. Visualization of validation results

Author: GenSpark AI Developer
Version: 1.0.0
Date: 2025-11-04
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore')

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10


class ModelValidator:
    """
    Comprehensive validation of crystallization drivers model
    """
    
    def __init__(self, drivers_path: str, components_path: str):
        """
        Initialize validator with data paths
        
        Args:
            drivers_path: Path to crystallization_drivers.csv
            components_path: Path to driver_components.csv
        """
        self.drivers_df = pd.read_csv(drivers_path)
        self.components_df = pd.read_csv(components_path)
        self.validation_results = {}
    
    def validate_formula_based(self) -> dict:
        """
        Validate the theoretical formula-based model
        
        Returns:
            Dictionary with validation metrics
        """
        # Filter valid observations
        valid_df = self.drivers_df[self.drivers_df['cli_observed'].notna()].copy()
        
        if len(valid_df) == 0:
            raise ValueError("No valid observations for validation")
        
        # Calculate metrics
        mae = mean_absolute_error(valid_df['cli_observed'], valid_df['cli_predicted'])
        rmse = np.sqrt(mean_squared_error(valid_df['cli_observed'], valid_df['cli_predicted']))
        r2 = r2_score(valid_df['cli_observed'], valid_df['cli_predicted'])
        
        # Additional metrics
        max_error = valid_df['abs_error'].max()
        median_error = valid_df['abs_error'].median()
        
        # Residual analysis
        residuals = valid_df['error']
        mean_residual = residuals.mean()
        std_residual = residuals.std()
        
        results = {
            'model_type': 'Formula-Based (Theoretical)',
            'n_cases': len(valid_df),
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'max_error': max_error,
            'median_error': median_error,
            'mean_residual': mean_residual,
            'std_residual': std_residual
        }
        
        self.validation_results['formula_based'] = results
        return results
    
    def validate_linear_regression(self) -> dict:
        """
        Benchmark against linear regression model
        
        Returns:
            Dictionary with ML validation metrics
        """
        # Prepare data
        valid_df = self.drivers_df[self.drivers_df['cli_observed'].notna()].copy()
        
        X = valid_df[['esri', 'pci', 'rca', 'vpfi', 'eili']].values
        y = valid_df['cli_observed'].values
        
        # Fit linear regression
        lr_model = LinearRegression()
        lr_model.fit(X, y)
        
        # Predictions
        y_pred = lr_model.predict(X)
        
        # Calculate metrics
        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        r2 = r2_score(y, y_pred)
        
        # Cross-validation (leave-one-out for small sample)
        if len(valid_df) >= 5:
            cv_scores = cross_val_score(lr_model, X, y, cv=min(5, len(valid_df)),
                                       scoring='neg_mean_absolute_error')
            cv_mae = -cv_scores.mean()
            cv_std = cv_scores.std()
        else:
            cv_mae = np.nan
            cv_std = np.nan
        
        # Get coefficients
        coefficients = dict(zip(['esri', 'pci', 'rca', 'vpfi', 'eili'], 
                               lr_model.coef_))
        intercept = lr_model.intercept_
        
        results = {
            'model_type': 'Linear Regression (ML Benchmark)',
            'n_cases': len(valid_df),
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'cv_mae': cv_mae,
            'cv_std': cv_std,
            'coefficients': coefficients,
            'intercept': intercept,
            'predictions': y_pred
        }
        
        self.validation_results['linear_regression'] = results
        return results
    
    def sensitivity_analysis(self, perturbation: float = 0.1) -> dict:
        """
        Perform sensitivity analysis by perturbing each driver
        
        Args:
            perturbation: Percentage to perturb (default 10%)
        
        Returns:
            Dictionary with sensitivity results for each driver
        """
        valid_df = self.drivers_df[self.drivers_df['cli_observed'].notna()].copy()
        drivers = ['esri', 'pci', 'rca', 'vpfi', 'eili']
        
        sensitivity = {}
        
        for driver in drivers:
            # Perturb driver by +/- perturbation
            original = valid_df['cli_predicted'].values
            
            # Create perturbed predictions
            perturbed_up = []
            perturbed_down = []
            
            for _, row in valid_df.iterrows():
                # Get driver values
                d_values = {d: row[d] for d in drivers}
                
                # Perturb up
                d_values_up = d_values.copy()
                d_values_up[driver] = min(d_values[driver] * (1 + perturbation), 1.0)
                cli_up = self._predict_cli_from_drivers(**d_values_up)
                perturbed_up.append(cli_up)
                
                # Perturb down
                d_values_down = d_values.copy()
                d_values_down[driver] = max(d_values[driver] * (1 - perturbation), 0.0)
                cli_down = self._predict_cli_from_drivers(**d_values_down)
                perturbed_down.append(cli_down)
            
            # Calculate sensitivity metrics
            delta_up = np.array(perturbed_up) - original
            delta_down = original - np.array(perturbed_down)
            
            sensitivity[driver] = {
                'mean_delta_up': delta_up.mean(),
                'mean_delta_down': delta_down.mean(),
                'max_delta_up': delta_up.max(),
                'max_delta_down': delta_down.max(),
                'elasticity': (delta_up.mean() + delta_down.mean()) / (2 * perturbation)
            }
        
        self.validation_results['sensitivity'] = sensitivity
        return sensitivity
    
    def _predict_cli_from_drivers(self, esri: float, pci: float, rca: float,
                                  vpfi: float, eili: float) -> float:
        """
        Internal method to recalculate CLI from drivers
        Uses same formula as calculate_drivers.py
        """
        # Economic component
        economic_base = 0.30 * esri + 0.10 * pci + 0.10 * rca
        
        # Political component
        political_base = 0.25 * vpfi + 0.30 * eili
        
        # Interaction
        interaction_boost = 0.10 * (vpfi * eili)
        
        # Combined prediction
        cli_pred = economic_base + political_base + interaction_boost
        
        # Ensure bounds [0, 1]
        cli_pred = max(0.0, min(1.0, cli_pred))
        
        return cli_pred
    
    def plot_sensitivity(self, output_path: str):
        """
        Create sensitivity analysis visualization
        
        Args:
            output_path: Path to save PNG file
        """
        if 'sensitivity' not in self.validation_results:
            self.sensitivity_analysis()
        
        sensitivity = self.validation_results['sensitivity']
        drivers = list(sensitivity.keys())
        driver_labels = ['ESRI\n(Economic)', 'PCI\n(Premature\nConst.)', 
                        'RCA\n(Cost\nAsymmetry)', 'VPFI\n(Veto\nPlayers)', 
                        'EILI\n(Identity)']
        
        # Create figure
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        # Colors
        colors = sns.color_palette("husl", 5)
        
        # 1-5. Individual driver sensitivity bars
        for idx, (driver, label) in enumerate(zip(drivers, driver_labels)):
            ax = axes[idx]
            
            delta_up = sensitivity[driver]['mean_delta_up']
            delta_down = sensitivity[driver]['mean_delta_down']
            
            bars = ax.bar(['−10%', '+10%'], [delta_down, delta_up],
                         color=[colors[idx], colors[idx]], alpha=0.7,
                         edgecolor='black', linewidth=1.5)
            
            ax.set_ylabel('Δ CLI', fontsize=10, weight='bold')
            ax.set_title(f'{label} Sensitivity', fontsize=11, weight='bold')
            ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
            ax.grid(axis='y', alpha=0.3)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.4f}',
                       ha='center', va='bottom' if height > 0 else 'top',
                       fontsize=9)
        
        # 6. Comparative elasticity
        ax = axes[5]
        elasticities = [sensitivity[d]['elasticity'] for d in drivers]
        bars = ax.barh(driver_labels, elasticities, color=colors, alpha=0.7,
                      edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Elasticity (ΔCLI / Δdriver)', fontsize=10, weight='bold')
        ax.set_title('Comparative Driver Elasticity', fontsize=11, weight='bold')
        ax.axvline(x=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{width:.3f}',
                   ha='left' if width > 0 else 'right',
                   va='center', fontsize=9)
        
        # Overall title
        fig.suptitle('Driver Sensitivity Analysis (±10% Perturbation)', 
                    fontsize=14, weight='bold', y=0.995)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Sensitivity plot saved: {output_path}")
    
    def generate_validation_report(self) -> str:
        """
        Generate comprehensive text validation report
        
        Returns:
            Formatted validation report string
        """
        report = []
        report.append("="*70)
        report.append("CRYSTALLIZATION DRIVERS MODEL - VALIDATION REPORT")
        report.append("="*70)
        report.append("")
        
        # Formula-based results
        if 'formula_based' in self.validation_results:
            fb = self.validation_results['formula_based']
            report.append("1. FORMULA-BASED MODEL (THEORETICAL)")
            report.append("-" * 70)
            report.append(f"   Sample size: {fb['n_cases']} cases")
            report.append(f"   MAE (Mean Absolute Error): {fb['mae']:.4f}")
            report.append(f"   RMSE (Root Mean Squared Error): {fb['rmse']:.4f}")
            report.append(f"   R² (Coefficient of Determination): {fb['r2']:.4f}")
            report.append(f"   Max Error: {fb['max_error']:.4f}")
            report.append(f"   Median Error: {fb['median_error']:.4f}")
            report.append(f"   Mean Residual: {fb['mean_residual']:.4f}")
            report.append(f"   Std Residual: {fb['std_residual']:.4f}")
            report.append("")
            
            # Assessment
            if fb['mae'] < 0.15:
                report.append("   ✓ EXCELLENT: MAE < 0.15 (target met)")
            elif fb['mae'] < 0.20:
                report.append("   ✓ GOOD: MAE < 0.20 (acceptable)")
            else:
                report.append("   ⚠ WARNING: MAE ≥ 0.20 (needs improvement)")
            report.append("")
        
        # Linear regression results
        if 'linear_regression' in self.validation_results:
            lr = self.validation_results['linear_regression']
            report.append("2. LINEAR REGRESSION BENCHMARK (ML COMPARISON)")
            report.append("-" * 70)
            report.append(f"   Sample size: {lr['n_cases']} cases")
            report.append(f"   MAE: {lr['mae']:.4f}")
            report.append(f"   RMSE: {lr['rmse']:.4f}")
            report.append(f"   R²: {lr['r2']:.4f}")
            if not np.isnan(lr['cv_mae']):
                report.append(f"   Cross-validation MAE: {lr['cv_mae']:.4f} ± {lr['cv_std']:.4f}")
            report.append("")
            report.append("   Learned Coefficients:")
            for driver, coef in lr['coefficients'].items():
                report.append(f"      {driver.upper()}: {coef:.4f}")
            report.append(f"      Intercept: {lr['intercept']:.4f}")
            report.append("")
        
        # Comparison
        if 'formula_based' in self.validation_results and 'linear_regression' in self.validation_results:
            fb = self.validation_results['formula_based']
            lr = self.validation_results['linear_regression']
            
            report.append("3. MODEL COMPARISON")
            report.append("-" * 70)
            report.append(f"   Formula-based MAE: {fb['mae']:.4f}")
            report.append(f"   ML benchmark MAE: {lr['mae']:.4f}")
            report.append(f"   Difference: {fb['mae'] - lr['mae']:.4f}")
            
            if fb['mae'] <= lr['mae'] * 1.1:
                report.append("   ✓ Theoretical formula competitive with ML benchmark")
            else:
                report.append("   ⚠ ML benchmark significantly outperforms formula")
            report.append("")
        
        # Sensitivity analysis
        if 'sensitivity' in self.validation_results:
            sens = self.validation_results['sensitivity']
            report.append("4. SENSITIVITY ANALYSIS (±10% PERTURBATION)")
            report.append("-" * 70)
            
            for driver, metrics in sens.items():
                report.append(f"   {driver.upper()}:")
                report.append(f"      Elasticity: {metrics['elasticity']:.4f}")
                report.append(f"      Mean Δ (+10%): {metrics['mean_delta_up']:.4f}")
                report.append(f"      Mean Δ (-10%): {metrics['mean_delta_down']:.4f}")
            report.append("")
            
            # Identify most influential driver
            most_elastic = max(sens.items(), key=lambda x: abs(x[1]['elasticity']))
            report.append(f"   Most influential driver: {most_elastic[0].upper()} " +
                        f"(elasticity = {most_elastic[1]['elasticity']:.4f})")
            report.append("")
        
        report.append("="*70)
        
        return "\n".join(report)
    
    def print_report(self):
        """Print validation report to console"""
        print(self.generate_validation_report())
    
    def save_report(self, output_path: str):
        """Save validation report to text file"""
        report = self.generate_validation_report()
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"✓ Validation report saved: {output_path}")


def main():
    """Main execution function"""
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    viz_dir = script_dir.parent / 'visualizations'
    docs_dir = script_dir.parent / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    drivers_path = data_dir / 'crystallization_drivers.csv'
    components_path = data_dir / 'driver_components.csv'
    
    print("Crystallization Drivers Model Validation")
    print("="*70)
    print(f"Drivers data: {drivers_path}")
    print(f"Components data: {components_path}")
    print()
    
    # Initialize validator
    validator = ModelValidator(str(drivers_path), str(components_path))
    
    # Run validations
    print("Running validations...")
    print()
    
    print("1. Formula-based validation...")
    validator.validate_formula_based()
    
    print("2. Linear regression benchmark...")
    validator.validate_linear_regression()
    
    print("3. Sensitivity analysis...")
    validator.sensitivity_analysis()
    print()
    
    # Generate visualizations
    print("Generating visualizations...")
    validator.plot_sensitivity(str(viz_dir / 'sensitivity_analysis.png'))
    print()
    
    # Print and save report
    validator.print_report()
    validator.save_report(str(docs_dir / 'validation_report.txt'))
    print()
    print("="*70)
    print("✓ Validation complete!")
    print("="*70)


if __name__ == '__main__':
    main()

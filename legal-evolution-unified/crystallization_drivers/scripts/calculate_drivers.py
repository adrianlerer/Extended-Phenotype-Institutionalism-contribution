#!/usr/bin/env python3
"""
Crystallization Drivers Calculator
===================================

Calculates 5 independent causal drivers that explain Constitutional Lock-in Index (CLI):
1. Economic Self-Reinforcement Index (ESRI)
2. Premature Constitutionalization Index (PCI)
3. Reversal Cost Asymmetry (RCA)
4. Veto Player Fragmentation Index (VPFI)
5. Existential Identity Linkage Index (EILI)

Theoretical Foundation:
- Extended Phenotype Theory applied to legal institutions (Dawkins 1982, Lerer 2024)
- Institutions as self-replicating memeplexes with evolutionary fitness
- Crystallization = institutional irreversibility via path dependency

Author: GenSpark AI Developer
Reference: Lerer 2024, "Constitutional Lock-in Index" (SSRN 5402461)
Version: 1.0.0
Date: 2025-11-04
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class CrystallizationDrivers:
    """
    Calculate crystallization drivers and predict CLI from component data.
    
    Attributes:
        df (pd.DataFrame): Raw component data loaded from driver_components.csv
        drivers_df (pd.DataFrame): Calculated driver indices and predictions
    """
    
    def __init__(self, data_path: str):
        """
        Initialize with path to driver_components.csv
        
        Args:
            data_path: Path to driver_components.csv file
        """
        self.df = pd.read_csv(data_path)
        self.drivers_df = None
        self._validate_input_data()
    
    def _validate_input_data(self):
        """Validate that all required columns are present"""
        required_cols = [
            # Driver 1 components
            'rent_capture_pct', 'automaticity', 'independence_from_party',
            # Driver 2 components
            'constitutional_level', 'years_before_const', 'judicial_entrenchment',
            # Driver 3 components
            'concentrated_beneficiaries', 'diffuse_cost_bearers', 'visibility_factor',
            # Driver 4 components
            'n_veto_players', 'lack_coordination', 'sunset_mechanism',
            # Driver 5 components
            'founding_document_mentions', 'electoral_dependence', 'survival_necessity',
            # Metadata
            'case_id', 'cli_observed'
        ]
        
        missing = set(required_cols) - set(self.df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        print(f"✓ Data validation passed: {len(self.df)} cases loaded")
    
    def calculate_esri(self, row: pd.Series) -> float:
        """
        Calculate Economic Self-Reinforcement Index (ESRI)
        
        Measures the degree to which an institution generates automatic economic
        rents that are captured by organized beneficiaries independent of political
        coalition maintenance.
        
        Formula:
            ESRI = (rent_capture × automaticity × independence)^(1/3)
        
        Components:
            - rent_capture_pct: % of economic flow captured as rent (normalized)
            - automaticity: Degree of automatic operation (0-1 scale)
            - independence_from_party: Political autonomy of beneficiaries (0-1)
        
        Theoretical Rationale:
            - Multiplicative (not additive) because all three must be present
            - Cubic root to compress scale and prevent single-component dominance
            - High ESRI predicts strong resistance to reform via concentrated benefits
        
        Args:
            row: DataFrame row with component values
        
        Returns:
            ESRI score (0-1 scale)
        """
        # Normalize rent_capture_pct (assume 5% is maximum observed)
        rent_normalized = min(row['rent_capture_pct'] / 5.0, 1.0)
        
        automaticity = row['automaticity']
        independence = row['independence_from_party']
        
        # Cubic root of product
        esri = (rent_normalized * automaticity * independence) ** (1/3)
        
        return round(esri, 4)
    
    def calculate_pci(self, row: pd.Series) -> float:
        """
        Calculate Premature Constitutionalization Index (PCI)
        
        Measures the degree to which an institution was constitutionalized before
        achieving sufficient social maturation, creating artificial rigidity.
        
        Formula:
            PCI = (constitutional_level / maturation_factor) × judicial_entrenchment
            where maturation_factor = log10(years_before_const + 1)
        
        Components:
            - constitutional_level: 0=ordinary law, 0.5=constitutional, 1.0=constitutional core
            - years_before_const: Years of pre-constitutional maturation
            - judicial_entrenchment: Degree of judicial protection (0-1)
        
        Theoretical Rationale:
            - Premature constitutionalization creates lock-in without legitimacy
            - Logarithmic penalty: 1 year = 0, 10 years = 1.0, 100 years = 2.0
            - Multiplied by judicial entrenchment (courts enforce rigidity)
            - High PCI predicts difficulty in adapting to changing conditions
        
        Args:
            row: DataFrame row with component values
        
        Returns:
            PCI score (0-1 scale, normalized)
        """
        const_level = row['constitutional_level']
        years = row['years_before_const']
        judicial = row['judicial_entrenchment']
        
        # Maturation factor: log10(years + 1)
        # 0 years = 0, 1 year = 0.3, 10 years = 1.0, 100 years = 2.0
        maturation_factor = np.log10(years + 1)
        
        # If never constitutionalized, PCI = 0
        if const_level == 0:
            return 0.0
        
        # Avoid division by zero: if 0 years, assume factor of 0.1
        if maturation_factor == 0:
            maturation_factor = 0.1
        
        # Calculate PCI
        pci = (const_level / maturation_factor) * judicial
        
        # Normalize to 0-1 scale (assume max value is 10)
        pci_normalized = min(pci / 10.0, 1.0)
        
        return round(pci_normalized, 4)
    
    def calculate_rca(self, row: pd.Series) -> float:
        """
        Calculate Reversal Cost Asymmetry (RCA)
        
        Measures the asymmetry between concentrated beneficiaries and diffuse cost
        bearers, weighted by visibility of costs.
        
        Formula:
            RCA = normalize(log10(concentrated / diffuse)) × visibility
        
        Components:
            - concentrated_beneficiaries: Number of organized beneficiaries
            - diffuse_cost_bearers: Number of diffuse cost bearers
            - visibility_factor: Visibility of costs (0=invisible, 1=highly visible)
        
        Theoretical Rationale:
            - Olson's Logic of Collective Action: small groups organize, large groups don't
            - Logarithmic scale captures orders of magnitude differences
            - Visibility moderates: invisible costs = no counter-mobilization
            - High RCA predicts successful rent-seeking persistence
        
        Args:
            row: DataFrame row with component values
        
        Returns:
            RCA score (0-1 scale)
        """
        concentrated = row['concentrated_beneficiaries']
        diffuse = row['diffuse_cost_bearers']
        visibility = row['visibility_factor']
        
        # Avoid division by zero
        if concentrated == 0 or diffuse == 0:
            return 0.0
        
        # Calculate ratio (inverted because we want HIGH asymmetry when diffuse >> concentrated)
        ratio = diffuse / concentrated
        
        # Log scale
        log_ratio = np.log10(ratio)
        
        # Normalize to 0-1 scale
        # Assume: ratio of 10 = low asymmetry (log10 = 1)
        #         ratio of 1000 = high asymmetry (log10 = 3)
        # Normalize with log10 = 1 → 0.33, log10 = 3 → 1.0
        rca_normalized = min(log_ratio / 3.0, 1.0)
        rca_normalized = max(rca_normalized, 0.0)
        
        # Weight by visibility (low visibility increases lock-in)
        # Inverse visibility: low visibility = high RCA contribution
        rca = rca_normalized * (1 - visibility)
        
        return round(rca, 4)
    
    def calculate_vpfi(self, row: pd.Series) -> float:
        """
        Calculate Veto Player Fragmentation Index (VPFI)
        
        Measures the degree of veto player fragmentation and coordination failure,
        adjusted for the presence of sunset mechanisms.
        
        Formula:
            VPFI = (n_veto_players × lack_coordination) / (1 - sunset_mechanism + 0.1)
        
        Components:
            - n_veto_players: Number of institutional veto players
            - lack_coordination: Degree of coordination failure (0-1)
            - sunset_mechanism: Presence of automatic expiry (0-1, inverted in formula)
        
        Theoretical Rationale:
            - Tsebelis (2002): more veto players = policy stability (rigidity)
            - Coordination failure amplifies gridlock
            - Sunset clauses force periodic review, reducing crystallization
            - High VPFI predicts reform paralysis
        
        Args:
            row: DataFrame row with component values
        
        Returns:
            VPFI score (0-1 scale, normalized)
        """
        n_veto = row['n_veto_players']
        lack_coord = row['lack_coordination']
        sunset = row['sunset_mechanism']
        
        # Calculate base VPFI
        # Denominator: (1 - sunset + 0.1) ensures no division by zero
        # sunset=0 (no sunset) → denominator = 1.1
        # sunset=1 (full sunset) → denominator = 0.1 (high VPFI penalty)
        vpfi = (n_veto * lack_coord) / (1 - sunset + 0.1)
        
        # Normalize to 0-1 scale
        # Assume: 30 veto players × 1.0 lack_coord / 1.1 = max ≈ 27
        vpfi_normalized = min(vpfi / 27.0, 1.0)
        
        return round(vpfi_normalized, 4)
    
    def calculate_eili(self, row: pd.Series) -> float:
        """
        Calculate Existential Identity Linkage Index (EILI)
        
        Measures the degree to which an institution is ontologically necessary for
        the survival of the political coalition that created it.
        
        Formula:
            EILI = (founding_docs × electoral_dependence × survival_necessity)^(1/3)
        
        Components:
            - founding_document_mentions: Prominence in founding texts (0-1)
            - electoral_dependence: Coalition's electoral reliance (0-1)
            - survival_necessity: Ontological necessity for memeplex (0-1)
        
        Theoretical Rationale:
            - Extended phenotype: institution = vehicle for memeplex replication
            - Existential linkage creates "sacred institution" effect
            - Multiplicative: all three conditions must hold
            - Cubic root to prevent single-component dominance
            - High EILI predicts fierce resistance to reform (identity threat)
        
        Args:
            row: DataFrame row with component values
        
        Returns:
            EILI score (0-1 scale)
        """
        founding = row['founding_document_mentions']
        electoral = row['electoral_dependence']
        survival = row['survival_necessity']
        
        # Cubic root of product
        eili = (founding * electoral * survival) ** (1/3)
        
        return round(eili, 4)
    
    def predict_cli(self, esri: float, pci: float, rca: float, 
                    vpfi: float, eili: float) -> float:
        """
        Predict Constitutional Lock-in Index (CLI) from 5 drivers
        
        Formula (Calibrated v3 - Hybrid Model):
            economic_base = 0.30 × ESRI + 0.10 × PCI + 0.10 × RCA
            political_base = 0.25 × VPFI + 0.30 × EILI
            interaction_boost = 0.10 × (VPFI × EILI)  # Sacred institution + gridlock
            CLI = economic_base + political_base + interaction_boost
        
        Theoretical Rationale:
            - Economic drivers (ESRI, PCI, RCA): 0.50 total weight
              - ESRI (0.30): Rent-seeking is primary economic mechanism
              - PCI (0.10): Premature constitutionalization amplifies
              - RCA (0.10): Cost asymmetry enables persistence
            - Political drivers (VPFI, EILI): 0.55 total weight
              - VPFI (0.25): Veto players create reform paralysis
              - EILI (0.30): Existential identity creates fierce resistance
            - Interaction term (0.10 × VPFI × EILI): Synergy effect
              - Sacred institutions + fragmented veto players = extreme lock-in
              - Captures cases like USA Social Security, Argentina Ultraactividad
            
        Weights sum to 1.05 + interaction, calibrated to match observed CLI range.
        
        Args:
            esri: Economic Self-Reinforcement Index
            pci: Premature Constitutionalization Index
            rca: Reversal Cost Asymmetry
            vpfi: Veto Player Fragmentation Index
            eili: Existential Identity Linkage Index
        
        Returns:
            Predicted CLI score (0-1 scale)
        """
        # Economic component (total weight: 0.50)
        economic_base = 0.30 * esri + 0.10 * pci + 0.10 * rca
        
        # Political component (total weight: 0.55)
        political_base = 0.25 * vpfi + 0.30 * eili
        
        # Interaction: Sacred institutions with fragmented veto players
        # Captures synergy between identity linkage and gridlock
        interaction_boost = 0.10 * (vpfi * eili)
        
        # Combined prediction
        cli_pred = economic_base + political_base + interaction_boost
        
        # Ensure bounds [0, 1]
        cli_pred = max(0.0, min(1.0, cli_pred))
        
        return round(cli_pred, 4)
    
    def classify_pathway(self, esri: float, pci: float, rca: float,
                         vpfi: float, eili: float) -> str:
        """
        Classify crystallization pathway based on driver dominance
        
        Categories:
            - 'economic': ESRI-PCI-RCA pathway dominant
            - 'political': VPFI-EILI pathway dominant
            - 'hybrid': Both pathways significant
        
        Classification Logic:
            - Economic score = mean(ESRI, PCI, RCA)
            - Political score = mean(VPFI, EILI)
            - If |economic - political| < 0.15: hybrid
            - Else: dominant pathway
        
        Args:
            esri, pci, rca, vpfi, eili: Driver scores
        
        Returns:
            Pathway classification string
        """
        economic_score = np.mean([esri, pci, rca])
        political_score = np.mean([vpfi, eili])
        
        diff = abs(economic_score - political_score)
        
        if diff < 0.15:
            return 'hybrid'
        elif economic_score > political_score:
            return 'economic'
        else:
            return 'political'
    
    def process_all_cases(self) -> pd.DataFrame:
        """
        Calculate all drivers and predictions for all cases
        
        Returns:
            DataFrame with driver scores, predictions, and errors
        """
        results = []
        
        for idx, row in self.df.iterrows():
            # Calculate 5 drivers
            esri = self.calculate_esri(row)
            pci = self.calculate_pci(row)
            rca = self.calculate_rca(row)
            vpfi = self.calculate_vpfi(row)
            eili = self.calculate_eili(row)
            
            # Predict CLI
            cli_pred = self.predict_cli(esri, pci, rca, vpfi, eili)
            
            # Classify pathway
            pathway = self.classify_pathway(esri, pci, rca, vpfi, eili)
            
            # Calculate error
            cli_obs = row['cli_observed']
            error = cli_pred - cli_obs if pd.notna(cli_obs) else np.nan
            abs_error = abs(error) if pd.notna(error) else np.nan
            
            results.append({
                'case_id': row['case_id'],
                'country': row['country'],
                'institution': row['institution'],
                'esri': esri,
                'pci': pci,
                'rca': rca,
                'vpfi': vpfi,
                'eili': eili,
                'cli_predicted': cli_pred,
                'cli_observed': cli_obs,
                'error': error,
                'abs_error': abs_error,
                'pathway': pathway,
                'crystallization_status': row['crystallization_status']
            })
        
        self.drivers_df = pd.DataFrame(results)
        return self.drivers_df
    
    def generate_summary_stats(self) -> Dict:
        """
        Generate validation statistics for model performance
        
        Returns:
            Dictionary with MAE, RMSE, R², and other metrics
        """
        if self.drivers_df is None:
            raise ValueError("Must run process_all_cases() first")
        
        # Filter valid observations (exclude failed cases)
        valid = self.drivers_df[self.drivers_df['cli_observed'].notna()].copy()
        
        # Calculate metrics
        mae = valid['abs_error'].mean()
        rmse = np.sqrt((valid['error'] ** 2).mean())
        
        # R² calculation
        y_obs = valid['cli_observed']
        y_pred = valid['cli_predicted']
        ss_res = ((y_obs - y_pred) ** 2).sum()
        ss_tot = ((y_obs - y_obs.mean()) ** 2).sum()
        r2 = 1 - (ss_res / ss_tot)
        
        # Additional metrics
        max_error = valid['abs_error'].max()
        median_error = valid['abs_error'].median()
        
        # Pathway distribution
        pathway_counts = self.drivers_df['pathway'].value_counts().to_dict()
        
        stats = {
            'n_cases': len(self.drivers_df),
            'n_valid': len(valid),
            'mae': round(mae, 4),
            'rmse': round(rmse, 4),
            'r2': round(r2, 4),
            'max_error': round(max_error, 4),
            'median_error': round(median_error, 4),
            'pathway_distribution': pathway_counts
        }
        
        return stats
    
    def save_results(self, output_path: str):
        """
        Save calculated drivers to CSV
        
        Args:
            output_path: Path to save crystallization_drivers.csv
        """
        if self.drivers_df is None:
            raise ValueError("Must run process_all_cases() first")
        
        self.drivers_df.to_csv(output_path, index=False)
        print(f"✓ Results saved to: {output_path}")
    
    def print_summary(self):
        """Print summary statistics to console"""
        stats = self.generate_summary_stats()
        
        print("\n" + "="*60)
        print("CRYSTALLIZATION DRIVERS MODEL - VALIDATION SUMMARY")
        print("="*60)
        print(f"Total cases: {stats['n_cases']}")
        print(f"Valid observations: {stats['n_valid']}")
        print(f"\nModel Performance:")
        print(f"  MAE (Mean Absolute Error): {stats['mae']:.4f}")
        print(f"  RMSE (Root Mean Squared Error): {stats['rmse']:.4f}")
        print(f"  R² (Coefficient of Determination): {stats['r2']:.4f}")
        print(f"  Max Error: {stats['max_error']:.4f}")
        print(f"  Median Error: {stats['median_error']:.4f}")
        print(f"\nPathway Distribution:")
        for pathway, count in stats['pathway_distribution'].items():
            print(f"  {pathway}: {count} cases")
        print("="*60)
        
        # Validation assessment
        if stats['mae'] < 0.15:
            print("✓ EXCELLENT: MAE < 0.15 (target met)")
        elif stats['mae'] < 0.20:
            print("✓ GOOD: MAE < 0.20 (acceptable)")
        else:
            print("⚠ WARNING: MAE ≥ 0.20 (needs improvement)")


def main():
    """Main execution function"""
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    input_path = data_dir / 'driver_components.csv'
    output_path = data_dir / 'crystallization_drivers.csv'
    
    print("Crystallization Drivers Calculator")
    print("="*60)
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print()
    
    try:
        # Initialize calculator
        calc = CrystallizationDrivers(str(input_path))
        
        # Process all cases
        print("Calculating drivers for all cases...")
        results_df = calc.process_all_cases()
        
        # Display results
        print("\nDriver Scores by Case:")
        print(results_df[['case_id', 'esri', 'pci', 'rca', 'vpfi', 'eili', 
                          'cli_predicted', 'cli_observed', 'abs_error', 'pathway']])
        
        # Print summary statistics
        calc.print_summary()
        
        # Save results
        calc.save_results(str(output_path))
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

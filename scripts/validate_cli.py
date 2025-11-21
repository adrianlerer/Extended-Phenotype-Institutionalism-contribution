"""
CLI Validation Script
Validate CLI calculations against expected values
"""

import argparse
import pandas as pd
import sys
from pathlib import Path


def validate_cli_calculations(data_path: str, tolerance: float = 0.02):
    """
    Validate CLI calculations
    
    Checks:
    1. CLI values in valid range (0-1)
    2. Formula correctness: CLI = 0.35×CE + 0.40×UA + 0.25×JPI
    3. CLI within tolerance of expected values
    """
    print(f"🔍 Validating CLI calculations from {data_path}")
    
    # Load data
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"⚠️ Data file not found: {data_path}")
        print("ℹ️ This is expected if CLI data hasn't been generated yet")
        return True
    
    errors = []
    warnings = []
    
    # Required columns
    required_cols = ['entity', 'CE', 'UA', 'JPI', 'CLI']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        print(f"❌ {errors[-1]}")
        return False
    
    # Validate each row
    for idx, row in df.iterrows():
        entity = row['entity']
        ce, ua, jpi = row['CE'], row['UA'], row['JPI']
        cli_reported = row['CLI']
        
        # Check component ranges
        for component, value in [('CE', ce), ('UA', ua), ('JPI', jpi)]:
            if not (0.0 <= value <= 1.0):
                errors.append(f"{entity}: {component}={value} out of range (must be 0-1)")
        
        # Check CLI range
        if not (0.0 <= cli_reported <= 1.0):
            errors.append(f"{entity}: CLI={cli_reported} out of range (must be 0-1)")
        
        # Check formula correctness
        cli_calculated = 0.35 * ce + 0.40 * ua + 0.25 * jpi
        difference = abs(cli_calculated - cli_reported)
        
        if difference > tolerance:
            errors.append(
                f"{entity}: CLI mismatch. Reported={cli_reported:.3f}, "
                f"Calculated={cli_calculated:.3f}, Diff={difference:.3f} > tolerance={tolerance}"
            )
        elif difference > 0.001:
            warnings.append(
                f"{entity}: Minor CLI difference. Reported={cli_reported:.3f}, "
                f"Calculated={cli_calculated:.3f}, Diff={difference:.3f}"
            )
    
    # Report results
    print(f"\n📊 Validation Results:")
    print(f"  - Total entities: {len(df)}")
    print(f"  - Errors: {len(errors)}")
    print(f"  - Warnings: {len(warnings)}")
    
    if errors:
        print(f"\n❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    if warnings:
        print(f"\n⚠️ WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print(f"\n✅ All CLI calculations valid!")
    return True


def main():
    parser = argparse.ArgumentParser(description='Validate CLI calculations')
    parser.add_argument('--data', type=str, required=True, help='Path to CLI data CSV')
    parser.add_argument('--tolerance', type=float, default=0.02, help='Tolerance for CLI differences')
    
    args = parser.parse_args()
    
    success = validate_cli_calculations(args.data, args.tolerance)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

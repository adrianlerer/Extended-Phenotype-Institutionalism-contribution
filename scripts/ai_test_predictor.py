"""
AI Test Predictor
Predict which tests are most likely to fail based on changed files
"""

import argparse
import json
from pathlib import Path
from typing import List, Set


def predict_tests(changed_files: List[str]) -> Set[str]:
    """
    Predict high-risk tests based on changed files
    
    Simple heuristic approach:
    - If CLI calculation file changed → run CLI tests
    - If data files changed → run data validation tests
    - If paper generation changed → run paper builder tests
    """
    predicted_tests = set()
    
    for file_path in changed_files:
        file_path_lower = file_path.lower()
        
        # CLI calculation changes
        if 'cli' in file_path_lower and ('calculator' in file_path_lower or 'calculation' in file_path_lower):
            predicted_tests.add('tests/test_cli_calculator.py')
        
        # Data file changes
        if file_path.startswith('data/') or file_path.endswith('.csv'):
            predicted_tests.add('tests/test_data_validation.py')
        
        # Paper generation changes
        if 'paper' in file_path_lower or 'generate' in file_path_lower:
            predicted_tests.add('tests/test_paper_builder.py')
        
        # Visualization changes
        if 'visual' in file_path_lower or 'figure' in file_path_lower:
            predicted_tests.add('tests/test_visualizations.py')
        
        # Backend route changes
        if 'routes/' in file_path or 'backend/' in file_path:
            predicted_tests.add('tests/test_api.py')
    
    return predicted_tests


def main():
    parser = argparse.ArgumentParser(description='Predict high-risk tests based on changed files')
    parser.add_argument('--changed-files', type=str, required=True, help='Comma-separated list of changed files')
    parser.add_argument('--output-tests', type=str, default='predicted_tests.txt', help='Output file for predicted tests')
    
    args = parser.parse_args()
    
    # Parse changed files
    changed_files = [f.strip() for f in args.changed_files.split(',') if f.strip()]
    
    # Predict tests
    predicted_tests = predict_tests(changed_files)
    
    if predicted_tests:
        # Write to output file
        output_path = Path(args.output_tests)
        output_path.write_text(' '.join(predicted_tests))
        
        print(f"✅ Predicted {len(predicted_tests)} high-risk tests:")
        for test in predicted_tests:
            print(f"  - {test}")
    else:
        print("ℹ️ No high-risk tests predicted")
        # Write empty file
        Path(args.output_tests).write_text('')


if __name__ == '__main__':
    main()

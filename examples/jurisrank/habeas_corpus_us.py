"""
JurisRank Example: Habeas Corpus Doctrine Evolution in U.S. Supreme Court
===========================================================================

This example demonstrates how to use JurisRank to measure doctrinal fitness
of Habeas Corpus cases across multiple decades.

Author: Ignacio Adrián Lerer
License: MIT
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from tools.jurisrank.jurisrank import JurisRank


def create_sample_habeas_corpus_network():
    """
    Create sample citation network for landmark Habeas Corpus cases.
    
    Includes 10 major SCOTUS cases spanning 1953-2008.
    
    Returns:
        tuple: (citation_matrix, case_metadata)
    """
    # 10 landmark Habeas Corpus cases
    cases = [
        {"case_id": "brown_v_allen_1953", "name": "Brown v. Allen", 
         "year": 1953, "court_level": 3},
        {"case_id": "fay_v_noia_1963", "name": "Fay v. Noia", 
         "year": 1963, "court_level": 3},
        {"case_id": "wainwright_v_sykes_1977", "name": "Wainwright v. Sykes", 
         "year": 1977, "court_level": 3},
        {"case_id": "stone_v_powell_1976", "name": "Stone v. Powell", 
         "year": 1976, "court_level": 3},
        {"case_id": "teague_v_lane_1989", "name": "Teague v. Lane", 
         "year": 1989, "court_level": 3},
        {"case_id": "felker_v_turpin_1996", "name": "Felker v. Turpin", 
         "year": 1996, "court_level": 3},
        {"case_id": "ins_v_st_cyr_2001", "name": "INS v. St. Cyr", 
         "year": 2001, "court_level": 3},
        {"case_id": "hamdi_v_rumsfeld_2004", "name": "Hamdi v. Rumsfeld", 
         "year": 2004, "court_level": 3},
        {"case_id": "rasul_v_bush_2004", "name": "Rasul v. Bush", 
         "year": 2004, "court_level": 3},
        {"case_id": "boumediene_v_bush_2008", "name": "Boumediene v. Bush", 
         "year": 2008, "court_level": 3}
    ]
    
    # Create metadata DataFrame
    metadata = pd.DataFrame(cases)
    metadata['date'] = pd.to_datetime(metadata['year'], format='%Y')
    
    # Citation matrix (10x10)
    # Row cites Column (recent cases cite older ones)
    citation_matrix = np.array([
        # Brown  Fay  Wain  Stone Teague Felker St_Cyr Hamdi Rasul Boum
        [  0,    0,    0,    0,    0,     0,     0,     0,    0,    0  ],  # Brown (1953)
        [  1,    0,    0,    0,    0,     0,     0,     0,    0,    0  ],  # Fay (1963)
        [  1,    1,    0,    0,    0,     0,     0,     0,    0,    0  ],  # Wainwright (1977)
        [  1,    1,    0,    0,    0,     0,     0,     0,    0,    0  ],  # Stone (1976)
        [  1,    0,    1,    1,    0,     0,     0,     0,    0,    0  ],  # Teague (1989)
        [  0,    0,    1,    0,    1,     0,     0,     0,    0,    0  ],  # Felker (1996)
        [  1,    1,    0,    0,    1,     1,     0,     0,    0,    0  ],  # St. Cyr (2001)
        [  0,    0,    0,    0,    0,     0,     1,     0,    0,    0  ],  # Hamdi (2004)
        [  0,    0,    0,    0,    0,     0,     1,     0,    0,    0  ],  # Rasul (2004)
        [  1,    1,    1,    1,    1,     1,     1,     1,    1,    0  ]   # Boumediene (2008)
    ])
    
    return citation_matrix, metadata


def run_jurisrank_analysis():
    """Run complete JurisRank analysis on Habeas Corpus cases."""
    
    print("=" * 80)
    print("JURISRANK ANALYSIS: U.S. SUPREME COURT HABEAS CORPUS DOCTRINE")
    print("=" * 80)
    print()
    
    # Step 1: Load data
    print("Step 1: Loading citation network...")
    citation_matrix, metadata = create_sample_habeas_corpus_network()
    print(f"  ✓ Loaded {len(metadata)} cases spanning {metadata['year'].min()}-{metadata['year'].max()}")
    print()
    
    # Step 2: Initialize JurisRank
    print("Step 2: Initializing JurisRank calculator...")
    ranker = JurisRank(
        damping_factor=0.85,          # Standard PageRank damping
        temporal_decay=0.05,          # 5% annual decay
        convergence_threshold=0.0001,
        max_iterations=100
    )
    print("  ✓ JurisRank initialized")
    print()
    
    # Step 3: Calculate fitness scores
    print("Step 3: Calculating doctrinal fitness scores...")
    fitness_scores = ranker.calculate_jurisrank(citation_matrix, metadata)
    print(f"  ✓ Converged in {len(ranker.fitness_history)} iterations")
    print()
    
    # Step 4: Analyze results
    print("Step 4: Analyzing results...")
    print()
    
    # Create results DataFrame
    results = []
    for case_id, fitness in fitness_scores.items():
        case_info = metadata[metadata['case_id'] == case_id].iloc[0]
        
        # Calculate citation counts
        case_idx = metadata[metadata['case_id'] == case_id].index[0]
        citations_received = citation_matrix[:, case_idx].sum()
        citations_made = citation_matrix[case_idx, :].sum()
        
        # Classify fitness
        if fitness >= 0.70:
            fitness_category = "DOMINANT"
        elif fitness >= 0.40:
            fitness_category = "HIGH"
        elif fitness >= 0.20:
            fitness_category = "MODERATE"
        elif fitness >= 0.10:
            fitness_category = "LOW"
        else:
            fitness_category = "MARGINAL"
        
        results.append({
            'case_name': case_info['name'],
            'year': case_info['year'],
            'jurisrank': fitness,
            'citations_received': int(citations_received),
            'citations_made': int(citations_made),
            'fitness_category': fitness_category
        })
    
    results_df = pd.DataFrame(results).sort_values('jurisrank', ascending=False)
    
    # Display top cases
    print("=" * 80)
    print("TOP 5 MOST FIT DOCTRINES")
    print("=" * 80)
    print()
    
    for idx, row in results_df.head(5).iterrows():
        print(f"{idx+1}. {row['case_name']} ({int(row['year'])})")
        print(f"   JurisRank: {row['jurisrank']:.3f}")
        print(f"   Citations Received: {int(row['citations_received'])}")
        print(f"   Citations Made: {int(row['citations_made'])}")
        print(f"   Fitness: {row['fitness_category']}")
        print()
    
    # Display full ranking table
    print("=" * 80)
    print("COMPLETE RANKING")
    print("=" * 80)
    print()
    print(results_df.to_string(index=False))
    print()
    
    # Key insights
    print("=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print()
    
    # Most fit doctrine
    top_case = results_df.iloc[0]
    print(f"📌 MOST FIT DOCTRINE:")
    print(f"   {top_case['case_name']} ({int(top_case['year'])}) with JurisRank = {top_case['jurisrank']:.3f}")
    print(f"   This doctrine has the highest replicative strength and is most likely")
    print(f"   to persist transgenerationally.")
    print()
    
    # Temporal pattern
    print(f"📈 TEMPORAL PATTERN:")
    recent_avg = results_df[results_df['year'] >= 2000]['jurisrank'].mean()
    older_avg = results_df[results_df['year'] < 2000]['jurisrank'].mean()
    print(f"   Recent cases (2000+): Average JurisRank = {recent_avg:.3f}")
    print(f"   Older cases (<2000):  Average JurisRank = {older_avg:.3f}")
    
    if recent_avg > older_avg:
        print(f"   → Recent doctrines gaining dominance (temporal recency effect)")
    else:
        print(f"   → Older doctrines retain influence (precedential weight effect)")
    print()
    
    # Hub identification
    dominant_cases = results_df[results_df['fitness_category'] == 'DOMINANT']
    print(f"🎯 DOMINANT DOCTRINES:")
    print(f"   {len(dominant_cases)} case(s) achieved DOMINANT fitness (≥0.70)")
    if len(dominant_cases) > 0:
        print(f"   These are 'hub' cases in the doctrinal space:")
        for _, case in dominant_cases.iterrows():
            print(f"     - {case['case_name']} ({int(case['year'])})")
    print()
    
    # Extinction risk
    marginal_cases = results_df[results_df['fitness_category'].isin(['LOW', 'MARGINAL'])]
    if len(marginal_cases) > 0:
        print(f"⚠️  EXTINCTION RISK:")
        print(f"   {len(marginal_cases)} case(s) have LOW/MARGINAL fitness (<0.20)")
        print(f"   These doctrines are peripheral and may face eventual extinction:")
        for _, case in marginal_cases.iterrows():
            print(f"     - {case['case_name']} ({int(case['year'])}): JurisRank = {case['jurisrank']:.3f}")
    print()
    
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Use RootFinder to trace genealogy of top-fitness doctrines")
    print("  2. Use Legal-Memespace to map competitive dynamics")
    print("  3. Track fitness evolution over time with temporal slices")
    print()
    
    return results_df, fitness_scores


if __name__ == "__main__":
    results_df, fitness_scores = run_jurisrank_analysis()
    
    # Optional: Save results
    # results_df.to_csv('habeas_corpus_jurisrank_results.csv', index=False)
    # print("Results saved to habeas_corpus_jurisrank_results.csv")

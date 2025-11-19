"""
Enhanced Interactive Coder with FRP Integration
================================================

Extends InteractiveCoder to include optional Fractal Reasoning Protocol (FRP) analysis
for deeper narrative understanding beyond simple complexity scoring.

Author: Legal Evolution Project
Date: 2025-11-01
"""

import pandas as pd
import os
from typing import Optional, Dict, List
from datetime import datetime

from ..interactive_coder import InteractiveCoder, NarrativeScore
from ..complexity_heuristics import ComplexityScorer
from .fractal_analyzer import FractalAnalyzer, DomainContext, FRPAnalysis


class EnhancedInteractiveCoder(InteractiveCoder):
    """
    Extended InteractiveCoder with FRP capabilities.
    
    Adds optional multi-level FRP analysis to complexity scoring workflow.
    Useful for:
    - Deep-dive analysis of select cases
    - Training data for future ML models
    - Qualitative validation of complexity scores
    """
    
    def __init__(self,
                 scoring_method: str = 'heuristic',
                 language: str = 'es',
                 verbose: bool = True,
                 enable_frp: bool = False,
                 frp_domain: str = 'constitutional',
                 frp_levels: List[str] = ['L1', 'L2', 'L3']):
        """
        Initialize enhanced coder.
        
        Args:
            scoring_method: 'heuristic' (only option for Level 1)
            language: 'es' or 'en'
            verbose: Print detailed output
            enable_frp: Whether to include FRP analysis
            frp_domain: Domain for FRP analysis ('constitutional', 'political', etc.)
            frp_levels: Which FRP levels to execute (default: L1-L3 for speed)
        """
        super().__init__(scoring_method, language, verbose)
        
        self.enable_frp = enable_frp
        self.frp_levels = frp_levels
        
        if enable_frp:
            # Initialize FRP analyzer
            domain_context = DomainContext(
                domain=frp_domain,
                sub_domain='sovereignty_vs_globalism' if frp_domain == 'constitutional' else None,
                jurisdiction='comparative',
                additional_context={'language': language}
            )
            self.frp_analyzer = FractalAnalyzer(domain_context)
        else:
            self.frp_analyzer = None
    
    def propose_score_with_frp(
        self,
        text: str,
        case_id: str = '',
        ai_callback: Optional[callable] = None
    ) -> Dict:
        """
        Propose C score AND generate FRP analysis.
        
        Args:
            text: Narrative text
            case_id: Case identifier
            ai_callback: Function to call AI model for FRP (optional)
        
        Returns:
            Dict with both complexity score and FRP analysis
        """
        # Get base complexity score
        narrative_score = self.propose_score(text, case_id)
        
        result = {
            'case_id': case_id,
            'complexity_score': narrative_score.proposed_score,
            'confidence': narrative_score.confidence,
            'features': narrative_score.features,
            'frp_analysis': None
        }
        
        # Add FRP analysis if enabled
        if self.enable_frp and self.frp_analyzer:
            question = f"Analyze the complexity and strategic framing of this sovereignty narrative (C={narrative_score.proposed_score:.1f})."
            
            frp_result = self.frp_analyzer.analyze_narrative(
                text,
                question,
                levels=self.frp_levels,
                ai_callback=ai_callback
            )
            
            result['frp_analysis'] = frp_result
        
        return result
    
    def code_with_frp_deepdive(
        self,
        input_file: str,
        text_column: str,
        id_column: str,
        output_file: str,
        frp_output_dir: str = 'data/processed/frp_deepdive',
        deepdive_threshold: float = 7.0,
        ai_callback: Optional[callable] = None
    ) -> pd.DataFrame:
        """
        Code dataset with FRP deep-dive for high-complexity cases.
        
        Workflow:
        1. Score all narratives normally
        2. For cases with C >= deepdive_threshold, run full FRP analysis
        3. Save FRP analyses separately for manual review
        
        Args:
            input_file: Input CSV/Excel
            text_column: Column with narrative text
            id_column: Column with case IDs
            output_file: Output CSV for scores
            frp_output_dir: Directory for FRP analyses
            deepdive_threshold: C score threshold for FRP analysis
            ai_callback: AI model callback (required for FRP)
        
        Returns:
            DataFrame with scores and FRP flags
        """
        # First pass: code all narratives
        print(f"\n{'='*80}")
        print("PHASE 1: Complexity Scoring (All Cases)")
        print(f"{'='*80}\n")
        
        df_scored = self.code_dataset_interactive(
            input_file=input_file,
            text_column=text_column,
            id_column=id_column,
            output_file=output_file,
            resume=False
        )
        
        # Second pass: FRP deep-dive for high-complexity cases
        if self.enable_frp and ai_callback:
            print(f"\n{'='*80}")
            print(f"PHASE 2: FRP Deep-Dive (C >= {deepdive_threshold})")
            print(f"{'='*80}\n")
            
            os.makedirs(frp_output_dir, exist_ok=True)
            
            high_complexity = df_scored[df_scored['C_Coded'] >= deepdive_threshold]
            
            if len(high_complexity) == 0:
                print(f"No cases meet threshold C >= {deepdive_threshold}. Skipping FRP phase.")
            else:
                print(f"Found {len(high_complexity)} cases for deep-dive analysis.\n")
                
                frp_files = []
                
                for idx, row in high_complexity.iterrows():
                    case_id = row[id_column]
                    text = row[text_column]
                    c_score = row['C_Coded']
                    
                    print(f"[{case_id}] Running FRP analysis (C={c_score:.1f})...")
                    
                    question = f"Conduct deep analysis of this sovereignty narrative (Complexity Score: {c_score:.1f})."
                    
                    frp_analysis = self.frp_analyzer.analyze_narrative(
                        text,
                        question,
                        levels=['L1', 'L2', 'L3', 'L4', 'L5'],  # Full 5 levels for deepdive
                        ai_callback=ai_callback
                    )
                    
                    # Save as JSON
                    json_file = os.path.join(frp_output_dir, f"frp_{case_id}.json")
                    frp_analysis.to_json(json_file)
                    
                    # Save as Markdown for easy reading
                    md_file = os.path.join(frp_output_dir, f"frp_{case_id}.md")
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(frp_analysis.to_markdown())
                    
                    frp_files.append(json_file)
                    print(f"  ✓ Saved: {md_file}\n")
                
                # Add FRP file paths to dataframe
                df_scored['FRP_Analysis'] = None
                for idx, row in high_complexity.iterrows():
                    case_id = row[id_column]
                    frp_file = os.path.join(frp_output_dir, f"frp_{case_id}.json")
                    df_scored.at[idx, 'FRP_Analysis'] = frp_file
                
                # Save updated dataframe
                df_scored.to_csv(output_file, index=False)
                print(f"✓ Updated {output_file} with FRP analysis paths.")
        
        return df_scored
    
    def display_proposal_with_frp(
        self,
        proposal: Dict,
        show_frp_levels: List[str] = ['L1', 'L2']
    ):
        """
        Display proposal with optional FRP insights.
        
        Args:
            proposal: Result from propose_score_with_frp()
            show_frp_levels: Which FRP levels to display in terminal
        """
        # Show standard complexity score
        print(f"\n{'='*80}")
        print(f"PROPOSED COMPLEXITY SCORE: {proposal['complexity_score']:.1f}/10")
        print(f"Confidence: {proposal['confidence']:.0f}%")
        print(f"{'='*80}")
        
        print("\n📊 FEATURES DETECTED:")
        features = proposal['features']
        print(f"  • Binary markers: {features['binary_markers']} occurrences")
        print(f"  • Technical terms: {features['technical_terms']} occurrences")
        print(f"  • Emotional words: {features['emotional_words']} occurrences")
        print(f"  • Avg sentence length: {features['avg_sentence_length']:.1f} words")
        print(f"  • Subordinate clauses: {features['subordinate_clauses']} clauses")
        
        # Show FRP insights if available
        if proposal.get('frp_analysis'):
            frp: FRPAnalysis = proposal['frp_analysis']
            
            print(f"\n{'='*80}")
            print("🧠 FRACTAL REASONING INSIGHTS")
            print(f"{'='*80}")
            
            for level in frp.levels:
                if level.level in show_frp_levels:
                    print(f"\n{level.title}:")
                    print(f"{level.content[:300]}..." if len(level.content) > 300 else level.content)
        
        print(f"\n{'='*80}\n")


# ============================================================================
# CLI INTEGRATION
# ============================================================================

def main():
    """CLI entry point for enhanced coder"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Enhanced Interactive Coder with FRP capabilities'
    )
    parser.add_argument('--input', required=True, help='Input CSV/Excel file')
    parser.add_argument('--text-column', required=True, help='Column with narrative text')
    parser.add_argument('--id-column', required=True, help='Column with case IDs')
    parser.add_argument('--output', required=True, help='Output CSV file')
    parser.add_argument('--enable-frp', action='store_true', help='Enable FRP analysis')
    parser.add_argument('--frp-domain', default='constitutional', 
                       choices=['constitutional', 'political', 'legal'],
                       help='Domain for FRP analysis')
    parser.add_argument('--frp-deepdive', action='store_true',
                       help='Run full FRP for high-complexity cases')
    parser.add_argument('--deepdive-threshold', type=float, default=7.0,
                       help='C score threshold for FRP deepdive')
    parser.add_argument('--frp-output-dir', default='data/processed/frp_deepdive',
                       help='Directory for FRP analyses')
    parser.add_argument('--language', default='es', choices=['es', 'en'],
                       help='Language for analysis')
    parser.add_argument('--resume', action='store_true', help='Resume previous session')
    
    args = parser.parse_args()
    
    # Initialize coder
    coder = EnhancedInteractiveCoder(
        language=args.language,
        enable_frp=args.enable_frp or args.frp_deepdive,
        frp_domain=args.frp_domain,
        frp_levels=['L1', 'L2', 'L3']
    )
    
    # Run coding
    if args.frp_deepdive:
        print("⚠️  FRP Deep-Dive requires AI callback. Run programmatically with ai_callback parameter.")
        print("    Falling back to standard coding...\n")
        df = coder.code_dataset_interactive(
            input_file=args.input,
            text_column=args.text_column,
            id_column=args.id_column,
            output_file=args.output,
            resume=args.resume
        )
    else:
        df = coder.code_dataset_interactive(
            input_file=args.input,
            text_column=args.text_column,
            id_column=args.id_column,
            output_file=args.output,
            resume=args.resume
        )
    
    print(f"\n✅ Coding complete! Results saved to: {args.output}")


if __name__ == '__main__':
    main()

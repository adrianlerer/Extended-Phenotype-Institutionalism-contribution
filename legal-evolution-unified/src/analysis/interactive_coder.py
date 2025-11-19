"""
Interactive Narrative Complexity Coder

CLI tool for coding political narratives with AI assistance.

Features:
- Proposes C scores using heuristics
- Interactive accept/edit/skip workflow
- Auto-save after each case (no data loss)
- Resume capability
- Progress tracking
"""

import pandas as pd
import sys
import os
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime
import argparse

from .complexity_heuristics import ComplexityScorer


@dataclass
class NarrativeScore:
    """Result of scoring a narrative."""
    case_id: str
    text: str
    proposed_score: float
    confidence: float
    features: dict
    human_score: Optional[float] = None
    notes: Optional[str] = None
    timestamp: Optional[str] = None


class InteractiveCoder:
    """
    Interactive CLI tool for coding narrative complexity.
    
    Workflow:
    1. Load CSV/Excel with narratives
    2. For each narrative:
       a. Propose C score using heuristics
       b. Show features and justification
       c. User accepts/edits in terminal
       d. Save to CSV progressively
    3. Generate completion report
    """
    
    def __init__(self, 
                 scoring_method: str = 'heuristic',
                 language: str = 'es',
                 verbose: bool = True):
        """
        Initialize coder.
        
        Args:
            scoring_method: 'heuristic' (only option for Level 1)
            language: 'es' or 'en'
            verbose: Print detailed output
        """
        self.scoring_method = scoring_method
        self.language = language
        self.verbose = verbose
        self.scorer = ComplexityScorer(language=language)
        self.corrections = []  # Track user edits
        self.start_time = None
        self.end_time = None
    
    def propose_score(self, text: str, case_id: str = '') -> NarrativeScore:
        """
        Propose C score for a narrative.
        
        Args:
            text: Narrative text
            case_id: Case identifier
            
        Returns:
            NarrativeScore with proposal and justification
        """
        result = self.scorer.score_narrative(text)
        
        return NarrativeScore(
            case_id=case_id,
            text=text,
            proposed_score=result['score'],
            confidence=result['confidence'],
            features=result['features']
        )
    
    def code_dataset_interactive(self,
                                 input_file: str,
                                 text_column: str,
                                 id_column: str,
                                 output_file: str,
                                 resume: bool = False) -> pd.DataFrame:
        """
        Interactive CLI coding of dataset.
        
        For each case:
        1. Display ID and narrative text
        2. Propose C score with justification
        3. Prompt: Accept/Edit/Skip/Info/Quit
        4. Save after each case
        
        Args:
            input_file: CSV or Excel with narratives
            text_column: Column name with narrative text
            id_column: Column name with unique ID
            output_file: CSV output file path
            resume: Continue from last saved case
            
        Returns:
            DataFrame with coded results
        """
        self.start_time = datetime.now()
        
        # Load input data
        if input_file.endswith('.xlsx'):
            df = pd.read_excel(input_file)
        else:
            df = pd.read_csv(input_file)
        
        if self.verbose:
            print(f"\n{'='*60}")
            print("Interactive Narrative Complexity Coder")
            print(f"{'='*60}")
            print(f"Input: {input_file}")
            print(f"Text column: {text_column}")
            print(f"ID column: {id_column}")
            print(f"Output: {output_file}")
            print(f"{'='*60}\n")
        
        # Check columns exist
        if id_column not in df.columns:
            raise ValueError(f"ID column '{id_column}' not found in dataset")
        if text_column not in df.columns:
            raise ValueError(f"Text column '{text_column}' not found in dataset")
        
        # Load existing coded data if resuming
        coded_ids = set()
        if resume and os.path.exists(output_file):
            try:
                existing_df = pd.read_csv(output_file)
                coded_ids = set(existing_df[id_column].values)
                if self.verbose:
                    print(f"📂 Resuming: {len(coded_ids)} cases already coded")
                    print(f"{'='*60}\n")
            except Exception as e:
                print(f"⚠️  Warning: Could not load existing file: {e}")
                print("Starting fresh...\n")
        else:
            if self.verbose:
                print(f"📝 Starting fresh: 0 cases coded")
                print(f"{'='*60}\n")
        
        # Filter to uncoded cases
        uncoded_df = df[~df[id_column].isin(coded_ids)].reset_index(drop=True)
        total_to_code = len(uncoded_df)
        
        if total_to_code == 0:
            print("✅ All cases already coded!")
            return pd.read_csv(output_file)
        
        if self.verbose:
            print(f"Cases to code: {total_to_code}")
            print(f"{'='*60}\n")
        
        # Interactive loop
        results = []
        cases_coded = 0
        
        for idx, row in uncoded_df.iterrows():
            case_id = row[id_column]
            text = str(row[text_column])
            
            if pd.isna(text) or text.strip() == '':
                print(f"⚠️  Skipping {case_id}: Empty narrative")
                continue
            
            # Propose score
            proposal = self.propose_score(text, case_id=case_id)
            
            # Display to user
            self._display_case(case_id, text, proposal, 
                             idx + 1, total_to_code, cases_coded + len(coded_ids))
            
            # Get user input
            action, human_score, notes = self._get_user_input(proposal.proposed_score)
            
            if action == 'quit':
                print("\n🛑 Quitting... Progress saved.")
                break
            elif action == 'skip':
                print("⏭️  Skipped\n")
                continue
            elif action == 'accept':
                human_score = proposal.proposed_score
                print(f"✅ Accepted: C = {human_score}\n")
            elif action == 'edit':
                print(f"✏️  Edited: C = {human_score}\n")
                self.corrections.append({
                    'case_id': case_id,
                    'proposed': proposal.proposed_score,
                    'human': human_score,
                    'diff': human_score - proposal.proposed_score
                })
            
            # Save result
            result_row = {
                id_column: case_id,
                text_column: text,
                'proposed_score': proposal.proposed_score,
                'human_score': human_score,
                'confidence': proposal.confidence,
                'notes': notes if notes else '',
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result_row)
            cases_coded += 1
            
            # Auto-save after each case
            self._save_progress(results, output_file, existing_df if resume else None)
        
        # Final report
        self.end_time = datetime.now()
        coded_df = pd.read_csv(output_file)
        
        if self.verbose:
            self._print_completion_report(cases_coded, total_to_code)
        
        return coded_df
    
    def _display_case(self, case_id: str, text: str, proposal: NarrativeScore,
                     current: int, total: int, total_coded: int):
        """Display case information to user."""
        print(f"\n[{current}/{total}] Case ID: {case_id}")
        print(f"Total coded so far: {total_coded + current - 1}")
        print("━" * 60)
        
        # Wrap text for readability
        wrapped_text = self._wrap_text(text, width=58)
        print("Narrative:")
        print(wrapped_text)
        print("━" * 60)
        print()
        
        # Show proposed score
        print(f"Proposed C Score: {proposal.proposed_score} / 10")
        print(f"Confidence: {proposal.confidence:.0%}")
        print()
        
        # Show features analysis
        print("Features Analysis:")
        result = self.scorer.score_narrative(text)
        for line in result['explanation']:
            print(f"  {line}")
        print()
    
    def _get_user_input(self, proposed_score: float) -> tuple:
        """
        Get user action and optional new score/notes.
        
        Returns:
            (action, human_score, notes)
            action: 'accept', 'edit', 'skip', 'quit', 'info'
        """
        while True:
            prompt = f"Accept [{proposed_score}], Edit [e], Skip [s], Info [i], Quit [q]: "
            user_input = input(prompt).strip().lower()
            
            if user_input == '' or user_input == str(proposed_score):
                return ('accept', proposed_score, None)
            
            elif user_input == 'e':
                while True:
                    try:
                        new_score = input("Enter new C score (1-10): ").strip()
                        new_score = float(new_score)
                        if 1 <= new_score <= 10:
                            break
                        else:
                            print("⚠️  Score must be between 1 and 10")
                    except ValueError:
                        print("⚠️  Please enter a valid number")
                
                notes = input("Optional note (press Enter to skip): ").strip()
                return ('edit', new_score, notes if notes else None)
            
            elif user_input == 's':
                return ('skip', None, None)
            
            elif user_input == 'q':
                return ('quit', None, None)
            
            elif user_input == 'i':
                self._show_info()
                continue
            
            else:
                print("⚠️  Invalid input. Use: Enter/e/s/i/q")
    
    def _show_info(self):
        """Show help information."""
        print("\n" + "─" * 60)
        print("HELP:")
        print("  [Enter] or [score]  → Accept proposed score")
        print("  [e]                 → Edit score manually")
        print("  [s]                 → Skip this case")
        print("  [i]                 → Show this help")
        print("  [q]                 → Quit and save progress")
        print("─" * 60 + "\n")
    
    def _wrap_text(self, text: str, width: int = 58) -> str:
        """Wrap text for display."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > width:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                current_line.append(word)
                current_length += len(word) + 1
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def _save_progress(self, results: list, output_file: str, 
                      existing_df: Optional[pd.DataFrame] = None):
        """Save progress to CSV."""
        new_df = pd.DataFrame(results)
        
        if existing_df is not None:
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        combined_df.to_csv(output_file, index=False)
    
    def _print_completion_report(self, coded_count: int, total_count: int):
        """Print final completion report."""
        print("\n" + "=" * 60)
        print("CODING SESSION COMPLETED!")
        print("=" * 60)
        
        elapsed = (self.end_time - self.start_time).total_seconds()
        
        print(f"Cases coded this session: {coded_count} / {total_count}")
        print(f"Total time: {elapsed/60:.1f} minutes")
        
        if coded_count > 0:
            print(f"Average time per case: {elapsed/coded_count:.1f} seconds")
        
        if self.corrections:
            acceptance_rate = 1 - (len(self.corrections) / coded_count)
            print(f"Acceptance rate: {acceptance_rate:.1%}")
            
            avg_adjustment = sum(abs(c['diff']) for c in self.corrections) / len(self.corrections)
            print(f"Average adjustment when edited: {avg_adjustment:.2f} points")
        else:
            print("Acceptance rate: 100% (all proposals accepted)")
        
        print("=" * 60 + "\n")
    
    def generate_report(self, coded_df: pd.DataFrame) -> dict:
        """
        Generate coding statistics report.
        
        Args:
            coded_df: DataFrame with coded results
            
        Returns:
            Dict with metrics
        """
        n_coded = len(coded_df)
        
        if 'proposed_score' in coded_df.columns and 'human_score' in coded_df.columns:
            n_accepted = (coded_df['proposed_score'] == coded_df['human_score']).sum()
            acceptance_rate = n_accepted / n_coded if n_coded > 0 else 0
            
            adjustments = coded_df['human_score'] - coded_df['proposed_score']
            avg_adjustment = adjustments[adjustments != 0].abs().mean()
        else:
            acceptance_rate = 0
            avg_adjustment = 0
        
        return {
            'n_coded': n_coded,
            'acceptance_rate': acceptance_rate,
            'avg_adjustment': avg_adjustment if not pd.isna(avg_adjustment) else 0,
            'avg_time_seconds': 0  # Would need timestamp tracking
        }


# ===== CLI ENTRY POINT =====

def main():
    """CLI entry point for interactive coder."""
    parser = argparse.ArgumentParser(
        description='Interactive narrative complexity coder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python -m src.analysis.interactive_coder \\
    --input data/raw/cases.csv \\
    --text-column Sov_Narrative \\
    --id-column Case_ID \\
    --output data/processed/coded_sov.csv \\
    --resume
        """
    )
    
    parser.add_argument('--input', required=True, 
                       help='Input file (CSV or Excel)')
    parser.add_argument('--text-column', required=True,
                       help='Column with narrative text')
    parser.add_argument('--id-column', required=True,
                       help='Column with unique case ID')
    parser.add_argument('--output', required=True,
                       help='Output CSV file path')
    parser.add_argument('--resume', action='store_true',
                       help='Resume from last saved case')
    parser.add_argument('--method', default='heuristic',
                       choices=['heuristic'],
                       help='Scoring method (only heuristic for Level 1)')
    parser.add_argument('--language', default='es',
                       choices=['es', 'en'],
                       help='Language of narratives')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output')
    
    args = parser.parse_args()
    
    # Create coder
    coder = InteractiveCoder(
        scoring_method=args.method,
        language=args.language,
        verbose=not args.quiet
    )
    
    try:
        # Run interactive coding
        result_df = coder.code_dataset_interactive(
            input_file=args.input,
            text_column=args.text_column,
            id_column=args.id_column,
            output_file=args.output,
            resume=args.resume
        )
        
        # Print final summary
        if not args.quiet:
            print(f"\n✅ Output saved to: {args.output}")
            print(f"   Total cases coded: {len(result_df)}\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user. Progress saved.")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

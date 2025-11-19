"""
Tests for Fractal Reasoning Protocol (FRP) Analyzer

Tests cover:
- Prompt generation for all 5 levels
- Domain-specific guidance
- Batch analysis functionality
- Integration with complexity scoring
"""

import pytest
import pandas as pd
import json
import os
from pathlib import Path

from src.analysis.frp import (
    FractalAnalyzer,
    DomainContext,
    FRPAnalysis,
    FRPLevelOutput,
    FRPPromptGenerator,
    create_constitutional_analyzer,
    create_political_analyzer
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def sample_narrative():
    """Sample sovereignty narrative for testing"""
    return """
    Our nation's sovereignty is under threat from international tribunals that 
    seek to impose their will on our democratic institutions. We must defend our 
    constitutional order against these external pressures that undermine the voice 
    of our people and their elected representatives. The principle of complementarity
    must be respected, and our domestic courts must retain final authority over 
    matters of national importance.
    """


@pytest.fixture
def constitutional_context():
    """Constitutional domain context"""
    return DomainContext(
        domain='constitutional',
        sub_domain='sovereignty_vs_globalism',
        jurisdiction='comparative',
        additional_context={'focus': 'narrative_complexity'}
    )


@pytest.fixture
def political_context():
    """Political domain context"""
    return DomainContext(
        domain='political',
        sub_domain='constitutional_conflict',
        additional_context={'focus': 'framing_strategies'}
    )


@pytest.fixture
def analyzer(constitutional_context):
    """FractalAnalyzer instance"""
    return FractalAnalyzer(constitutional_context)


# ============================================================================
# DOMAIN CONTEXT TESTS
# ============================================================================

def test_domain_context_creation(constitutional_context):
    """Test DomainContext initialization"""
    assert constitutional_context.domain == 'constitutional'
    assert constitutional_context.sub_domain == 'sovereignty_vs_globalism'
    assert constitutional_context.jurisdiction == 'comparative'
    assert 'focus' in constitutional_context.additional_context


def test_constitutional_analyzer_factory():
    """Test factory function for constitutional analyzer"""
    analyzer = create_constitutional_analyzer()
    assert analyzer.domain_context.domain == 'constitutional'
    assert analyzer.domain_context.sub_domain == 'sovereignty_vs_globalism'


def test_political_analyzer_factory():
    """Test factory function for political analyzer"""
    analyzer = create_political_analyzer()
    assert analyzer.domain_context.domain == 'political'
    assert analyzer.domain_context.sub_domain == 'constitutional_conflict'


# ============================================================================
# PROMPT GENERATION TESTS
# ============================================================================

def test_prompt_generator_l1(sample_narrative, constitutional_context):
    """Test L1 prompt generation"""
    question = "Analyze the complexity of this narrative."
    
    prompt = FRPPromptGenerator.get_l1_prompt(
        sample_narrative,
        question,
        constitutional_context
    )
    
    # Check key elements present
    assert "LEVEL 1: MACRO VIEW" in prompt
    assert constitutional_context.domain in prompt
    assert question in prompt
    assert "What's at stake here?" in prompt
    assert "3-5 sentences" in prompt


def test_prompt_generator_l2(sample_narrative, constitutional_context):
    """Test L2 prompt generation"""
    question = "Analyze the complexity of this narrative."
    l1_output = "This narrative reflects tensions between sovereignty and international law."
    
    prompt = FRPPromptGenerator.get_l2_prompt(
        sample_narrative,
        question,
        constitutional_context,
        l1_output
    )
    
    # Check key elements
    assert "LEVEL 2: INNER STRUCTURE" in prompt
    assert l1_output in prompt
    assert "Key pillars" in prompt
    assert "Domain-Specific Focus" in prompt
    assert constitutional_context.domain in prompt


def test_prompt_generator_l3(sample_narrative, constitutional_context):
    """Test L3 prompt generation"""
    question = "Analyze the complexity of this narrative."
    l1_output = "Macro view content..."
    l2_output = "Structural analysis content..."
    
    prompt = FRPPromptGenerator.get_l3_prompt(
        sample_narrative,
        question,
        constitutional_context,
        l1_output,
        l2_output
    )
    
    # Check key elements
    assert "LEVEL 3: RELATIONAL DYNAMICS" in prompt
    assert l1_output in prompt
    assert l2_output in prompt
    assert "Synergies" in prompt
    assert "Feedback loops" in prompt


def test_prompt_generator_l4(sample_narrative, constitutional_context):
    """Test L4 prompt generation"""
    question = "Analyze the complexity of this narrative."
    l1_output = "Macro..."
    l2_output = "Structure..."
    l3_output = "Interactions..."
    
    prompt = FRPPromptGenerator.get_l4_prompt(
        sample_narrative,
        question,
        constitutional_context,
        l1_output,
        l2_output,
        l3_output
    )
    
    # Check key elements
    assert "LEVEL 4: FRACTAL PERSPECTIVE" in prompt
    assert "MEANINGFUL ZOOM" in prompt  # Fixed: check uppercase version
    assert "fractal case" in prompt
    assert all(output in prompt for output in [l1_output, l2_output, l3_output])


def test_prompt_generator_l5(sample_narrative, constitutional_context):
    """Test L5 prompt generation"""
    question = "Analyze the complexity of this narrative."
    l1_output = "Macro..."
    l2_output = "Structure..."
    l3_output = "Interactions..."
    l4_output = "Fractal case..."
    
    prompt = FRPPromptGenerator.get_l5_prompt(
        sample_narrative,
        question,
        constitutional_context,
        l1_output,
        l2_output,
        l3_output,
        l4_output
    )
    
    # Check key elements
    assert "LEVEL 5: STRATEGIC RESONANCE" in prompt
    assert "universal pattern" in prompt
    assert "Actionable insight" in prompt
    assert all(output in prompt for output in [l1_output, l2_output, l3_output, l4_output])


def test_domain_specific_guidance_constitutional():
    """Test that constitutional domain gets specific guidance"""
    context = DomainContext(domain='constitutional')
    
    l2_guidance = FRPPromptGenerator._get_domain_l2_guidance('constitutional')
    assert "constitutional principles" in l2_guidance.lower()
    assert "sovereignty" in l2_guidance.lower()
    
    l3_guidance = FRPPromptGenerator._get_domain_l3_guidance('constitutional')
    assert "sovereignty" in l3_guidance.lower() or "international" in l3_guidance.lower()


def test_domain_specific_guidance_political():
    """Test that political domain gets specific guidance"""
    l2_guidance = FRPPromptGenerator._get_domain_l2_guidance('political')
    assert "narrative" in l2_guidance.lower() or "framing" in l2_guidance.lower()
    
    l3_guidance = FRPPromptGenerator._get_domain_l3_guidance('political')
    assert "narrative" in l3_guidance.lower() or "framing" in l3_guidance.lower()


# ============================================================================
# ANALYZER TESTS
# ============================================================================

def test_analyzer_initialization(analyzer, constitutional_context):
    """Test FractalAnalyzer initialization"""
    assert analyzer.domain_context == constitutional_context
    assert analyzer.prompt_generator is not None


def test_analyze_narrative_without_ai(analyzer, sample_narrative):
    """Test analysis without AI callback (prompts only)"""
    question = "Analyze the strategic framing of this narrative."
    
    analysis = analyzer.analyze_narrative(
        sample_narrative,
        question,
        levels=['L1', 'L2'],
        ai_callback=None  # No AI execution
    )
    
    # Check structure
    assert isinstance(analysis, FRPAnalysis)
    assert analysis.input_text == sample_narrative
    assert analysis.question == question
    assert len(analysis.levels) == 2
    assert analysis.levels[0].level == 'L1'
    assert analysis.levels[1].level == 'L2'
    
    # Without AI, should have placeholder responses
    assert "[AI response for" in analysis.levels[0].content


def test_analyze_narrative_with_mock_ai(analyzer, sample_narrative):
    """Test analysis with mock AI callback"""
    def mock_ai(prompt: str) -> str:
        if "LEVEL 1" in prompt:
            return "This narrative exemplifies sovereignty defense rhetoric. Strategic stakes involve..."
        elif "LEVEL 2" in prompt:
            return "The structure relies on three pillars: national authority, democratic legitimacy..."
        else:
            return "Mock response for other levels."
    
    question = "Analyze this narrative."
    
    analysis = analyzer.analyze_narrative(
        sample_narrative,
        question,
        levels=['L1', 'L2'],
        ai_callback=mock_ai
    )
    
    # Check AI responses used
    assert "sovereignty defense rhetoric" in analysis.levels[0].content
    assert "three pillars" in analysis.levels[1].content


def test_analyze_all_five_levels(analyzer, sample_narrative):
    """Test full 5-level analysis"""
    def mock_ai(prompt: str) -> str:
        return f"Mock analysis for this prompt (length: {len(prompt)} chars)"
    
    question = "Conduct full analysis."
    
    analysis = analyzer.analyze_narrative(
        sample_narrative,
        question,
        levels=['L1', 'L2', 'L3', 'L4', 'L5'],
        ai_callback=mock_ai
    )
    
    assert len(analysis.levels) == 5
    assert [level.level for level in analysis.levels] == ['L1', 'L2', 'L3', 'L4', 'L5']
    
    # Each level should have proper title
    expected_titles = [
        'Macro View (Strategic Panorama)',
        'Inner Structure (System Architecture)',
        'Interactions (Relational Dynamics)',
        'Fractal Perspective (Meaningful Zoom)',
        'Strategic Resonance (Transferable Wisdom)'
    ]
    
    actual_titles = [level.title for level in analysis.levels]
    assert actual_titles == expected_titles


# ============================================================================
# EXPORT TESTS
# ============================================================================

def test_analysis_to_dict(analyzer, sample_narrative):
    """Test conversion to dictionary"""
    question = "Test question"
    
    analysis = analyzer.analyze_narrative(
        sample_narrative,
        question,
        levels=['L1'],
        ai_callback=None
    )
    
    result_dict = analysis.to_dict()
    
    assert isinstance(result_dict, dict)
    assert 'input_text' in result_dict
    assert 'question' in result_dict
    assert 'domain_context' in result_dict
    assert 'levels' in result_dict
    assert 'timestamp' in result_dict


def test_analysis_to_json(analyzer, sample_narrative, tmp_path):
    """Test JSON export"""
    question = "Test question"
    
    analysis = analyzer.analyze_narrative(
        sample_narrative,
        question,
        levels=['L1'],
        ai_callback=None
    )
    
    # Save to temp file
    output_file = tmp_path / "test_analysis.json"
    analysis.to_json(str(output_file))
    
    # Verify file exists and is valid JSON
    assert output_file.exists()
    
    with open(output_file, 'r') as f:
        data = json.load(f)
    
    assert data['question'] == question
    assert len(data['levels']) == 1


def test_analysis_to_markdown(analyzer, sample_narrative):
    """Test markdown export"""
    question = "Test question"
    
    def mock_ai(prompt: str) -> str:
        return "Mock analysis content with insights."
    
    analysis = analyzer.analyze_narrative(
        sample_narrative,
        question,
        levels=['L1', 'L2'],
        ai_callback=mock_ai
    )
    
    markdown = analysis.to_markdown()
    
    # Check structure
    assert "# Fractal Reasoning Analysis" in markdown
    assert question in markdown
    assert "## Macro View" in markdown
    assert "## Inner Structure" in markdown
    assert "Mock analysis content" in markdown


# ============================================================================
# BATCH ANALYSIS TESTS
# ============================================================================

def test_batch_analyze_dataset(analyzer, tmp_path):
    """Test batch analysis on small dataset"""
    # Create sample dataset
    df = pd.DataFrame({
        'Case_ID': ['TEST-01', 'TEST-02'],
        'Narrative': [
            'Our sovereignty must be protected from external interference.',
            'International cooperation is essential for global justice.'
        ]
    })
    
    def mock_ai(prompt: str) -> str:
        return "Mock batch analysis response."
    
    output_dir = tmp_path / "frp_batch"
    
    result_df = analyzer.batch_analyze_dataset(
        df,
        text_column='Narrative',
        question_template="Analyze this {domain} narrative.",
        output_dir=str(output_dir),
        ai_callback=mock_ai
    )
    
    # Check outputs
    assert len(result_df) == 2
    assert 'L1_length' in result_df.columns
    assert 'analysis_file' in result_df.columns
    
    # Check files created
    analysis_files = list(output_dir.glob("*.json"))
    assert len(analysis_files) == 2


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_integration_with_complexity_scorer(sample_narrative):
    """Test that FRP can work alongside complexity scoring"""
    from src.analysis.complexity_heuristics import ComplexityScorer
    
    # Score complexity
    scorer = ComplexityScorer(language='es')
    score_result = scorer.score_narrative(sample_narrative)
    c_score = score_result['score']
    
    # Run FRP analysis
    analyzer = create_constitutional_analyzer()
    question = f"Analyze this narrative with complexity score C={c_score:.1f}."
    
    frp_result = analyzer.analyze_narrative(
        sample_narrative,
        question,
        levels=['L1'],
        ai_callback=None
    )
    
    # Check both work together
    assert c_score >= 1.0 and c_score <= 10.0
    assert frp_result.question == question
    assert str(c_score) in frp_result.question


def test_level_metadata_consistency():
    """Test that level definitions are consistent"""
    from src.analysis.frp.fractal_analyzer import FRPPromptGenerator
    
    definitions = FRPPromptGenerator.LEVEL_DEFINITIONS
    
    assert len(definitions) == 5
    assert all(level in definitions for level in ['L1', 'L2', 'L3', 'L4', 'L5'])
    
    for level, metadata in definitions.items():
        assert 'title' in metadata
        assert 'objective' in metadata
        assert 'typical_length' in metadata
        assert len(metadata['title']) > 0
        assert len(metadata['objective']) > 0


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

"""
Example: Using Neural Networks to Predict CLI from Constitutional Text

This script demonstrates how to use the ML-powered CLI predictor to:
1. Auto-score CLI from constitutional text (no manual annotation)
2. Classify individual provisions
3. Detect ultraactivity risk
4. Calculate semantic narrative continuity (CT1)

Requirements:
    pip install requests pandas matplotlib
"""

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List

# API base URL
API_BASE = "http://localhost:8000/api/ml"


def predict_cli_from_text(constitution_text: str, country: str = None) -> Dict:
    """
    Predict CLI score using neural network.
    
    Args:
        constitution_text: Full constitutional text or relevant excerpts
        country: Optional country name for context
    
    Returns:
        Dictionary with CLI, components (CE/UA/JPI), confidence
    """
    url = f"{API_BASE}/predict-cli"
    
    payload = {
        "constitution_text": constitution_text,
        "country": country,
        "max_length": 512
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")


def classify_provision(provision_text: str) -> Dict:
    """
    Classify a constitutional provision.
    
    Args:
        provision_text: Text of provision to classify
    
    Returns:
        Dictionary with provision type and probabilities
    """
    url = f"{API_BASE}/classify-provision"
    
    payload = {
        "provision_text": provision_text
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}")


def detect_ultraactivity(
    provision_text: str, 
    years_active: int, 
    intended_duration: int = None
) -> Dict:
    """
    Predict if provision will persist beyond expiration.
    
    Args:
        provision_text: Text of provision
        years_active: Number of years provision has been active
        intended_duration: Originally intended duration (if transitional)
    
    Returns:
        Dictionary with ultraactivity probability, risk level
    """
    url = f"{API_BASE}/detect-ultraactivity"
    
    payload = {
        "provision_text": provision_text,
        "years_active": years_active,
        "intended_duration": intended_duration
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}")


def calculate_semantic_ct1(text_t1: str, text_t2: str) -> Dict:
    """
    Calculate narrative continuity using semantic embeddings.
    
    Args:
        text_t1: Constitutional text at time 1 (earlier)
        text_t2: Constitutional text at time 2 (later)
    
    Returns:
        Dictionary with CT1 score, semantic similarity, Jaccard similarity
    """
    url = f"{API_BASE}/calculate-ct1"
    
    payload = {
        "constitution_text_t1": text_t1,
        "constitution_text_t2": text_t2
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}")


# ==============================================================================
# EXAMPLE 1: Predict CLI for Somalia Federal (2012 Constitution)
# ==============================================================================

def example_somalia_cli_prediction():
    """
    Example: Predict CLI for Somalia's 2012 Provisional Constitution
    """
    print("=" * 80)
    print("EXAMPLE 1: Somalia Federal CLI Prediction (Neural Network)")
    print("=" * 80)
    
    # Sample text from Somalia's 2012 Provisional Constitution
    somalia_text = """
    PROVISIONAL CONSTITUTION OF THE FEDERAL REPUBLIC OF SOMALIA
    
    Article 1. The Federal Republic of Somalia is a sovereign, independent, 
    and democratic state founded on inclusive representation of the people.
    
    Article 132. Constitutional Amendment - Before the first parliament completes 
    its term, the constitution may be amended by a two-thirds vote of both houses 
    of parliament and approval by two-thirds of state legislatures.
    
    Article 134. The transitional federal government shall operate according to 
    the 4.5 formula for clan representation, allocating seats proportionally 
    to the four major clan families (Hawiye, Darod, Dir, Rahanweyn) plus 
    minorities receiving 0.5 allocation.
    
    Article 115. The Constitutional Court shall have jurisdiction over 
    constitutional matters but has not been established as of 2024.
    """
    
    # Predict CLI
    result = predict_cli_from_text(somalia_text, country="Somalia Federal")
    
    print(f"\n📊 PREDICTION RESULTS:")
    print(f"   Predicted CLI: {result['predicted_CLI']:.2f}")
    print(f"   Components:")
    print(f"      CE (Constitutional Entrenchment): {result['components']['CE']:.2f}")
    print(f"      UA (Ultraactivity): {result['components']['UA']:.2f}")
    print(f"      JPI (Judicial Protection Intensity): {result['components']['JPI']:.2f}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Classification: {result['classification']}")
    print(f"   Inference Time: {result['inference_time_ms']} ms")
    
    # Compare to manual scoring
    print(f"\n🔍 COMPARISON TO MANUAL SCORING:")
    print(f"   Manual CLI (paper): 0.76")
    print(f"   Neural CLI (predicted): {result['predicted_CLI']:.2f}")
    print(f"   Absolute Error: {abs(0.76 - result['predicted_CLI']):.3f}")
    
    if abs(0.76 - result['predicted_CLI']) < 0.05:
        print(f"   ✅ Excellent prediction (error < 0.05)")
    elif abs(0.76 - result['predicted_CLI']) < 0.10:
        print(f"   ✅ Good prediction (error < 0.10)")
    else:
        print(f"   ⚠️ Needs model improvement (error >= 0.10)")


# ==============================================================================
# EXAMPLE 2: Classify Constitutional Provisions
# ==============================================================================

def example_provision_classification():
    """
    Example: Classify different types of constitutional provisions
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Constitutional Provision Classification")
    print("=" * 80)
    
    provisions = [
        {
            "text": "The President may serve a maximum of two consecutive terms of five years each.",
            "expected_type": "executive_constraint"
        },
        {
            "text": "Parliament shall have the power to levy taxes and approve the national budget.",
            "expected_type": "legislative_power"
        },
        {
            "text": "The Supreme Court shall have authority to review the constitutionality of laws.",
            "expected_type": "judicial_authority"
        },
        {
            "text": "All citizens have the right to freedom of expression and assembly.",
            "expected_type": "rights_guarantee"
        }
    ]
    
    results = []
    
    for i, prov in enumerate(provisions, 1):
        print(f"\n📄 PROVISION {i}:")
        print(f"   Text: {prov['text']}")
        
        result = classify_provision(prov['text'])
        
        print(f"   Predicted Type: {result['provision_type']}")
        print(f"   Expected Type: {prov['expected_type']}")
        print(f"   Match: {'✅' if result['provision_type'] == prov['expected_type'] else '❌'}")
        print(f"   Probabilities:")
        for ptype, prob in result['probabilities'].items():
            print(f"      {ptype}: {prob:.2f}")
        print(f"   Contributes to CLI Components:")
        for component, value in result['contributes_to'].items():
            print(f"      {component}: {value:.2f}")
        
        results.append(result)
    
    return results


# ==============================================================================
# EXAMPLE 3: Detect Ultraactivity in Somalia's 4.5 Formula
# ==============================================================================

def example_ultraactivity_detection():
    """
    Example: Predict ultraactivity for Somalia's 4.5 clan formula
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Ultraactivity Detection - Somalia 4.5 Formula")
    print("=" * 80)
    
    # Somalia's 4.5 formula
    formula_text = """
    The 4.5 clan formula allocates parliamentary seats as follows:
    Hawiye: 61 seats, Darod: 61 seats, Dir: 61 seats, Rahanweyn: 61 seats,
    Minorities (combined): 24 seats. This arrangement was designated as 
    'transitional' at the 2000 Arta Conference but has persisted unchanged 
    for 25 years (2000-2025).
    """
    
    result = detect_ultraactivity(
        provision_text=formula_text,
        years_active=25,
        intended_duration=4  # Originally "transitional" for TNG 2000-2004
    )
    
    print(f"\n⚠️ ULTRAACTIVITY ANALYSIS:")
    print(f"   Provision: 4.5 Clan Formula")
    print(f"   Years Active: 25 years (2000-2025)")
    print(f"   Intended Duration: 4 years (transitional)")
    print(f"   Years Overdue: {25 - 4} years")
    print(f"\n📊 PREDICTIONS:")
    print(f"   Ultraactivity Probability: {result['ultraactivity_probability']:.2%}")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Estimated Additional Persistence: {result['estimated_persistence_years']} years")
    print(f"   Contributing Factors:")
    for factor in result['contributing_factors']:
        print(f"      • {factor}")
    
    # Interpretation
    if result['ultraactivity_probability'] > 0.85:
        print(f"\n💡 INTERPRETATION:")
        print(f"   EXTREME ultraactivity risk. Provision has exceeded intended ")
        print(f"   duration by {25 - 4}x and shows no signs of expiration.")
        print(f"   Extended phenotype mechanism: Elite entrenchment + distributed")
        print(f"   reproduction through parliamentary allocation machinery.")


# ==============================================================================
# EXAMPLE 4: Calculate Semantic CT1 (Narrative Continuity)
# ==============================================================================

def example_semantic_ct1():
    """
    Example: Calculate CT1 using semantic embeddings vs Jaccard similarity
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Semantic CT1 Calculation (Neural Embeddings)")
    print("=" * 80)
    
    # Somalia: 2000 vs 2012 constitutions (low continuity)
    somalia_2000 = """
    Transitional National Charter (2000):
    Establish transitional government through Arta Conference.
    Implement 4.5 clan formula for representation.
    Operate under Islamic principles.
    Rebuild state institutions after civil war.
    """
    
    somalia_2012 = """
    Provisional Federal Constitution (2012):
    Federal Republic with five member states.
    Parliament elected via 4.5 clan formula.
    Islamic law as source of legislation.
    Constitutional Court (not yet established).
    """
    
    # Somaliland: 1991 vs 2001 constitutions (high continuity)
    somaliland_1991 = """
    Independence Declaration (1991):
    Restore sovereignty of former British Somaliland.
    Integrate Guurti (clan elders) into governance.
    Islamic identity and democratic principles.
    Build bottom-up institutions through clan conferences.
    """
    
    somaliland_2001 = """
    Constitution of Republic of Somaliland (2001):
    Sovereign state based on clan confederation.
    Bicameral parliament with Guurti (House of Elders).
    Islamic law and democratic multi-party system.
    Institutions evolved through Borama, Hargeisa conferences.
    """
    
    print("\n📊 SOMALIA FEDERAL (2000 vs 2012):")
    result_somalia = calculate_semantic_ct1(somalia_2000, somalia_2012)
    print(f"   CT1 Score (Neural): {result_somalia['ct1_score']:.2f}")
    print(f"   Semantic Similarity (Cosine): {result_somalia['semantic_similarity']:.2f}")
    print(f"   Jaccard Similarity (Word Overlap): {result_somalia['jaccard_similarity']:.2f}")
    print(f"   Interpretation: {result_somalia['interpretation']}")
    
    print("\n📊 SOMALILAND (1991 vs 2001):")
    result_somaliland = calculate_semantic_ct1(somaliland_1991, somaliland_2001)
    print(f"   CT1 Score (Neural): {result_somaliland['ct1_score']:.2f}")
    print(f"   Semantic Similarity (Cosine): {result_somaliland['semantic_similarity']:.2f}")
    print(f"   Jaccard Similarity (Word Overlap): {result_somaliland['jaccard_similarity']:.2f}")
    print(f"   Interpretation: {result_somaliland['interpretation']}")
    
    print("\n🔍 COMPARISON:")
    print(f"   Somalia CT1: {result_somalia['ct1_score']:.2f} (discontinuity)")
    print(f"   Somaliland CT1: {result_somaliland['ct1_score']:.2f} (continuity)")
    print(f"   Gap: {result_somaliland['ct1_score'] - result_somalia['ct1_score']:.2f}")
    
    print("\n💡 ADVANTAGE OF NEURAL CT1:")
    print(f"   Traditional Jaccard: Somalia {result_somalia['jaccard_similarity']:.2f}, Somaliland {result_somaliland['jaccard_similarity']:.2f}")
    print(f"   Neural Semantic: Somalia {result_somalia['ct1_score']:.2f}, Somaliland {result_somaliland['ct1_score']:.2f}")
    print(f"   Neural embeddings capture semantic meaning (not just word overlap),")
    print(f"   detecting that Somaliland maintained core narrative despite textual changes.")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     NEURAL NETWORK-POWERED CONSTITUTIONAL ANALYSIS                       ║
    ║     Legal Evolution Analysis Platform v2.0                               ║
    ║                                                                          ║
    ║     Using: LegalBERT + ReLU/Sigmoid Activation Functions                ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Run all examples
        example_somalia_cli_prediction()
        example_provision_classification()
        example_ultraactivity_detection()
        example_semantic_ct1()
        
        print("\n" + "=" * 80)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\n📚 Key Takeaways:")
        print("   1. Neural networks reduce CLI scoring from 2-3 hours to seconds")
        print("   2. Provision classification enables automated constitutional annotation")
        print("   3. Ultraactivity detection predicts institutional persistence patterns")
        print("   4. Semantic CT1 captures narrative meaning (not just word overlap)")
        print("\n🚀 Next Steps:")
        print("   • Train model on 100+ constitutions for production use")
        print("   • Fine-tune LegalBERT on Horn of Africa legal corpus")
        print("   • Deploy model with GPU for faster inference")
        print("   • Integrate with existing CLI calculator for validation")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("   Make sure the backend is running:")
        print("   cd backend && uvicorn app:app --reload --port 8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

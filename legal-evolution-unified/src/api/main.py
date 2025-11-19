"""
Legal Evolution Unified REST API

FastAPI application providing endpoints for:
- Legal fitness calculation
- Genealogy analysis
- Transplant prediction
- Network analysis
- Bootstrap validation

Integrates all platform tools via unified pipeline.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import logging

from src.integration.unified_pipeline import LegalEvolutionPipeline
from code.bootstrap import BootstrapValidator
from code.analysis import LegalConceptAnalysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Evolution Unified API",
    description="Integrated platform for legal concept analysis combining JurisRank, RootFinder, Iusmorfos, and Peralta methodologies",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline (singleton)
pipeline = None


def get_pipeline() -> LegalEvolutionPipeline:
    """Get or create pipeline instance."""
    global pipeline
    if pipeline is None:
        pipeline = LegalEvolutionPipeline(db=None, n_bootstrap=1000)
        logger.info("Pipeline initialized")
    return pipeline


# ============================================================================
# Request/Response Models
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request model for concept analysis."""
    concept_name: str = Field(..., description="Legal concept to analyze")
    jurisdiction: str = Field(..., description="Jurisdiction context")
    include_genealogy: bool = Field(True, description="Include genealogical analysis")
    include_network: bool = Field(False, description="Include network analysis")


class TransplantRequest(BaseModel):
    """Request model for transplant prediction."""
    concept_name: str = Field(..., description="Legal concept to transplant")
    source_jurisdiction: str = Field(..., description="Source jurisdiction")
    target_jurisdictions: List[str] = Field(..., description="Target jurisdictions to compare")


class GenealogicalHypothesis(BaseModel):
    """Request model for genealogical hypothesis testing."""
    source_concept: str = Field(..., description="Source concept name")
    source_jurisdiction: str = Field(..., description="Source jurisdiction")
    target_concept: str = Field(..., description="Target concept name")
    target_jurisdiction: str = Field(..., description="Target jurisdiction")


class BootstrapRequest(BaseModel):
    """Request model for bootstrap validation."""
    group1: List[float] = Field(..., description="First data group")
    group2: List[float] = Field(..., description="Second data group")
    n_iterations: int = Field(1000, description="Bootstrap iterations")


# ============================================================================
# Health & Info Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Legal Evolution Unified API",
        "version": "1.0.0",
        "description": "Integrated legal concept analysis platform",
        "documentation": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "pipeline_initialized": pipeline is not None
    }


# ============================================================================
# Legal Fitness Endpoints (JurisRank)
# ============================================================================

@app.post("/api/v1/fitness")
async def calculate_fitness(request: AnalysisRequest):
    """
    Calculate legal fitness with bootstrap validation.
    
    Uses JurisRank methodology enhanced with Peralta's bootstrap validation.
    """
    try:
        pipe = get_pipeline()
        
        result = pipe.jurisrank.calculate_fitness_with_validation(
            request.concept_name,
            request.jurisdiction
        )
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error calculating fitness: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/fitness/{concept}/{jurisdiction}")
async def get_fitness(
    concept: str,
    jurisdiction: str,
    baseline: float = Query(0.5, description="Comparison baseline")
):
    """
    Get legal fitness for a specific concept-jurisdiction pair.
    """
    try:
        pipe = get_pipeline()
        
        result = pipe.jurisrank.calculate_fitness_with_validation(
            concept,
            jurisdiction,
            comparison_baseline=baseline
        )
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error getting fitness: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Comprehensive Analysis Endpoint
# ============================================================================

@app.post("/api/v1/analyze")
async def analyze_concept(request: AnalysisRequest):
    """
    Comprehensive legal concept analysis.
    
    Integrates:
    - Legal fitness (JurisRank + Bootstrap)
    - Genealogy (RootFinder)
    - Network position (Peralta)
    """
    try:
        pipe = get_pipeline()
        
        result = pipe.comprehensive_analysis(
            request.concept_name,
            request.jurisdiction,
            include_genealogy=request.include_genealogy,
            include_network=request.include_network
        )
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyze/report")
async def generate_analysis_report(request: AnalysisRequest):
    """
    Generate comprehensive analysis report in text format.
    """
    try:
        pipe = get_pipeline()
        
        report = pipe.generate_integrated_report(
            request.concept_name,
            request.jurisdiction,
            include_genealogy=request.include_genealogy,
            include_network=request.include_network
        )
        
        return {
            "success": True,
            "report": report
        }
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Transplant Prediction Endpoints (Iusmorfos)
# ============================================================================

@app.post("/api/v1/transplant/predict")
async def predict_transplant(request: TransplantRequest):
    """
    Predict transplant success for multiple target jurisdictions.
    
    Uses Iusmorfos methodology with WEIRD/No-WEIRD classification.
    """
    try:
        pipe = get_pipeline()
        
        # Compare all targets
        comparison = pipe.compare_transplant_targets(
            request.concept_name,
            request.source_jurisdiction,
            request.target_jurisdictions
        )
        
        return {
            "success": True,
            "data": comparison.to_dict(orient='records')
        }
        
    except Exception as e:
        logger.error(f"Error predicting transplant: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/transplant/predict/{concept}/{source}/{target}")
async def predict_single_transplant(concept: str, source: str, target: str):
    """
    Predict transplant success for a single source-target pair.
    """
    try:
        pipe = get_pipeline()
        
        prediction = pipe.predict_transplant(
            concept,
            source,
            target
        )
        
        return {
            "success": True,
            "data": prediction
        }
        
    except Exception as e:
        logger.error(f"Error predicting transplant: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Genealogy Endpoints (RootFinder)
# ============================================================================

@app.get("/api/v1/genealogy/ancestors/{concept}/{jurisdiction}")
async def get_ancestors(
    concept: str,
    jurisdiction: str,
    max_depth: int = Query(5, description="Maximum genealogical depth")
):
    """
    Find conceptual ancestors of a legal concept.
    """
    try:
        pipe = get_pipeline()
        
        ancestors = pipe.rootfinder.find_conceptual_ancestors(
            concept,
            jurisdiction,
            max_depth=max_depth
        )
        
        return {
            "success": True,
            "data": ancestors
        }
        
    except Exception as e:
        logger.error(f"Error finding ancestors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/genealogy/descendants/{concept}/{jurisdiction}")
async def get_descendants(
    concept: str,
    jurisdiction: str,
    max_depth: int = Query(5, description="Maximum genealogical depth")
):
    """
    Find conceptual descendants of a legal concept.
    """
    try:
        pipe = get_pipeline()
        
        descendants = pipe.rootfinder.find_conceptual_descendants(
            concept,
            jurisdiction,
            max_depth=max_depth
        )
        
        return {
            "success": True,
            "data": descendants
        }
        
    except Exception as e:
        logger.error(f"Error finding descendants: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/genealogy/validate")
async def validate_genealogy(request: GenealogicalHypothesis):
    """
    Validate genealogical hypothesis between two concepts.
    
    Uses RootFinder + Peralta bootstrap validation.
    """
    try:
        pipe = get_pipeline()
        
        validation = pipe.validate_genealogical_hypothesis(
            (request.source_concept, request.source_jurisdiction),
            (request.target_concept, request.target_jurisdiction)
        )
        
        return {
            "success": True,
            "data": validation
        }
        
    except Exception as e:
        logger.error(f"Error validating genealogy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Bootstrap Validation Endpoints (Peralta)
# ============================================================================

@app.post("/api/v1/bootstrap/validate")
async def bootstrap_validate(request: BootstrapRequest):
    """
    Perform bootstrap comparison between two groups.
    
    Uses Peralta's bootstrap validation methodology.
    """
    try:
        validator = BootstrapValidator(n_iterations=request.n_iterations)
        
        # Define comparison function
        def compare_groups(data_df):
            n = len(data_df) // 2
            return abs(data_df.iloc[:n].mean() - data_df.iloc[n:].mean())
        
        # Create combined dataset
        import pandas as pd
        combined = pd.Series(request.group1 + request.group2)
        
        # Bootstrap
        import numpy as np
        bootstrap_stats = []
        for i in range(request.n_iterations):
            sample = combined.sample(n=len(combined), replace=True)
            stat = compare_groups(sample)
            bootstrap_stats.append(stat)
        
        bootstrap_array = np.array(bootstrap_stats)
        
        # Calculate confidence interval
        ci_lower, ci_upper = validator.calculate_bootstrap_ci(bootstrap_array, 0.95)
        
        # Hypothesis test
        from code.bootstrap import bootstrap_hypothesis_test
        observed_diff = abs(np.mean(request.group1) - np.mean(request.group2))
        p_value = bootstrap_hypothesis_test(observed_diff, bootstrap_array, 'two-sided')
        
        return {
            "success": True,
            "data": {
                "observed_difference": float(observed_diff),
                "mean_bootstrap": float(np.mean(bootstrap_array)),
                "std_bootstrap": float(np.std(bootstrap_array)),
                "ci_95": [float(ci_lower), float(ci_upper)],
                "p_value": float(p_value),
                "significant": p_value < 0.05,
                "n_iterations": request.n_iterations
            }
        }
        
    except Exception as e:
        logger.error(f"Error in bootstrap validation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Network Analysis Endpoints (Peralta)
# ============================================================================

@app.get("/api/v1/network/status")
async def network_status():
    """
    Check if network analysis is available.
    """
    pipe = get_pipeline()
    
    return {
        "success": True,
        "data": {
            "data_loaded": pipe.analyzer.data is not None,
            "similarity_calculated": pipe.analyzer.similarity_matrix is not None,
            "network_built": pipe.analyzer.network is not None,
            "num_concepts": len(pipe.analyzer.concept_names) if pipe.analyzer.data is not None else 0
        }
    }


@app.get("/api/v1/network/metrics/{concept}")
async def get_network_metrics(concept: str):
    """
    Get network metrics for a specific concept.
    """
    try:
        pipe = get_pipeline()
        
        if pipe.analyzer.network is None:
            raise HTTPException(
                status_code=400,
                detail="Network not built. Load data first."
            )
        
        metrics = pipe.analyzer.calculate_network_metrics()
        
        concept_metrics = {
            metric_name: metric_values.get(concept, 0.0)
            for metric_name, metric_values in metrics.items()
        }
        
        return {
            "success": True,
            "data": {
                "concept": concept,
                "metrics": concept_metrics
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting network metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Run API
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

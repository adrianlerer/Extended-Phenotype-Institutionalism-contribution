"""
Figure Generator Routes
Generate publication-quality visualizations (CLI matrices, timelines, correlations)
"""

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import numpy as np
from matplotlib.patches import Rectangle
import io
import base64
from datetime import datetime
import sys
from pathlib import Path

# Add backend services to path
sys.path.append(str(Path(__file__).parent.parent))
from services.feature_registry import registry

router = APIRouter()


class CountryData(BaseModel):
    """Country data for CLI matrix"""
    name: str
    CLI: float = Field(..., ge=0.0, le=1.0)
    CLI_cultural: float = Field(..., ge=0.0, le=1.0)
    color: Optional[str] = None


class CLIMatrixInput(BaseModel):
    """Input for CLI matrix visualization"""
    countries: List[CountryData]
    title: Optional[str] = "CLI × CLI_cultural Interaction Matrix"
    show_threshold: bool = True
    threshold_value: float = 0.30
    dpi: int = 300


class TimelineEvent(BaseModel):
    """Timeline event"""
    year: int
    event: str
    marker_color: Optional[str] = "blue"


class TimelineInput(BaseModel):
    """Input for timeline visualization"""
    country: str
    events: List[TimelineEvent]
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    title: Optional[str] = None


class CorrelationInput(BaseModel):
    """Input for correlation plot"""
    x_values: List[float]
    y_values: List[float]
    x_label: str
    y_label: str
    title: Optional[str] = None
    show_trendline: bool = True


@router.post("/cli-matrix")
async def generate_cli_matrix(data: CLIMatrixInput):
    """
    Generate CLI × CLI_cultural interaction matrix
    
    Returns base64-encoded PNG image
    """
    # Check if feature is enabled
    feature = registry.get_feature("cli_matrix_visualizer")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="CLI Matrix Visualizer feature is disabled")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Quadrant shading
    ax.add_patch(Rectangle((0.60, 0.60), 0.40, 0.40, alpha=0.15, color='lightgreen', label='Stable Rigidity'))
    ax.add_patch(Rectangle((0.60, 0.00), 0.40, 0.60, alpha=0.25, color='red', label='Brittle Rigidity'))
    ax.add_patch(Rectangle((0.00, 0.60), 0.60, 0.40, alpha=0.15, color='lightblue', label='Adaptive Stability'))
    ax.add_patch(Rectangle((0.00, 0.00), 0.60, 0.60, alpha=0.10, color='gray', label='Chaotic Fragility'))
    
    # Collapse risk threshold curve (hyperbola: CLI × CLI_cultural = threshold)
    if data.show_threshold:
        x_threshold = np.linspace(data.threshold_value, 1.0, 1000)
        y_threshold = data.threshold_value / x_threshold
        ax.plot(x_threshold, y_threshold, 'k--', linewidth=3, 
                label=f'Collapse Risk Threshold ({data.threshold_value})', zorder=2)
    
    # Plot country data points
    default_colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    for idx, country in enumerate(data.countries):
        color = country.color or default_colors[idx % len(default_colors)]
        
        # Calculate interaction
        interaction = country.CLI * country.CLI_cultural
        below_threshold = interaction < data.threshold_value
        
        # Marker size based on risk
        marker_size = 300 if below_threshold else 200
        
        ax.scatter(country.CLI, country.CLI_cultural, s=marker_size, c=color,
                  alpha=0.7, edgecolors='black', linewidths=2, zorder=3)
        
        # Label with name
        ax.annotate(country.name, (country.CLI, country.CLI_cultural),
                   fontsize=12, fontweight='bold', ha='center', va='bottom',
                   xytext=(0, 10), textcoords='offset points')
    
    # Quadrant labels
    ax.text(0.80, 0.80, 'STABLE\nRIGIDITY', fontsize=14, fontweight='bold',
           ha='center', va='center', color='darkgreen', alpha=0.7)
    ax.text(0.80, 0.30, 'BRITTLE\nRIGIDITY', fontsize=16, fontweight='bold',
           ha='center', va='center', color='darkred', alpha=0.9)
    ax.text(0.30, 0.80, 'ADAPTIVE\nSTABILITY', fontsize=14, fontweight='bold',
           ha='center', va='center', color='darkblue', alpha=0.7)
    ax.text(0.30, 0.30, 'CHAOTIC\nFRAGILITY', fontsize=12, fontweight='bold',
           ha='center', va='center', color='gray', alpha=0.7)
    
    # Axis configuration
    ax.set_xlabel('Constitutional Lock-In Index (CLI)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Cultural Lock-In Index (CLI_cultural)', fontsize=14, fontweight='bold')
    ax.set_title(data.title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=10, loc='upper left')
    
    plt.tight_layout()
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=data.dpi, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    # Encode to base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    # Track usage
    registry.track_usage("cli_matrix_visualizer")
    
    return {
        "image_base64": img_base64,
        "format": "PNG",
        "dpi": data.dpi,
        "countries_count": len(data.countries),
        "generated_at": datetime.now().isoformat()
    }


@router.post("/timeline")
async def generate_timeline(data: TimelineInput):
    """
    Generate constitutional timeline visualization
    
    Returns base64-encoded PNG image
    """
    # Check if feature is enabled
    feature = registry.get_feature("timeline_generator")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="Timeline Generator feature is disabled")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Extract years and events
    years = [event.year for event in data.events]
    events = [event.event for event in data.events]
    colors = [event.marker_color or 'blue' for event in data.events]
    
    # Determine y-positions (alternate high/low for readability)
    y_positions = [1 if i % 2 == 0 else 0.5 for i in range(len(years))]
    
    # Plot timeline
    ax.plot(years, [0.75] * len(years), 'k-', linewidth=2, zorder=1)
    
    # Plot events
    for year, y_pos, color, event_text in zip(years, y_positions, colors, events):
        # Marker
        ax.scatter(year, 0.75, s=200, c=color, edgecolors='black', linewidths=2, zorder=3)
        
        # Vertical line to text
        ax.plot([year, year], [0.75, y_pos], 'k--', linewidth=1, alpha=0.5)
        
        # Event text
        ax.text(year, y_pos, event_text, fontsize=10, ha='center', va='bottom' if y_pos > 0.75 else 'top',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', alpha=0.8))
    
    # Axis configuration
    start_year = data.start_year or min(years) - 5
    end_year = data.end_year or max(years) + 5
    
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0, 1.5)
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_title(data.title or f'Constitutional Timeline: {data.country}', fontsize=16, fontweight='bold', pad=20)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    # Encode to base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    # Track usage
    registry.track_usage("timeline_generator")
    
    return {
        "image_base64": img_base64,
        "format": "PNG",
        "dpi": 300,
        "events_count": len(data.events),
        "generated_at": datetime.now().isoformat()
    }


@router.post("/correlation")
async def generate_correlation_plot(data: CorrelationInput):
    """
    Generate correlation scatterplot with optional trendline
    
    Returns base64-encoded PNG image
    """
    # Check if feature is enabled
    feature = registry.get_feature("correlation_plotter")
    if not feature or not feature.enabled:
        raise HTTPException(status_code=403, detail="Correlation Plotter feature is disabled")
    
    if len(data.x_values) != len(data.y_values):
        raise HTTPException(status_code=400, detail="x_values and y_values must have same length")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Convert to numpy arrays
    x = np.array(data.x_values)
    y = np.array(data.y_values)
    
    # Scatterplot
    ax.scatter(x, y, s=100, alpha=0.6, edgecolors='black', linewidths=1.5)
    
    # Trendline
    if data.show_trendline:
        # Calculate linear regression
        coeffs = np.polyfit(x, y, 1)
        poly = np.poly1d(coeffs)
        x_trend = np.linspace(x.min(), x.max(), 100)
        y_trend = poly(x_trend)
        
        ax.plot(x_trend, y_trend, 'r--', linewidth=2, label=f'Trendline: y = {coeffs[0]:.3f}x + {coeffs[1]:.3f}')
        
        # Calculate R²
        y_pred = poly(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Correlation coefficient
        correlation = np.corrcoef(x, y)[0, 1]
        
        # Add statistics to plot
        textstr = f'Correlation: r = {correlation:.3f}\nR² = {r_squared:.3f}'
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Axis configuration
    ax.set_xlabel(data.x_label, fontsize=14, fontweight='bold')
    ax.set_ylabel(data.y_label, fontsize=14, fontweight='bold')
    ax.set_title(data.title or f'{data.y_label} vs {data.x_label}', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    if data.show_trendline:
        ax.legend(fontsize=12)
    
    plt.tight_layout()
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    # Encode to base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    # Track usage
    registry.track_usage("correlation_plotter")
    
    return {
        "image_base64": img_base64,
        "format": "PNG",
        "dpi": 300,
        "data_points": len(data.x_values),
        "correlation": float(correlation) if data.show_trendline else None,
        "r_squared": float(r_squared) if data.show_trendline else None,
        "generated_at": datetime.now().isoformat()
    }


@router.get("/examples")
async def get_figure_examples():
    """Get example figure generation requests"""
    return {
        "cli_matrix_example": {
            "countries": [
                {"name": "Somalia Federal", "CLI": 0.76, "CLI_cultural": 0.34, "color": "red"},
                {"name": "Somalilandia", "CLI": 0.54, "CLI_cultural": 0.70, "color": "green"},
                {"name": "Uruguay", "CLI": 0.75, "CLI_cultural": 0.77, "color": "blue"}
            ],
            "title": "Dual-Index Framework: Horn of Africa",
            "show_threshold": True,
            "threshold_value": 0.30,
            "dpi": 300
        },
        "timeline_example": {
            "country": "Somalia",
            "events": [
                {"year": 1960, "event": "Independence", "marker_color": "green"},
                {"year": 1991, "event": "State Collapse", "marker_color": "red"},
                {"year": 2012, "event": "Federal Constitution", "marker_color": "blue"},
                {"year": 2025, "event": "Present Day", "marker_color": "orange"}
            ],
            "title": "Somalia Constitutional Timeline (1960-2025)"
        },
        "correlation_example": {
            "x_values": [0.76, 0.54, 0.75, 0.68, 0.55],
            "y_values": [2.5, 6.8, 7.2, 6.5, 5.8],
            "x_label": "CLI (Constitutional Lock-In Index)",
            "y_label": "Freedom House Political Rights Score",
            "title": "CLI vs Political Rights",
            "show_trendline": True
        }
    }

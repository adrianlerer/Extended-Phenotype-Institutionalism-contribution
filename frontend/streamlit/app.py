"""
Legal Evolution Analysis Platform - Streamlit UI
AI-Powered Constitutional Analysis & Policy Intelligence
For researchers, consultants, legal professionals, analysts, and policy makers
"""

import streamlit as st
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent / "backend"))

from services.feature_registry import registry, FeatureCategory
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Legal Evolution Analysis Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.legal-evolution.ai',
        'Report a bug': 'https://github.com/your-org/legal-evolution-unified/issues',
        'About': '''
        # Legal Evolution Analysis Platform
        
        **AI-Powered Constitutional & Policy Intelligence**
        
        For researchers, policy consultants, legal professionals, 
        political analysts, journalists, and government agencies.
        
        Version 1.0.0 | 2025
        '''
    }
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .feature-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #E5E7EB;
        margin-bottom: 1rem;
        background-color: #F9FAFB;
    }
    .feature-enabled {
        border-color: #10B981;
        background-color: #ECFDF5;
    }
    .feature-disabled {
        border-color: #EF4444;
        background-color: #FEF2F2;
        opacity: 0.6;
    }
    .tier-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .tier-free { background-color: #DBEAFE; color: #1E40AF; }
    .tier-basic { background-color: #FEF3C7; color: #92400E; }
    .tier-pro { background-color: #E0E7FF; color: #3730A3; }
    .tier-enterprise { background-color: #FCE7F3; color: #831843; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'backend_url' not in st.session_state:
    st.session_state.backend_url = "http://localhost:8000"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_features' not in st.session_state:
    st.session_state.selected_features = set(f.id for f in registry.get_enabled_features())


def render_sidebar():
    """Render sidebar with feature selection"""
    with st.sidebar:
        st.markdown("# ⚖️ Analysis Platform")
        st.caption("Constitutional & Policy Intelligence")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "📊 CLI Calculator", "🎯 Dual-Index Analyzer", 
             "🌳 Rootfinder", "📄 Paper Builder", "📈 Visualizations", 
             "🤖 AI Assistant", "🎛️ Feature Manager", "📚 Documentation"],
            key="navigation"
        )
        
        st.markdown("---")
        
        # Quick feature toggles
        st.markdown("### ⚡ Quick Toggle")
        
        # Get top 5 most used features
        top_features = sorted(
            registry.features.values(),
            key=lambda f: f.usage_count,
            reverse=True
        )[:5]
        
        for feature in top_features:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"{feature.icon} **{feature.name}**")
            with col2:
                enabled = st.checkbox(
                    "",
                    value=feature.enabled,
                    key=f"toggle_{feature.id}",
                    label_visibility="collapsed"
                )
                if enabled != feature.enabled:
                    if enabled:
                        registry.enable_feature(feature.id)
                    else:
                        registry.disable_feature(feature.id)
        
        st.markdown("---")
        st.markdown(f"**Enabled**: {len(registry.get_enabled_features())}/{len(registry.features)}")
        
        return page


def render_dashboard():
    """Render main dashboard"""
    st.markdown('<p class="main-header">📊 Legal Evolution Analysis Platform</p>', unsafe_allow_html=True)
    st.markdown("**AI-Powered Constitutional Analysis & Policy Intelligence**")
    
    # User type selector
    st.markdown("### 👤 I am a...")
    user_type = st.selectbox(
        "Select your role",
        [
            "Academic Researcher",
            "Policy Consultant / Think Tank",
            "Legal Practitioner",
            "Political Analyst / Journalist",
            "Government / International Organization",
            "Investment Analyst / Risk Assessment",
            "Student / Learning",
            "Other"
        ],
        label_visibility="collapsed"
    )
    
    # Show relevant use cases based on user type
    if user_type == "Academic Researcher":
        st.info("📚 **For Researchers**: Generate SSRN papers, validate statistical models, compare constitutional frameworks")
    elif user_type == "Policy Consultant / Think Tank":
        st.info("🏛️ **For Consultants**: Assess reform proposals, predict stability risks, generate policy briefs")
    elif user_type == "Legal Practitioner":
        st.info("⚖️ **For Legal Professionals**: Trace provision genealogy, analyze litigation strategy, constitutional impact assessments")
    elif user_type == "Political Analyst / Journalist":
        st.info("📊 **For Analysts**: Generate visualizations, analyze regime stability, predict political outcomes")
    elif user_type == "Government / International Organization":
        st.info("🏢 **For Government/UN/World Bank**: Constitutional design consulting, post-conflict evaluation, stability forecasting")
    elif user_type == "Investment Analyst / Risk Assessment":
        st.info("💼 **For Investors**: Political risk scoring, country stability metrics, constitutional crisis prediction")
    
    st.markdown("---")
    
    # Feature statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Features",
            len(registry.features),
            delta=None
        )
    
    with col2:
        enabled = len(registry.get_enabled_features())
        st.metric(
            "Enabled Features",
            enabled,
            delta=f"{enabled}/{len(registry.features)}"
        )
    
    with col3:
        total_usage = sum(f.usage_count for f in registry.features.values())
        st.metric(
            "Total Usage",
            total_usage,
            delta="All time"
        )
    
    with col4:
        free_features = len(registry.get_features_by_tier("free"))
        st.metric(
            "Free Features",
            free_features,
            delta=f"{free_features}/{len(registry.features)}"
        )
    
    st.markdown("---")
    
    # Feature categories overview
    st.markdown("### 🗂️ Feature Categories")
    
    for category in FeatureCategory:
        features = registry.get_features_by_category(category)
        if not features:
            continue
        
        with st.expander(f"{features[0].icon if features else '🔧'} {category.value.upper()} ({len(features)} tools)", expanded=False):
            for feature in features:
                render_feature_card(feature, compact=True)
    
    st.markdown("---")
    
    # Usage analytics
    st.markdown("### 📊 Usage Analytics")
    
    usage_data = pd.DataFrame([
        {
            "Feature": f.name,
            "Category": f.category.value,
            "Usage Count": f.usage_count,
            "Tier": f.saas_tier,
            "Enabled": "✅" if f.enabled else "❌"
        }
        for f in sorted(registry.features.values(), key=lambda x: x.usage_count, reverse=True)[:10]
    ])
    
    if not usage_data.empty:
        fig = px.bar(
            usage_data,
            x="Feature",
            y="Usage Count",
            color="Category",
            title="Top 10 Most Used Features",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(usage_data, use_container_width=True, hide_index=True)


def render_feature_card(feature, compact=False):
    """Render a feature card"""
    card_class = "feature-enabled" if feature.enabled else "feature-disabled"
    
    if compact:
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            st.markdown(f"## {feature.icon}")
        
        with col2:
            st.markdown(f"**{feature.name}**")
            st.caption(feature.description[:100] + "..." if len(feature.description) > 100 else feature.description)
        
        with col3:
            tier_class = f"tier-{feature.saas_tier}"
            st.markdown(f'<span class="tier-badge {tier_class}">{feature.saas_tier.upper()}</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="feature-card {card_class}">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 10])
        
        with col1:
            st.markdown(f"## {feature.icon}")
        
        with col2:
            st.markdown(f"### {feature.name}")
            tier_class = f"tier-{feature.saas_tier}"
            st.markdown(f'<span class="tier-badge {tier_class}">{feature.saas_tier.upper()}</span>', unsafe_allow_html=True)
            st.markdown(feature.description)
            
            if feature.dependencies:
                st.markdown(f"**Dependencies**: {', '.join(feature.dependencies)}")
            
            if feature.examples:
                with st.expander("📖 Examples"):
                    for example in feature.examples:
                        st.markdown(f"**Input**: `{example.get('input', 'N/A')}`")
                        st.markdown(f"**Output**: `{example.get('output', 'N/A')}`")
                        st.markdown("---")
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if feature.enabled:
                    if st.button(f"❌ Disable", key=f"disable_{feature.id}"):
                        registry.disable_feature(feature.id)
                        st.rerun()
                else:
                    if st.button(f"✅ Enable", key=f"enable_{feature.id}"):
                        registry.enable_feature(feature.id)
                        st.rerun()
            
            with col_btn2:
                if feature.endpoint:
                    if st.button(f"🚀 Use", key=f"use_{feature.id}"):
                        st.session_state.navigation = feature.name
            
            with col_btn3:
                if feature.documentation_url:
                    st.markdown(f"[📖 Docs]({feature.documentation_url})")
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_cli_calculator():
    """Render CLI Calculator tool"""
    feature = registry.get_feature("cli_calculator")
    
    if not feature or not feature.enabled:
        st.error("❌ CLI Calculator is disabled. Enable it in Feature Manager.")
        return
    
    st.markdown(f"# {feature.icon} {feature.name}")
    st.markdown(feature.description)
    
    st.markdown("---")
    
    # Input form
    st.markdown("### 📝 Input Values")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entity = st.text_input("Entity Name", value="Example Country", help="Name of the country/jurisdiction")
        ce = st.slider("CE - Constitutional Entrenchment", 0.0, 1.0, 0.70, 0.01, help="How difficult to amend constitution (0=easy, 1=very difficult)")
        ua = st.slider("UA - Unilateral Amendment", 0.0, 1.0, 0.60, 0.01, help="Ability to amend without broad consensus (0=many actors needed, 1=one actor can amend)")
        jpi = st.slider("JPI - Judicial Power Index", 0.0, 1.0, 0.65, 0.01, help="Strength of judicial review (0=weak, 1=strong)")
    
    with col2:
        st.markdown("### 📊 Formula")
        st.latex(r"CLI = 0.35 \times CE + 0.40 \times UA + 0.25 \times JPI")
        
        # Calculate CLI
        cli = 0.35 * ce + 0.40 * ua + 0.25 * jpi
        
        st.markdown("### 🎯 Result")
        st.metric("Constitutional Lock-In Index (CLI)", f"{cli:.3f}")
        
        # Classification
        if cli >= 0.70:
            st.success("✅ **HIGH Lock-In**: Very rigid constitutional system")
        elif cli >= 0.50:
            st.warning("⚠️ **MEDIUM Lock-In**: Moderately rigid system")
        else:
            st.info("ℹ️ **LOW Lock-In**: Flexible constitutional system")
    
    st.markdown("---")
    
    # Calculation details
    with st.expander("🔍 Calculation Details"):
        st.markdown(f"""
        **Entity**: {entity}
        
        **Components**:
        - CE (Constitutional Entrenchment): {ce:.2f} × 0.35 = {ce * 0.35:.3f}
        - UA (Unilateral Amendment): {ua:.2f} × 0.40 = {ua * 0.40:.3f}
        - JPI (Judicial Power Index): {jpi:.2f} × 0.25 = {jpi * 0.25:.3f}
        
        **Total CLI**: {ce * 0.35:.3f} + {ua * 0.40:.3f} + {jpi * 0.25:.3f} = **{cli:.3f}**
        """)
    
    # Track usage
    if st.button("💾 Save Calculation"):
        registry.track_usage("cli_calculator")
        st.success(f"✅ Saved: {entity} - CLI = {cli:.3f}")


def render_dual_index_analyzer():
    """Render Dual-Index Analyzer tool"""
    feature = registry.get_feature("dual_index_analyzer")
    
    if not feature or not feature.enabled:
        st.error("❌ Dual-Index Analyzer is disabled. Enable it in Feature Manager.")
        return
    
    st.markdown(f"# {feature.icon} {feature.name}")
    st.markdown(feature.description)
    
    st.markdown("---")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Constitutional Lock-In")
        entity = st.text_input("Entity Name", value="Example Country")
        ce = st.slider("CE", 0.0, 1.0, 0.70, 0.01, key="dual_ce")
        ua = st.slider("UA", 0.0, 1.0, 0.60, 0.01, key="dual_ua")
        jpi = st.slider("JPI", 0.0, 1.0, 0.65, 0.01, key="dual_jpi")
        
        cli = 0.35 * ce + 0.40 * ua + 0.25 * jpi
        st.metric("CLI", f"{cli:.3f}")
    
    with col2:
        st.markdown("### 🏛️ Cultural Lock-In")
        ct1 = st.slider("CT1 - Narrative Stability", 0.0, 1.0, 0.50, 0.01, help="Durability of founding myths")
        ct2 = st.slider("CT2 - Shock Resistance", 0.0, 1.0, 0.45, 0.01, help="Cultural persistence through crises")
        ct3 = st.slider("CT3 - Policy Continuity", 0.0, 1.0, 0.55, 0.01, help="Institutional path dependency")
        
        cli_cultural = 0.40 * ct1 + 0.30 * ct2 + 0.30 * ct3
        st.metric("CLI_cultural", f"{cli_cultural:.3f}")
    
    # Analysis
    st.markdown("---")
    st.markdown("### 🎯 Dual-Index Analysis")
    
    interaction = cli * cli_cultural
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Interaction Score", f"{interaction:.3f}")
    
    with col2:
        risk = "HIGH" if interaction < 0.30 else ("MEDIUM" if interaction < 0.40 else "LOW")
        risk_color = "🔴" if risk == "HIGH" else ("🟡" if risk == "MEDIUM" else "🟢")
        st.metric("Collapse Risk", f"{risk_color} {risk}")
    
    with col3:
        # Classify profile
        if cli >= 0.60 and cli_cultural >= 0.60:
            profile = "Stable Rigidity"
            profile_icon = "🟢"
        elif cli >= 0.60 and cli_cultural < 0.60:
            profile = "Brittle Rigidity"
            profile_icon = "🔴"
        elif cli < 0.60 and cli_cultural >= 0.60:
            profile = "Adaptive Stability"
            profile_icon = "🟦"
        else:
            profile = "Chaotic Fragility"
            profile_icon = "🟠"
        
        st.metric("Institutional Profile", f"{profile_icon} {profile}")
    
    # Visualization
    st.markdown("---")
    st.markdown("### 📈 Quadrant Matrix")
    
    # Create matrix plot
    fig = go.Figure()
    
    # Quadrant shading
    fig.add_shape(type="rect", x0=0.60, y0=0.60, x1=1.0, y1=1.0,
                  fillcolor="lightgreen", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=0.60, y0=0.0, x1=1.0, y1=0.60,
                  fillcolor="red", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=0.0, y0=0.60, x1=0.60, y1=1.0,
                  fillcolor="lightblue", opacity=0.2, line_width=0)
    fig.add_shape(type="rect", x0=0.0, y0=0.0, x1=0.60, y1=0.60,
                  fillcolor="gray", opacity=0.1, line_width=0)
    
    # Collapse risk threshold (hyperbola: CLI × CLI_cultural = 0.30)
    import numpy as np
    x_threshold = np.linspace(0.30, 1.0, 1000)
    y_threshold = 0.30 / x_threshold
    fig.add_trace(go.Scatter(x=x_threshold, y=y_threshold, mode='lines',
                             name='Collapse Risk Threshold (0.30)',
                             line=dict(color='black', dash='dash', width=3)))
    
    # Data point
    fig.add_trace(go.Scatter(x=[cli], y=[cli_cultural], mode='markers+text',
                             name=entity, text=[entity], textposition='top center',
                             marker=dict(size=15, color=profile_icon)))
    
    fig.update_layout(
        xaxis_title="Constitutional Lock-In Index (CLI)",
        yaxis_title="Cultural Lock-In Index (CLI_cultural)",
        xaxis=dict(range=[0, 1], dtick=0.1),
        yaxis=dict(range=[0, 1], dtick=0.1),
        height=600,
        title="Dual-Index Interaction Matrix"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Explanation
    with st.expander("📖 Profile Explanation"):
        if profile == "Stable Rigidity":
            st.markdown("""
            **Stable Rigidity**: High constitutional lock-in WITH strong cultural foundation.
            - ✅ Constitutional stability backed by cultural legitimacy
            - ✅ Institutions anchored in social norms
            - ⚠️ Risk: Over-rigidity may prevent necessary adaptation
            """)
        elif profile == "Brittle Rigidity":
            st.markdown("""
            **Brittle Rigidity**: High constitutional lock-in WITHOUT cultural foundation.
            - ❌ "Scaffold without foundation" - rigid structure, no cultural support
            - ❌ HIGH COLLAPSE RISK - formal institutions lack legitimacy
            - ⚠️ Example: Somalia Federal (CLI=0.76, CLI_cultural=0.34, Interaction=0.26)
            """)
        elif profile == "Adaptive Stability":
            st.markdown("""
            **Adaptive Stability**: Low constitutional lock-in WITH strong cultural foundation.
            - ✅ Flexible institutions anchored in cultural norms
            - ✅ Can adapt to shocks while maintaining continuity
            - ✅ Example: Somalilandia (CLI=0.54, CLI_cultural=0.70, Interaction=0.38)
            """)
        else:
            st.markdown("""
            **Chaotic Fragility**: Low constitutional lock-in WITHOUT cultural foundation.
            - ⚠️ Weak institutions, weak cultural transmission
            - ⚠️ MEDIUM RISK - susceptible to instability
            - ⚠️ Requires building both constitutional and cultural lock-in
            """)
    
    # Track usage
    if st.button("💾 Save Analysis"):
        registry.track_usage("dual_index_analyzer")
        st.success(f"✅ Saved: {entity} - {profile}")


def render_rootfinder():
    """Render Rootfinder tool"""
    feature = registry.get_feature("rootfinder")
    
    if not feature or not feature.enabled:
        st.error("❌ Rootfinder is disabled or requires Pro tier.")
        return
    
    st.markdown(f"# {feature.icon} {feature.name}")
    st.markdown(feature.description)
    
    st.markdown("---")
    
    st.markdown("### 🔍 Trace Constitutional Genealogy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        constitution = st.selectbox(
            "Select Constitution",
            ["Argentina 2025", "Chile 2025", "Uruguay 2025", "Colombia 2025", "Custom"]
        )
        
        article = st.text_input("Article Number", value="14", help="e.g., 14, 75.22, 1")
    
    with col2:
        search_type = st.radio(
            "Search Type",
            ["Exact Match", "Semantic Similarity", "Keyword Search"]
        )
    
    if st.button("🌳 Trace Root"):
        # Simulate rootfinder analysis
        st.markdown("---")
        st.markdown("### 📊 Genealogy Results")
        
        # Example result for Argentine Art. 14
        if "Argentina" in constitution and article == "14":
            st.success("✅ Root Found!")
            
            st.markdown("""
            **Article 14 - Freedom of Work and Economic Rights**
            
            **Root**: 1853 Constitution, Art. 14 (Original text)
            
            **Genealogy**:
            - **1853**: Original formulation (Independence era)
            - **1860**: Minor revision (Buenos Aires integration)
            - **1949**: Suspended during Peronist constitution
            - **1956**: Reinstated after 1955 coup
            - **1994**: Confirmed unchanged in constitutional reform
            - **2025**: Still unchanged (172 years old)
            
            **Classification**: 🦴 **LIVING FOSSIL**
            - Age: 172 years
            - Survival rate: 100%
            - Mutations: 0
            - Extinction events: 1 (temporary, 1949-1956)
            
            **Original Text** (1853):
            > "Todos los habitantes de la Nación gozan de los siguientes derechos conforme a las leyes que reglamenten su ejercicio: de trabajar y ejercer toda industria lícita..."
            
            **Current Text** (2025):
            > [IDENTICAL]
            """)
            
            # Timeline visualization
            timeline_data = pd.DataFrame({
                "Year": [1853, 1860, 1949, 1956, 1994, 2025],
                "Event": ["Original", "Revision", "Suspended", "Reinstated", "Confirmed", "Present"],
                "Status": ["✅", "✅", "❌", "✅", "✅", "✅"]
            })
            
            fig = px.timeline(
                timeline_data,
                x_start="Year",
                x_end="Year",
                y="Event",
                title="Art. 14 Timeline (1853-2025)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("🔍 Analyzing constitutional genealogy...")
            st.markdown("""
            **Note**: Rootfinder Pro feature activated.
            
            Real implementation would:
            1. Parse historical constitutions
            2. Extract article texts
            3. Compare using NLP (TF-IDF, embeddings)
            4. Build genealogy tree
            5. Classify provisions (living fossil, mutation, extinction)
            """)
        
        # Track usage
        registry.track_usage("rootfinder")


def render_paper_builder():
    """Render Paper Builder tool"""
    feature = registry.get_feature("paper_builder")
    
    if not feature or not feature.enabled:
        st.error("❌ Paper Builder is disabled. Enable it in Feature Manager.")
        return
    
    st.markdown(f"# {feature.icon} {feature.name}")
    st.markdown(feature.description)
    
    st.markdown("---")
    
    st.markdown("### 📄 Select Paper Project")
    
    paper_projects = [
        "somalia_somalilandia_ept",
        "argentina_taxes_phenotype",
        "constitutional_paleontology",
        "golden_ratio_analysis"
    ]
    
    selected_paper = st.selectbox("Project", paper_projects)
    
    st.markdown("### ⚙️ Build Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_tables = st.checkbox("Include Tables", value=True)
        include_figures = st.checkbox("Include Figure Placeholders", value=True)
        include_appendices = st.checkbox("Include Appendices", value=True)
    
    with col2:
        format_style = st.selectbox("Citation Style", ["APA 7", "Chicago", "MLA", "Harvard"])
        output_format = st.selectbox("Output Format", ["DOCX", "PDF", "LaTeX"])
    
    if st.button("🚀 Build Paper"):
        with st.spinner("Building paper..."):
            import time
            time.sleep(2)  # Simulate build process
            
            st.success("✅ Paper built successfully!")
            
            st.markdown("---")
            st.markdown("### 📊 Build Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Paragraphs", "629")
            with col2:
                st.metric("Word Count", "~18,000")
            with col3:
                st.metric("Pages", "~45")
            
            st.markdown("### 📥 Download")
            st.download_button(
                label="📥 Download SSRN Document",
                data=b"Mock DOCX file content",
                file_name=f"{selected_paper}_SSRN.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
            # Track usage
            registry.track_usage("paper_builder")


def render_visualizations():
    """Render Visualizations hub"""
    st.markdown("# 📈 Visualizations")
    
    tabs = st.tabs(["📊 CLI Matrix", "📅 Timeline", "📉 Correlations"])
    
    with tabs[0]:
        render_cli_matrix_viz()
    
    with tabs[1]:
        render_timeline_viz()
    
    with tabs[2]:
        render_correlations_viz()


def render_cli_matrix_viz():
    """Render CLI Matrix visualizer"""
    st.markdown("### 📊 CLI × CLI_cultural Matrix")
    
    st.markdown("Upload CLI data or use example dataset")
    
    use_example = st.checkbox("Use example dataset (Somalia, Somalilandia, Uruguay, Chile, Argentina)")
    
    if use_example:
        # Example data
        data = pd.DataFrame({
            "Country": ["Somalia Federal", "Somalilandia", "Uruguay", "Chile", "Argentina"],
            "CLI": [0.76, 0.54, 0.75, 0.68, 0.55],
            "CLI_cultural": [0.34, 0.70, 0.77, 0.65, 0.59]
        })
        
        st.dataframe(data, use_container_width=True, hide_index=True)
        
        if st.button("📈 Generate Matrix"):
            # Create visualization (same as dual-index analyzer)
            fig = go.Figure()
            
            # Quadrants and threshold (same as before)
            fig.add_shape(type="rect", x0=0.60, y0=0.60, x1=1.0, y1=1.0,
                          fillcolor="lightgreen", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=0.60, y0=0.0, x1=1.0, y1=0.60,
                          fillcolor="red", opacity=0.2, line_width=0)
            fig.add_shape(type="rect", x0=0.0, y0=0.60, x1=0.60, y1=1.0,
                          fillcolor="lightblue", opacity=0.2, line_width=0)
            
            # Data points
            fig.add_trace(go.Scatter(
                x=data["CLI"],
                y=data["CLI_cultural"],
                mode='markers+text',
                text=data["Country"],
                textposition='top center',
                marker=dict(size=15, color=['red', 'green', 'blue', 'blue', 'orange'])
            ))
            
            fig.update_layout(
                xaxis_title="Constitutional Lock-In Index (CLI)",
                yaxis_title="Cultural Lock-In Index (CLI_cultural)",
                xaxis=dict(range=[0, 1]),
                yaxis=dict(range=[0, 1]),
                height=600,
                title="CLI × CLI_cultural Interaction Matrix"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.download_button(
                "📥 Download PNG (300 DPI)",
                data=b"Mock PNG data",
                file_name="figure3_cli_matrix.png",
                mime="image/png"
            )
            
            registry.track_usage("cli_matrix_visualizer")


def render_timeline_viz():
    """Render Timeline generator"""
    st.markdown("### 📅 Constitutional Timeline")
    
    st.markdown("Create timeline of constitutional events")
    
    country = st.text_input("Country", value="Somalia")
    
    # Event input
    st.markdown("**Add Events**:")
    
    events = []
    for i in range(3):
        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input(f"Year {i+1}", min_value=1800, max_value=2025, value=1960 + i*30, key=f"year_{i}")
        with col2:
            event = st.text_input(f"Event {i+1}", value=f"Event {i+1}", key=f"event_{i}")
        
        events.append({"year": year, "event": event})
    
    if st.button("📅 Generate Timeline"):
        fig = go.Figure()
        
        years = [e["year"] for e in events]
        event_names = [e["event"] for e in events]
        
        fig.add_trace(go.Scatter(
            x=years,
            y=[1] * len(years),
            mode='markers+text',
            text=event_names,
            textposition='top center',
            marker=dict(size=15, color='blue')
        ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis=dict(visible=False),
            height=400,
            title=f"Constitutional Timeline: {country}"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        registry.track_usage("timeline_generator")


def render_correlations_viz():
    """Render Correlations plotter"""
    st.markdown("### 📉 CLI Correlations")
    
    st.markdown("Visualize CLI correlations with governance outcomes")
    
    correlation_type = st.selectbox(
        "Select Correlation",
        ["CLI vs Freedom House", "CLI vs Conflict Intensity", "CLI vs GDP per capita"]
    )
    
    if st.button("📉 Generate Plot"):
        # Example data
        import numpy as np
        cli_values = np.random.uniform(0.3, 0.9, 20)
        outcome_values = -0.7 * cli_values + np.random.normal(0, 0.1, 20) + 0.8
        
        fig = px.scatter(
            x=cli_values,
            y=outcome_values,
            trendline="ols",
            labels={"x": "CLI", "y": "Freedom House Score"},
            title=correlation_type
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        registry.track_usage("correlation_plotter")


def render_ai_assistant():
    """Render AI Assistant chat interface"""
    feature = registry.get_feature("genspark_assistant")
    
    if not feature or not feature.enabled:
        st.error("❌ AI Assistant is disabled. Enable it in Feature Manager.")
        return
    
    st.markdown(f"# {feature.icon} {feature.name}")
    st.markdown(feature.description)
    
    st.markdown("---")
    
    # Chat interface
    st.markdown("### 💬 Ask Genspark")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about methodology, formulas, or data sources..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response (mock)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                import time
                time.sleep(1)
                
                # Mock responses
                if "cli_cultural" in prompt.lower() or "cultural lock-in" in prompt.lower():
                    response = """
                    **CLI_cultural (Cultural Lock-In Index)** is calculated using the formula:
                    
                    ```
                    CLI_cultural = 0.40 × CT1 + 0.30 × CT2 + 0.30 × CT3
                    ```
                    
                    Where:
                    - **CT1** = Cultural Transmission - Narrative Stability (0.0-1.0)
                    - **CT2** = Cultural Transmission - Shock Resistance (0.0-1.0)
                    - **CT3** = Cultural Transmission - Policy Continuity (0.0-1.0)
                    
                    The weights reflect that **narrative stability (40%)** is the PRIMARY mechanism of cultural transmission according to Extended Phenotype Theory (EPT).
                    
                    📚 **Source**: APPENDICES_SPECIFICATIONS.md, Appendix D, Section D.1
                    """
                elif "data sources" in prompt.lower() and "ct1" in prompt.lower():
                    response = """
                    **Data sources for CT1 (Narrative Stability)**:
                    
                    1. **Constitutional Preambles**: Textual analysis of founding narratives
                    2. **Public Opinion Surveys**: 
                       - World Values Survey
                       - Afrobarometer (for African countries)
                       - Latinobarómetro (for Latin America)
                    3. **Historical Documents**:
                       - Independence declarations
                       - Peace agreements
                       - National symbols analysis
                    
                    📚 **Source**: APPENDICES_SPECIFICATIONS.md, Appendix D, Section D.3
                    """
                else:
                    response = f"""
                    I'm Genspark, your research assistant! I can help with:
                    
                    - 📊 Formula explanations (CLI, CLI_cultural)
                    - 📚 Data source recommendations
                    - 🔍 Methodology guidance
                    - 💻 Code examples
                    - 📖 Literature references
                    
                    Try asking:
                    - "How is CLI_cultural calculated?"
                    - "What data sources for CT1?"
                    - "Explain the Brittle Rigidity profile"
                    - "Show me code to calculate CLI"
                    """
                
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Track usage
        registry.track_usage("genspark_assistant")


def render_feature_manager():
    """Render Feature Manager"""
    st.markdown("# 🎛️ Feature Manager")
    st.markdown("Enable or disable research tools")
    
    st.markdown("---")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + [c.value for c in FeatureCategory]
        )
    
    with col2:
        filter_tier = st.selectbox(
            "Filter by Tier",
            ["All", "free", "basic", "pro", "enterprise"]
        )
    
    with col3:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "Enabled", "Disabled"]
        )
    
    # Get filtered features
    features = list(registry.features.values())
    
    if filter_category != "All":
        features = [f for f in features if f.category.value == filter_category]
    
    if filter_tier != "All":
        features = [f for f in features if f.saas_tier == filter_tier]
    
    if filter_status == "Enabled":
        features = [f for f in features if f.enabled]
    elif filter_status == "Disabled":
        features = [f for f in features if not f.enabled]
    
    st.markdown(f"### 📊 Showing {len(features)} features")
    
    # Bulk actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Enable All"):
            for f in features:
                registry.enable_feature(f.id)
            st.success(f"✅ Enabled {len(features)} features")
            st.rerun()
    
    with col2:
        if st.button("❌ Disable All"):
            for f in features:
                registry.disable_feature(f.id)
            st.success(f"❌ Disabled {len(features)} features")
            st.rerun()
    
    st.markdown("---")
    
    # Feature cards
    for feature in features:
        render_feature_card(feature, compact=False)


def render_documentation():
    """Render Documentation hub"""
    st.markdown("# 📚 Documentation")
    
    tabs = st.tabs(["📖 Quick Start", "🔧 API Reference", "💡 Examples", "🎓 Tutorials"])
    
    with tabs[0]:
        st.markdown("""
        ## 🚀 Quick Start Guide
        
        ### 1. Enable Features
        Navigate to **Feature Manager** and enable the tools you need.
        
        ### 2. Calculate CLI
        Use the **CLI Calculator** to measure constitutional rigidity.
        
        ### 3. Analyze Profiles
        Use the **Dual-Index Analyzer** to classify institutional configurations.
        
        ### 4. Generate Papers
        Use the **Paper Builder** to create SSRN-ready documents.
        
        ### 5. Ask Questions
        Use the **AI Assistant** for methodology guidance.
        """)
    
    with tabs[1]:
        st.markdown("""
        ## 🔧 API Reference
        
        ### Base URL
        ```
        http://localhost:8000/api
        ```
        
        ### Endpoints
        
        #### CLI Calculator
        ```
        POST /api/cli/calculate
        {
          "CE": 0.80,
          "UA": 0.85,
          "JPI": 0.55
        }
        ```
        
        #### Dual-Index Analyzer
        ```
        POST /api/cli/dual-index
        {
          "CLI": 0.76,
          "CLI_cultural": 0.34,
          "entity": "Somalia Federal"
        }
        ```
        
        #### Paper Builder
        ```
        POST /api/papers/build
        {
          "paper_id": "somalia_somalilandia_ept"
        }
        ```
        """)
    
    with tabs[2]:
        st.markdown("""
        ## 💡 Examples
        
        ### Example 1: Calculate CLI for Somalia
        ```python
        CE = 0.80
        UA = 0.85
        JPI = 0.55
        
        CLI = 0.35 * CE + 0.40 * UA + 0.25 * JPI
        # CLI = 0.76
        ```
        
        ### Example 2: Classify Institutional Profile
        ```python
        CLI = 0.76
        CLI_cultural = 0.34
        interaction = CLI * CLI_cultural  # 0.26
        
        if interaction < 0.30:
            profile = "Brittle Rigidity (HIGH RISK)"
        ```
        """)
    
    with tabs[3]:
        st.markdown("""
        ## 🎓 Tutorials
        
        ### Video Tutorials
        - 📹 Introduction to CLI Framework (10 min)
        - 📹 Using the Dual-Index Analyzer (15 min)
        - 📹 Building Research Papers (20 min)
        
        ### Written Tutorials
        - 📝 CLI Calculator Step-by-Step
        - 📝 Interpreting Institutional Profiles
        - 📝 Advanced Feature Configuration
        """)


def main():
    """Main application"""
    page = render_sidebar()
    
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "📊 CLI Calculator":
        render_cli_calculator()
    elif page == "🎯 Dual-Index Analyzer":
        render_dual_index_analyzer()
    elif page == "🌳 Rootfinder":
        render_rootfinder()
    elif page == "📄 Paper Builder":
        render_paper_builder()
    elif page == "📈 Visualizations":
        render_visualizations()
    elif page == "🤖 AI Assistant":
        render_ai_assistant()
    elif page == "🎛️ Feature Manager":
        render_feature_manager()
    elif page == "📚 Documentation":
        render_documentation()


if __name__ == "__main__":
    main()

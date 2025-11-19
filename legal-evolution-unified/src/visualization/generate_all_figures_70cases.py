#!/usr/bin/env python3
"""
Generate ALL 8 publication-quality figures for 70-case analysis at 300 DPI.
Figures 1-8: Complete visualization set.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.linear_model import LogisticRegression
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Color scheme
COLORS = {
    'Sovereignty Wins': '#E74C3C',     # Red
    'Globalism Wins': '#3498DB',        # Blue
    'Mixed': '#F39C12',                 # Orange
    'Negotiated': '#9B59B6'             # Purple
}

def load_data():
    """Load analyzed dataset."""
    df = pd.read_csv('results/sovereignty_globalism_70cases_analyzed.csv')
    return df

def infer_iuspace_coordinates(row):
    """Infer 12-dimensional IusSpace coordinates from case characteristics."""
    coords = {}
    
    common_law = ['UK', 'Ireland', 'Canada', 'Australia', 'India']
    coords['Dim1'] = 7 if row['Country'] in common_law else 2
    coords['Dim2'] = 8 if row['Event_Type'] == 'Constitutional' else 5
    coords['Dim3'] = 9 if row['Event_Type'] == 'Judicial' else 5
    coords['Dim4'] = 7 if 'EU' in str(row['Institution']) else 4
    
    federal = ['Germany', 'Canada', 'Australia', 'Switzerland', 'Belgium', 'Spain']
    coords['Dim5'] = 8 if row['Country'] in federal else 3
    
    low_democracy = ['Russia', 'Turkey', 'Hungary', 'Poland', 'Philippines']
    coords['Dim6'] = 4 if row['Country'] in low_democracy else 8
    coords['Dim7'] = 7 if row['Year'] > 2000 else 6
    
    strong_admin = ['Germany', 'UK', 'France', 'Netherlands', 'Sweden', 'Denmark']
    coords['Dim8'] = 9 if row['Country'] in strong_admin else 5
    
    individualist = ['UK', 'USA', 'Australia', 'Canada', 'Netherlands']
    coords['Dim9'] = 8 if row['Country'] in individualist else 4
    coords['Dim10'] = 7 if coords['Dim1'] == 7 else 4
    
    high_trust = ['Denmark', 'Sweden', 'Finland', 'Norway', 'Switzerland', 'Netherlands']
    coords['Dim11'] = 9 if row['Country'] in high_trust else 5
    coords['Dim12'] = row['IusSpace_Dim12_IntegrationScore']
    
    return coords

def figure1_phenotype_competition(df):
    """Figure 1: Sovereignty vs Globalism Phenotype Competition."""
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    
    # Scatter plot with color by outcome
    for outcome, color in COLORS.items():
        mask = df['Outcome'] == outcome
        if mask.sum() > 0:
            ax.scatter(df[mask]['Globalism_Phenotype_Score'],
                      df[mask]['Sovereignty_Phenotype_Score'],
                      c=color, label=outcome, s=100, alpha=0.7, edgecolors='black')
    
    # Regression line
    z = np.polyfit(df['Globalism_Phenotype_Score'], df['Sovereignty_Phenotype_Score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(0, 1, 100)
    ax.plot(x_line, p(x_line), "k--", linewidth=2, label=f'Linear fit (r={stats.pearsonr(df["Globalism_Phenotype_Score"], df["Sovereignty_Phenotype_Score"])[0]:.3f})')
    
    # Annotate key cases
    key_cases = df[df['Country'].isin(['UK', 'Russia', 'Netherlands', 'Poland', 'Philippines', 'Hungary'])].nlargest(6, 'Year')
    for _, case in key_cases.iterrows():
        ax.annotate(f"{case['Country']}\n{int(case['Year'])}", 
                   xy=(case['Globalism_Phenotype_Score'], case['Sovereignty_Phenotype_Score']),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    ax.set_xlabel('Globalism Phenotype Score', fontsize=14, fontweight='bold')
    ax.set_ylabel('Sovereignty Phenotype Score', fontsize=14, fontweight='bold')
    ax.set_title('Figure 1: Phenotype Competition - Sovereignty vs Globalism\n70 Cases (1985-2024)', 
                fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure1_phenotype_competition.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 1: Phenotype Competition")

def figure2_integration_threshold(df):
    """Figure 2: Integration Threshold Effect (Dim12)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    
    # Left: Scatter plot
    for outcome, color in COLORS.items():
        mask = df['Outcome'] == outcome
        if mask.sum() > 0:
            ax1.scatter(df[mask]['IusSpace_Dim12_IntegrationScore'],
                       df[mask]['Sovereignty_Phenotype_Score'],
                       c=color, label=outcome, s=100, alpha=0.7, edgecolors='black')
    
    # Threshold line at Dim12 = 4
    ax1.axvline(x=4, color='red', linestyle='--', linewidth=3, label='Threshold (Dim12=4)')
    
    ax1.set_xlabel('IusSpace Dim12 (International Integration)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Sovereignty Phenotype Score', fontsize=14, fontweight='bold')
    ax1.set_title('Integration Score vs Sovereignty', fontsize=14, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Right: Win rate by Dim12 bins
    bins = [0, 2, 4, 6, 8, 11]
    labels = ['0-2', '2-4', '4-6', '6-8', '8+']
    df['Dim12_Bin'] = pd.cut(df['IusSpace_Dim12_IntegrationScore'], bins=bins, labels=labels, include_lowest=True)
    
    win_rates = df.groupby('Dim12_Bin')['Sovereignty_Win'].agg(['mean', 'count'])
    win_rates['mean'] *= 100  # Convert to percentage
    
    bars = ax2.bar(range(len(win_rates)), win_rates['mean'], 
                   color=['#27AE60' if x >= 90 else '#E74C3C' if x < 50 else '#F39C12' for x in win_rates['mean']],
                   edgecolor='black', linewidth=1.5)
    
    # Add count labels on bars
    for i, (idx, row) in enumerate(win_rates.iterrows()):
        ax2.text(i, row['mean'] + 3, f"n={int(row['count'])}", 
                ha='center', fontsize=10, fontweight='bold')
    
    ax2.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5, label='100% Threshold')
    ax2.set_xlabel('Dim12 Integration Bins', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Sovereignty Win Rate (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Win Rate by Integration Level', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(win_rates)))
    ax2.set_xticklabels(win_rates.index, fontsize=11)
    ax2.set_ylim(0, 110)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Figure 2: Integration Threshold Effect - Dim12 Analysis\n70 Cases (1985-2024)', 
                fontsize=18, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure2_integration_threshold.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 2: Integration Threshold")

def figure3_fitness_trajectories(df):
    """Figure 3: Evolutionary Fitness Trajectories Over Time."""
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    
    # Aggregate by year
    yearly = df.groupby('Year').agg({
        'Sovereignty_Phenotype_Score': 'mean',
        'Globalism_Phenotype_Score': 'mean',
        'IusSpace_Dim12_IntegrationScore': 'mean'
    }).reset_index()
    
    ax.plot(yearly['Year'], yearly['Sovereignty_Phenotype_Score'], 
           'o-', color='#E74C3C', linewidth=3, markersize=8, label='Sovereignty Phenotype', markeredgecolor='black')
    ax.plot(yearly['Year'], yearly['Globalism_Phenotype_Score'], 
           's-', color='#3498DB', linewidth=3, markersize=8, label='Globalism Phenotype', markeredgecolor='black')
    
    # Normalize Dim12 to 0-1 scale for comparison
    yearly['Dim12_Normalized'] = yearly['IusSpace_Dim12_IntegrationScore'] / 10
    ax.plot(yearly['Year'], yearly['Dim12_Normalized'], 
           '^-', color='#9B59B6', linewidth=3, markersize=8, label='Integration (Dim12/10)', markeredgecolor='black')
    
    # Crisis periods shading
    crisis_periods = [(2008, 2009), (2015, 2016), (2020, 2021), (2022, 2023)]
    for start, end in crisis_periods:
        ax.axvspan(start, end, alpha=0.2, color='gray', label='Crisis Period' if start == 2008 else '')
    
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Phenotype Score (0-1)', fontsize=14, fontweight='bold')
    ax.set_title('Figure 3: Evolutionary Fitness Trajectories (1985-2024)\nMean Phenotype Scores Over Time', 
                fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1983, 2026)
    ax.set_ylim(-0.05, 1.05)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure3_fitness_trajectories.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 3: Fitness Trajectories")

def figure4_crisis_effect(df):
    """Figure 4: Crisis Catalysis Effect."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    
    # Left: Box plot
    crisis_data = [df[df['Crisis_Catalyzed'] == 'Yes']['Sovereignty_Phenotype_Score'],
                   df[df['Crisis_Catalyzed'] == 'No']['Sovereignty_Phenotype_Score']]
    
    bp = ax1.boxplot(crisis_data, labels=['Crisis Yes', 'Crisis No'],
                     patch_artist=True, widths=0.6,
                     boxprops=dict(facecolor='#F39C12', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5))
    
    # Add individual points
    for i, data in enumerate(crisis_data, 1):
        y = data.values
        x = np.random.normal(i, 0.04, size=len(y))
        ax1.scatter(x, y, alpha=0.4, s=50, color='black')
    
    # Add mean markers
    means = [d.mean() for d in crisis_data]
    ax1.plot([1, 2], means, 'D-', color='red', markersize=12, linewidth=2, label=f'Means: Δ={means[0]-means[1]:.3f}')
    
    # Statistical test results
    t_stat, p_val = stats.ttest_ind(crisis_data[0], crisis_data[1])
    ax1.text(1.5, 0.95, f't={t_stat:.3f}, p={p_val:.3f}', 
            fontsize=12, ha='center', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax1.set_ylabel('Sovereignty Phenotype Score', fontsize=14, fontweight='bold')
    ax1.set_title('Crisis vs Non-Crisis Cases', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_ylim(-0.05, 1.05)
    
    # Right: Scatter plot over time
    for crisis in ['Yes', 'No']:
        mask = df['Crisis_Catalyzed'] == crisis
        color = '#E74C3C' if crisis == 'Yes' else '#3498DB'
        marker = 'o' if crisis == 'Yes' else 's'
        ax2.scatter(df[mask]['Year'], df[mask]['Sovereignty_Phenotype_Score'],
                   c=color, marker=marker, s=100, alpha=0.7, 
                   label=f'Crisis {crisis}', edgecolors='black')
    
    # Crisis period shading
    crisis_periods = [(2008, 2009), (2015, 2016), (2020, 2021), (2022, 2023)]
    for start, end in crisis_periods:
        ax2.axvspan(start, end, alpha=0.15, color='gray')
    
    ax2.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Sovereignty Phenotype Score', fontsize=14, fontweight='bold')
    ax2.set_title('Temporal Distribution', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)
    
    fig.suptitle('Figure 4: Crisis Catalysis Effect on Sovereignty Phenotype\n70 Cases (1985-2024)', 
                fontsize=18, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure4_crisis_effect.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 4: Crisis Effect")

def figure5_predictive_model(df):
    """Figure 5: Predictive Model ROC Curve."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    
    # Train logistic regression
    X = df[['Sovereignty_Phenotype_Score', 'Globalism_Phenotype_Score', 
            'IusSpace_Dim12_IntegrationScore']].values
    y = df['Sovereignty_Win'].values
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X, y)
    y_prob = model.predict_proba(X)[:, 1]
    
    # Left: ROC Curve
    fpr, tpr, thresholds = roc_curve(y, y_prob)
    roc_auc = roc_auc_score(y, y_prob)
    
    ax1.plot(fpr, tpr, color='#E74C3C', linewidth=3, label=f'ROC Curve (AUC = {roc_auc:.4f})')
    ax1.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Random Classifier (AUC = 0.50)')
    ax1.fill_between(fpr, tpr, alpha=0.3, color='#E74C3C')
    
    ax1.set_xlabel('False Positive Rate', fontsize=14, fontweight='bold')
    ax1.set_ylabel('True Positive Rate', fontsize=14, fontweight='bold')
    ax1.set_title('ROC Curve', fontsize=14, fontweight='bold')
    ax1.legend(loc='lower right', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-0.02, 1.02)
    ax1.set_ylim(-0.02, 1.02)
    
    # Right: Predicted probability distribution
    df_plot = df.copy()
    df_plot['Predicted_Prob'] = y_prob
    
    for outcome, color in {'Sovereignty Wins': '#E74C3C', 'Globalism Wins': '#3498DB'}.items():
        mask = df_plot['Outcome'] == outcome
        if mask.sum() > 0:
            ax2.hist(df_plot[mask]['Predicted_Prob'], bins=20, alpha=0.6, 
                    color=color, label=outcome, edgecolor='black')
    
    ax2.axvline(x=0.5, color='black', linestyle='--', linewidth=2, label='Decision Threshold')
    ax2.set_xlabel('Predicted Probability (Sovereignty Win)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=14, fontweight='bold')
    ax2.set_title('Predicted Probability Distribution', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Figure 5: Predictive Model Performance - Logistic Regression\n70 Cases (1985-2024)', 
                fontsize=18, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure5_predictive_model.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 5: Predictive Model")

def figure6_pca_3d(df):
    """Figure 6: 3D PCA Projection (updated for 70 cases)."""
    # Infer full 12D coordinates
    iuspace_coords = df.apply(infer_iuspace_coordinates, axis=1)
    iuspace_df = pd.DataFrame(iuspace_coords.tolist())
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(iuspace_df)
    
    # PCA
    pca = PCA(n_components=3, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    fig = plt.figure(figsize=(14, 10), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot points
    for outcome, color in COLORS.items():
        mask = df['Outcome'] == outcome
        if mask.sum() > 0:
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1], X_pca[mask, 2],
                      c=color, label=outcome, s=100, alpha=0.7, edgecolors='black')
    
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', fontsize=12, fontweight='bold')
    ax.set_zlabel(f'PC3 ({pca.explained_variance_ratio_[2]:.1%})', fontsize=12, fontweight='bold')
    ax.set_title(f'Figure 6: 3D PCA Projection in 12D IusSpace\n70 Cases - {pca.explained_variance_ratio_.sum():.1%} Variance Explained', 
                fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure6_pca_3d_projection.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 6: 3D PCA Projection (UPDATED)")

def figure7_tsne_clusters(df):
    """Figure 7: t-SNE Clustering (updated for 70 cases)."""
    # Infer full 12D coordinates
    iuspace_coords = df.apply(infer_iuspace_coordinates, axis=1)
    iuspace_df = pd.DataFrame(iuspace_coords.tolist())
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(iuspace_df)
    
    # t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(df)-1))
    X_tsne = tsne.fit_transform(X_scaled)
    
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    
    # Plot clusters
    for cluster in df['Cluster'].unique():
        mask = df['Cluster'] == cluster
        ax.scatter(X_tsne[mask, 0], X_tsne[mask, 1],
                  label=f'Cluster {cluster} (n={mask.sum()})',
                  s=150, alpha=0.7, edgecolors='black', linewidth=1.5)
    
    # Annotate key cases
    key_cases = df[df['Country'].isin(['UK', 'Russia', 'Poland', 'Hungary', 'France', 'Netherlands'])].nlargest(8, 'Year')
    for idx, case in key_cases.iterrows():
        case_idx = df.index.get_loc(idx)
        ax.annotate(f"{case['Country']}\n{int(case['Year'])}", 
                   xy=(X_tsne[case_idx, 0], X_tsne[case_idx, 1]),
                   xytext=(15, 15), textcoords='offset points',
                   fontsize=9, bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.4),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
    
    ax.set_xlabel('t-SNE Dimension 1', fontsize=14, fontweight='bold')
    ax.set_ylabel('t-SNE Dimension 2', fontsize=14, fontweight='bold')
    ax.set_title('Figure 7: t-SNE Clustering in 12D IusSpace\n70 Cases with k=5 Clusters', 
                fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=10, ncol=2)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure7_tsne_clusters.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 7: t-SNE Clusters (UPDATED)")

def figure8_crisis_timeline(df):
    """Figure 8: Crisis Timeline with Influence (updated for 70 cases)."""
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    
    # Normalize PageRank for bubble sizes
    if 'PageRank' in df.columns:
        sizes = (df['PageRank'] - df['PageRank'].min()) / (df['PageRank'].max() - df['PageRank'].min()) * 1000 + 100
    else:
        sizes = 200
    
    # Plot bubbles
    for outcome, color in COLORS.items():
        mask = df['Outcome'] == outcome
        if mask.sum() > 0:
            ax.scatter(df[mask]['Year'], df[mask]['Sovereignty_Phenotype_Score'],
                      s=sizes[mask] if hasattr(sizes, '__getitem__') else sizes,
                      c=color, label=outcome, alpha=0.6, edgecolors='black', linewidth=1)
    
    # Crisis period shading
    crisis_periods = [(2008, 2009), (2015, 2016), (2020, 2021), (2022, 2023)]
    for start, end in crisis_periods:
        ax.axvspan(start, end, alpha=0.15, color='red', label='Crisis Period' if start == 2008 else '')
    
    # Annotate top influential cases
    if 'PageRank' in df.columns:
        top_cases = df.nlargest(8, 'PageRank')
        for _, case in top_cases.iterrows():
            ax.annotate(f"{case['Country']}\n{int(case['Year'])}", 
                       xy=(case['Year'], case['Sovereignty_Phenotype_Score']),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1'))
    
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Sovereignty Phenotype Score', fontsize=14, fontweight='bold')
    ax.set_title('Figure 8: Crisis Timeline with Genealogical Influence\n70 Cases (1985-2024) - Bubble Size = PageRank', 
                fontsize=16, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10, ncol=2)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1983, 2026)
    ax.set_ylim(-0.05, 1.05)
    
    plt.tight_layout()
    plt.savefig('visualizations/figure8_crisis_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Figure 8: Crisis Timeline (UPDATED)")

def main():
    print("="*80)
    print("GENERATING ALL 8 FIGURES - 70 Cases at 300 DPI")
    print("="*80)
    
    df = load_data()
    print(f"\n✅ Loaded {len(df)} cases")
    
    print("\nGenerating figures...")
    figure1_phenotype_competition(df)
    figure2_integration_threshold(df)
    figure3_fitness_trajectories(df)
    figure4_crisis_effect(df)
    figure5_predictive_model(df)
    figure6_pca_3d(df)
    figure7_tsne_clusters(df)
    figure8_crisis_timeline(df)
    
    print("\n" + "="*80)
    print("✅ ALL 8 FIGURES GENERATED SUCCESSFULLY")
    print("="*80)
    print("\nSaved to: visualizations/")
    print("  - figure1_phenotype_competition.png")
    print("  - figure2_integration_threshold.png")
    print("  - figure3_fitness_trajectories.png")
    print("  - figure4_crisis_effect.png")
    print("  - figure5_predictive_model.png")
    print("  - figure6_pca_3d_projection.png (UPDATED)")
    print("  - figure7_tsne_clusters.png (UPDATED)")
    print("  - figure8_crisis_timeline.png (UPDATED)")

if __name__ == '__main__':
    main()

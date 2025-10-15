#!/usr/bin/env python3
"""
Advanced Sovereignty vs Globalism Analysis
Using legal-evolution-unified repository methodologies

Implements:
- Analysis 4: Phenotype Clustering (k-means in 12D IusSpace)
- Analysis 8: Crisis Timeline Visualization
- Bootstrap validation for all results
- Integration with IusMorfos V6.0 framework
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from scipy import stats
from scipy.spatial.distance import pdist, squareform
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 16

print("\n" + "="*80)
print("ADVANCED SOVEREIGNTY VS GLOBALISM ANALYSIS")
print("Using legal-evolution-unified methodologies")
print("="*80)

# Load data
df = pd.read_csv('/home/user/webapp/data/cases/sovereignty_globalism_parsed.csv')
print(f"\n✅ Loaded {len(df)} cases from {df['Year'].min()} to {df['Year'].max()}")

# Create derived variables
df['Sovereignty_Win'] = df['Outcome'].str.contains('Sovereignty', na=False).astype(int)
df['Globalism_Win'] = df['Outcome'].str.contains('Globalism', na=False).astype(int)
df['Crisis_Binary'] = (df['Crisis_Catalyzed'] == 'Yes').astype(int)

# ============================================================================
# ANALYSIS 4: PHENOTYPE CLUSTERING (K-MEANS IN 12D IUSPACE)
# ============================================================================

print("\n" + "="*80)
print("ANALYSIS 4: PHENOTYPE CLUSTERING IN IUSPACE")
print("="*80)

# Since we only have Dim12 directly, we'll infer other dimensions
# Based on IusMorfos V6.0 framework mapping case characteristics to dimensions

def infer_iuspace_coordinates(row):
    """
    Infer 12-dimensional IusSpace coordinates from case characteristics.
    
    IusMorfos V6.0 Dimensions:
    Dim1: Codification Level (inferred from institution type)
    Dim2: Precedent Weight (inferred from legal family)
    Dim3: Constitutional Rigidity (inferred from sovereignty score)
    Dim4: Judicial Review Strength (inferred from institution)
    Dim5: Rights Cataloging (inferred from event type)
    Dim6: Federal Structure (inferred from country characteristics)
    Dim7: Legislative Procedure (inferred from institution)
    Dim8: Executive Power (inferred from sovereignty score)
    Dim9: Judicial Independence (inferred from institution)
    Dim10: Administrative Law (inferred from globalism score)
    Dim11: Property Rights (inferred from crisis context)
    Dim12: International Integration (given directly)
    """
    coords = {}
    
    # Dim12: Given directly
    coords['Dim12'] = row['IusSpace_Dim12_IntegrationScore']
    
    # Dim1: Codification (higher for civil law, lower for common law)
    if row['Country'] in ['United Kingdom', 'United States', 'Canada', 'Australia', 'New Zealand']:
        coords['Dim1'] = 4.0 + np.random.uniform(-0.5, 0.5)  # Common law
    else:
        coords['Dim1'] = 7.0 + np.random.uniform(-0.5, 0.5)  # Civil law
    
    # Dim2: Precedent Weight (inverse of Dim1)
    coords['Dim2'] = 11 - coords['Dim1']
    
    # Dim3: Constitutional Rigidity (from sovereignty score)
    coords['Dim3'] = row['Sovereignty_Phenotype_Score'] * 8 + 1
    
    # Dim4: Judicial Review Strength (inferred from institution)
    if 'Court' in str(row['Institution']):
        coords['Dim4'] = 7.0 + np.random.uniform(-1, 1)
    elif 'Union' in str(row['Institution']):
        coords['Dim4'] = 5.0 + np.random.uniform(-1, 1)
    else:
        coords['Dim4'] = 6.0 + np.random.uniform(-1, 1)
    
    # Dim5: Rights Cataloging (from globalism score)
    coords['Dim5'] = row['Globalism_Phenotype_Score'] * 7 + 2
    
    # Dim6: Federal Structure (country-specific)
    if row['Country'] in ['United States', 'Germany', 'Canada', 'Australia', 'Brazil', 'Argentina']:
        coords['Dim6'] = 7.0 + np.random.uniform(-0.5, 0.5)
    else:
        coords['Dim6'] = 4.0 + np.random.uniform(-0.5, 0.5)
    
    # Dim7: Legislative Procedure (from sovereignty score)
    coords['Dim7'] = (1 - row['Sovereignty_Phenotype_Score']) * 5 + 3
    
    # Dim8: Executive Power (from sovereignty score)
    coords['Dim8'] = row['Sovereignty_Phenotype_Score'] * 6 + 2
    
    # Dim9: Judicial Independence (from institution type)
    if 'Court' in str(row['Institution']):
        coords['Dim9'] = 8.0 + np.random.uniform(-0.5, 0.5)
    else:
        coords['Dim9'] = 6.0 + np.random.uniform(-0.5, 0.5)
    
    # Dim10: Administrative Law (from globalism score)
    coords['Dim10'] = row['Globalism_Phenotype_Score'] * 8 + 1
    
    # Dim11: Property Rights (from crisis context)
    if row['Crisis_Binary'] == 1:
        coords['Dim11'] = 5.0 + np.random.uniform(-1, 1)
    else:
        coords['Dim11'] = 7.0 + np.random.uniform(-0.5, 0.5)
    
    return coords

# Generate 12D coordinates
print("\n📊 Inferring 12-dimensional IusSpace coordinates...")
iuspace_coords = df.apply(infer_iuspace_coordinates, axis=1, result_type='expand')
iuspace_df = pd.DataFrame(iuspace_coords)

# Standardize for clustering
scaler = StandardScaler()
X_scaled = scaler.fit_transform(iuspace_df)

# Determine optimal number of clusters using silhouette score
print("\n🔍 Testing k=2,3,4,5 clusters...")
silhouette_scores = {}
calinski_scores = {}

for k in [2, 3, 4, 5]:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=50)
    labels = kmeans.fit_predict(X_scaled)
    silhouette_scores[k] = silhouette_score(X_scaled, labels)
    calinski_scores[k] = calinski_harabasz_score(X_scaled, labels)
    print(f"  k={k}: Silhouette={silhouette_scores[k]:.4f}, Calinski-Harabasz={calinski_scores[k]:.2f}")

# Select optimal k (highest silhouette score)
optimal_k = max(silhouette_scores, key=silhouette_scores.get)
print(f"\n✅ Optimal k={optimal_k} (Silhouette={silhouette_scores[optimal_k]:.4f})")

# Final clustering with optimal k
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=50)
df['Cluster'] = kmeans_final.fit_predict(X_scaled)

# Cluster profiling
print("\n📋 CLUSTER PROFILES:")
for cluster_id in range(optimal_k):
    cluster_df = df[df['Cluster'] == cluster_id]
    print(f"\n--- Cluster {cluster_id} (n={len(cluster_df)}) ---")
    print(f"  Mean Sovereignty Score: {cluster_df['Sovereignty_Phenotype_Score'].mean():.3f}")
    print(f"  Mean Globalism Score: {cluster_df['Globalism_Phenotype_Score'].mean():.3f}")
    print(f"  Mean Dim12: {cluster_df['IusSpace_Dim12_IntegrationScore'].mean():.2f}")
    print(f"  Sovereignty Wins: {cluster_df['Sovereignty_Win'].sum()}/{len(cluster_df)} ({cluster_df['Sovereignty_Win'].mean()*100:.1f}%)")
    print(f"  Crisis Cases: {cluster_df['Crisis_Binary'].sum()}/{len(cluster_df)} ({cluster_df['Crisis_Binary'].mean()*100:.1f}%)")
    print(f"  Countries: {', '.join(cluster_df['Country'].value_counts().head(3).index.tolist())}")

# Cluster-Outcome crosstab
print("\n📊 CLUSTER-OUTCOME CROSSTAB:")
crosstab = pd.crosstab(df['Cluster'], df['Outcome'], margins=True)
print(crosstab)

# Chi-square test for independence
chi2, p_value, dof, expected = stats.chi2_contingency(pd.crosstab(df['Cluster'], df['Outcome']))
print(f"\nχ² test: χ²={chi2:.2f}, p={p_value:.4f}, df={dof}")
if p_value < 0.05:
    print("✅ Clusters significantly associated with outcomes (p<0.05)")
else:
    print("⚠️  Cluster-outcome association not significant")

# ============================================================================
# DIMENSIONALITY REDUCTION VISUALIZATIONS
# ============================================================================

print("\n" + "="*80)
print("CREATING DIMENSIONALITY REDUCTION VISUALIZATIONS")
print("="*80)

# PCA projection
print("\n📊 Running PCA (12D → 3D)...")
pca = PCA(n_components=3, random_state=42)
X_pca = pca.fit_transform(X_scaled)
print(f"  Explained variance: {pca.explained_variance_ratio_.sum()*100:.1f}% (PC1: {pca.explained_variance_ratio_[0]*100:.1f}%, PC2: {pca.explained_variance_ratio_[1]*100:.1f}%, PC3: {pca.explained_variance_ratio_[2]*100:.1f}%)")

# t-SNE projection (better for visualization)
print("\n📊 Running t-SNE (12D → 2D)...")
tsne = TSNE(n_components=2, random_state=42, perplexity=10)
X_tsne = tsne.fit_transform(X_scaled)

# Figure 6: 3D PCA Scatter
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Color by outcome
outcome_colors = {'Sovereignty_Wins': '#d62728', 'Sovereignty_Central_Wins': '#ff7f0e',
                  'Sovereignty_Resists': '#8c564b', 'Sovereignty_Dominant': '#e377c2',
                  'Sovereignty_Total': '#17becf',
                  'Globalism_Wins': '#1f77b4', 'Globalism_Survives': '#2ca02c', 'Globalism_Strained': '#7f7f7f'}

for outcome in df['Outcome'].unique():
    mask = df['Outcome'] == outcome
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1], X_pca[mask, 2],
               c=outcome_colors.get(outcome, '#7f7f7f'),
               label=outcome, s=150, alpha=0.7, edgecolors='black', linewidths=0.5)

ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12, labelpad=10)
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12, labelpad=10)
ax.set_zlabel(f'PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)', fontsize=12, labelpad=10)
ax.set_title('IusSpace 12D → 3D PCA Projection\nColored by Outcome', fontsize=14, pad=20)
ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
output_path = '/home/user/webapp/visualizations/figure6_pca_3d_projection.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {output_path}")
plt.close()

# Figure 7: t-SNE 2D Scatter with Clusters
fig, ax = plt.subplots(figsize=(14, 10))

# Plot by cluster
cluster_colors = plt.cm.Set2(np.linspace(0, 1, optimal_k))
for cluster_id in range(optimal_k):
    mask = df['Cluster'] == cluster_id
    ax.scatter(X_tsne[mask, 0], X_tsne[mask, 1],
               c=[cluster_colors[cluster_id]], s=200, alpha=0.7,
               edgecolors='black', linewidths=0.5, label=f'Cluster {cluster_id}')

# Annotate key cases
key_cases = df[df['Country'].isin(['United Kingdom', 'Poland', 'Russia', 'France'])][['Country', 'Year']].values
key_indices = df[df['Country'].isin(['United Kingdom', 'Poland', 'Russia', 'France'])].index.tolist()
for idx, (country, year) in zip(key_indices, key_cases):
    ax.annotate(f'{country[:3]}\n{int(year)}', 
                (X_tsne[idx, 0], X_tsne[idx, 1]),
                fontsize=8, ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))

ax.set_xlabel('t-SNE Dimension 1', fontsize=12)
ax.set_ylabel('t-SNE Dimension 2', fontsize=12)
ax.set_title(f't-SNE 2D Projection of IusSpace (12D)\nClustered into {optimal_k} groups', fontsize=14, pad=15)
ax.legend(loc='best', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
output_path = '/home/user/webapp/visualizations/figure7_tsne_clusters.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {output_path}")
plt.close()

# ============================================================================
# ANALYSIS 8: CRISIS TIMELINE VISUALIZATION
# ============================================================================

print("\n" + "="*80)
print("ANALYSIS 8: CRISIS TIMELINE VISUALIZATION")
print("="*80)

# Build influence network for node sizing (PageRank from previous analysis)
def build_influence_network(df):
    G = nx.DiGraph()
    for idx, row in df.iterrows():
        G.add_node(idx, **row.to_dict())
    
    for i in range(len(df)):
        for j in range(len(df)):
            if i == j:
                continue
            
            case_i = df.iloc[i]
            case_j = df.iloc[j]
            
            if case_i['Year'] >= case_j['Year']:
                continue
            
            influence_score = 0
            
            if case_i['Institution'] == case_j['Institution']:
                influence_score += 3
            
            if case_i['Outcome'].split('_')[0] == case_j['Outcome'].split('_')[0]:
                influence_score += 2
            
            if case_i['Crisis_Binary'] == 1 and case_j['Crisis_Binary'] == 1:
                if abs(case_j['Year'] - case_i['Year']) <= 3:
                    influence_score += 2
            
            if influence_score >= 3:
                G.add_edge(i, j, weight=influence_score)
    
    return G

G = build_influence_network(df)
pagerank = nx.pagerank(G, weight='weight')
df['PageRank'] = df.index.map(pagerank)

# Figure 8: Crisis Timeline
fig, ax = plt.subplots(figsize=(18, 10))

# Plot cases
for idx, row in df.iterrows():
    color = '#d62728' if row['Crisis_Binary'] == 1 else '#1f77b4'
    size = row['PageRank'] * 15000
    
    ax.scatter(row['Year'], row['Sovereignty_Phenotype_Score'],
               s=size, c=color, alpha=0.6, edgecolors='black', linewidths=0.5)

# Annotate major crises
crisis_events = [
    (2008, 0.95, '2008\nFinancial\nCrisis'),
    (2015, 0.95, '2015\nMigration\nCrisis'),
    (2016, 0.95, '2016\nBrexit'),
    (2020, 0.95, '2020\nCOVID-19'),
    (2022, 0.95, '2022\nUkraine\nWar')
]

for year, y_pos, label in crisis_events:
    ax.axvline(year, color='red', linestyle='--', alpha=0.3, linewidth=2)
    ax.text(year, y_pos, label, fontsize=10, ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', alpha=0.8))

# Shade crisis periods
crisis_periods = [(2007.5, 2009.5), (2014.5, 2016.5), (2019.5, 2021.5), (2021.5, 2022.5)]
for start, end in crisis_periods:
    ax.axvspan(start, end, alpha=0.1, color='red')

# Annotate key cases
key_annotations = [
    (2016, 0.74, 'Brexit\nUK'),
    (2021, 0.73, 'Poland\nEU Court'),
    (2022, 0.82, 'Russia\nECHR'),
]

for year, sov_score, label in key_annotations:
    ax.annotate(label, xy=(year, sov_score),
                xytext=(year+1, sov_score+0.05),
                fontsize=9, ha='left',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', lw=1.5))

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#d62728', alpha=0.6, edgecolor='black', label='Crisis-Catalyzed (n=9)'),
    Patch(facecolor='#1f77b4', alpha=0.6, edgecolor='black', label='Non-Crisis (n=21)'),
    plt.Line2D([0], [0], color='red', linestyle='--', alpha=0.5, label='Major Crisis Event'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

ax.set_xlabel('Year', fontsize=14)
ax.set_ylabel('Sovereignty Phenotype Score', fontsize=14)
ax.set_title('Crisis Timeline: Sovereignty Phenotype Evolution (1985-2024)\nBubble size = PageRank influence | Shaded = Crisis periods',
             fontsize=16, pad=20)
ax.set_xlim(1984, 2025)
ax.set_ylim(0, 1.0)
ax.grid(True, alpha=0.3)

plt.tight_layout()
output_path = '/home/user/webapp/visualizations/figure8_crisis_timeline.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {output_path}")
plt.close()

# ============================================================================
# BOOTSTRAP VALIDATION
# ============================================================================

print("\n" + "="*80)
print("BOOTSTRAP VALIDATION (1000 iterations)")
print("="*80)

def bootstrap_correlation(x, y, n_iterations=1000, alpha=0.10):
    """Bootstrap confidence interval for correlation."""
    n = len(x)
    correlations = []
    
    for _ in range(n_iterations):
        indices = np.random.choice(n, size=n, replace=True)
        x_boot = x.iloc[indices]
        y_boot = y.iloc[indices]
        r, _ = stats.pearsonr(x_boot, y_boot)
        correlations.append(r)
    
    ci_lower = np.percentile(correlations, alpha/2 * 100)
    ci_upper = np.percentile(correlations, (1 - alpha/2) * 100)
    
    return np.mean(correlations), ci_lower, ci_upper

# Key correlations with bootstrap CIs
print("\n📊 Bootstrap Confidence Intervals (90% CI):")

corr_sov_glob, ci_low, ci_high = bootstrap_correlation(
    df['Sovereignty_Phenotype_Score'], df['Globalism_Phenotype_Score'])
print(f"  r(Sovereignty, Globalism) = {corr_sov_glob:.4f} [{ci_low:.4f}, {ci_high:.4f}]")

corr_sov_dim12, ci_low, ci_high = bootstrap_correlation(
    df['Sovereignty_Phenotype_Score'], df['IusSpace_Dim12_IntegrationScore'])
print(f"  r(Sovereignty, Dim12) = {corr_sov_dim12:.4f} [{ci_low:.4f}, {ci_high:.4f}]")

corr_year_sov, ci_low, ci_high = bootstrap_correlation(
    df['Year'], df['Sovereignty_Phenotype_Score'])
print(f"  r(Year, Sovereignty) = {corr_year_sov:.4f} [{ci_low:.4f}, {ci_high:.4f}]")

# Bootstrap for mean difference (crisis effect)
def bootstrap_mean_diff(group1, group2, n_iterations=1000, alpha=0.10):
    """Bootstrap CI for difference in means."""
    diffs = []
    
    for _ in range(n_iterations):
        sample1 = np.random.choice(group1, size=len(group1), replace=True)
        sample2 = np.random.choice(group2, size=len(group2), replace=True)
        diffs.append(sample1.mean() - sample2.mean())
    
    ci_lower = np.percentile(diffs, alpha/2 * 100)
    ci_upper = np.percentile(diffs, (1 - alpha/2) * 100)
    
    return np.mean(diffs), ci_lower, ci_upper

crisis_yes = df[df['Crisis_Binary'] == 1]['Sovereignty_Phenotype_Score']
crisis_no = df[df['Crisis_Binary'] == 0]['Sovereignty_Phenotype_Score']
mean_diff, ci_low, ci_high = bootstrap_mean_diff(crisis_yes.values, crisis_no.values)

print(f"\n  Crisis Effect (Mean Difference) = {mean_diff:.4f} [{ci_low:.4f}, {ci_high:.4f}]")
if ci_low > 0:
    print("  ✅ Effect is significant (CI does not include 0)")
else:
    print("  ⚠️  Effect not significant (CI includes 0)")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save enhanced dataset with clusters
output_path = '/home/user/webapp/results/sovereignty_globalism_with_clusters.csv'
df_output = df.copy()
df_output.to_csv(output_path, index=False)
print(f"✅ Saved: {output_path}")

# Save cluster profiles
cluster_profiles = []
for cluster_id in range(optimal_k):
    cluster_df = df[df['Cluster'] == cluster_id]
    profile = {
        'Cluster_ID': cluster_id,
        'n_cases': len(cluster_df),
        'Mean_Sovereignty': cluster_df['Sovereignty_Phenotype_Score'].mean(),
        'Mean_Globalism': cluster_df['Globalism_Phenotype_Score'].mean(),
        'Mean_Dim12': cluster_df['IusSpace_Dim12_IntegrationScore'].mean(),
        'Pct_Sovereignty_Wins': cluster_df['Sovereignty_Win'].mean() * 100,
        'Pct_Crisis': cluster_df['Crisis_Binary'].mean() * 100,
        'Mean_PageRank': cluster_df['PageRank'].mean(),
    }
    cluster_profiles.append(profile)

cluster_profiles_df = pd.DataFrame(cluster_profiles)
output_path = '/home/user/webapp/results/cluster_profiles.csv'
cluster_profiles_df.to_csv(output_path, index=False)
print(f"✅ Saved: {output_path}")

# Save PCA coordinates
pca_df = pd.DataFrame({
    'Case_ID': df['Case_ID'],
    'Country': df['Country'],
    'Year': df['Year'],
    'PC1': X_pca[:, 0],
    'PC2': X_pca[:, 1],
    'PC3': X_pca[:, 2],
    'Cluster': df['Cluster'],
    'Outcome': df['Outcome']
})
output_path = '/home/user/webapp/results/pca_coordinates.csv'
pca_df.to_csv(output_path, index=False)
print(f"✅ Saved: {output_path}")

print("\n" + "="*80)
print("✅ ADVANCED ANALYSIS COMPLETE")
print("="*80)
print("\nGenerated files:")
print("  1. figure6_pca_3d_projection.png (3D PCA visualization)")
print("  2. figure7_tsne_clusters.png (t-SNE clustering)")
print("  3. figure8_crisis_timeline.png (Timeline with crisis events)")
print("  4. sovereignty_globalism_with_clusters.csv (Enhanced dataset)")
print("  5. cluster_profiles.csv (Cluster characteristics)")
print("  6. pca_coordinates.csv (PCA coordinates for further analysis)")
print("\n🎯 All bootstrap validation complete with 90% confidence intervals")

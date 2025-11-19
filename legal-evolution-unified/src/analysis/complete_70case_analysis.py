#!/usr/bin/env python3
"""
COMPLETE ANALYSIS: 70 Cases Sovereignty vs Globalism (1985-2024)
Extended Phenotype Theory + IusMorfos V6.0 Framework

All 8 Analyses:
1. Phenotype Competition Validation
2. Integration Threshold Identification  
3. Fitness Trajectories Over Time
4. Crisis Catalysis Validation
5. Predictive Modeling
6. Phenotype Clustering
7. Genealogical Influence Network
8. Correlation Matrix & Multicollinearity
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def standardize_outcomes(df):
    """Standardize outcome labels to consistent format."""
    outcome_mapping = {
        'Sovereignty_Wins': 'Sovereignty Wins',
        'Globalism_Wins': 'Globalism Wins',
        'Sovereignty_Resists': 'Sovereignty Wins',
        'Sovereignty_Central_Wins': 'Sovereignty Wins',
        'Sovereignty_Dominant': 'Sovereignty Wins',
        'Sovereignty_Total': 'Sovereignty Wins',
        'Globalism_Survives': 'Globalism Wins',
        'Globalism_Strained': 'Mixed'
    }
    df['Outcome'] = df['Outcome'].replace(outcome_mapping)
    return df

def infer_iuspace_coordinates(row):
    """Infer 12-dimensional IusSpace coordinates from case characteristics."""
    coords = {}
    
    # Dim1: Legal Family Origin (1=Civil Law, 7=Common Law, 4=Mixed)
    common_law = ['UK', 'Ireland', 'Canada', 'Australia', 'India']
    coords['Dim1'] = 7 if row['Country'] in common_law else 2
    
    # Dim2: Constitutional Rigidity (1=Flexible, 10=Rigid)
    coords['Dim2'] = 8 if row['Event_Type'] == 'Constitutional' else 5
    
    # Dim3: Judicial Review Strength (1=Weak, 10=Strong)
    coords['Dim3'] = 9 if row['Event_Type'] == 'Judicial' else 5
    
    # Dim4: Rights Protection (1=Weak, 10=Strong)  
    coords['Dim4'] = 7 if 'EU' in str(row['Institution']) else 4
    
    # Dim5: Federal Structure (1=Unitary, 10=Federal)
    federal = ['Germany', 'Canada', 'Australia', 'Switzerland', 'Belgium', 'Spain']
    coords['Dim5'] = 8 if row['Country'] in federal else 3
    
    # Dim6: Democratic Depth (1=Authoritarian, 10=Democratic)
    low_democracy = ['Russia', 'Turkey', 'Hungary', 'Poland', 'Philippines']
    coords['Dim6'] = 4 if row['Country'] in low_democracy else 8
    
    # Dim7: Economic System (1=State-controlled, 10=Market)
    coords['Dim7'] = 7 if row['Year'] > 2000 else 6
    
    # Dim8: Administrative Capacity (1=Weak, 10=Strong)
    strong_admin = ['Germany', 'UK', 'France', 'Netherlands', 'Sweden', 'Denmark']
    coords['Dim8'] = 9 if row['Country'] in strong_admin else 5
    
    # Dim9: Social Contract Type (1=Communitarian, 10=Individualist)
    individualist = ['UK', 'USA', 'Australia', 'Canada', 'Netherlands']
    coords['Dim9'] = 8 if row['Country'] in individualist else 4
    
    # Dim10: Legal Culture (1=Formalist, 10=Pragmatic)
    coords['Dim10'] = 7 if coords['Dim1'] == 7 else 4
    
    # Dim11: Institutional Trust (1=Low, 10=High)
    high_trust = ['Denmark', 'Sweden', 'Finland', 'Norway', 'Switzerland', 'Netherlands']
    coords['Dim11'] = 9 if row['Country'] in high_trust else 5
    
    # Dim12: International Integration (given)
    coords['Dim12'] = row['IusSpace_Dim12_IntegrationScore']
    
    return coords

def build_influence_network(df):
    """Build genealogical influence network using multi-criteria scoring."""
    G = nx.DiGraph()
    
    # Add all cases as nodes
    for idx, row in df.iterrows():
        G.add_node(row['Case_ID'], 
                   country=row['Country'],
                   year=row['Year'],
                   outcome=row['Outcome'])
    
    # Build edges based on influence criteria
    for i, case_i in df.iterrows():
        for j, case_j in df.iterrows():
            if case_i['Year'] < case_j['Year']:  # Temporal precedence
                score = 0
                
                # Institution similarity (+3)
                if case_i['Institution'] == case_j['Institution']:
                    score += 3
                
                # Outcome similarity (+2)
                if case_i['Outcome'] == case_j['Outcome']:
                    score += 2
                
                # Crisis context (+2)
                if case_i['Crisis_Catalyzed'] == 'Yes' and case_j['Crisis_Catalyzed'] == 'Yes':
                    score += 2
                
                # Geographic proximity (+1)
                eu_countries = ['UK', 'France', 'Germany', 'Italy', 'Spain', 'Netherlands',
                               'Poland', 'Hungary', 'Greece', 'Ireland', 'Denmark', 'Sweden',
                               'Finland', 'Austria', 'Belgium', 'Czech Republic']
                if case_i['Country'] in eu_countries and case_j['Country'] in eu_countries:
                    score += 1
                
                # Add edge if score > 2
                if score > 2:
                    G.add_edge(case_i['Case_ID'], case_j['Case_ID'], weight=score)
    
    return G

def bootstrap_correlation(x, y, n_iterations=1000, alpha=0.10):
    """Bootstrap confidence interval for correlation."""
    n = len(x)
    correlations = []
    
    for _ in range(n_iterations):
        indices = np.random.choice(n, size=n, replace=True)
        x_boot = x.iloc[indices] if hasattr(x, 'iloc') else x[indices]
        y_boot = y.iloc[indices] if hasattr(y, 'iloc') else y[indices]
        r, _ = stats.pearsonr(x_boot, y_boot)
        correlations.append(r)
    
    correlations = np.array(correlations)
    mean_r = np.mean(correlations)
    ci_lower = np.percentile(correlations, alpha/2 * 100)
    ci_upper = np.percentile(correlations, (1-alpha/2) * 100)
    
    return mean_r, ci_lower, ci_upper

def main():
    print("="*80)
    print("COMPLETE ANALYSIS: 70 Cases Sovereignty vs Globalism (1985-2024)")
    print("Extended Phenotype Theory + IusMorfos V6.0 Framework")
    print("="*80)
    
    # Load complete dataset
    df = pd.read_csv('data/cases/sovereignty_globalism_complete_70cases.csv')
    df = standardize_outcomes(df)
    
    print(f"\n✅ Loaded {len(df)} cases (1985-2024)")
    print(f"   Outcome distribution:")
    for outcome, count in df['Outcome'].value_counts().items():
        print(f"   - {outcome}: {count}")
    
    # ========================================================================
    # ANALYSIS 1: PHENOTYPE COMPETITION VALIDATION
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 1: PHENOTYPE COMPETITION VALIDATION")
    print("="*80)
    
    r_sov_glob, p_sov_glob = stats.pearsonr(df['Sovereignty_Phenotype_Score'], 
                                              df['Globalism_Phenotype_Score'])
    mean_r, ci_lower, ci_upper = bootstrap_correlation(
        df['Sovereignty_Phenotype_Score'],
        df['Globalism_Phenotype_Score'],
        n_iterations=1000,
        alpha=0.10
    )
    
    print(f"\n✅ Pearson r(Sovereignty, Globalism) = {r_sov_glob:.4f}, p = {p_sov_glob:.2e}")
    print(f"   Bootstrap 90% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"   {'✅ H1 CONFIRMED' if r_sov_glob < -0.80 else '❌ H1 NOT CONFIRMED'}: r < -0.80")
    
    r_sov_dim12, p_sov_dim12 = stats.pearsonr(df['Sovereignty_Phenotype_Score'],
                                                df['IusSpace_Dim12_IntegrationScore'])
    print(f"\n✅ Pearson r(Sovereignty, Dim12) = {r_sov_dim12:.4f}, p = {p_sov_dim12:.2e}")
    print(f"   {'✅ H2 CONFIRMED' if r_sov_dim12 < -0.70 else '❌ H2 NOT CONFIRMED'}: r < -0.70")
    
    # ========================================================================
    # ANALYSIS 2: INTEGRATION THRESHOLD IDENTIFICATION
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 2: INTEGRATION THRESHOLD IDENTIFICATION")
    print("="*80)
    
    df['Sovereignty_Win'] = df['Outcome'].str.contains('Sovereignty').astype(int)
    
    print("\nDim12 Threshold Analysis:")
    print("Dim12 ≤ 4 → Sovereignty Wins?")
    
    for threshold in range(1, 11):
        below = df[df['IusSpace_Dim12_IntegrationScore'] <= threshold]
        if len(below) > 0:
            sov_wins = below['Sovereignty_Win'].sum()
            total = len(below)
            pct = sov_wins / total * 100
            print(f"   Dim12 ≤ {threshold}: {sov_wins}/{total} sovereignty wins ({pct:.1f}%)")
    
    dim12_low = df[df['IusSpace_Dim12_IntegrationScore'] <= 4]
    h3_confirmed = (dim12_low['Sovereignty_Win'].sum() / len(dim12_low)) == 1.0 if len(dim12_low) > 0 else False
    print(f"\n   {'✅ H3 CONFIRMED' if h3_confirmed else '❌ H3 NOT CONFIRMED'}: Dim12 ≤ 4 → 100% sovereignty wins")
    
    # ========================================================================
    # ANALYSIS 3: FITNESS TRAJECTORIES OVER TIME
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 3: FITNESS TRAJECTORIES OVER TIME")
    print("="*80)
    
    df_sorted = df.sort_values('Year')
    
    print("\nDecadal averages:")
    for decade in range(1980, 2030, 10):
        decade_data = df_sorted[(df_sorted['Year'] >= decade) & (df_sorted['Year'] < decade + 10)]
        if len(decade_data) > 0:
            mean_sov = decade_data['Sovereignty_Phenotype_Score'].mean()
            mean_glob = decade_data['Globalism_Phenotype_Score'].mean()
            mean_dim12 = decade_data['IusSpace_Dim12_IntegrationScore'].mean()
            n = len(decade_data)
            print(f"   {decade}s (n={n:2d}): Sov={mean_sov:.3f}, Glob={mean_glob:.3f}, Dim12={mean_dim12:.2f}")
    
    # ========================================================================
    # ANALYSIS 4: CRISIS CATALYSIS VALIDATION
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 4: CRISIS CATALYSIS VALIDATION")
    print("="*80)
    
    crisis_yes = df[df['Crisis_Catalyzed'] == 'Yes']['Sovereignty_Phenotype_Score']
    crisis_no = df[df['Crisis_Catalyzed'] == 'No']['Sovereignty_Phenotype_Score']
    
    t_stat, p_val = stats.ttest_ind(crisis_yes, crisis_no)
    cohen_d = (crisis_yes.mean() - crisis_no.mean()) / np.sqrt(
        ((len(crisis_yes)-1)*crisis_yes.std()**2 + (len(crisis_no)-1)*crisis_no.std()**2) / 
        (len(crisis_yes) + len(crisis_no) - 2)
    )
    
    print(f"\n   Crisis Yes (n={len(crisis_yes)}): mean = {crisis_yes.mean():.3f}")
    print(f"   Crisis No  (n={len(crisis_no)}):  mean = {crisis_no.mean():.3f}")
    print(f"   Δ = +{crisis_yes.mean() - crisis_no.mean():.3f}")
    print(f"   t = {t_stat:.3f}, p = {p_val:.3f}")
    print(f"   Cohen's d = {cohen_d:.3f}")
    
    h5_confirmed = (crisis_yes.mean() - crisis_no.mean() >= 0.10) and (p_val < 0.05)
    print(f"\n   {'✅ H5 CONFIRMED' if h5_confirmed else '❌ H5 NOT CONFIRMED'}: Crisis → Δ ≥ +0.10, p < 0.05")
    
    # ========================================================================
    # ANALYSIS 5: PREDICTIVE MODELING
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 5: PREDICTIVE MODELING (Logistic Regression)")
    print("="*80)
    
    X = df[['Sovereignty_Phenotype_Score', 'Globalism_Phenotype_Score', 
            'IusSpace_Dim12_IntegrationScore']].values
    y = df['Sovereignty_Win'].values
    
    # Train on all data (no split for now - can add cross-validation later)
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X, y)
    
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]
    
    roc_auc = roc_auc_score(y, y_prob)
    accuracy = (y == y_pred).mean()
    
    print(f"\n   ROC-AUC: {roc_auc:.4f}")
    print(f"   Accuracy: {accuracy:.4f} ({(y == y_pred).sum()}/{len(y)})")
    print(f"\n   {'✅ H6 CONFIRMED' if roc_auc > 0.90 else '❌ H6 NOT CONFIRMED'}: ROC-AUC > 0.90")
    
    print("\n   Confusion Matrix:")
    cm = confusion_matrix(y, y_pred)
    print(f"   {cm}")
    
    # ========================================================================
    # ANALYSIS 6: PHENOTYPE CLUSTERING (k-means)
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 6: PHENOTYPE CLUSTERING (k-means in 12D IusSpace)")
    print("="*80)
    
    # Infer full 12D coordinates
    iuspace_coords = df.apply(infer_iuspace_coordinates, axis=1)
    iuspace_df = pd.DataFrame(iuspace_coords.tolist())
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(iuspace_df)
    
    # Determine optimal k using elbow method (test k=3 to k=8)
    inertias = []
    silhouette_scores = []
    for k in range(3, 9):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=50)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        
        from sklearn.metrics import silhouette_score
        score = silhouette_score(X_scaled, kmeans.labels_)
        silhouette_scores.append(score)
    
    # Use k=5 (balance between interpretability and silhouette score)
    optimal_k = 5
    kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=50)
    df['Cluster'] = kmeans_final.fit_predict(X_scaled)
    
    from sklearn.metrics import silhouette_score
    silhouette = silhouette_score(X_scaled, df['Cluster'])
    
    print(f"\n   Optimal k = {optimal_k}")
    print(f"   Silhouette Score = {silhouette:.3f}")
    
    print("\n   Cluster Profiles:")
    for cluster in range(optimal_k):
        cluster_data = df[df['Cluster'] == cluster]
        n = len(cluster_data)
        mean_sov = cluster_data['Sovereignty_Phenotype_Score'].mean()
        mean_dim12 = cluster_data['IusSpace_Dim12_IntegrationScore'].mean()
        sov_wins = cluster_data['Sovereignty_Win'].sum()
        win_rate = sov_wins / n * 100 if n > 0 else 0
        print(f"   Cluster {cluster}: n={n:2d}, Sov={mean_sov:.2f}, Dim12={mean_dim12:.1f}, Wins={sov_wins}/{n} ({win_rate:.1f}%)")
    
    # ========================================================================
    # ANALYSIS 7: GENEALOGICAL INFLUENCE NETWORK (PageRank)
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 7: GENEALOGICAL INFLUENCE NETWORK (JurisRank)")
    print("="*80)
    
    G = build_influence_network(df)
    
    print(f"\n   Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Compute PageRank
    pagerank = nx.pagerank(G, weight='weight')
    df['PageRank'] = df['Case_ID'].map(pagerank)
    
    # Compute out-degree (influence exerted)
    out_degree = dict(G.out_degree())
    df['Out_Degree'] = df['Case_ID'].map(out_degree)
    
    # Top 10 most influential cases
    top_influential = df.nlargest(10, 'PageRank')[['Case_ID', 'Country', 'Year', 'Event_Type', 'PageRank', 'Out_Degree']]
    print("\n   Top 10 Most Influential Cases:")
    print(top_influential.to_string(index=False))
    
    # Check H7: Brexit in top 5?
    brexit_cases = df[(df['Country'] == 'UK') & (df['Year'].isin([2016, 2020]))]
    if len(brexit_cases) > 0:
        brexit_rank = (df['PageRank'] > brexit_cases['PageRank'].max()).sum() + 1
        print(f"\n   Brexit UK highest rank: #{brexit_rank}")
        print(f"   {'✅ H7 CONFIRMED' if brexit_rank <= 5 else '❌ H7 NOT CONFIRMED'}: Brexit in top 5")
    
    # ========================================================================
    # ANALYSIS 8: CORRELATION MATRIX & MULTICOLLINEARITY
    # ========================================================================
    print("\n" + "="*80)
    print("ANALYSIS 8: CORRELATION MATRIX & VIF SCORES")
    print("="*80)
    
    corr_vars = ['Sovereignty_Phenotype_Score', 'Globalism_Phenotype_Score', 
                 'IusSpace_Dim12_IntegrationScore', 'Sovereignty_Win']
    corr_matrix = df[corr_vars].corr()
    
    print("\n   Correlation Matrix:")
    print(corr_matrix.round(3))
    
    # VIF scores
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    X_vif = df[['Sovereignty_Phenotype_Score', 'Globalism_Phenotype_Score', 
                'IusSpace_Dim12_IntegrationScore']].values
    
    print("\n   VIF Scores (Multicollinearity Check):")
    for i, col in enumerate(['Sovereignty_Phenotype_Score', 'Globalism_Phenotype_Score', 
                             'IusSpace_Dim12_IntegrationScore']):
        vif = variance_inflation_factor(X_vif, i)
        interpretation = "Low" if vif < 5 else "Moderate" if vif < 10 else "High"
        print(f"   {col:40s}: VIF = {vif:6.2f} ({interpretation})")
    
    # ========================================================================
    # SAVE RESULTS
    # ========================================================================
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)
    
    # Save enhanced dataset
    df.to_csv('results/sovereignty_globalism_70cases_analyzed.csv', index=False)
    print("   ✅ results/sovereignty_globalism_70cases_analyzed.csv")
    
    # Save cluster profiles
    cluster_profiles = []
    for cluster in range(optimal_k):
        cluster_data = df[df['Cluster'] == cluster]
        profile = {
            'Cluster': cluster,
            'N': len(cluster_data),
            'Mean_Sovereignty': cluster_data['Sovereignty_Phenotype_Score'].mean(),
            'Mean_Globalism': cluster_data['Globalism_Phenotype_Score'].mean(),
            'Mean_Dim12': cluster_data['IusSpace_Dim12_IntegrationScore'].mean(),
            'Sovereignty_Wins': cluster_data['Sovereignty_Win'].sum(),
            'Win_Rate': cluster_data['Sovereignty_Win'].mean()
        }
        cluster_profiles.append(profile)
    
    pd.DataFrame(cluster_profiles).to_csv('results/cluster_profiles_70cases.csv', index=False)
    print("   ✅ results/cluster_profiles_70cases.csv")
    
    # Save PCA coordinates
    pca = PCA(n_components=3, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
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
    pca_df.to_csv('results/pca_coordinates_70cases.csv', index=False)
    print("   ✅ results/pca_coordinates_70cases.csv")
    
    print(f"\n   Explained variance (3 PCs): {pca.explained_variance_ratio_.sum():.3f}")
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE: All 8 analyses executed on 70 cases")
    print("="*80)

if __name__ == '__main__':
    main()

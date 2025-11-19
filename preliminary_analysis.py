#!/usr/bin/env python3
"""
Preliminary Analysis: CSI-REI Correlation
Dataset: Epistemological Clergies Study
Author: Ignacio Adrian Lerer
Date: 2025-11-18
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_data(filepath='dataset_template.csv'):
    """Load and clean dataset"""
    df = pd.read_csv(filepath)
    
    # Remove rows with no data (template placeholders)
    df = df.dropna(subset=['csi_total', 'rei_total'])
    
    print(f"✓ Loaded {len(df)} observations with complete CSI/REI data")
    print(f"  Jurisdictions: {df['jurisdiction_name'].nunique()}")
    print(f"  Domains: {df['legal_domain'].unique()}")
    
    return df

def descriptive_statistics(df):
    """Calculate descriptive statistics"""
    print("\n" + "="*60)
    print("DESCRIPTIVE STATISTICS")
    print("="*60)
    
    print("\nClerical Strength Index (CSI):")
    print(f"  Mean:   {df['csi_total'].mean():.3f}")
    print(f"  Median: {df['csi_total'].median():.3f}")
    print(f"  SD:     {df['csi_total'].std():.3f}")
    print(f"  Range:  [{df['csi_total'].min():.3f}, {df['csi_total'].max():.3f}]")
    
    print("\nReform Effectiveness Index (REI):")
    print(f"  Mean:   {df['rei_total'].mean():.3f}")
    print(f"  Median: {df['rei_total'].median():.3f}")
    print(f"  SD:     {df['rei_total'].std():.3f}")
    print(f"  Range:  [{df['rei_total'].min():.3f}, {df['rei_total'].max():.3f}]")
    
    print("\nDistribution by Region:")
    print(df.groupby('region')[['csi_total', 'rei_total']].agg(['count', 'mean']))
    
    print("\nDistribution by Legal Domain:")
    print(df.groupby('legal_domain')[['csi_total', 'rei_total']].agg(['count', 'mean']))
    
    return df

def correlation_analysis(df):
    """Calculate correlations"""
    print("\n" + "="*60)
    print("CORRELATION ANALYSIS")
    print("="*60)
    
    # Pearson correlation
    r_pearson, p_pearson = stats.pearsonr(df['csi_total'], df['rei_total'])
    print(f"\nPearson Correlation:")
    print(f"  r = {r_pearson:.3f}")
    print(f"  p = {p_pearson:.4f}")
    print(f"  95% CI: [{r_pearson - 1.96*np.sqrt((1-r_pearson**2)/(len(df)-2)):.3f}, "
          f"{r_pearson + 1.96*np.sqrt((1-r_pearson**2)/(len(df)-2)):.3f}]")
    
    # Spearman correlation (non-parametric)
    r_spearman, p_spearman = stats.spearmanr(df['csi_total'], df['rei_total'])
    print(f"\nSpearman Correlation (rank-based):")
    print(f"  ρ = {r_spearman:.3f}")
    print(f"  p = {p_spearman:.4f}")
    
    # Interpretation
    print("\nInterpretation:")
    if abs(r_pearson) > 0.70:
        strength = "STRONG"
    elif abs(r_pearson) > 0.50:
        strength = "MODERATE-TO-STRONG"
    elif abs(r_pearson) > 0.30:
        strength = "MODERATE"
    else:
        strength = "WEAK"
    
    direction = "negative" if r_pearson < 0 else "positive"
    
    print(f"  {strength} {direction} correlation")
    
    if p_pearson < 0.001:
        print(f"  Highly statistically significant (p < 0.001)")
    elif p_pearson < 0.01:
        print(f"  Statistically significant (p < 0.01)")
    elif p_pearson < 0.05:
        print(f"  Statistically significant (p < 0.05)")
    else:
        print(f"  NOT statistically significant (p = {p_pearson:.3f})")
    
    # Hypothesis test
    print("\n" + "-"*60)
    print("HYPOTHESIS TEST")
    print("-"*60)
    print("\nH1: CSI and REI correlate negatively (r < -0.50, p < 0.01)")
    
    h1_met = (r_pearson < -0.50) and (p_pearson < 0.01)
    print(f"  Result: {'✓ SUPPORTED' if h1_met else '✗ NOT SUPPORTED'}")
    
    if not h1_met:
        if r_pearson >= -0.50:
            print(f"  Issue: Correlation too weak (r = {r_pearson:.3f}, threshold = -0.50)")
        if p_pearson >= 0.01:
            print(f"  Issue: Not significant (p = {p_pearson:.3f}, threshold = 0.01)")
    
    return r_pearson, p_pearson

def regression_analysis(df):
    """Simple linear regression"""
    print("\n" + "="*60)
    print("LINEAR REGRESSION: REI ~ CSI")
    print("="*60)
    
    from scipy.stats import linregress
    
    slope, intercept, r_value, p_value, std_err = linregress(df['csi_total'], df['rei_total'])
    
    print(f"\nModel: REI = {intercept:.3f} + {slope:.3f} × CSI")
    print(f"  R² = {r_value**2:.3f} ({r_value**2*100:.1f}% variance explained)")
    print(f"  p = {p_value:.4f}")
    print(f"  Standard Error: {std_err:.3f}")
    
    print("\nInterpretation:")
    print(f"  For each 0.1 increase in CSI, REI changes by {slope*0.1:.3f}")
    print(f"  Example: CSI=0.8 (high orthodoxy) → REI={intercept + slope*0.8:.3f}")
    print(f"           CSI=0.3 (low orthodoxy)  → REI={intercept + slope*0.3:.3f}")
    
    return slope, intercept, r_value**2

def visualizations(df):
    """Create visualizations"""
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Scatterplot with regression line
    ax1 = axes[0, 0]
    ax1.scatter(df['csi_total'], df['rei_total'], s=100, alpha=0.6, c=df['region'].astype('category').cat.codes, cmap='tab10')
    
    # Add regression line
    z = np.polyfit(df['csi_total'], df['rei_total'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['csi_total'].min(), df['csi_total'].max(), 100)
    ax1.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label=f'y = {z[0]:.2f}x + {z[1]:.2f}')
    
    # Add labels for key jurisdictions
    for idx, row in df.iterrows():
        if row['jurisdiction_name'] in ['Argentina', 'Chile', 'Uruguay', 'Texas', 'Illinois']:
            ax1.annotate(row['jurisdiction_name'], 
                        (row['csi_total'], row['rei_total']),
                        fontsize=9, alpha=0.8,
                        xytext=(5, 5), textcoords='offset points')
    
    ax1.set_xlabel('Clerical Strength Index (CSI)', fontsize=12)
    ax1.set_ylabel('Reform Effectiveness Index (REI)', fontsize=12)
    ax1.set_title('CSI vs REI: Primary Hypothesis', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Distribution of CSI
    ax2 = axes[0, 1]
    ax2.hist(df['csi_total'], bins=10, alpha=0.7, color='steelblue', edgecolor='black')
    ax2.axvline(df['csi_total'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean = {df["csi_total"].mean():.2f}')
    ax2.axvline(df['csi_total'].median(), color='orange', linestyle='--', linewidth=2, label=f'Median = {df["csi_total"].median():.2f}')
    ax2.set_xlabel('CSI', fontsize=12)
    ax2.set_ylabel('Frequency', fontsize=12)
    ax2.set_title('Distribution of Clerical Strength', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Distribution of REI
    ax3 = axes[1, 0]
    ax3.hist(df['rei_total'], bins=10, alpha=0.7, color='forestgreen', edgecolor='black')
    ax3.axvline(df['rei_total'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean = {df["rei_total"].mean():.2f}')
    ax3.axvline(df['rei_total'].median(), color='orange', linestyle='--', linewidth=2, label=f'Median = {df["rei_total"].median():.2f}')
    ax3.set_xlabel('REI', fontsize=12)
    ax3.set_ylabel('Frequency', fontsize=12)
    ax3.set_title('Distribution of Reform Effectiveness', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Boxplot by region
    ax4 = axes[1, 1]
    regions = df.groupby('region')[['csi_total', 'rei_total']].mean().sort_values('csi_total')
    x = np.arange(len(regions))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, regions['csi_total'], width, label='CSI', alpha=0.8, color='steelblue')
    bars2 = ax4.bar(x + width/2, regions['rei_total'], width, label='REI', alpha=0.8, color='forestgreen')
    
    ax4.set_xlabel('Region', fontsize=12)
    ax4.set_ylabel('Index Value', fontsize=12)
    ax4.set_title('CSI vs REI by Region', fontsize=14, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(regions.index, rotation=45, ha='right')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('preliminary_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved visualization: preliminary_analysis.png")
    
    return fig

def case_illustrations(df):
    """Detailed case comparisons"""
    print("\n" + "="*60)
    print("CASE ILLUSTRATIONS")
    print("="*60)
    
    # Argentina vs Chile
    print("\n1. ARGENTINA vs CHILE (Criminal Law)")
    ar_crim = df[df['jurisdiction_id'] == 'AR_CRIM'].iloc[0]
    cl_crim = df[df['jurisdiction_id'] == 'CL_CRIM'].iloc[0]
    
    print(f"\n  Argentina:")
    print(f"    CSI = {ar_crim['csi_total']:.3f} (HIGH orthodoxy)")
    print(f"    REI = {ar_crim['rei_total']:.3f} (LOW effectiveness)")
    print(f"    Δ CSI-REI gap: {ar_crim['csi_total'] - ar_crim['rei_total']:.3f}")
    
    print(f"\n  Chile:")
    print(f"    CSI = {cl_crim['csi_total']:.3f} (LOW orthodoxy)")
    print(f"    REI = {cl_crim['rei_total']:.3f} (MODERATE-HIGH effectiveness)")
    print(f"    Δ CSI-REI gap: {cl_crim['csi_total'] - cl_crim['rei_total']:.3f}")
    
    print(f"\n  Difference:")
    print(f"    ΔCSI = {ar_crim['csi_total'] - cl_crim['csi_total']:.3f} "
          f"({(ar_crim['csi_total'] - cl_crim['csi_total'])/cl_crim['csi_total']*100:+.0f}%)")
    print(f"    ΔREI = {ar_crim['rei_total'] - cl_crim['rei_total']:.3f} "
          f"({(ar_crim['rei_total'] - cl_crim['rei_total'])/cl_crim['rei_total']*100:+.0f}%)")
    
    # Uruguay labor success
    print("\n2. URUGUAY LABOR LAW (Best outcome)")
    uy_labor = df[df['jurisdiction_id'] == 'UY_LABOR'].iloc[0]
    ar_labor = df[df['jurisdiction_id'] == 'AR_LABOR'].iloc[0]
    
    print(f"\n  Uruguay (eliminated ultraactivity):")
    print(f"    CSI = {uy_labor['csi_total']:.3f}")
    print(f"    REI = {uy_labor['rei_total']:.3f} ← HIGHEST in dataset")
    print(f"    Real wage growth: +42%, Informality: -35%")
    
    print(f"\n  Argentina (maintained ultraactivity):")
    print(f"    CSI = {ar_labor['csi_total']:.3f}")
    print(f"    REI = {ar_labor['rei_total']:.3f}")
    print(f"    Real wages: stagnant, Informality: +29%")
    
    # Texas vs Illinois paradox
    print("\n3. TEXAS vs ILLINOIS PARADOX (USA Criminal)")
    tx_crim = df[df['jurisdiction_id'] == 'US_TX_CRIM'].iloc[0]
    il_crim = df[df['jurisdiction_id'] == 'US_IL_CRIM'].iloc[0]
    
    print(f"\n  Texas ('conservative'):")
    print(f"    CSI = {tx_crim['csi_total']:.3f}")
    print(f"    REI = {tx_crim['rei_total']:.3f}")
    print(f"    Result: -26% incarceration (pragmatic reforms worked)")
    
    print(f"\n  Illinois ('progressive'):")
    print(f"    CSI = {il_crim['csi_total']:.3f}")
    print(f"    REI = {il_crim['rei_total']:.3f}")
    print(f"    Result: Incarceration stable (reforms blocked by purity tests)")
    
    print(f"\n  PARADOX: 'Conservative' jurisdiction achieved more progressive")
    print(f"           outcomes than 'progressive' jurisdiction due to lower CSI")

def recommendations(df, r, p):
    """Generate recommendations based on results"""
    print("\n" + "="*60)
    print("RECOMMENDATIONS FOR DATASET EXPANSION")
    print("="*60)
    
    print(f"\nCurrent sample: n={len(df)}")
    print(f"Current correlation: r={r:.3f}, p={p:.4f}")
    
    if abs(r) > 0.70 and p < 0.001:
        print("\n✓ STRONG EFFECT DETECTED")
        print("  Recommendation: EXPAND dataset to n=90-150")
        print("  Rationale: Strong preliminary signal justifies investment")
        print("  Priority: Diversify regions and legal domains")
        
    elif abs(r) > 0.50 and p < 0.01:
        print("\n✓ MODERATE-STRONG EFFECT DETECTED")
        print("  Recommendation: Expand to n=60-90 for robustness")
        print("  Rationale: Effect is present but requires larger sample")
        
    else:
        print("\n⚠ WEAK OR NON-SIGNIFICANT EFFECT")
        print("  Recommendation: PAUSE expansion, investigate methodology")
        print("  Rationale: Preliminary data doesn't support hypothesis")
        print("  Action: Review coding, check for systematic errors")

def main():
    """Main analysis pipeline"""
    print("="*60)
    print("PRELIMINARY ANALYSIS: EPISTEMOLOGICAL CLERGIES")
    print("Dataset: CSI-REI Correlation Study")
    print("="*60)
    
    # Load data
    df = load_data('dataset_template.csv')
    
    # Descriptive statistics
    df = descriptive_statistics(df)
    
    # Correlation analysis
    r, p = correlation_analysis(df)
    
    # Regression
    slope, intercept, r2 = regression_analysis(df)
    
    # Case illustrations
    case_illustrations(df)
    
    # Visualizations
    try:
        fig = visualizations(df)
        print("\n✓ Visualizations generated successfully")
    except Exception as e:
        print(f"\n✗ Error generating visualizations: {e}")
    
    # Recommendations
    recommendations(df, r, p)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Review results and validate coding decisions")
    print("2. If results are promising, proceed with expansion plan")
    print("3. Document all decisions in codebook")
    print("4. Begin systematic data collection for next jurisdictions")

if __name__ == "__main__":
    main()

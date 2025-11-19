#!/usr/bin/env python3
"""
Crystallization Drivers Visualization Module
============================================

Creates 4 types of visualizations for driver analysis:
1. Radar charts - Compare driver profiles across cases
2. Heatmap - Driver correlation matrix
3. Scatter plot - Prediction accuracy (predicted vs observed)
4. Pathway distribution - Bar charts and boxplots by crystallization pathway

Author: GenSpark AI Developer
Version: 1.0.0
Date: 2025-11-04
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Optional
import warnings

warnings.filterwarnings('ignore')

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9


def plot_driver_radar(df: pd.DataFrame, cases: List[str], 
                       output_path: str, title: str = "Driver Profile Comparison"):
    """
    Create radar chart comparing driver profiles across selected cases
    
    Args:
        df: DataFrame with driver scores
        cases: List of case_ids to compare
        output_path: Path to save PNG file
        title: Chart title
    """
    # Filter selected cases
    plot_df = df[df['case_id'].isin(cases)].copy()
    
    if len(plot_df) == 0:
        raise ValueError(f"No cases found matching: {cases}")
    
    # Driver columns
    drivers = ['esri', 'pci', 'rca', 'vpfi', 'eili']
    driver_labels = ['ESRI\n(Economic)', 'PCI\n(Premature\nConst.)', 
                     'RCA\n(Cost\nAsymmetry)', 'VPFI\n(Veto\nPlayers)', 
                     'EILI\n(Identity)']
    
    # Number of variables
    num_vars = len(drivers)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    # Color palette
    colors = sns.color_palette("husl", len(plot_df))
    
    # Plot each case
    for idx, (_, row) in enumerate(plot_df.iterrows()):
        values = [row[d] for d in drivers]
        values += values[:1]  # Complete the circle
        
        label = f"{row['case_id']} ({row['country']})"
        ax.plot(angles, values, 'o-', linewidth=2, label=label, color=colors[idx])
        ax.fill(angles, values, alpha=0.15, color=colors[idx])
    
    # Fix axis to go in the right order
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(driver_labels)
    
    # Set y-axis limits
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
    ax.set_rlabel_position(180)
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add title and legend
    plt.title(title, size=14, weight='bold', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Radar chart saved: {output_path}")


def plot_driver_heatmap(df: pd.DataFrame, output_path: str,
                         title: str = "Driver Correlation Matrix"):
    """
    Create correlation heatmap for drivers and CLI
    
    Args:
        df: DataFrame with driver scores
        output_path: Path to save PNG file
        title: Chart title
    """
    # Select driver columns + CLI
    columns = ['esri', 'pci', 'rca', 'vpfi', 'eili', 'cli_observed']
    labels = ['ESRI', 'PCI', 'RCA', 'VPFI', 'EILI', 'CLI\n(Observed)']
    
    # Calculate correlation matrix
    corr_df = df[columns].corr()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    sns.heatmap(corr_df, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                xticklabels=labels, yticklabels=labels, ax=ax,
                vmin=-1, vmax=1)
    
    # Title
    plt.title(title, size=14, weight='bold', pad=15)
    
    # Rotate labels
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Heatmap saved: {output_path}")


def plot_prediction_scatter(df: pd.DataFrame, output_path: str,
                             title: str = "CLI Prediction Accuracy"):
    """
    Create scatter plot of predicted vs observed CLI with error metrics
    
    Args:
        df: DataFrame with predictions and observations
        output_path: Path to save PNG file
        title: Chart title
    """
    # Filter valid observations
    valid_df = df[df['cli_observed'].notna()].copy()
    
    # Calculate metrics
    mae = valid_df['abs_error'].mean()
    rmse = np.sqrt((valid_df['error'] ** 2).mean())
    
    # Calculate R²
    y_obs = valid_df['cli_observed']
    y_pred = valid_df['cli_predicted']
    ss_res = ((y_obs - y_pred) ** 2).sum()
    ss_tot = ((y_obs - y_obs.mean()) ** 2).sum()
    r2 = 1 - (ss_res / ss_tot)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 9))
    
    # Color by pathway
    pathway_colors = {'economic': '#e74c3c', 'political': '#3498db', 'hybrid': '#95a5a6'}
    
    for pathway in valid_df['pathway'].unique():
        subset = valid_df[valid_df['pathway'] == pathway]
        ax.scatter(subset['cli_observed'], subset['cli_predicted'],
                  s=150, alpha=0.7, edgecolors='black', linewidth=1.5,
                  color=pathway_colors.get(pathway, '#95a5a6'),
                  label=f"{pathway.capitalize()} ({len(subset)} cases)")
    
    # Add case labels
    for _, row in valid_df.iterrows():
        ax.annotate(row['case_id'], 
                   (row['cli_observed'], row['cli_predicted']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8, alpha=0.7)
    
    # Add perfect prediction line
    ax.plot([0, 1], [0, 1], 'k--', linewidth=2, alpha=0.5, label='Perfect Prediction')
    
    # Add ±0.15 error bands
    x_range = np.linspace(0, 1, 100)
    ax.fill_between(x_range, x_range - 0.15, x_range + 0.15,
                     alpha=0.1, color='green', label='±0.15 Error Band')
    
    # Labels and title
    ax.set_xlabel('Observed CLI', fontsize=12, weight='bold')
    ax.set_ylabel('Predicted CLI', fontsize=12, weight='bold')
    ax.set_title(title, fontsize=14, weight='bold', pad=15)
    
    # Set axis limits
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect('equal')
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Add metrics text box
    metrics_text = f'MAE = {mae:.4f}\nRMSE = {rmse:.4f}\nR² = {r2:.4f}\nn = {len(valid_df)}'
    ax.text(0.05, 0.95, metrics_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Legend
    ax.legend(loc='lower right', fontsize=9)
    
    # Save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Scatter plot saved: {output_path}")


def plot_pathway_distribution(df: pd.DataFrame, output_path: str,
                               title: str = "Crystallization Pathways Analysis"):
    """
    Create multi-panel figure showing pathway distributions
    
    Args:
        df: DataFrame with driver scores and pathways
        output_path: Path to save PNG file
        title: Chart title
    """
    # Create figure with subplots (4 rows x 2 cols = 8 subplots for 7 total plots)
    fig = plt.figure(figsize=(14, 14))
    gs = fig.add_gridspec(4, 2, hspace=0.35, wspace=0.3)
    
    # Color palette
    pathway_colors = {'economic': '#e74c3c', 'political': '#3498db', 'hybrid': '#95a5a6'}
    
    # 1. Pathway count bar chart
    ax1 = fig.add_subplot(gs[0, 0])
    pathway_counts = df['pathway'].value_counts()
    bars = ax1.bar(pathway_counts.index, pathway_counts.values,
                   color=[pathway_colors[p] for p in pathway_counts.index],
                   edgecolor='black', linewidth=1.5, alpha=0.7)
    ax1.set_xlabel('Pathway Type', fontsize=10, weight='bold')
    ax1.set_ylabel('Number of Cases', fontsize=10, weight='bold')
    ax1.set_title('Pathway Distribution', fontsize=11, weight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, weight='bold')
    
    # 2. CLI by pathway boxplot
    ax2 = fig.add_subplot(gs[0, 1])
    valid_df = df[df['cli_observed'].notna()].copy()
    pathway_order = ['economic', 'political', 'hybrid']
    present_pathways = [p for p in pathway_order if p in valid_df['pathway'].values]
    
    box_data = [valid_df[valid_df['pathway'] == p]['cli_observed'].values 
                for p in present_pathways]
    bp = ax2.boxplot(box_data, labels=present_pathways, patch_artist=True,
                     widths=0.6, showfliers=True)
    
    for patch, pathway in zip(bp['boxes'], present_pathways):
        patch.set_facecolor(pathway_colors[pathway])
        patch.set_alpha(0.7)
    
    ax2.set_xlabel('Pathway Type', fontsize=10, weight='bold')
    ax2.set_ylabel('Observed CLI', fontsize=10, weight='bold')
    ax2.set_title('CLI Distribution by Pathway', fontsize=11, weight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)
    
    # 3-7. Individual driver boxplots by pathway
    drivers = ['esri', 'pci', 'rca', 'vpfi', 'eili']
    driver_labels = ['ESRI (Economic)', 'PCI (Premature Const.)', 
                     'RCA (Cost Asymmetry)', 'VPFI (Veto Players)', 
                     'EILI (Identity)']
    
    for idx, (driver, label) in enumerate(zip(drivers, driver_labels)):
        row = 1 + idx // 2
        col = idx % 2
        ax = fig.add_subplot(gs[row, col])
        
        box_data = [df[df['pathway'] == p][driver].values for p in present_pathways]
        bp = ax.boxplot(box_data, labels=present_pathways, patch_artist=True,
                       widths=0.6, showfliers=True)
        
        for patch, pathway in zip(bp['boxes'], present_pathways):
            patch.set_facecolor(pathway_colors[pathway])
            patch.set_alpha(0.7)
        
        ax.set_xlabel('Pathway Type', fontsize=9)
        ax.set_ylabel(label, fontsize=9, weight='bold')
        ax.set_title(f'{label} by Pathway', fontsize=10, weight='bold')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
    
    # Overall title
    fig.suptitle(title, fontsize=14, weight='bold', y=0.995)
    
    # Save
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Pathway distribution plot saved: {output_path}")


def main():
    """Main execution function"""
    # Setup paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    viz_dir = script_dir.parent / 'visualizations'
    viz_dir.mkdir(exist_ok=True)
    
    input_path = data_dir / 'crystallization_drivers.csv'
    
    print("Crystallization Drivers Visualization")
    print("="*60)
    print(f"Input: {input_path}")
    print(f"Output directory: {viz_dir}")
    print()
    
    # Load data
    df = pd.read_csv(input_path)
    print(f"✓ Loaded {len(df)} cases")
    print()
    
    # 1. Radar chart - Compare high crystallization cases
    print("Creating visualizations...")
    radar_cases = ['ARG_001', 'USA_002', 'BRA_001', 'CHL_002']
    plot_driver_radar(
        df, radar_cases,
        str(viz_dir / 'driver_radar_comparison.png'),
        title="Driver Profile Comparison - High Crystallization Cases"
    )
    
    # 2. Correlation heatmap
    plot_driver_heatmap(
        df,
        str(viz_dir / 'driver_correlation_heatmap.png'),
        title="Driver Correlation Matrix"
    )
    
    # 3. Prediction scatter plot
    plot_prediction_scatter(
        df,
        str(viz_dir / 'prediction_accuracy_scatter.png'),
        title="CLI Prediction Accuracy - Observed vs Predicted"
    )
    
    # 4. Pathway distribution
    plot_pathway_distribution(
        df,
        str(viz_dir / 'pathway_distribution.png'),
        title="Crystallization Pathway Analysis"
    )
    
    print()
    print("="*60)
    print("✓ All visualizations complete!")
    print("="*60)


if __name__ == '__main__':
    main()

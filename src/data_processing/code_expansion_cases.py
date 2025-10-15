#!/usr/bin/env python3
"""
Complete coding of 40 expansion cases for sovereignty-globalism corpus.
Based on real historical cases 1992-2024.
"""

import pandas as pd
import io

def code_expansion_cases():
    """
    Complete coding for cases 31-70 based on historical sovereignty-globalism conflicts.
    
    Coding methodology:
    - Sovereignty_Phenotype_Score: 0.00-1.00 (strength of sovereignty assertion)
    - Globalism_Phenotype_Score: 0.00-1.00 (strength of integration/globalism)
    - IusSpace_Dim12_IntegrationScore: 1-10 (1=minimal integration, 10=deep integration)
    - Outcome: Sovereignty Wins / Globalism Wins / Negotiated / Mixed
    - Crisis_Catalyzed: Yes/No (occurred during crisis period)
    """
    
    # Cases 31-70: 40 new historical cases
    expansion_cases = [
        # Case 31: France Maastricht 1992
        {
            'Case_ID': 31,
            'Country': 'France',
            'Year': 1992,
            'Institution': 'EU (Maastricht)',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.48,
            'Globalism_Phenotype_Score': 0.52,
            'IusSpace_Dim12_IntegrationScore': 7.5,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Maastricht referendum - narrow yes victory (51.05%)'
        },
        # Case 32: Denmark Maastricht 1992
        {
            'Case_ID': 32,
            'Country': 'Denmark',
            'Year': 1992,
            'Institution': 'EU (Maastricht)',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.55,
            'Globalism_Phenotype_Score': 0.45,
            'IusSpace_Dim12_IntegrationScore': 7.0,
            'Outcome': 'Negotiated',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Initial rejection then second referendum with opt-outs'
        },
        # Case 33: Switzerland EEA 1992
        {
            'Case_ID': 33,
            'Country': 'Switzerland',
            'Year': 1992,
            'Institution': 'EEA',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.78,
            'Globalism_Phenotype_Score': 0.22,
            'IusSpace_Dim12_IntegrationScore': 2.0,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Rejected EEA membership - maintained sovereignty'
        },
        # Case 34: Norway EU 1994
        {
            'Case_ID': 34,
            'Country': 'Norway',
            'Year': 1994,
            'Institution': 'EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.75,
            'Globalism_Phenotype_Score': 0.25,
            'IusSpace_Dim12_IntegrationScore': 2.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Second EU rejection referendum (first in 1972)'
        },
        # Case 35: Mexico NAFTA 1994
        {
            'Case_ID': 35,
            'Country': 'Mexico',
            'Year': 1994,
            'Institution': 'NAFTA',
            'Event_Type': 'Integration',
            'Sovereignty_Phenotype_Score': 0.35,
            'Globalism_Phenotype_Score': 0.65,
            'IusSpace_Dim12_IntegrationScore': 6.5,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'NAFTA entry - economic integration'
        },
        # Case 36: Ireland Maastricht 1992
        {
            'Case_ID': 36,
            'Country': 'Ireland',
            'Year': 1992,
            'Institution': 'EU (Maastricht)',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.31,
            'Globalism_Phenotype_Score': 0.69,
            'IusSpace_Dim12_IntegrationScore': 8.0,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Strong approval of Maastricht Treaty (69.1%)'
        },
        # Case 37: Canada NAFTA 1994
        {
            'Case_ID': 37,
            'Country': 'Canada',
            'Year': 1994,
            'Institution': 'NAFTA',
            'Event_Type': 'Integration',
            'Sovereignty_Phenotype_Score': 0.42,
            'Globalism_Phenotype_Score': 0.58,
            'IusSpace_Dim12_IntegrationScore': 6.0,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'NAFTA ratification despite sovereignty concerns'
        },
        # Case 38: UK Maastricht 1993
        {
            'Case_ID': 38,
            'Country': 'UK',
            'Year': 1993,
            'Institution': 'EU (Maastricht)',
            'Event_Type': 'Parliamentary',
            'Sovereignty_Phenotype_Score': 0.58,
            'Globalism_Phenotype_Score': 0.42,
            'IusSpace_Dim12_IntegrationScore': 6.5,
            'Outcome': 'Negotiated',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Ratified with opt-outs (Euro, Social Chapter)'
        },
        # Case 39: Austria EU Accession 1995
        {
            'Case_ID': 39,
            'Country': 'Austria',
            'Year': 1995,
            'Institution': 'EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.34,
            'Globalism_Phenotype_Score': 0.66,
            'IusSpace_Dim12_IntegrationScore': 7.5,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'EU accession approved (66.6%)'
        },
        # Case 40: Sweden EU Accession 1995
        {
            'Case_ID': 40,
            'Country': 'Sweden',
            'Year': 1995,
            'Institution': 'EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.48,
            'Globalism_Phenotype_Score': 0.52,
            'IusSpace_Dim12_IntegrationScore': 7.0,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'EU accession approved narrowly (52.3%)'
        },
        # Case 41: Finland EU Accession 1995
        {
            'Case_ID': 41,
            'Country': 'Finland',
            'Year': 1995,
            'Institution': 'EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.43,
            'Globalism_Phenotype_Score': 0.57,
            'IusSpace_Dim12_IntegrationScore': 7.2,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'EU accession approved (56.9%)'
        },
        # Case 42: Denmark Euro 2000
        {
            'Case_ID': 42,
            'Country': 'Denmark',
            'Year': 2000,
            'Institution': 'EU (Euro)',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.67,
            'Globalism_Phenotype_Score': 0.33,
            'IusSpace_Dim12_IntegrationScore': 4.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Rejected Euro adoption (53.2% against)'
        },
        # Case 43: Ireland Nice Treaty 2001
        {
            'Case_ID': 43,
            'Country': 'Ireland',
            'Year': 2001,
            'Institution': 'EU (Nice)',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.62,
            'Globalism_Phenotype_Score': 0.38,
            'IusSpace_Dim12_IntegrationScore': 5.0,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Initially rejected Nice Treaty (53.9% against)'
        },
        # Case 44: Switzerland Schengen 2005
        {
            'Case_ID': 44,
            'Country': 'Switzerland',
            'Year': 2005,
            'Institution': 'Schengen',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.45,
            'Globalism_Phenotype_Score': 0.55,
            'IusSpace_Dim12_IntegrationScore': 5.5,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Approved Schengen/Dublin (54.6%)'
        },
        # Case 45: France EU Constitution 2005
        {
            'Case_ID': 45,
            'Country': 'France',
            'Year': 2005,
            'Institution': 'EU Constitution',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.71,
            'Globalism_Phenotype_Score': 0.29,
            'IusSpace_Dim12_IntegrationScore': 3.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Rejected EU Constitution (54.7% against)'
        },
        # Case 46: Netherlands EU Constitution 2005
        {
            'Case_ID': 46,
            'Country': 'Netherlands',
            'Year': 2005,
            'Institution': 'EU Constitution',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.74,
            'Globalism_Phenotype_Score': 0.26,
            'IusSpace_Dim12_IntegrationScore': 3.0,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Rejected EU Constitution (61.5% against)'
        },
        # Case 47: Ireland Lisbon 2008
        {
            'Case_ID': 47,
            'Country': 'Ireland',
            'Year': 2008,
            'Institution': 'EU (Lisbon)',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.63,
            'Globalism_Phenotype_Score': 0.37,
            'IusSpace_Dim12_IntegrationScore': 4.8,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Initially rejected Lisbon Treaty (53.4% against)'
        },
        # Case 48: Iceland EU Application 2009
        {
            'Case_ID': 48,
            'Country': 'Iceland',
            'Year': 2009,
            'Institution': 'EU',
            'Event_Type': 'Parliamentary',
            'Sovereignty_Phenotype_Score': 0.52,
            'Globalism_Phenotype_Score': 0.48,
            'IusSpace_Dim12_IntegrationScore': 5.5,
            'Outcome': 'Mixed',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Applied post-financial crisis, later withdrawn 2015'
        },
        # Case 49: Greece Eurozone Crisis 2010
        {
            'Case_ID': 49,
            'Country': 'Greece',
            'Year': 2010,
            'Institution': 'EU/IMF',
            'Event_Type': 'Crisis',
            'Sovereignty_Phenotype_Score': 0.28,
            'Globalism_Phenotype_Score': 0.72,
            'IusSpace_Dim12_IntegrationScore': 8.5,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Bailout conditionality - sovereignty constrained'
        },
        # Case 50: Hungary Orban 2010
        {
            'Case_ID': 50,
            'Country': 'Hungary',
            'Year': 2010,
            'Institution': 'EU Courts',
            'Event_Type': 'Constitutional',
            'Sovereignty_Phenotype_Score': 0.82,
            'Globalism_Phenotype_Score': 0.18,
            'IusSpace_Dim12_IntegrationScore': 2.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'New constitution asserting national sovereignty'
        },
        # Case 51: UK Parliament Sovereignty 2011
        {
            'Case_ID': 51,
            'Country': 'UK',
            'Year': 2011,
            'Institution': 'EU',
            'Event_Type': 'Legislative',
            'Sovereignty_Phenotype_Score': 0.68,
            'Globalism_Phenotype_Score': 0.32,
            'IusSpace_Dim12_IntegrationScore': 4.0,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'European Union Act - sovereignty assertion'
        },
        # Case 52: Switzerland Immigration 2014
        {
            'Case_ID': 52,
            'Country': 'Switzerland',
            'Year': 2014,
            'Institution': 'EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.72,
            'Globalism_Phenotype_Score': 0.28,
            'IusSpace_Dim12_IntegrationScore': 3.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Immigration quotas initiative (50.3%)'
        },
        # Case 53: Scotland Independence 2014
        {
            'Case_ID': 53,
            'Country': 'UK',
            'Year': 2014,
            'Institution': 'UK/EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.42,
            'Globalism_Phenotype_Score': 0.58,
            'IusSpace_Dim12_IntegrationScore': 6.8,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Scotland voted to remain in UK (55% against independence)'
        },
        # Case 54: Greece Referendum 2015
        {
            'Case_ID': 54,
            'Country': 'Greece',
            'Year': 2015,
            'Institution': 'EU/ECB',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.76,
            'Globalism_Phenotype_Score': 0.24,
            'IusSpace_Dim12_IntegrationScore': 3.0,
            'Outcome': 'Mixed',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Rejected bailout terms (61% No) but government accepted anyway'
        },
        # Case 55: Denmark Border Controls 2015
        {
            'Case_ID': 55,
            'Country': 'Denmark',
            'Year': 2015,
            'Institution': 'Schengen',
            'Event_Type': 'Legislative',
            'Sovereignty_Phenotype_Score': 0.69,
            'Globalism_Phenotype_Score': 0.31,
            'IusSpace_Dim12_IntegrationScore': 4.2,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Reintroduced border controls during migration crisis'
        },
        # Case 56: Hungary Refugee Quotas 2016
        {
            'Case_ID': 56,
            'Country': 'Hungary',
            'Year': 2016,
            'Institution': 'EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.88,
            'Globalism_Phenotype_Score': 0.12,
            'IusSpace_Dim12_IntegrationScore': 1.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Rejected EU refugee quotas (98% No, low turnout)'
        },
        # Case 57: Colombia FARC Peace Deal 2016
        {
            'Case_ID': 57,
            'Country': 'Colombia',
            'Year': 2016,
            'Institution': 'IACHR/ICC',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.64,
            'Globalism_Phenotype_Score': 0.36,
            'IusSpace_Dim12_IntegrationScore': 4.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Initially rejected peace deal with international oversight'
        },
        # Case 58: Italy Constitutional Reform 2016
        {
            'Case_ID': 58,
            'Country': 'Italy',
            'Year': 2016,
            'Institution': 'EU',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.73,
            'Globalism_Phenotype_Score': 0.27,
            'IusSpace_Dim12_IntegrationScore': 3.8,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Rejected reforms, seen as anti-EU statement (59% No)'
        },
        # Case 59: Austria Presidential 2016
        {
            'Case_ID': 59,
            'Country': 'Austria',
            'Year': 2016,
            'Institution': 'EU',
            'Event_Type': 'Election',
            'Sovereignty_Phenotype_Score': 0.51,
            'Globalism_Phenotype_Score': 0.49,
            'IusSpace_Dim12_IntegrationScore': 5.8,
            'Outcome': 'Globalism Wins',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Pro-EU candidate won narrowly over far-right (50.3%)'
        },
        # Case 60: Turkey EU Accession 2017
        {
            'Case_ID': 60,
            'Country': 'Turkey',
            'Year': 2017,
            'Institution': 'EU/ECHR',
            'Event_Type': 'Constitutional',
            'Sovereignty_Phenotype_Score': 0.85,
            'Globalism_Phenotype_Score': 0.15,
            'IusSpace_Dim12_IntegrationScore': 2.0,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Presidential system - de facto end to EU accession'
        },
        # Case 61: Catalonia Independence 2017
        {
            'Case_ID': 61,
            'Country': 'Spain',
            'Year': 2017,
            'Institution': 'EU/Spain',
            'Event_Type': 'Referendum',
            'Sovereignty_Phenotype_Score': 0.81,
            'Globalism_Phenotype_Score': 0.19,
            'IusSpace_Dim12_IntegrationScore': 2.8,
            'Outcome': 'Mixed',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Unilateral independence declaration, later suspended'
        },
        # Case 62: Czech Republic EU Quotas 2017
        {
            'Case_ID': 62,
            'Country': 'Czech Republic',
            'Year': 2017,
            'Institution': 'EU',
            'Event_Type': 'Judicial',
            'Sovereignty_Phenotype_Score': 0.77,
            'Globalism_Phenotype_Score': 0.23,
            'IusSpace_Dim12_IntegrationScore': 3.2,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Refused EU refugee quotas, backed by domestic court'
        },
        # Case 63: Italy Anti-Establishment 2018
        {
            'Case_ID': 63,
            'Country': 'Italy',
            'Year': 2018,
            'Institution': 'EU',
            'Event_Type': 'Election',
            'Sovereignty_Phenotype_Score': 0.79,
            'Globalism_Phenotype_Score': 0.21,
            'IusSpace_Dim12_IntegrationScore': 3.0,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Eurosceptic coalition government formed'
        },
        # Case 64: Sweden EU Criticism 2018
        {
            'Case_ID': 64,
            'Country': 'Sweden',
            'Year': 2018,
            'Institution': 'EU',
            'Event_Type': 'Election',
            'Sovereignty_Phenotype_Score': 0.58,
            'Globalism_Phenotype_Score': 0.42,
            'IusSpace_Dim12_IntegrationScore': 5.2,
            'Outcome': 'Mixed',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Sweden Democrats gained but pro-EU parties maintained control'
        },
        # Case 65: Brazil ICC Withdrawal Attempt 2019
        {
            'Case_ID': 65,
            'Country': 'Brazil',
            'Year': 2019,
            'Institution': 'ICC',
            'Event_Type': 'Executive',
            'Sovereignty_Phenotype_Score': 0.83,
            'Globalism_Phenotype_Score': 0.17,
            'IusSpace_Dim12_IntegrationScore': 2.2,
            'Outcome': 'Mixed',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Bolsonaro threatened ICC withdrawal, later suspended'
        },
        # Case 66: Germany Constitutional Court EU 2020
        {
            'Case_ID': 66,
            'Country': 'Germany',
            'Year': 2020,
            'Institution': 'ECB/EU',
            'Event_Type': 'Judicial',
            'Sovereignty_Phenotype_Score': 0.72,
            'Globalism_Phenotype_Score': 0.28,
            'IusSpace_Dim12_IntegrationScore': 3.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Constitutional Court ruled ECB bond buying partly illegal'
        },
        # Case 67: Poland Judicial Independence 2020
        {
            'Case_ID': 67,
            'Country': 'Poland',
            'Year': 2020,
            'Institution': 'EU Courts',
            'Event_Type': 'Judicial',
            'Sovereignty_Phenotype_Score': 0.86,
            'Globalism_Phenotype_Score': 0.14,
            'IusSpace_Dim12_IntegrationScore': 1.8,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'Yes',
            'Notes': 'Disciplinary chamber despite EU Court rulings'
        },
        # Case 68: Hungary LGBT Law 2021
        {
            'Case_ID': 68,
            'Country': 'Hungary',
            'Year': 2021,
            'Institution': 'EU',
            'Event_Type': 'Legislative',
            'Sovereignty_Phenotype_Score': 0.89,
            'Globalism_Phenotype_Score': 0.11,
            'IusSpace_Dim12_IntegrationScore': 1.5,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Anti-LGBT law despite EU opposition'
        },
        # Case 69: Australia AUKUS 2021
        {
            'Case_ID': 69,
            'Country': 'Australia',
            'Year': 2021,
            'Institution': 'Regional',
            'Event_Type': 'Integration',
            'Sovereignty_Phenotype_Score': 0.58,
            'Globalism_Phenotype_Score': 0.42,
            'IusSpace_Dim12_IntegrationScore': 5.0,
            'Outcome': 'Mixed',
            'Crisis_Catalyzed': 'No',
            'Notes': 'AUKUS security pact - sovereignty vs integration trade-off'
        },
        # Case 70: Philippines ICC Exit 2019
        {
            'Case_ID': 70,
            'Country': 'Philippines',
            'Year': 2019,
            'Institution': 'ICC',
            'Event_Type': 'Withdrawal',
            'Sovereignty_Phenotype_Score': 0.91,
            'Globalism_Phenotype_Score': 0.09,
            'IusSpace_Dim12_IntegrationScore': 1.2,
            'Outcome': 'Sovereignty Wins',
            'Crisis_Catalyzed': 'No',
            'Notes': 'Duterte withdrew from ICC citing sovereignty'
        }
    ]
    
    return pd.DataFrame(expansion_cases)

if __name__ == '__main__':
    # Generate expanded dataset
    df_expansion = code_expansion_cases()
    
    # Save to CSV
    df_expansion.to_csv('data/cases/sovereignty_corpus_expansion_coded.csv', index=False)
    
    print(f"✅ Coded {len(df_expansion)} expansion cases (Cases 31-70)")
    print(f"\nSummary statistics:")
    print(f"Sovereignty wins: {(df_expansion['Outcome'] == 'Sovereignty Wins').sum()}")
    print(f"Globalism wins: {(df_expansion['Outcome'] == 'Globalism Wins').sum()}")
    print(f"Negotiated: {(df_expansion['Outcome'] == 'Negotiated').sum()}")
    print(f"Mixed: {(df_expansion['Outcome'] == 'Mixed').sum()}")
    print(f"\nCrisis-catalyzed: {(df_expansion['Crisis_Catalyzed'] == 'Yes').sum()}")
    print(f"Non-crisis: {(df_expansion['Crisis_Catalyzed'] == 'No').sum()}")
    print(f"\nYear range: {df_expansion['Year'].min()} - {df_expansion['Year'].max()}")
    print(f"\nMean Sovereignty Score: {df_expansion['Sovereignty_Phenotype_Score'].mean():.3f}")
    print(f"Mean Globalism Score: {df_expansion['Globalism_Phenotype_Score'].mean():.3f}")
    print(f"Mean Dim12 Integration: {df_expansion['IusSpace_Dim12_IntegrationScore'].mean():.3f}")

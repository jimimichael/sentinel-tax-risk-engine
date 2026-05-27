import pandas as pd
import numpy as np
from pathlib import Path

"""Risk Scoring Script for Synthetic Taxpayer Data - the core analytics"""

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'
OUTPUTS_DIR = BASE_DIR / 'data' / 'outputs'
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / 'cleaned_taxpayers.csv'
RISK_SCORED_PATH = PROCESSED_DATA_DIR / 'risk_scored_taxpayers.csv'
AUDIT_PRIORITY_PATH = OUTPUTS_DIR / 'audit_priority_list.csv'


def calculate_risk_score(df):
    """Calculate composite risk score (0-100) with calibrated weights."""

    df['risk_score'] = 0

    # Factor 1: Filing lateness (0-30 points)
    df['risk_score'] += np.minimum(df['days_late_filing'] / 3, 30)

    # Factor 2: Payment lateness (0-30 points)
    df['risk_score'] += np.minimum(df['days_late_payment'] / 3, 30)

    # Factor 3: Under-reporting gap (0-35 points)
    df['under_report_pct'] = (df['annual_turnover_£'] - df['reported_turnover_£']) / df['annual_turnover_£']
    df['under_report_pct'] = df['under_report_pct'].clip(lower=0)
    df['risk_score'] += np.minimum(df['under_report_pct'] * 35, 35)

    if 'estimated_tax_gap_£' not in df.columns:
        df['estimated_tax_gap_£'] = (df['annual_turnover_£'] - df['reported_turnover_£']) * 0.2

    # Factor 4: Filing inconsistency (0-25 points)
    df['risk_score'] += (1 - df['filing_consistency_score']) * 25

    escalation_mask = (
        (df['under_report_pct'] > 0.5) &
        (df['days_late_filing'] > 120) &
        (df['filing_consistency_score'] < 0.2)
    )
    df.loc[escalation_mask, 'risk_score'] += 15

    df['risk_score'] = df['risk_score'].round(0).clip(0, 100)
    df['risk_band'] = pd.cut(df['risk_score'],
                             bins=[0, 15, 35, 60, 80, 101],
                             labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

    return df


def prioritize_audits(df, top_n=1000):
    """Return top N highest-risk taxpayers for compliance intervention."""

    df = df.sort_values('risk_score', ascending=False)
    high_risk = df[df['risk_band'].isin(['High', 'Very High'])].copy()
    high_risk['audit_priority'] = range(1, len(high_risk) + 1)
    return high_risk.head(top_n)


def print_calibration_report(df):
    """Print calibration metrics to verify realistic distribution."""

    print("\n" + "=" * 60)
    print("RISK CALIBRATION REPORT")
    print("=" * 60)

    band_dist = df['risk_band'].value_counts(normalize=True) * 100
    print("\nRisk Band Distribution (%):")
    for band in ['Very Low', 'Low', 'Medium', 'High', 'Very High']:
        pct = band_dist.get(band, 0)
        bar = "█" * int(pct / 2)
        print(f"  {band:12} {pct:5.1f}% {bar}")

    high_count = df['risk_band'].isin(['High', 'Very High']).sum()
    print(f"\nAverage risk score: {df['risk_score'].mean():.1f}/100")
    print(f"Median risk score: {df['risk_score'].median():.1f}/100")
    print(f"High/Very High count: {high_count} ({high_count / len(df) * 100:.1f}%)")
    print(f"\nTotal estimated tax gap: £{df['estimated_tax_gap_£'].sum():,.0f}")
    print(f"Tax gap from High/Very High only: £{df[df['risk_band'].isin(['High', 'Very High'])]['estimated_tax_gap_£'].sum():,.0f}")


if __name__ == "__main__":
    df = pd.read_csv(CLEANED_DATA_PATH)
    df = calculate_risk_score(df)
    print_calibration_report(df)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(RISK_SCORED_PATH, index=False)
    audit_list = prioritize_audits(df, top_n=1000)
    audit_list.to_csv(AUDIT_PRIORITY_PATH, index=False)

    print(f"\n✓ Audit priority list saved - {len(audit_list)} taxpayers")
    print(f"  Total estimated tax gap in priority list: £{audit_list['estimated_tax_gap_£'].sum():,.0f}")
    
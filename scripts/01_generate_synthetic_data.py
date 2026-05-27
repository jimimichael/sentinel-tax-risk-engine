import pandas as pd
import numpy as np
import random
from faker import Faker
from pathlib import Path

# This script creates 100,000 synthetic data taxpayer records. It generates a CSV file with random data.
# scripts/01_generate_synthetic_data.py

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / 'data' / 'raw' / 'synthetic_taxpayers.csv'

# Initialize Faker
fake = Faker('en_GB')  # UK specific data
Faker.seed(42)
random.seed(42)
np.random.seed(42)


def generate_taxpayers(n=100000):
    """Generate synthetic taxpayer records with realistic risk distribution."""

    industries = ['Retail', 'Construction', 'Hospitality', 'Professional Services',
                  'Manufacturing', 'Transport', 'Wholesale', 'Agriculture', 'Finance']

    data = []

    for i in range(n):
        taxpayer = {
            'taxpayer_id': f'TX{i:06d}',
            'industry': random.choice(industries),
            'region': random.choice(['North', 'South', 'East', 'West', 'London', 'Scotland', 'Wales']),
            'years_in_business': random.randint(1, 30),
        }

        turnover = np.random.lognormal(mean=12, sigma=1.5)
        taxpayer['annual_turnover_£'] = round(turnover, 0)
        taxpayer['vat_due_£'] = round(turnover * 0.2, 0)

        taxpayer['days_late_filing'] = max(0, int(np.random.exponential(scale=3)))
        taxpayer['days_late_payment'] = max(0, int(np.random.exponential(scale=2)))
        taxpayer['reported_turnover_£'] = round(turnover, 0)
        taxpayer['filing_consistency_score'] = np.random.beta(a=8, b=2)
        taxpayer['risk_flag'] = 'Normal'

        data.append(taxpayer)

    df = pd.DataFrame(data)
    df['estimated_tax_gap_£'] = (df['annual_turnover_£'] - df['reported_turnover_£']) * 0.2
    return df


def add_realistic_tail_risk(df, high_risk_percent=4.0):
    """Create correlated high-risk profiles to simulate tail-risk enforcement volume."""

    n_high_risk = int(len(df) * high_risk_percent / 100)
    high_risk_indices = np.random.choice(df.index, n_high_risk, replace=False)

    for idx in high_risk_indices:
        under_report_pct = np.random.uniform(0.40, 0.60)
        df.loc[idx, 'reported_turnover_£'] = int(df.loc[idx, 'annual_turnover_£'] * (1 - under_report_pct))
        df.loc[idx, 'estimated_tax_gap_£'] = int(df.loc[idx, 'annual_turnover_£'] * under_report_pct * 0.2)
        df.loc[idx, 'days_late_filing'] = np.random.randint(60, 120)
        df.loc[idx, 'days_late_payment'] = np.random.randint(60, 120)
        df.loc[idx, 'filing_consistency_score'] = np.random.uniform(0, 0.3)

        if under_report_pct > 0.6 or df.loc[idx, 'days_late_filing'] > 150:
            df.loc[idx, 'risk_flag'] = 'Potential Under-Reporting'
        else:
            df.loc[idx, 'risk_flag'] = 'Suspicious Pattern'

    n_extreme = int(len(df) * 0.5 / 100)
    if 0 < n_extreme < n_high_risk:
        extreme_indices = np.random.choice(high_risk_indices, n_extreme, replace=False)
        for idx in extreme_indices:
            under_report_pct = np.random.uniform(0.7, 0.9)
            df.loc[idx, 'reported_turnover_£'] = int(df.loc[idx, 'annual_turnover_£'] * (1 - under_report_pct))
            df.loc[idx, 'estimated_tax_gap_£'] = int(df.loc[idx, 'annual_turnover_£'] * under_report_pct * 0.2)
            df.loc[idx, 'days_late_filing'] = np.random.randint(180, 365)
            df.loc[idx, 'days_late_payment'] = np.random.randint(180, 365)
            df.loc[idx, 'filing_consistency_score'] = np.random.uniform(0, 0.1)
            df.loc[idx, 'risk_flag'] = 'Potential Under-Reporting'

    return df


if __name__ == '__main__':
    print('Generating base taxpayer population...')
    df = generate_taxpayers(100000)

    print('Adding realistic tail-risk profiles (4.0% High/Very High)...')
    df = add_realistic_tail_risk(df, high_risk_percent=4.0)

    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f'Generated {len(df)} taxpayer records and saved to "{RAW_DATA_PATH}"')
    print('Risk flag distribution:')
    print(df['risk_flag'].value_counts())

import pandas as pd
from pathlib import Path

"""Quality Assurance Script for Synthetic Taxpayer Data"""

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / 'data' / 'raw' / 'synthetic_taxpayers.csv'
PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'
REPORT_PATH = PROCESSED_DATA_DIR / 'validation_report.txt'
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / 'cleaned_taxpayers.csv'

"""This script performs data validation checks on the synthetic taxpayer dataset generated in the previous step. 
It checks for missing values, data consistency, and basic statistical properties to ensure the data is suitable for analysis and 
modeling. A validation report is generated summarizing the findings."""

def validate_taxpayer_data(filepath):
    """Run some data quality checks on the taxpayer data and output a validation report"""
    df = pd.read_csv(filepath)
    results = []

    # Check 1: No nulls in key identifiers
    null_check = df[['taxpayer_id', 'industry', 'annual_turnover_£', 'vat_due_£']].isnull().sum().sum()
    results.append(f"Null check - missing values: {null_check}")

    # Check 2: No negative turnover
    negative_turnover = (df['annual_turnover_£'] < 0).sum()
    results.append(f"Negative turnover check - {negative_turnover} records (should be 0)")

    # Check 3: VAT due is exactly 20% of turnover
    vat_check = (abs(df['vat_due_£'] - df['annual_turnover_£'] * 0.2) > 1).sum()
    results.append(f"VAT Calculation check - {vat_check} mismatches (should be 0)")

    # Check 4: Risk flags are valid categories
    valid_flags = ['Normal', 'Suspicious Pattern', 'Potential Under-Reporting']
    invalid_flags = (~df['risk_flag'].isin(valid_flags)).sum()
    results.append(f"Risk flag validity check - {invalid_flags} invalid (should be 0)")

    # Check 5: Reported turnover never exceeds actual turnover
    over_report = (df['reported_turnover_£'] > df['annual_turnover_£']).sum()
    results.append(f"Over-reporting check - {over_report} records (should be 0)")

    # Check 6: Days late are non-negative and reasonable
    high_late = (df['days_late_filing'] > 365).sum() + (df['days_late_payment'] > 365).sum()
    results.append(f"Late days reasonable - {high_late} records > 365 days")

    # Check 7: All taxpayer IDs are unique
    unique_ids = df['taxpayer_id'].nunique() == len(df)
    results.append(f"Unique IDs - {'Pass' if unique_ids else 'Fail'}")

    # Check 8: Ensure all values in 'region' are valid
    valid_regions = ['North', 'South', 'East', 'West', 'London', 'Scotland', 'Wales']
    results.append(f"valid_regions check - {'Pass' if df['region'].isin(valid_regions).all() else 'Fail'}")

    # Check 9: Ensure all financial values are positive
    financial_columns = ['annual_turnover_£', 'vat_due_£', 'reported_turnover_£']
    financial_positive = all((df[col] > 0).all() for col in financial_columns)
    results.append(f"financial_columns check - {'Pass' if financial_positive else 'Fail'}")

    # Check 10: Ensure filing consistency scores are within valid range
    filing_consistency = ((df['filing_consistency_score'] >= 0) & (df['filing_consistency_score'] <= 1)).all()
    results.append(f"Filing consistency score check - {'Pass' if filing_consistency else 'Fail'}")

    # Summary        
    print("\n" + "=" * 50)
    print("Data Validation Report")
    print("=" * 50)
    for result in results:
        print(result)
    print("=" * 50 + "\n")


    # Save report to file
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    print(f"validation report saved to '{REPORT_PATH}' successfully")


    # Save cleaned data
    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Cleaned data saved to '{CLEANED_DATA_PATH}' successfully")

    return df

if __name__ == "__main__":
    df = validate_taxpayer_data(RAW_DATA_PATH)
    print(f"\n/ Cleaned data saved to {CLEANED_DATA_PATH} successfully")

    

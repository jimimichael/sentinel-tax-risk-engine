<<<<<<< HEAD
# Sentinel – Synthetic Tax Risk & Compliance Profiling Engine

## Purpose

Sentinel is an educational analytics project that simulates a simplified tax compliance risk-scoring workflow inspired by publicly documented HMRC Risk & Intelligence Service (RIS) and Connect analytics concepts.

The project demonstrates how multi-source taxpayer data can be validated, scored for potential compliance risk, prioritised for intervention, and visualised through a reproducible analytics pipeline using entirely synthetic data - designed to showcase the analytical thinking, data validation discipline, risk modelling, and stakeholder communication skills relevant to Senior Data Analyst roles in public-sector risk, compliance, and intelligence environments.

No real taxpayer or HMRC data is used.
---

## Disclaimer

Sentinel is an independent educational project using fully synthetic data generated for learning and portfolio purposes.

It is not affiliated with, endorsed by, or connected to HMRC.

All references to HMRC systems, workflows, and methodologies are derived solely from publicly available government and National Audit Office documentation.

---

## What This Project Demonstrates

- **Python (Pandas, NumPy, Faker):** Synthetic data generation and transformation
- **Data Validation:** 10 explicit QA checks with validation reporting
- **Risk Scoring:** Composite scoring algorithm (0–100) with configurable weights
- **SQL Analytics:** Window functions for industry-level risk ranking
- **Power BI:** Interactive dashboard for stakeholder reporting and audit triage
- **Reproducibility:** End-to-end pipeline with deterministic random seeds

---

## Project Pipeline

1. Generate 100,000 synthetic taxpayer records
2. Validate data quality using automated QA checks
3. Calculate composite compliance risk scores
4. Assign risk bands and prioritise high-risk cases
5. Export audit priority datasets
6. Visualise outputs in Power BI dashboards

---

## Key Outputs

- `data/processed/cleaned_taxpayers.csv` — Cleaned validated taxpayer dataset
- `data/processed/risk_scored_taxpayers.csv` — Risk-scored taxpayer dataset
- `data/outputs/audit_priority_list.csv` — Top 1,000 highest-risk taxpayers
- `data/processed/validation_report.txt` — Data quality validation evidence
- Power BI Dashboard — Executive and analyst-focused reporting views

---

## Tech Stack

| Area | Tools |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Synthetic Data | Faker |
| Data Validation | Custom QA Rules |
| SQL Analytics | SQLite/PostgreSQL-compatible SQL |
| Visualisation | Power BI |

---

## How to Run

```bash
git clone https://github.com/jimimichael/sentinel-tax-risk-engine
cd sentinel-tax-risk-engine

pip install -r requirements.txt

python scripts/01_generate_synthetic_data.py
python scripts/02_data_validation.py
python scripts/03_risk_scoring.py
```

---

## Risk Calibration Approach

The synthetic population intentionally includes a small number of correlated high-risk outlier profiles (around 4% of total records) to simulate realistic compliance-risk distributions and operational audit prioritisation workflows.

**Calibration decisions:**
- Under-reporting carries the highest weight (35%) – reflects HMRC's strategic focus on hidden income
- Repeated lateness (filing + payment) contributes 60 points max – operational significance
- Escalation logic adds a bonus for correlated severe behaviours (e.g., >50% under-reporting + >120 days late)
- Risk thresholds keep `High` at 60+ – no artificial lowering to force outputs

**Target distribution:**
- Very Low/Low: ~75-80% (compliant population)
- Medium: ~12-15% (deserves review, not full audit)
- High/Very High: ~3-5% (enforcement prioritisation)

Risk thresholds and scoring weights are calibrated for educational demonstration purposes and do not represent HMRC operational models or thresholds.

---

# How Sentinel Mirrors Publicly Documented HMRC Risk Analytics Concepts

Sentinel is a simplified educational analogue inspired by publicly documented HMRC compliance analytics approaches.

While HMRC operates large-scale real-world compliance systems using billions of data points across multiple tax regimes, Sentinel demonstrates similar analytical principles using 100,000 fully synthetic taxpayer records.

The sections below compare publicly documented HMRC concepts with Sentinel's educational implementation.

---

# Official Sources Informing This Project

This project is informed by publicly available HMRC and National Audit Office documentation:

| Source | Key Insights Used |
|---|---|
| HMRC Annual Report & Accounts 2024–2025 | Tax gap estimates, compliance yield, strategic priorities |
| NAO – HMRC's Connect Data Analytics Platform (2021) | Data-matching, risk analysis, connected datasets |
| HMRC's Approach to Tackling Tax Fraud (2022) | Promote / Prevent / Respond framework |
| HMRC Single Departmental Plan 2022–2025 | Compliance and enforcement priorities |

---

# 1. Multi-Source Data Integration

## Public HMRC Concept

According to publicly available NAO documentation, HMRC Connect integrates billions of data points from internal and external sources to support compliance risk analysis.

Examples of publicly referenced data categories include:

- Tax returns and VAT filings
- PAYE and employer records
- Property and financial information
- Third-party transactional data
- Online marketplace/platform data
- International reporting channels

## Sentinel Implementation

Sentinel generates 100,000 synthetic taxpayer records representing similar analytical categories.

| HMRC Conceptual Category | Sentinel Synthetic Equivalent | Code Location |
|---|---|---|
| Tax declarations | `annual_turnover_£`, `vat_due_£` | `01_generate_synthetic_data.py` |
| Filing behaviour | `days_late_filing`, `days_late_payment` | `01_generate_synthetic_data.py` |
| Industry benchmarking | `industry`, `region`, `years_in_business` | `01_generate_synthetic_data.py` |
| Compliance indicators | `risk_flag` | `01_generate_synthetic_data.py` |

### Key Difference

HMRC uses real operational datasets across multiple systems and tax regimes.

Sentinel uses fully synthetic data for safe, reproducible learning and portfolio demonstration purposes.

---

# 2. Risk Scoring & Compliance Profiling

## Public HMRC Concept

Publicly available HMRC and NAO documentation describes risk-based compliance approaches involving:

- Data matching
- Entity linking across datasets
- Industry benchmarking
- Anomaly detection
- Automated risk prioritisation

The Connect platform supports compliance teams by identifying patterns that may indicate non-compliance risks.

## Sentinel Implementation

Sentinel calculates a composite compliance risk score (0–100) using configurable weighted risk factors.

| Risk Factor | Sentinel Implementation | Weight |
|---|---|---|
| Filing lateness | `days_late_filing` | 25% |
| Payment lateness | `days_late_payment` | 25% |
| Under-reporting gap | `under_report_ratio` | 30% |
| Filing consistency | `consistency_score` | 20% |

### Sentinel Risk Score Logic

- Filing lateness capped at 25 points
- Payment lateness capped at 25 points
- Under-reporting ratio capped at 30 points
- Consistency adjustment capped at 20 points

### Output Risk Bands

| Score Range | Risk Band |
|---|---|
| 0–20 | Very Low |
| 20–40 | Low |
| 40–60 | Medium |
| 60–80 | High |
| 80–100 | Very High |

**Code Location:** `scripts/03_risk_scoring.py`

---

# 3. Anomaly Detection & Audit Prioritisation

## Public HMRC Concept

Public documentation indicates that higher-risk cases may undergo additional compliance review and prioritisation for intervention.

Compliance teams may use:
- Cross-regime analysis
- Pattern detection
- Risk thresholding
- Case prioritisation workflows

## Sentinel Implementation

Sentinel identifies high-risk taxpayers and generates a prioritised audit list.

| HMRC Concept | Sentinel Implementation | Output |
|---|---|---|
| Threshold-based risk review | Filter `High` and `Very High` risk bands | High-risk subset |
| Estimated exposure calculation | Estimated tax gap formula | Potential non-compliance estimate |
| Risk prioritisation | Ranked risk scoring | Top 1,000 cases |

### Example SQL Window Function

```sql
ROW_NUMBER() OVER (
    PARTITION BY industry
    ORDER BY risk_score DESC
) AS rank_in_industry
```

**SQL File:** `scripts/04_sql_ranking.sql`

---

# 4. Compliance Intervention Triage

## Public HMRC Concept

HMRC's published compliance strategy references the “Promote, Prevent, Respond” framework for addressing non-compliance risks.

Publicly documented intervention types include:
- Educational nudges
- Automated communications
- Civil compliance investigations
- Criminal investigation pathways

## Sentinel Demonstration

Sentinel models simplified intervention triage logic using risk bands.

| Risk Band | Example Intervention Type | Sentinel Demonstration |
|---|---|---|
| Very Low / Low | Automated nudge | Dashboard segmentation |
| Medium | Additional review | Medium-risk dashboard filter |
| High / Very High | Compliance intervention | `audit_priority_list.csv` |

### Not Modelled

- Criminal investigation workflows
- Legal enforcement processes
- Real taxpayer case management

---

# 5. Validation & Reproducibility

## Public HMRC Concept

Public-sector analytics environments depend heavily on:
- Data quality controls
- Model monitoring
- Validation frameworks
- Iterative refinement

## Sentinel Implementation

Sentinel includes automated QA validation checks and reproducible pipeline execution.

### Validation Checks

- No null taxpayer IDs
- No negative turnover values
- VAT equals 20% of turnover
- Valid risk flag categories
- Reported turnover does not exceed actual turnover
- Late filing/payment days within expected ranges
- All taxpayer IDs unique

### Reproducibility Features

- Fixed random seed (`random.seed(42)`)
- Modular pipeline architecture
- Configurable scoring weights

---

# Example Project Outputs

## Validation Report
- QA pass/fail checks
- Null analysis
- Duplicate detection
- Business rule validation

## Audit Priority List
- Ranked high-risk taxpayers
- Estimated tax exposure
- Industry-level prioritisation

## Power BI Dashboard
- Executive risk summary
- Regional risk heatmaps
- Industry breakdowns
- Audit prioritisation views

---

# Key Public Statistics Referenced

| Statistic | Value | Source |
|---|---|---|
| UK Tax Gap | £46.8bn (5.3%) | HMRC Annual Report 2024–25 |
| Compliance Yield | ~£48bn | HMRC Annual Report 2024–25 |
| Connect-related additional revenue impact | £3–4bn annually | NAO Connect Report (2021) |
| Prosecution success rate | ~91% | HMRC Annual Report 2024–25 |

---

# Sentinel vs. Real-World Compliance Analytics

| Aspect | Real-World HMRC Environment | Sentinel |
|---|---|---|
| Data Volume | Billions of operational data points | 100,000 synthetic records |
| Data Source | Real compliance datasets | Synthetic Faker-generated data |
| Risk Scoring | Proprietary internal models | Transparent weighted scoring |
| Infrastructure | Enterprise-scale analytics platforms | Local Python + SQL pipeline |
| Feedback Loop | Operational compliance outcomes | Validation framework |
| Purpose | Tax compliance operations | Educational analytics project |

---

# Skills Demonstrated

- Risk analytics
- Data validation
- Data engineering workflows
- SQL analytical querying
- Dashboard storytelling
- Reproducible analytics pipelines
- Public-sector analytical thinking
- Compliance risk modelling

---

# References

## HMRC Annual Report & Accounts 2024–2025
https://www.gov.uk/government/publications/hmrc-annual-report-and-accounts-2024-to-2025

## National Audit Office – HMRC's Connect Data Analytics Platform (2021)
https://www.nao.org.uk/reports/hmrcs-connect-data-analytics-platform/

## HMRC's Approach to Tackling Tax Fraud (2022)
https://www.gov.uk/government/publications/hmrcs-approach-to-tackling-tax-fraud

## HMRC Single Departmental Plan 2022–2025
https://www.gov.uk/government/publications/hmrc-single-departmental-plan/hmrc-single-departmental-plan-2022-to-2025

---

# Possible Enhancements

1. Add time-series analysis for filing pattern changes
2. Implement machine learning (Isolation Forest) for anomaly detection
3. Automate weekly refresh with GitHub Actions

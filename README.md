# Sentinel – Synthetic Tax Risk & Compliance Profiling Engine

## Executive Summary

Sentinel is a proof-of-concept analytics engine built to mirror the risk profiling workflows used by HMRC’s Risk & Intelligence Service (RIS). It simulates multi-source taxpayer data feeds, applies risk-scoring logic, and prioritises cases for review using fully synthetic data.

This version focuses on high-risk industries where cash-heavy or complex transactions are common, and on self-employed populations whose income is not automatically taxed at source.

---

## Business Context

HMRC’s Connect system targets sectors where tax discrepancies are harder to detect, including:

- Self-employed contractors, freelancers, tradespeople, IT consultants, and gig economy workers
- Cash-intensive businesses such as restaurants, takeaways, hair and beauty salons, and market traders
- Online platform sellers and delivery drivers whose income is now shareable via marketplace reporting
- Property investors with rental income or capital gains from second homes

Sentinel demonstrates how data analytics can give senior leaders a clear, at-a-glance view of compliance risk and investigation priority.

---

## What Sentinel Demonstrates

- Synthetic Tax Data Generation: creates a privacy-safe population of taxpayers and businesses
- Data Validation: checks for missing values, logic consistency, and financial integrity
- Risk Modelling: composite score generation and risk band assignment
- Audit Prioritisation: ranks the highest-risk cases for review
- Stakeholder Visualisation: builds a dashboard for executive decision support

---

## Target Population & Industries

This project represents the types of taxpayers that HMRC’s analytics teams typically scrutinise:

- Self-employed / contractors
- Cash-intensive sectors
- Gig economy participants
- Property investors and landlords

---

## Key Outputs

- `data/processed/cleaned_taxpayers.csv` — validated synthetic taxpayer dataset
- `data/processed/risk_scored_taxpayers.csv` — risk scoring and categorisation output
- `data/outputs/audit_priority_list.csv` — top compliance cases for investigation
- `data/processed/validation_report.txt` — data quality evidence
- `dashboard_output.png` — stakeholder dashboard visualisation

![Risk Dashboard](dashboard_output.png)

---

## Project Pipeline

1. Generate synthetic taxpayer data
2. Validate data quality and consistency
3. Calculate composite compliance risk scores
4. Assign risk bands and audit priorities
5. Export priority reports for review
6. Build a stakeholder-facing dashboard

---

## Tech Stack

| Area | Tools |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Synthetic Data | Faker |
| Data Validation | Custom QA rules |
| Visualisation | Matplotlib, Seaborn |
| Reporting | CSV, Power BI-compatible exports |

---

## How to Run

```powershell
cd c:\Users\oluji\Documents\sentinel-tax-risk-engine
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts\01_generate_synthetic_data.py
.venv\Scripts\python.exe scripts\02_data_validation.py
.venv\Scripts\python.exe scripts\03_risk_scoring.py
.venv\Scripts\python.exe visualize_risk.py
```

> Running `visualize_risk.py` generates `dashboard_output.png` for executive reporting.

---

## Visualization

A new dashboard script creates a stakeholder-ready view of the compliance funnel and anomalous risk signals:

- Priority distribution across `Clear`, `Monitor`, and `Investigate`
- Turnover versus estimated tax gap, sized by under-reporting intensity

**File:** `visualize_risk.py`

### How to Read `dashboard_output.png`

1. **Compliance Funnel (left panel)**
   - Shows how the population is divided by priority level.
   - `Clear` is low-risk and can be deprioritised.
   - `Investigate` is high-risk and should be escalated for review.
   - Use this view to show senior leaders the operational triage balance.

2. **Declared Turnover vs Estimated Tax Gap (right panel)**
   - X-axis is declared turnover; Y-axis is estimated tax gap.
   - Bubble color shows action priority (`Clear`, `Monitor`, `Investigate`).
   - Bubble size represents under-reporting intensity.
   - Large red bubbles in the top-right are highest-priority anomalies.

This section helps explain the dashboard to stakeholders by translating charts into investigation priorities and risk exposure signals.

---

## Risk Calibration Approach

Sentinel uses an educational risk model calibrated to highlight likely non-compliance patterns:

- Filing lateness and payment lateness are each capped at 30 points
- Under-reporting gap contributes up to 35 points
- Inconsistency penalties add up to 25 points
- Severe combined behaviours trigger escalation bonuses

**Risk bands:**

| Score Range | Risk Band |
|---|---|
| 0–15 | Very Low |
| 15–35 | Low |
| 35–60 | Medium |
| 60–80 | High |
| 80–100 | Very High |

---

## HMRC Inspiration

This project is an independent educational demonstration and is not affiliated with HMRC. It is inspired by publicly available HMRC and National Audit Office material on risk analytics, data matching, and compliance profiling.

**Relevant sources:**

- HMRC Annual Report & Accounts
- NAO reports on HMRC Connect and compliance analytics
- HMRC compliance strategy publications

---

## File Summary

- `scripts/01_generate_synthetic_data.py` — build synthetic taxpayer dataset
- `scripts/02_data_validation.py` — run QA checks and save cleaned data
- `scripts/03_risk_scoring.py` — calculate risk score and export audit priority list
- `scripts/04_sql_ranking.sql` — example ranking query for industry analysis
- `scripts/05_power_bi_export.py` — export data for Power BI consumption
- `visualize_risk.py` — generate a stakeholder dashboard image

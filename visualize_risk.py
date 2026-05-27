import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RISK_DATA_PATH = BASE_DIR / 'data' / 'processed' / 'risk_scored_taxpayers.csv'
OUTPUT_IMAGE_PATH = BASE_DIR / 'dashboard_output.png'


def load_risk_data(path):
    df = pd.read_csv(path)
    if 'under_report_pct' not in df.columns:
        df['under_report_pct'] = ((df['annual_turnover_£'] - df['reported_turnover_£']) / df['annual_turnover_£']).clip(lower=0)
    df['priority_level'] = df['risk_band'].replace({
        'Very Low': 'Clear',
        'Low': 'Clear',
        'Medium': 'Monitor',
        'High': 'Investigate',
        'Very High': 'Investigate'
    })
    return df


def build_stakeholder_dashboard(df):
    sns.set_theme(style='whitegrid')
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

    # 1. Funnel view: priority distribution
    palette = {'Clear': '#28a745', 'Monitor': '#ffc107', 'Investigate': '#dc3545'}
    ax1 = axes[0]
    sns.countplot(x='priority_level', data=df, palette=palette, ax=ax1)
    ax1.set_title('Compliance Funnel: Case Priority Levels', fontsize=14)
    ax1.set_ylabel('Number of Taxpayers')
    ax1.set_xlabel('Action Required')
    for patch in ax1.patches:
        ax1.annotate(
            f'{int(patch.get_height()):,}',
            (patch.get_x() + patch.get_width() / 2., patch.get_height()),
            ha='center', va='center', xytext=(0, 10), textcoords='offset points'
        )

    # 2. Risk vs income / gap anomalies
    ax2 = axes[1]
    sns.scatterplot(
        x='annual_turnover_£',
        y='estimated_tax_gap_£',
        hue='priority_level',
        size='under_report_pct',
        sizes=(50, 300),
        data=df,
        palette=palette,
        alpha=0.75,
        ax=ax2,
        edgecolor='w',
        linewidth=0.5
    )
    ax2.set_title('Declared Turnover vs Estimated Tax Gap', fontsize=14)
    ax2.set_xlabel('Declared Annual Turnover (£)')
    ax2.set_ylabel('Estimated Tax Gap (£)')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    fig.suptitle('Sentinel Risk Dashboard: Executive Compliance Triage View', fontsize=16, y=1.02)
    fig.savefig(OUTPUT_IMAGE_PATH, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f'✓ Dashboard written to {OUTPUT_IMAGE_PATH}')


if __name__ == '__main__':
    df = load_risk_data(RISK_DATA_PATH)
    build_stakeholder_dashboard(df)

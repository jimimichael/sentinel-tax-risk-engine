-- Risk ranking using window functions

WITH risk_ranked AS (
    SELECT
        taxpayer_id,
        industry,
        region,
        annual_turnover_£,
        estimated_tax_gap_£,
        risk_score,
        risk_band,
        --Rank within industry
        ROW_NUMBER() OVER (PARTITION BY industry ORDER BY risk_score DESC) as rank)in_industry,
        -- Percentile rank overall
        PERCENT_RANK() OVER (ORDER BY risk_score DESC) as risk_percentile,
        -- Compare to indsutry average
        AVG(risk_score) OVER (PARTITION BY industry) as inddustry_avg_risk,
        risk_score - AVG(risk_score) OVER (PARTITION BY industry) as risk_vs_industry_avg
        FROM risk_scored_taxpayers
)
SELECT 
    taxpayer_id,
    industry,
    region,
    risk_score,
    risk_band,
    estimated_tax_gap_£,
    rank_in_industry,
    ROUND(risk_percentile * 100, 1) as risk_percentile_rank,
    ROUND(risk_vs_industry_avg, 1) as risk_vs_industry_avg
FROM risk_ranked
WHERE rank_in_industry <= 10 -- Top 10 highest risk in each industry
ORDER BY industry, risk_score DESC;
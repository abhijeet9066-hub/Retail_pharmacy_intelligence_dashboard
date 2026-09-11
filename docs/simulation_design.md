# Synthetic Retail Simulation Design

## Purpose

The medicine-details source does not contain retail sales, cost, inventory or expiry data. This project adds a transparent simulation layer for portfolio analytics.

## Reproducibility

- Random seed: `42`
- Reference date: `2026-04-01`
- Builder: `scripts/build_retail_analytics.py`

## Generated fields

- Selling price: uniform ₹50–₹500
- Purchase price: 60%–80% of simulated selling price
- Profit: selling price minus purchase price
- Profit margin: profit / selling price × 100
- Trust score: excellent review % + 0.5 × average review % − poor review %
- Monthly sales quantity: Poisson-style process around λ=30
- Expiry date: reference date + 30–719 days
- Expiry risk: High ≤30 days, Medium 31–90, Low >90
- Stock movement: Slow ≤10, Medium 11–40, Fast >40
- Competitor price: 90%–115% of simulated selling price
- Price position: Overpriced if selling price > competitor price; Competitive otherwise

`trust_score` is a portfolio scoring formula, not a clinical effectiveness score.

## Fixed April 2026 scenario date

The earlier notebook used `datetime.today()`, which made identical source data generate different expiry dates over time.

The repair uses `2026-04-01` as an explicit simulation scenario date for reproducibility. It is not a claim about source-data collection or real pharmacy inventory.

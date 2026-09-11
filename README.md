# Retail Pharmacy Intelligence Dashboard

A reproducible portfolio project that combines a public medicine-details dataset with a **clearly labeled synthetic retail-business simulation layer** for profitability, inventory movement, expiry-risk and competitor-pricing analytics.

> **Important:** Medicine metadata in `data/pharmacy_data.csv` are source data. Retail price, purchase price, profit, monthly sales, expiry date and competitor price are simulated fields created for portfolio analytics; they are not observed pharmacy transactions.

## Business Questions

- Which medicines appear most profitable under the simulated pricing assumptions?
- Which simulated inventory records are closest to expiry?
- Which products are slow-, medium- or fast-moving in the simulated sales layer?
- How do simulated selling prices compare with simulated competitor prices?
- Which manufacturers and medicines have stronger review/trust signals in the source data?

## Source Data

The committed source file is `data/pharmacy_data.csv`.

The repository notebook shows **11,825 rows and 9 source columns**: Medicine Name, Composition, Uses, Side_effects, Image URL, Manufacturer, Excellent Review %, Average Review %, and Poor Review %.

The schema and sample records match the widely circulated `Medicine_Details.csv` dataset. An external academic configuration manual attributes that dataset to **Navjot Singh — “11000 Medicine Details” (Kaggle)**:

`https://www.kaggle.com/datasets/singhnavjot2062001/11000-medicine-details`

Public mirrors of the same 11.8k-row structure also exist on Hugging Face.

Because the original download receipt/metadata is not stored in this repository, the Kaggle attribution is recorded as **probable / externally corroborated**, not as a claim provable solely from Git history.

See `docs/data_provenance.md` and `data/source_manifest.csv`.

## Synthetic Business Layer

The canonical deterministic builder is `scripts/build_retail_analytics.py`.

It adds simulated selling price, purchase price, profit, margin, monthly sales, expiry, competitor pricing and movement/risk fields.

Simulation settings:

- deterministic random seed: `42`
- fixed reference date: **2026-04-01**
- selling price: ₹50–₹500
- purchase-cost factor: 60%–80% of selling price
- competitor-price factor: 90%–115% of selling price
- expiry offset: 30–719 days
- monthly sales quantity: Poisson-style synthetic demand around λ=30

The fixed date makes the simulation reproducible. It is not the source-data collection date.

## Architecture

```text
data/pharmacy_data.csv
        ↓
scripts/build_retail_analytics.py
        ↓
outputs/retail_pharmacy_analytics.csv
        ↓
app.py (Streamlit)
```

The notebook is retained for exploratory analysis; the script is the canonical reproducible build path.

## Repository Structure

```text
.github/workflows/ci.yml
app.py
data/
  pharmacy_data.csv
  source_manifest.csv
docs/
  data_provenance.md
  simulation_design.md
  limitations.md
notebooks/
  01_pharma_analysis.ipynb
outputs/
  retail_pharmacy_analytics.csv
scripts/
  build_retail_analytics.py
  validate_repo.py
requirements.txt
README.md
```

## Run Locally

```bash
python -m pip install -r requirements.txt
python scripts/build_retail_analytics.py
streamlit run app.py
```

## Dashboard KPIs

**Source-derived:** total records, unique medicines, unique manufacturers and review/trust indicators.

**Simulated:** average profit, simulated sales, expiry-risk counts, stock movement and competitor-price position.

## Validation

```bash
python scripts/validate_repo.py
```

The validator checks source row count/schema, generated analytics fields, fixed simulation reference date, explicit synthetic labeling, notebook hygiene and repository placeholders.

## Skills Demonstrated

- data provenance
- deterministic synthetic feature generation
- Python analytics engineering
- healthcare/pharmacy business analysis
- Streamlit dashboard development
- inventory-risk logic
- reproducible repository design

## Limitations

This is a **portfolio simulation**, not a dispensing, procurement, pricing or clinical system. Simulated fields are not evidence of actual medicine prices, margins, sales volumes, expiry dates, competitor prices or inventory movement. Review percentages and `trust_score` are not clinical efficacy measures.

See `docs/limitations.md`.

## Interview Summary

> I used an 11,825-row medicine-details dataset as the descriptive source layer, then built a deterministic synthetic retail layer for price, cost, profit, monthly movement, competitor pricing and expiry-risk analytics. I separate source from simulated fields, use seed 42 and a fixed April 2026 scenario date, generate the analytical CSV through a standalone script, and document source-attribution uncertainty rather than presenting unverified download history as fact.

## Author

**Abhijeet Vasantrao Patil**  
GitHub: https://github.com/abhijeet9066-hub

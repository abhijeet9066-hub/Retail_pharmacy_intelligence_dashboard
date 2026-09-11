from __future__ import annotations

import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "pharmacy_data.csv"
OUTPUT = ROOT / "outputs" / "retail_pharmacy_analytics.csv"

SEED = 42
REFERENCE_DATE = date(2026, 4, 1)

SOURCE_MAP = {
    "Medicine Name": "medicine_name",
    "Composition": "composition",
    "Uses": "uses",
    "Side_effects": "side_effects",
    "Image URL": "image_url",
    "Manufacturer": "manufacturer",
    "Excellent Review %": "excellent_review_pct",
    "Average Review %": "average_review_pct",
    "Poor Review %": "poor_review_pct",
}

GENERATED_FIELDS = [
    "selling_price", "purchase_price", "profit", "profit_margin_pct",
    "trust_score", "monthly_sales_qty", "expiry_date", "days_to_expiry",
    "expiry_risk", "stock_movement", "competitor_price", "price_position",
    "simulation_reference_date", "business_layer_is_simulated",
]

def poisson(rng: random.Random, lam: float = 30.0) -> int:
    limit = math.exp(-lam)
    k = 0
    product = 1.0
    while product > limit:
        k += 1
        product *= rng.random()
    return k - 1

def classify_expiry(days: int) -> str:
    if days <= 30:
        return "High Risk"
    if days <= 90:
        return "Medium Risk"
    return "Low Risk"

def classify_movement(qty: int) -> str:
    if qty <= 10:
        return "Slow Moving"
    if qty <= 40:
        return "Medium Moving"
    return "Fast Moving"

def main() -> None:
    rng = random.Random(SEED)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with SOURCE.open("r", encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)
        missing = [c for c in SOURCE_MAP if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing expected source columns: {missing}")

        fieldnames = list(SOURCE_MAP.values()) + GENERATED_FIELDS
        with OUTPUT.open("w", encoding="utf-8", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=fieldnames)
            writer.writeheader()
            count = 0
            for raw in reader:
                row = {new: raw.get(old, "") for old, new in SOURCE_MAP.items()}
                excellent = float(row["excellent_review_pct"])
                average = float(row["average_review_pct"])
                poor = float(row["poor_review_pct"])

                selling = round(rng.uniform(50, 500), 2)
                purchase = round(selling * rng.uniform(0.60, 0.80), 2)
                profit = round(selling - purchase, 2)
                margin = round((profit / selling) * 100, 2)
                trust = round(excellent + 0.5 * average - poor, 2)
                qty = poisson(rng, 30.0)
                days = rng.randrange(30, 720)
                expiry = REFERENCE_DATE + timedelta(days=days)
                competitor = round(selling * rng.uniform(0.90, 1.15), 2)
                position = "Overpriced" if selling > competitor else "Competitive"

                row.update({
                    "selling_price": f"{selling:.2f}",
                    "purchase_price": f"{purchase:.2f}",
                    "profit": f"{profit:.2f}",
                    "profit_margin_pct": f"{margin:.2f}",
                    "trust_score": f"{trust:.2f}",
                    "monthly_sales_qty": qty,
                    "expiry_date": expiry.isoformat(),
                    "days_to_expiry": days,
                    "expiry_risk": classify_expiry(days),
                    "stock_movement": classify_movement(qty),
                    "competitor_price": f"{competitor:.2f}",
                    "price_position": position,
                    "simulation_reference_date": REFERENCE_DATE.isoformat(),
                    "business_layer_is_simulated": "true",
                })
                writer.writerow(row)
                count += 1

    print(f"Built {count:,} analytics rows")
    print(f"Simulation reference date: {REFERENCE_DATE.isoformat()}")
    print(f"Output: {OUTPUT}")

if __name__ == "__main__":
    main()

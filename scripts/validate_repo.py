from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

required = [
    "README.md", "requirements.txt", "app.py",
    "data/pharmacy_data.csv", "data/source_manifest.csv",
    "docs/data_provenance.md", "docs/simulation_design.md", "docs/limitations.md",
    "notebooks/01_pharma_analysis.ipynb",
    "outputs/retail_pharmacy_analytics.csv",
    "scripts/build_retail_analytics.py",
    ".github/workflows/ci.yml",
]
missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

if list(ROOT.rglob(".ipynb_checkpoints")):
    raise SystemExit("Jupyter checkpoint directories remain.")
if (ROOT / "notebooks/01_pharma_analysis.ipynb.ipynb").exists():
    raise SystemExit("Double-extension notebook still exists.")
if (ROOT / ".github/workflows/python-publish.yml").exists():
    raise SystemExit("Inappropriate PyPI workflow still exists.")

source_required = {
    "Medicine Name","Composition","Uses","Side_effects","Image URL",
    "Manufacturer","Excellent Review %","Average Review %","Poor Review %"
}
with (ROOT / "data/pharmacy_data.csv").open("r", encoding="utf-8-sig", newline="") as f:
    r = csv.DictReader(f)
    if not source_required.issubset(set(r.fieldnames or [])):
        raise SystemExit("Unexpected source schema.")
    source_count = sum(1 for _ in r)
if source_count != 11825:
    raise SystemExit(f"Expected 11,825 source rows, found {source_count}")

derived_required = {
    "medicine_name","selling_price","purchase_price","profit","monthly_sales_qty",
    "expiry_date","days_to_expiry","expiry_risk","competitor_price",
    "simulation_reference_date","business_layer_is_simulated"
}
with (ROOT / "outputs/retail_pharmacy_analytics.csv").open("r", encoding="utf-8-sig", newline="") as f:
    r = csv.DictReader(f)
    if not derived_required.issubset(set(r.fieldnames or [])):
        raise SystemExit("Generated analytics CSV is missing required fields.")
    n = 0
    refs, flags = set(), set()
    for row in r:
        n += 1
        refs.add(row["simulation_reference_date"])
        flags.add(row["business_layer_is_simulated"].lower())
if n != 11825:
    raise SystemExit(f"Expected 11,825 generated rows, found {n}")
if refs != {"2026-04-01"}:
    raise SystemExit(f"Unexpected simulation dates: {refs}")
if flags != {"true"}:
    raise SystemExit("Synthetic business layer is not explicitly labeled.")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for bad in ["abhijeetpatil-hub", "Define the concrete decision", "YYYY-MM", "TODO"]:
    if bad in readme:
        raise SystemExit(f"Blocked text remains: {bad}")

print("PASS: source dataset has 11,825 rows and expected schema")
print("PASS: derived analytics has 11,825 deterministic simulation rows")
print("PASS: simulation reference date is 2026-04-01")
print("PASS: synthetic business layer is explicitly labeled")
print("PASS: notebook/checkpoint/workflow hygiene checks passed")

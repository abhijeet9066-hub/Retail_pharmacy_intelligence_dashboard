from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "outputs" / "retail_pharmacy_analytics.csv"

st.set_page_config(page_title="Retail Pharmacy Intelligence", page_icon="💊", layout="wide")
st.title("💊 Retail Pharmacy Intelligence Dashboard")
st.caption("Medicine metadata + deterministic synthetic retail simulation.")

if not DATA.exists():
    st.error("Run `python scripts/build_retail_analytics.py` first.")
    st.stop()

df = pd.read_csv(DATA)

st.info(
    "Retail prices, profit, sales, competitor prices and expiry values are simulated. "
    f"Scenario date: {df['simulation_reference_date'].iloc[0]}."
)

with st.sidebar:
    st.header("Filters")
    manufacturers = sorted(df["manufacturer"].dropna().astype(str).unique())
    m = st.multiselect("Manufacturer", manufacturers)
    risks = sorted(df["expiry_risk"].dropna().astype(str).unique())
    r = st.multiselect("Expiry risk", risks)

view = df.copy()
if m:
    view = view[view["manufacturer"].isin(m)]
if r:
    view = view[view["expiry_risk"].isin(r)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records", f"{len(view):,}")
c2.metric("Unique Medicines", f"{view['medicine_name'].nunique():,}")
c3.metric("Avg Simulated Profit", f"₹{view['profit'].mean():,.2f}")
c4.metric("Avg Simulated Margin", f"{view['profit_margin_pct'].mean():.1f}%")

st.subheader("Top Simulated Profit Opportunities")
st.dataframe(
    view[["medicine_name","manufacturer","selling_price","purchase_price","profit","profit_margin_pct"]]
    .sort_values("profit", ascending=False).head(15),
    use_container_width=True
)

left, right = st.columns(2)
with left:
    st.subheader("Simulated Expiry Risk")
    st.bar_chart(view["expiry_risk"].value_counts())
with right:
    st.subheader("Simulated Price Position")
    st.bar_chart(view["price_position"].value_counts())

st.subheader("Highest Synthetic Expiry Priority")
st.dataframe(
    view[["medicine_name","manufacturer","days_to_expiry","expiry_risk","monthly_sales_qty","profit"]]
    .sort_values(["days_to_expiry","monthly_sales_qty"]).head(20),
    use_container_width=True
)

st.subheader("Source Review / Portfolio Trust Signal")
st.caption("`trust_score` is a portfolio formula, not a clinical effectiveness score.")
st.dataframe(
    view[["medicine_name","manufacturer","excellent_review_pct","average_review_pct","poor_review_pct","trust_score"]]
    .sort_values("trust_score", ascending=False).head(20),
    use_container_width=True
)

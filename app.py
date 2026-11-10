import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Strategic Product Placement Analysis", page_icon="🛒", layout="wide")
st.title("🛒 Strategic Product Placement Analysis")
st.caption("Explore how product placement, shelf position, and promotions relate to sales.")

DATA_FILE = Path(__file__).with_name("sample_data.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

try:
    df = load_data()
except Exception as exc:
    st.error(f"Could not load sample_data.csv: {exc}")
    st.stop()

required = {"Product", "Category", "Placement", "Shelf_Level", "Units_Sold", "Revenue", "Promotion"}
if not required.issubset(df.columns):
    st.error("The CSV is missing required columns. Please use the included sample_data.csv.")
    st.stop()

st.sidebar.header("Filters")
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
chosen_category = st.sidebar.selectbox("Product category", categories)
placements = ["All"] + sorted(df["Placement"].dropna().unique().tolist())
chosen_placement = st.sidebar.selectbox("Placement area", placements)

filtered = df.copy()
if chosen_category != "All":
    filtered = filtered[filtered["Category"] == chosen_category]
if chosen_placement != "All":
    filtered = filtered[filtered["Placement"] == chosen_placement]

if filtered.empty:
    st.warning("No rows match these filters. Try selecting All.")
    st.stop()

total_units = int(filtered["Units_Sold"].sum())
total_revenue = float(filtered["Revenue"].sum())
avg_units = float(filtered["Units_Sold"].mean())
promo_revenue = float(filtered.loc[filtered["Promotion"] == "Yes", "Revenue"].sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total units sold", f"{total_units:,}")
c2.metric("Total revenue", f"₹{total_revenue:,.0f}")
c3.metric("Average units / record", f"{avg_units:.1f}")
c4.metric("Revenue from promoted items", f"₹{promo_revenue:,.0f}")

st.subheader("Sales by placement area")
placement_summary = filtered.groupby("Placement", as_index=False).agg(
    Units_Sold=("Units_Sold", "sum"), Revenue=("Revenue", "sum")
)
fig1 = px.bar(placement_summary, x="Placement", y="Units_Sold", color="Placement",
              title="Units sold by placement", labels={"Units_Sold": "Units sold"})
st.plotly_chart(fig1, use_container_width=True)

left, right = st.columns(2)
with left:
    category_summary = filtered.groupby("Category", as_index=False)["Revenue"].sum()
    fig2 = px.pie(category_summary, names="Category", values="Revenue",
                  title="Revenue share by category")
    st.plotly_chart(fig2, use_container_width=True)
with right:
    shelf_summary = filtered.groupby("Shelf_Level", as_index=False)["Units_Sold"].mean()
    order = ["Eye Level", "Top Shelf", "Bottom Shelf"]
    shelf_summary["Shelf_Level"] = pd.Categorical(shelf_summary["Shelf_Level"], categories=order, ordered=True)
    shelf_summary = shelf_summary.sort_values("Shelf_Level")
    fig3 = px.bar(shelf_summary, x="Shelf_Level", y="Units_Sold", color="Shelf_Level",
                  title="Average units sold by shelf level",
                  labels={"Units_Sold": "Average units sold", "Shelf_Level": "Shelf level"})
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Promotion comparison")
promotion_summary = filtered.groupby("Promotion", as_index=False).agg(
    Average_Units=("Units_Sold", "mean"), Total_Revenue=("Revenue", "sum")
)
st.dataframe(promotion_summary, use_container_width=True, hide_index=True)

st.subheader("Simple data-based insights")
best_placement = placement_summary.sort_values("Units_Sold", ascending=False).iloc[0]
best_product = filtered.groupby("Product", as_index=False)["Units_Sold"].sum().sort_values("Units_Sold", ascending=False).iloc[0]
st.write(f"- **Highest-selling placement:** {best_placement['Placement']} ({int(best_placement['Units_Sold'])} units).")
st.write(f"- **Top product in the filtered data:** {best_product['Product']} ({int(best_product['Units_Sold'])} units).")
st.info("These are descriptive insights from sample data, not proof that placement caused higher sales. Replace the sample CSV with real store data before making business decisions.")

st.subheader("Filtered data")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_product_placement_data.csv", mime="text/csv")

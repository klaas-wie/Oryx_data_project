import pandas as pd
import plotly.express as px
import streamlit as st
import datetime

# Load CSV
df = pd.read_csv("russian_losses_with_dates.csv")

# Parse dates (dayfirst=True since your dates are dd-mm-yyyy)
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
df = df.dropna(subset=["date"])

st.title("📊 Russian equipment losses")

# --- Sidebar filters ---
st.sidebar.header("Filters")

# Equipment type filter
equipment_options = ["All"] + sorted(df["equipment_type"].dropna().unique())
equipment_choice = st.sidebar.selectbox("Equipment type", equipment_options)

# Category filter
category_options = ["All"] + sorted(df["category"].dropna().unique())
category_choice = st.sidebar.selectbox("Category", category_options)

# Loss type filter
loss_options = ["All"] + sorted(df["loss_type"].dropna().unique())
loss_choice = st.sidebar.selectbox("Loss type", loss_options)

# Link type filter
link_options = ["All"] + sorted(df["link_type"].dropna().unique())
link_choice = st.sidebar.selectbox("Link type", link_options)

# Date range filter: fixed from 24-02-2022 to today
start_date = st.sidebar.date_input("Start date", datetime.date(2022, 2, 24))
end_date   = st.sidebar.date_input("End date", datetime.date.today())

# Apply filters
mask = (df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))
if equipment_choice != "All":
    mask &= df["equipment_type"] == equipment_choice
if category_choice != "All":
    mask &= df["category"] == category_choice
if loss_choice != "All":
    mask &= df["loss_type"] == loss_choice
if link_choice != "All":
    mask &= df["link_type"] == link_choice

filtered = df.loc[mask]

st.markdown(f"### Showing {len(filtered)} records (of {len(df)})")

# --- Overall graphs first ---

# Monthly counts overall
monthly_counts = filtered.groupby(filtered["date"].dt.to_period("M")).size().reset_index(name="count")
monthly_counts["month_label"] = monthly_counts["date"].dt.strftime("%B")  # Only month name for hover
monthly_counts["date"] = monthly_counts["date"].dt.to_timestamp()  # Keep chronological x-axis
if not monthly_counts.empty:
    fig = px.bar(
        monthly_counts,
        x="date",
        y="count",
        title="Losses per Month (Overall)",
        hover_data={"month_label": True, "count": True, "date": False}
    )
    st.plotly_chart(fig, use_container_width=True)

# Distribution by category
cat_counts = filtered["category"].value_counts().reset_index()
cat_counts.columns = ["category", "count"]
if not cat_counts.empty:
    fig = px.bar(cat_counts, x="category", y="count", title="Distribution by Category")
    st.plotly_chart(fig, use_container_width=True)

# --- Monthly losses per category (descending order by total entries) ---
category_order = filtered["category"].value_counts().index.tolist()

for cat in category_order:
    cat_filtered = filtered[filtered["category"] == cat]
    if not cat_filtered.empty:
        monthly_counts_cat = cat_filtered.groupby(cat_filtered["date"].dt.to_period("M")).size().reset_index(name="count")
        monthly_counts_cat["month_label"] = monthly_counts_cat["date"].dt.strftime("%B")
        monthly_counts_cat["date"] = monthly_counts_cat["date"].dt.to_timestamp()  # Chronological x-axis
        fig = px.bar(
            monthly_counts_cat,
            x="date",
            y="count",
            title=f"Losses per Month - {cat}",
            hover_data={"month_label": True, "count": True, "date": False}
        )
        st.plotly_chart(fig, use_container_width=True)

# Show table of filtered data
st.subheader("Filtered Data")
st.dataframe(filtered)

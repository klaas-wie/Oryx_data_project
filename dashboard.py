import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import os

st.title("📊 Russian equipment losses Dashboard")

# --- Step 1: List CSV files ---
csv_files = [f for f in os.listdir() if f.endswith(".csv")]
if not csv_files:
    st.error("No CSV files found in the current folder.")
    st.stop()

# --- Step 2: Let user choose CSV ---
dataset_choice = st.selectbox("Choose dataset", csv_files)

# --- Step 3: Load CSV dynamically ---
df = pd.read_csv(dataset_choice)
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
df = df.dropna(subset=["date"])

# --- Sidebar filters ---
st.sidebar.header("Filters")

equipment_options = ["All"] + sorted(df["equipment_type"].dropna().unique())
equipment_choice = st.sidebar.selectbox("Equipment type", equipment_options)

category_options = ["All"] + sorted(df["category"].dropna().unique())
category_choice = st.sidebar.selectbox("Category", category_options)

loss_options = ["All"] + sorted(df["loss_type"].dropna().unique())
loss_choice = st.sidebar.selectbox("Loss type", loss_options)

link_options = ["All"] + sorted(df["link_type"].dropna().unique())
link_choice = st.sidebar.selectbox("Link type", link_options)

start_date = st.sidebar.date_input("Start date", datetime.date(2022, 2, 24))
end_date   = st.sidebar.date_input("End date", datetime.date.today())

# --- Apply filters ---
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

# --- Helper: create complete month range ---
def complete_month_range(df, start_date, end_date):
    all_months = pd.date_range(start=start_date, end=end_date, freq='MS')  # Month starts
    monthly_counts = pd.DataFrame()
    if not df.empty:
        monthly_counts = df.groupby(df["date"].dt.to_period("M")).size().reset_index(name="count")
        monthly_counts["date"] = monthly_counts["date"].dt.to_timestamp()
    complete_df = pd.DataFrame({"date": all_months})
    complete_df = complete_df.merge(monthly_counts, on="date", how="left")
    complete_df["count"] = complete_df["count"].fillna(0).astype(int)
    complete_df["month_label"] = complete_df["date"].dt.strftime("%B")
    return complete_df

# --- Chart helper ---
def plot_monthly_chart(data, title):
    fig = px.bar(
        data,
        x="date",
        y="count",
        title=title,
        hover_data={"month_label": True, "count": True, "date": False}
    )
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=data["date"],
            ticktext=data["date"].dt.strftime("%b %Y"),
            tickangle=45
        ),
        margin=dict(b=150, t=50, l=50, r=50),
        autosize=False,
        width=max(1000, len(data) * 40)  # dynamically widen based on number of months
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Overall monthly counts ---
monthly_counts = complete_month_range(filtered, start_date, end_date)
plot_monthly_chart(monthly_counts, "Losses per Month (Overall)")

# --- Distribution by category ---
cat_counts = filtered["category"].value_counts().reset_index()
cat_counts.columns = ["category", "count"]
if not cat_counts.empty:
    fig = px.bar(cat_counts, x="category", y="count", title="Distribution by Category")
    st.plotly_chart(fig, use_container_width=True)

# --- Monthly losses per category ---
category_order = filtered["category"].value_counts().index.tolist()

for cat in category_order:
    cat_filtered = filtered[filtered["category"] == cat]
    monthly_counts_cat = complete_month_range(cat_filtered, start_date, end_date)
    plot_monthly_chart(monthly_counts_cat, f"Losses per Month - {cat}")

# --- Filtered data table ---
st.subheader("Filtered Data")
st.dataframe(filtered)

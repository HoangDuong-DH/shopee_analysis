import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    layout="wide",
    page_icon="📊"
)

# Temporary data generation function (to simulate real data)
@st.cache_data
def load_sample_data():
    data = {
        "Date": pd.date_range(start="2023-01-01", periods=100, freq="D"),
        "Product": ["Product A", "Product B", "Product C"] * 34 + ["Product A"],
        "Category": ["Category 1", "Category 2", "Category 3"] * 34 + ["Category 1"],
        "Region": ["North", "South", "East", "West"] * 25,
        "Sales": [round(abs(x), 2) for x in pd.Series(range(100)).sample(100, replace=True) * 1.5],
        "Quantity": [round(x) for x in pd.Series(range(100)).sample(100, replace=True) % 10],
    }
    return pd.DataFrame(data)

# Load sample data
df = load_sample_data()

# Sidebar for user inputs
st.sidebar.header("Filter Options")
selected_product = st.sidebar.multiselect(
    "Select Product(s):",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)
selected_category = st.sidebar.multiselect(
    "Select Category(ies):",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

selected_region = st.sidebar.selectbox(
    "Select Region:",
    options=["All"] + df["Region"].unique().tolist(),
    index=0
)

# Filter data based on sidebar selections
filtered_df = df[df["Product"].isin(selected_product) & df["Category"].isin(selected_category)]
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

# Main dashboard layout
st.title("📊 Temporary Analytics Dashboard")
st.markdown("This is a temporary dashboard with sample data for analytics. Replace this placeholder with your actual implementation.")

# Display the filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Visualization: Sales Trends Over Time
st.subheader("Sales Trends Over Time")
fig1 = px.line(
    filtered_df,
    x="Date",
    y="Sales",
    color="Product",
    title="Sales Trends by Product"
)
st.plotly_chart(fig1, use_container_width=True)

# Visualization: Sales Distribution by Category
st.subheader("Sales Distribution by Category")
fig2 = px.pie(
    filtered_df,
    names="Category",
    values="Sales",
    title="Sales Distribution by Category"
)
st.plotly_chart(fig2, use_container_width=True)

# Visualization: Quantity Sold per Product
st.subheader("Quantity Sold per Product")
fig3 = px.bar(
    filtered_df,
    x="Product",
    y="Quantity",
    color="Category",
    title="Quantity Sold by Product"
)
st.plotly_chart(fig3, use_container_width=True)

# Sidebar export option
st.sidebar.header("Export Data")
if st.sidebar.button("Download Filtered Data as CSV"):
    csv_data = filtered_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

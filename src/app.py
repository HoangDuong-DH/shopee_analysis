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
    num_rows = 100  # Total number of rows to generate

    data = {
        "Date": pd.date_range(start="2023-01-01", periods=num_rows, freq="D"),
        "Product": ["Product A", "Product B", "Product C"] * (num_rows // 3) + ["Product A"] * (num_rows % 3),
        "Category": ["Category 1", "Category 2", "Category 3"] * (num_rows // 3) + ["Category 1"] * (num_rows % 3),
        "Store": ["VESTA", "Ya Samaya", "Hoang store", "Doraemon"] * (num_rows // 4) + ["Hoang store"] * (num_rows % 4),
        "Sales": [round(abs(x), 2) for x in pd.Series(range(num_rows)).sample(num_rows, replace=True) * 1.5],
        "Quantity": [round(x) % 10 for x in pd.Series(range(num_rows)).sample(num_rows, replace=True)],
    }
    return pd.DataFrame(data)

# Sidebar section: Import custom data
st.sidebar.header("Import Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Load data: Use uploaded data if available, otherwise use sample data
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("Custom data uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        df = load_sample_data()
else:
    df = load_sample_data()
    st.sidebar.info("Using sample data.")

# Ensure the dataset has required columns
required_columns = {"Date", "Product", "Category", "Store", "Sales", "Quantity"}
if not required_columns.issubset(df.columns):
    st.error(f"Uploaded data must contain the following columns: {', '.join(required_columns)}")
    st.stop()

# Sidebar for dynamic filtering options
st.sidebar.header("Filter Options")
unique_products = df["Product"].unique().tolist()
unique_categories = df["Category"].unique().tolist()
unique_Stores = ["All"] + df["Store"].unique().tolist()

selected_product = st.sidebar.multiselect(
    "Select Product(s):",
    options=unique_products,
    default=unique_products
)
selected_category = st.sidebar.multiselect(
    "Select Category(ies):",
    options=unique_categories,
    default=unique_categories
)
selected_Store = st.sidebar.selectbox(
    "Select Store:",
    options=unique_Stores,
    index=0
)

# Filter data based on sidebar selections
filtered_df = df[df["Product"].isin(selected_product) & df["Category"].isin(selected_category)]
if selected_Store != "All":
    filtered_df = filtered_df[filtered_df["Store"] == selected_Store]

# Main dashboard layout
st.title("📊 E-commerce Analytics Dashboard")
st.markdown("This dashboard provides an overview of e-commerce data. Replace this placeholder with real data.")

# Section: Data Summary
st.subheader("📋 Data Summary")
total_sales = filtered_df["Sales"].sum()
total_quantity = filtered_df["Quantity"].sum()
average_sales = filtered_df["Sales"].mean()
products_count = filtered_df["Product"].nunique()
categories_count = filtered_df["Category"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Quantity Sold", f"{total_quantity}")
col3.metric("Average Sales per Transaction", f"${average_sales:,.2f}")
col4.metric("Unique Products", f"{products_count}")
col5.metric("Unique Categories", f"{categories_count}")

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

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="RetailPulse Dashboard",
    layout="wide"
)

# =========================================
# TITLE
# =========================================

st.title("RetailPulse Customer Analytics Dashboard")

st.markdown("Interactive Retail Business Intelligence Dashboard")

# =========================================
# LOAD DATA
# =========================================

df = pd.read_csv(
    r"E:\RetailPulse_Project\data\cleaned\online_retail_eda_ready_big.csv"
)

rfm = pd.read_csv(
    r"E:\RetailPulse_Project\data\cleaned\rfm_clustered_large.csv"
)

# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.header("Dashboard Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    options=["All"] + list(df["Country"].unique())
)

# =========================================
# FILTER DATA
# =========================================

filtered_df = df.copy()

if selected_country != "All":

    filtered_df = filtered_df[
        filtered_df["Country"] == selected_country
    ]

# =========================================
# KPI SECTION
# =========================================

total_revenue = filtered_df["TotalPrice"].sum()

total_customers = filtered_df["CustomerID"].nunique()

total_orders = filtered_df["InvoiceNo"].nunique()

avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "Total Customers",
    f"{total_customers:,}"
)

col3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Average Order Value",
    f"${avg_order_value:,.2f}"
)

# =========================================
# TABS
# =========================================

tab1, tab2, tab3 = st.tabs([
    "Sales Analytics",
    "Customer Segmentation",
    "Machine Learning"
])

# =========================================
# TAB 1 : SALES ANALYTICS
# =========================================

with tab1:

    # =====================================
    # MONTHLY REVENUE TREND
    # =====================================

    st.header("Monthly Revenue Trend")

    monthly_revenue = filtered_df.groupby(
        "MonthName"
    )["TotalPrice"].sum()

    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    monthly_revenue = monthly_revenue.reindex(month_order)

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        monthly_revenue.index,
        monthly_revenue.values,
        marker="o"
    )

    ax.set_title("Monthly Revenue Trend")

    ax.set_xlabel("Month")

    ax.set_ylabel("Revenue")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    # =====================================
    # TOP PRODUCTS
    # =====================================

    st.header("Top 10 Products by Revenue")

    top_products = filtered_df.groupby(
        "Description"
    )["TotalPrice"].sum().sort_values(
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.barh(
        top_products.index,
        top_products.values
    )

    ax.set_title("Top 10 Products by Revenue")

    ax.set_xlabel("Revenue")

    ax.set_ylabel("Product")

    ax.invert_yaxis()

    st.pyplot(fig)

# =========================================
# TAB 2 : CUSTOMER SEGMENTATION
# =========================================

with tab2:

    # =====================================
    # SEGMENT DISTRIBUTION
    # =====================================

    st.header("Customer Segment Distribution")

    segment_counts = rfm["Segment"].value_counts()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        segment_counts.index,
        segment_counts.values
    )

    ax.set_title("Customer Count by Segment")

    ax.set_xlabel("Segment")

    ax.set_ylabel("Number of Customers")

    plt.xticks(rotation=15)

    st.pyplot(fig)

    # =====================================
    # REVENUE CONTRIBUTION
    # =====================================

    st.header("Revenue Contribution by Segment")

    segment_revenue = rfm.groupby(
        "Segment"
    )["Monetary"].sum().sort_values(
        ascending=False
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        segment_revenue.index,
        segment_revenue.values
    )

    ax.set_title("Revenue Contribution by Segment")

    ax.set_xlabel("Segment")

    ax.set_ylabel("Revenue")

    plt.xticks(rotation=15)

    st.pyplot(fig)

# =========================================
# TAB 3 : MACHINE LEARNING
# =========================================

with tab3:

    # =====================================
    # CUSTOMER CLUSTERS
    # =====================================

    st.header("Customer Clusters")

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(
        rfm["Frequency"],
        rfm["Monetary"],
        c=rfm["Cluster"]
    )

    ax.set_title("Customer Clusters")

    ax.set_xlabel("Frequency")

    ax.set_ylabel("Monetary")

    st.pyplot(fig)

country_revenue = filtered_df.groupby(
    "Country"
)["TotalPrice"].sum().sort_values(
    ascending=False
).head(10)
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
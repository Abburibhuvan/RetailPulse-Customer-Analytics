import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="RetailPulse Customer Analytics Dashboard",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3, h4 {
        color: white;
    }

    [data-testid="metric-container"] {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv("data/cleaned/online_retail_eda_ready_big.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "📊 Executive Overview",
        "📈 Sales Analytics",
        "👥 Customer Segmentation",
        "🧠 Customer Clustering",
        "📦 Product Analytics",
        "🌍 Country Analysis",
        "📑 Project Summary"
    ]
)

country_list = ["All"] + sorted(df["Country"].dropna().unique())

selected_country = st.sidebar.selectbox(
    "Select Country",
    country_list
)

if selected_country != "All":
    df = df[df["Country"] == selected_country]

if page == "📊 Executive Overview":
    st.title("RetailPulse Customer Analytics Dashboard")

    st.markdown("Interactive AI-Powered Retail Business Intelligence Dashboard")

    total_revenue = df["TotalPrice"].sum()
    total_customers = df["CustomerID"].nunique()
    total_orders = df["InvoiceNo"].nunique()
    avg_order_value = total_revenue / total_orders

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("Total Customers", f"{total_customers:,}")
    col3.metric("Total Orders", f"{total_orders:,}")
    col4.metric("Average Order Value", f"${avg_order_value:,.2f}")

    st.markdown("---")
    st.subheader("Monthly Revenue Trend")

    monthly_revenue = df.groupby("YearMonth")["TotalPrice"].sum()

    fig, ax = plt.subplots(figsize=(12, 5))
    monthly_revenue.plot(marker="o", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")

    st.pyplot(fig)

elif page == "📈 Sales Analytics":
    st.title("Sales Analytics")

    st.subheader("Top 10 Products by Revenue")

    top_products = (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    top_products.sort_values().plot(kind="barh", ax=ax)
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Product")

    st.pyplot(fig)

    st.subheader("Daily Revenue Trend")

    daily_revenue = (
        df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"]
        .sum()
    )

    fig2, ax2 = plt.subplots(figsize=(12, 5))
    daily_revenue.plot(ax=ax2)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Revenue")

    st.pyplot(fig2)

elif page == "👥 Customer Segmentation":
    st.title("Customer Segmentation using RFM Analysis")

    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "count",
        "TotalPrice": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    rfm["R_Score"] = pd.qcut(
        rfm["Recency"],
        4,
        labels=[4, 3, 2, 1]
    )

    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    )

    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"],
        4,
        labels=[1, 2, 3, 4]
    )

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    def segment_customer(row):
        if row["RFM_Score"] == "444":
            return "Champion"
        elif row["F_Score"] == 4:
            return "Loyal Customer"
        elif row["M_Score"] == 4:
            return "Big Spender"
        elif row["R_Score"] == 1:
            return "Lost Customer"
        elif row["R_Score"] == 2:
            return "At Risk"
        else:
            return "Others"

    rfm["Segment"] = rfm.apply(segment_customer, axis=1)

    segment_counts = rfm["Segment"].value_counts()

    st.subheader("Customer Count by Segment")

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    segment_counts.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("Segment")
    ax3.set_ylabel("Customers")

    st.pyplot(fig3)

    st.subheader("Revenue Contribution by Segment")

    segment_revenue = (
        rfm.groupby("Segment")["Monetary"]
        .sum()
        .sort_values(ascending=False)
    )

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    segment_revenue.plot(kind="bar", ax=ax4)
    ax4.set_xlabel("Segment")
    ax4.set_ylabel("Revenue")

    st.pyplot(fig4)

elif page == "🧠 Customer Clustering":
    st.title("Customer Clustering using KMeans")

    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "count",
        "TotalPrice": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)

    kmeans = KMeans(
        n_clusters=4,
        random_state=42
    )

    rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

    st.subheader("Cluster Distribution")
    st.write(rfm["Cluster"].value_counts())

    st.subheader("Cluster Scatter Plot")

    fig5, ax5 = plt.subplots(figsize=(12, 6))
    sns.scatterplot(
        x="Frequency",
        y="Monetary",
        hue="Cluster",
        data=rfm,
        palette="Set2",
        ax=ax5
    )

    st.pyplot(fig5)

elif page == "📦 Product Analytics":
    st.title("Product Analytics")

    st.subheader("Top 10 Products by Quantity Sold")

    top_quantity = (
        df.groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig6, ax6 = plt.subplots(figsize=(12, 6))
    top_quantity.sort_values().plot(kind="barh", ax=ax6)
    ax6.set_xlabel("Quantity Sold")
    ax6.set_ylabel("Product")

    st.pyplot(fig6)

    st.subheader("Top 10 Products by Revenue")

    top_revenue = (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig7, ax7 = plt.subplots(figsize=(12, 6))
    top_revenue.sort_values().plot(kind="barh", ax=ax7)
    ax7.set_xlabel("Revenue")
    ax7.set_ylabel("Product")

    st.pyplot(fig7)

elif page == "🌍 Country Analysis":
    st.title("Country Wise Analysis")

    country_revenue = (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("Top Countries by Revenue")

    fig8, ax8 = plt.subplots(figsize=(12, 6))
    country_revenue.sort_values().plot(kind="barh", ax=ax8)
    ax8.set_xlabel("Revenue")
    ax8.set_ylabel("Country")

    st.pyplot(fig8)

elif page == "📑 Project Summary":
    st.title("Project Summary")

    st.markdown(
        """
        ## RetailPulse Customer Analytics Dashboard

        This project is an end-to-end Retail Analytics and Business Intelligence platform built using Python and Streamlit.

        ### Features

        - Executive KPI Dashboard
        - Sales Analytics
        - Customer Segmentation using RFM
        - Customer Clustering using KMeans
        - Product Analytics
        - Country-wise Revenue Analysis
        - Interactive Filtering

        ### Technologies Used

        - Python
        - Pandas
        - NumPy
        - Matplotlib
        - Seaborn
        - Scikit-learn
        - Streamlit

        ### Business Benefits

        - Identify high-value customers
        - Track revenue trends
        - Improve customer retention
        - Analyze product performance
        - Support business decision making
        """
    )
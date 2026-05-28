# RetailPulse Customer Analytics Dashboard

## Project Overview

RetailPulse Customer Analytics Dashboard is an end-to-end data science and business intelligence project developed using Python, Machine Learning, and Streamlit.

The project focuses on analyzing retail transaction data to uncover business insights, customer behavior patterns, and revenue-driving customer segments.

The project includes:

* Data Cleaning
* Exploratory Data Analysis (EDA)
* Feature Engineering
* RFM Analysis
* Customer Segmentation
* KMeans Clustering
* Interactive Streamlit Dashboard

---

## Objectives

The main objectives of this project are:

* Analyze retail sales performance
* Identify high-value customers
* Discover customer purchasing behavior
* Segment customers using RFM analysis
* Apply Machine Learning clustering techniques
* Build an interactive analytics dashboard

---

## Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Streamlit

---

## Project Workflow

### 1. Data Cleaning

Performed:

* Missing value handling
* Duplicate removal
* Datatype correction
* Invalid transaction removal

### 2. Exploratory Data Analysis (EDA)

Analyzed:

* Revenue trends
* Sales by weekday
* Sales by hour
* Top customers
* Product performance
* Correlation analysis

### 3. Feature Engineering

Created:

* TotalPrice
* Year
* Month
* MonthName
* Weekday
* Hour

### 4. RFM Analysis

Calculated:

* Recency
* Frequency
* Monetary

Created customer segments:

* Champion
* Loyal Customer
* Big Spender
* At Risk
* Lost Customer
* Others

### 5. Customer Clustering

Applied:

* StandardScaler
* KMeans Clustering
* Elbow Method

Identified:

* Regular Customers
* Inactive Customers
* VIP Customers
* Ultra VIP Customers

### 6. Dashboard Development

Built an interactive Streamlit dashboard containing:

* KPI Cards
* Revenue Trends
* Product Analytics
* Customer Segmentation
* Machine Learning Cluster Visualization

---

## Key Business Insights

* Thursday generated the highest revenue.
* Afternoon hours showed peak sales activity.
* A small group of VIP customers contributed significantly to total revenue.
* Large numbers of customers belonged to inactive or low-value segments.
* Customer behavior patterns were successfully identified using clustering.

---

## Dashboard Features

### KPI Metrics

* Total Revenue
* Total Customers
* Total Orders
* Average Order Value

### Sales Analytics

* Monthly Revenue Trends
* Top Products by Revenue

### Customer Segmentation

* Customer Distribution by Segment
* Revenue Contribution by Segment

### Machine Learning Visualization

* Customer Cluster Scatter Plot

### Interactive Features

* Country Filter
* Dynamic Chart Updates
* Tab-based Navigation

---

## Project Structure

```text id="j1h0hq"
RetailPulse_Project/
│
├── dashboards/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── models/
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_rfm_analysis.ipynb
│   └── 04_customer_clustering.ipynb
│
├── reports/
│   ├── eda_insights.md
│   └── rfm_insights.md
│
├── screenshots/
│
├── README.md
│
└── requirements.txt
```

---

## How to Run the Project

### 1. Clone Repository

```bash id="fjlwm"
git clone <repository-link>
```

### 2. Install Requirements

```bash id="jlwm0m"
pip install -r requirements.txt
```

### 3. Run Streamlit Dashboard

```bash id="jlwmrf"
streamlit run app.py
```

---

## Future Improvements

* Recommendation System
* Sales Forecasting
* Customer Churn Prediction
* Advanced Interactive Visualizations
* Dashboard Deployment

---

## Author

Abburi Bhuvan

Data Science Internship Project

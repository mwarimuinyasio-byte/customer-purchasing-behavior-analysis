import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Customer Purchasing Behavior Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Customer-Purchasing-Behaviors.csv")


df = load_data()


# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------
st.title("Customer Purchasing Behavior Dataset Analysis")

st.markdown("""
This dashboard provides an interactive analysis of customer purchasing behavior,
including customer demographics, income, purchase amounts, loyalty scores,
purchase frequency, and regional distribution.
""")

st.divider()


# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.header("Dashboard Filters")

# Region Filter
regions = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

# Age Filter
min_age = int(df["age"].min())
max_age = int(df["age"].max())

age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)


# ---------------------------------------------------
# Filter Dataset
# ---------------------------------------------------
filtered_df = df[
    (df["region"].isin(regions)) &
    (df["age"].between(age_range[0], age_range[1]))
]


# ---------------------------------------------------
# Key Performance Indicators
# ---------------------------------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Average Age",
        f"{filtered_df['age'].mean():.1f}"
    )

with col3:
    st.metric(
        "Average Income",
        f"{filtered_df['annual_income'].mean():,.2f}"
    )

with col4:
    st.metric(
        "Average Purchase Amount",
        f"{filtered_df['purchase_amount'].mean():,.2f}"
    )


col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Average Loyalty Score",
        f"{filtered_df['loyalty_score'].mean():.2f}"
    )

with col6:
    st.metric(
        "Average Purchase Frequency",
        f"{filtered_df['purchase_frequency'].mean():.2f}"
    )

with col7:
    st.metric(
        "Number of Regions",
        filtered_df["region"].nunique()
    )


st.divider()


# ---------------------------------------------------
# Dataset Overview
# ---------------------------------------------------
st.header("Dataset Overview")

tab1, tab2, tab3, tab4 = st.tabs([
    "Full Dataset",
    "Dataset Information",
    "Missing Values",
    "Descriptive Statistics"
])


# Full Dataset
with tab1:

    st.subheader("Customer Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("First Five Rows")
        st.dataframe(filtered_df.head())

    with col2:
        st.subheader("Last Five Rows")
        st.dataframe(filtered_df.tail())


# Dataset Information
with tab2:

    st.subheader("Dataset Columns")

    column_info = pd.DataFrame({
        "Column Name": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str)
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )

    st.subheader("Dataset Shape")

    rows, columns = filtered_df.shape

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Number of Rows", rows)

    with col2:
        st.metric("Number of Columns", columns)


# Missing Values
with tab3:

    st.subheader("Missing Values")

    missing_values = filtered_df.isnull().sum().reset_index()

    missing_values.columns = [
        "Column",
        "Missing Values"
    ]

    st.dataframe(
        missing_values,
        use_container_width=True
    )


# Descriptive Statistics
with tab4:

    st.subheader("Statistical Summary")

    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )


st.divider()


# ---------------------------------------------------
# Visualizations
# ---------------------------------------------------
st.header("Data Visualizations")


# Row 1
col1, col2 = st.columns(2)

with col1:

    st.subheader("Customers by Region")

    region_counts = (
        filtered_df["region"]
        .value_counts()
        .reset_index()
    )

    region_counts.columns = [
        "Region",
        "Number of Customers"
    ]

    fig_region = px.bar(
        region_counts,
        x="Region",
        y="Number of Customers",
        title="Customer Distribution by Region",
        text="Number of Customers"
    )

    fig_region.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


with col2:

    st.subheader("Age Distribution")

    fig_age = px.histogram(
        filtered_df,
        x="age",
        nbins=20,
        title="Customer Age Distribution"
    )

    fig_age.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_age,
        use_container_width=True
    )


# Row 2
col1, col2 = st.columns(2)

with col1:

    st.subheader("Annual Income Distribution")

    fig_income = px.histogram(
        filtered_df,
        x="annual_income",
        nbins=30,
        title="Annual Income Distribution"
    )

    fig_income.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_income,
        use_container_width=True
    )


with col2:

    st.subheader("Purchase Amount by Region")

    fig_purchase_region = px.box(
        filtered_df,
        x="region",
        y="purchase_amount",
        title="Purchase Amount by Region",
        points=False
    )

    fig_purchase_region.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_purchase_region,
        use_container_width=True
    )


# Row 3
col1, col2 = st.columns(2)

with col1:

    st.subheader("Annual Income vs Purchase Amount")

    fig_scatter = px.scatter(
        filtered_df,
        x="annual_income",
        y="purchase_amount",
        color="region",
        size="purchase_frequency",
        hover_data=[
            "user_id",
            "age",
            "loyalty_score"
        ],
        title="Annual Income vs Purchase Amount"
    )

    fig_scatter.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


with col2:

    st.subheader("Loyalty Score by Region")

    fig_loyalty = px.box(
        filtered_df,
        x="region",
        y="loyalty_score",
        title="Loyalty Score Distribution by Region",
        points=False
    )

    fig_loyalty.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_loyalty,
        use_container_width=True
    )


# ---------------------------------------------------
# Average Values by Region
# ---------------------------------------------------
st.divider()

st.header("Regional Performance Analysis")

regional_summary = (
    filtered_df
    .groupby("region")
    .agg(
        Average_Income=("annual_income", "mean"),
        Average_Purchase_Amount=("purchase_amount", "mean"),
        Average_Loyalty_Score=("loyalty_score", "mean"),
        Average_Purchase_Frequency=("purchase_frequency", "mean")
    )
    .reset_index()
)

st.dataframe(
    regional_summary,
    use_container_width=True
)


# ---------------------------------------------------
# Average Purchase Amount by Region Chart
# ---------------------------------------------------
fig_avg_purchase = px.bar(
    regional_summary,
    x="region",
    y="Average_Purchase_Amount",
    title="Average Purchase Amount by Region",
    text_auto=".2f"
)

fig_avg_purchase.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_avg_purchase,
    use_container_width=True
)


# ---------------------------------------------------
# Download Filtered Dataset
# ---------------------------------------------------
st.divider()

st.header("Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset as CSV",
    data=csv,
    file_name="customer_purchasing_behavior_filtered.csv",
    mime="text/csv"
)
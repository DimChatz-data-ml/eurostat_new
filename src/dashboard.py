import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import plotly.express as px

load_dotenv()

st.title("Eurostat Housing Affordability Dashboard")

# --- Database connection ---
@st.cache_resource
def get_engine():
    password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    database_url = f"postgresql://postgres:{password}@localhost:5433/{db_name}"
    return create_engine(database_url)

engine = get_engine()

# --- Load data ---
@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM marts_metrics"
    return pd.read_sql(query, engine)

df = load_data()

# --- KPI cards: pick year, show ratio per country ---
years_with_data = sorted(df[df["housing_wage_ratio"].notna()]["year"].unique())
selected_year = st.selectbox("Select a year:", years_with_data, index=len(years_with_data) - 1)

year_data = df[df["year"] == selected_year]

col1, col2, col3 = st.columns(3)

for col, country in zip([col1, col2, col3], ["Germany", "Poland", "Greece"]):
    country_data = year_data[year_data["country"] == country]
    if not country_data.empty and country_data["housing_wage_ratio"].notna().any():
        ratio = country_data["housing_wage_ratio"].mean()
        col.metric(label=country, value=round(ratio, 2))
    else:
        col.metric(label=country, value="N/A")

# --- Country filter + chart ---
countries = df["country"].unique()
selected_country = st.selectbox("Select a country:", countries)

filtered_df = df[df["country"] == selected_country]
st.write(f"Showing data for: {selected_country}")
st.dataframe(filtered_df)

fig = px.line(
    filtered_df.sort_values("year"),
    x="year",
    y="housing_wage_ratio",
    title=f"Housing Affordability Ratio Over Time — {selected_country}"
)
st.plotly_chart(fig)


# Comparison of ALL countries in a single chart

st.subheader("All Countries Comparison")

fig_all = px.line(
    df.sort_values("year"),
    x="year",
    y="housing_wage_ratio",
    color="country",
    title="Housing Affordability Ratio — All Countries"
)
st.plotly_chart(fig_all)
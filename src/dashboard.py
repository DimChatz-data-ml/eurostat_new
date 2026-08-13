import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

st.title("Eurostat Housing Affordability Dashboard")
st.write("Hello! If you can see this, Streamlit is working.")

@st.cache_resource
def get_engine():
    password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    database_url = f"postgresql://postgres:{password}@localhost:5433/{db_name}"
    return create_engine(database_url)

engine = get_engine()
st.write("Database engine created successfully!")

@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM marts_metrics"
    return pd.read_sql(query, engine)

df = load_data()
st.write("Data loaded! Here are the first few rows:")
st.dataframe(df.head())
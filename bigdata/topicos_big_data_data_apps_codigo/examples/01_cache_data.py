import streamlit as st
import pandas as pd


@st.cache_data(ttl=300)
def carregar_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


df = carregar_csv(
    "data/supermarket_sales.csv"
)

st.dataframe(
    df.head()
)

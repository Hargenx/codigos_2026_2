from __future__ import annotations

import streamlit as st

from src.data import load_sales


@st.cache_data
def cached_load(path: str):
    return load_sales(path)


df = cached_load(
    st.session_state["dataset_path"]
)

st.title("Explorador de dados")

st.write(
    "Use esta página para inspecionar dados antes de criar novas análises."
)

columns = st.multiselect(
    "Colunas exibidas",
    df.columns.tolist(),
    default=[
        "Invoice ID",
        "Date",
        "City",
        "Product line",
        "Quantity",
        "Total",
        "Payment",
        "Rating",
    ],
)

if columns:
    st.dataframe(
        df.loc[:, columns],
        width="stretch",
        hide_index=True,
    )
else:
    st.info(
        "Selecione pelo menos uma coluna."
    )

st.download_button(
    "Baixar CSV tratado",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="supermarket_sales_tratado.csv",
    mime="text/csv",
)

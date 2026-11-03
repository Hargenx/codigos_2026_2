from __future__ import annotations

import streamlit as st

from src.analytics import filter_sales, kpis
from src.charts import (
    city_bar,
    monthly_line,
    payment_bar,
    product_bar,
    rating_scatter,
)
from src.data import load_sales


@st.cache_data(show_spinner="Carregando dados...")
def cached_load(path: str):
    return load_sales(path)


df = cached_load(
    st.session_state["dataset_path"]
)

st.title("Big Data Analytics — Visão geral")
st.caption(
    "Pandas + Plotly + Streamlit com separação de responsabilidades."
)

with st.sidebar.form(
    "filters",
    clear_on_submit=False,
):
    st.subheader("Filtros")

    cities = st.multiselect(
        "Cidade",
        sorted(df["City"].dropna().unique()),
        default=sorted(df["City"].dropna().unique()),
    )

    products = st.multiselect(
        "Linha de produto",
        sorted(df["Product line"].dropna().unique()),
    )

    payments = st.multiselect(
        "Forma de pagamento",
        sorted(df["Payment"].dropna().unique()),
    )

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    start_date, end_date = st.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    submitted = st.form_submit_button(
        "Aplicar filtros",
        type="primary",
        width="stretch",
    )

filtered = filter_sales(
    df,
    cities=cities,
    product_lines=products,
    payments=payments,
    start_date=start_date,
    end_date=end_date,
)

metrics = kpis(
    filtered
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Faturamento",
    f"R$ {metrics['revenue']:,.2f}",
)

col2.metric(
    "Margem bruta",
    f"{metrics['gross_margin_pct']:.2f}%",
)

col3.metric(
    "Ticket médio",
    f"R$ {metrics['avg_ticket']:,.2f}",
)

col4.metric(
    "Avaliação média",
    f"{metrics['avg_rating']:.2f}",
)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        city_bar(filtered),
        width="stretch",
    )

with right:
    st.plotly_chart(
        product_bar(filtered),
        width="stretch",
    )

st.plotly_chart(
    monthly_line(filtered),
    width="stretch",
)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        payment_bar(filtered),
        width="stretch",
    )

with right:
    st.plotly_chart(
        rating_scatter(filtered),
        width="stretch",
    )

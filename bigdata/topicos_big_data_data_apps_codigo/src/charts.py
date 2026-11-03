from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from .analytics import (
    monthly_revenue,
    revenue_by_city,
    revenue_by_payment,
    revenue_by_product,
)


def city_bar(df: pd.DataFrame) -> Figure:
    data = revenue_by_city(df)

    return px.bar(
        data,
        x="City",
        y="Revenue",
        text_auto=".2s",
        title="Faturamento por cidade",
        labels={
            "City": "Cidade",
            "Revenue": "Faturamento",
        },
    )


def product_bar(df: pd.DataFrame) -> Figure:
    data = revenue_by_product(df)

    return px.bar(
        data,
        x="Revenue",
        y="Product line",
        orientation="h",
        title="Faturamento por linha de produto",
        labels={
            "Product line": "Linha de produto",
            "Revenue": "Faturamento",
        },
    )


def monthly_line(df: pd.DataFrame) -> Figure:
    data = monthly_revenue(df)

    return px.line(
        data,
        x="Month",
        y="Revenue",
        color="City",
        markers=True,
        title="Evolução mensal do faturamento",
        labels={
            "Month": "Mês",
            "Revenue": "Faturamento",
            "City": "Cidade",
        },
    )


def payment_bar(df: pd.DataFrame) -> Figure:
    data = revenue_by_payment(df)

    return px.bar(
        data,
        x="Payment",
        y="Revenue",
        title="Faturamento por forma de pagamento",
        labels={
            "Payment": "Pagamento",
            "Revenue": "Faturamento",
        },
    )


def rating_scatter(df: pd.DataFrame) -> Figure:
    return px.scatter(
        df,
        x="Rating",
        y="Total",
        color="City",
        size="Quantity",
        hover_data=[
            "Product line",
            "Payment",
        ],
        title="Avaliação × valor da venda",
        labels={
            "Rating": "Avaliação",
            "Total": "Valor da venda",
            "City": "Cidade",
            "Quantity": "Quantidade",
        },
    )

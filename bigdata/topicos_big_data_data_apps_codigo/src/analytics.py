from __future__ import annotations

import pandas as pd


def filter_sales(
    df: pd.DataFrame,
    cities: list[str] | None = None,
    product_lines: list[str] | None = None,
    payments: list[str] | None = None,
    start_date=None,
    end_date=None,
) -> pd.DataFrame:
    """Filtra vendas sem alterar o DataFrame original."""
    mask = pd.Series(True, index=df.index)

    if cities:
        mask &= df["City"].isin(cities)

    if product_lines:
        mask &= df["Product line"].isin(product_lines)

    if payments:
        mask &= df["Payment"].isin(payments)

    if start_date is not None:
        mask &= df["Date"].dt.date >= start_date

    if end_date is not None:
        mask &= df["Date"].dt.date <= end_date

    return df.loc[mask].copy()


def kpis(df: pd.DataFrame) -> dict[str, float | int]:
    """Calcula indicadores básicos do subconjunto filtrado."""
    revenue = float(df["Total"].sum())
    cogs = float(df["cogs"].sum())
    gross_income = float(df["gross income"].sum())
    margin = (gross_income / revenue * 100) if revenue else 0.0

    return {
        "revenue": revenue,
        "cogs": cogs,
        "gross_income": gross_income,
        "gross_margin_pct": margin,
        "sales_count": int(len(df)),
        "avg_ticket": float(df["Total"].mean()) if len(df) else 0.0,
        "avg_rating": float(df["Rating"].mean()) if len(df) else 0.0,
    }


def revenue_by_city(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(
            "City",
            as_index=False,
            observed=True,
        )
        .agg(
            Revenue=("Total", "sum"),
            Sales=("Invoice ID", "nunique"),
        )
        .sort_values(
            "Revenue",
            ascending=False,
        )
    )


def revenue_by_product(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(
            "Product line",
            as_index=False,
            observed=True,
        )
        .agg(
            Revenue=("Total", "sum"),
            Quantity=("Quantity", "sum"),
        )
        .sort_values(
            "Revenue",
            ascending=False,
        )
    )


def revenue_by_payment(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(
            "Payment",
            as_index=False,
            observed=True,
        )
        .agg(
            Revenue=("Total", "sum"),
        )
        .sort_values(
            "Revenue",
            ascending=False,
        )
    )


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(
            ["Month", "City"],
            as_index=False,
            observed=True,
        )
        .agg(
            Revenue=("Total", "sum"),
        )
        .sort_values(
            ["Month", "City"]
        )
    )

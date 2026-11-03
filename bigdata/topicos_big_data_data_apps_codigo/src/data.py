from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "Invoice ID",
    "Branch",
    "City",
    "Product line",
    "Quantity",
    "Total",
    "Date",
    "Payment",
    "cogs",
    "gross income",
    "Rating",
}


def validate_schema(df: pd.DataFrame) -> None:
    """Valida as colunas mínimas esperadas pelo projeto."""
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(
            "Dataset incompatível. Colunas ausentes: "
            + ", ".join(sorted(missing))
        )


def load_sales(path: str | Path) -> pd.DataFrame:
    """Carrega, valida e prepara o dataset de vendas."""
    csv_path = Path(path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {csv_path.resolve()}"
        )

    df = pd.read_csv(csv_path)
    validate_schema(df)

    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce",
    )

    for column in [
        "Total",
        "cogs",
        "gross income",
        "Rating",
    ]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    df = (
        df
        .dropna(
            subset=[
                "Date",
                "Quantity",
                "Total",
                "cogs",
                "Rating",
            ]
        )
        .drop_duplicates()
        .sort_values("Date")
        .reset_index(drop=True)
    )

    df["Month"] = (
        df["Date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    return df

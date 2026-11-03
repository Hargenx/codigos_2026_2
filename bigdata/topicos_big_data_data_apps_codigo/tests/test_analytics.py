import pandas as pd

from src.analytics import (
    filter_sales,
    kpis,
)


def sample_df():
    return pd.DataFrame({
        "Invoice ID": ["A", "B"],
        "City": ["Rio", "São Paulo"],
        "Product line": ["X", "Y"],
        "Payment": ["Cash", "Ewallet"],
        "Date": pd.to_datetime(
            [
                "2026-01-01",
                "2026-01-02",
            ]
        ),
        "Quantity": [2, 1],
        "Total": [105.0, 210.0],
        "cogs": [100.0, 200.0],
        "gross income": [5.0, 10.0],
        "Rating": [8.0, 9.0],
    })


def test_filter_sales_by_city():
    df = sample_df()

    result = filter_sales(
        df,
        cities=["Rio"],
    )

    assert len(result) == 1
    assert result.iloc[0]["City"] == "Rio"


def test_kpis():
    result = kpis(
        sample_df()
    )

    assert result["revenue"] == 315.0
    assert result["cogs"] == 300.0
    assert result["sales_count"] == 2
    assert result["avg_ticket"] == 157.5

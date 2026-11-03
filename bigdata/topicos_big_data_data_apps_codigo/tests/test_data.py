import pandas as pd
import pytest

from src.data import validate_schema


def test_validate_schema_accepts_required_columns():
    df = pd.DataFrame(
        columns=[
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
        ]
    )

    validate_schema(df)


def test_validate_schema_rejects_missing_columns():
    df = pd.DataFrame(
        {"Total": [10.0]}
    )

    with pytest.raises(
        ValueError
    ):
        validate_schema(df)

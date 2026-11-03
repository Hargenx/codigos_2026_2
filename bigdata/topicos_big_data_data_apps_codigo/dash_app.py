from pathlib import Path

from dash import Dash, Input, Output, dcc, html
import plotly.express as px

from src.analytics import revenue_by_city
from src.data import load_sales


DATASET = Path(__file__).parent / "data" / "supermarket_sales.csv"

df = load_sales(DATASET)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Big Data Analytics — Dash"),
        dcc.Dropdown(
            id="city",
            options=[
                {"label": city, "value": city}
                for city in sorted(df["City"].unique())
            ],
            multi=True,
            placeholder="Filtre por cidade",
        ),
        dcc.Graph(id="revenue-chart"),
    ],
    style={
        "maxWidth": "1100px",
        "margin": "40px auto",
        "fontFamily": "Arial",
    },
)


@app.callback(
    Output(
        "revenue-chart",
        "figure",
    ),
    Input(
        "city",
        "value",
    ),
)
def update_chart(cities):
    filtered = df

    if cities:
        filtered = df.loc[
            df["City"].isin(cities)
        ]

    summary = revenue_by_city(
        filtered
    )

    return px.bar(
        summary,
        x="City",
        y="Revenue",
        title="Faturamento por cidade",
    )


if __name__ == "__main__":
    app.run(debug=True)

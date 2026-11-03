import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    "avaliacao": [6.5, 7.1, 8.2, 9.0],
    "valor": [250, 420, 390, 610],
    "cidade": ["A", "A", "B", "B"],
})

# Duas variáveis numéricas -> dispersão.
fig = px.scatter(
    df,
    x="avaliacao",
    y="valor",
    color="cidade",
    title="Avaliação × valor"
)

fig.show()

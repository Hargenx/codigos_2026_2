import streamlit as st

st.title("Sobre o projeto")

st.markdown(
    """
### Objetivos didáticos

- transformar análise em **data app**;
- separar carregamento, analytics e apresentação;
- usar cache somente em operações adequadas;
- evitar mutações acidentais em DataFrames;
- escolher gráficos compatíveis com a pergunta;
- preparar a aplicação para crescer sem misturar tudo em `app.py`.

### Arquitetura

```text
app / pages
    ↓
analytics / charts
    ↓
data
    ↓
CSV / Parquet / camada curada
```

Em cenários realmente grandes, o dashboard deve consumir
dados **agregados/curados**, não bilhões de eventos brutos.
"""
)

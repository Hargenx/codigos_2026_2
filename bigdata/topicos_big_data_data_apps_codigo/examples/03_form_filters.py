import streamlit as st

with st.form(
    "filtros"
):
    cidade = st.selectbox(
        "Cidade",
        [
            "Yangon",
            "Mandalay",
            "Naypyitaw",
        ]
    )

    periodo = st.date_input(
        "Período",
        value=[]
    )

    aplicar = st.form_submit_button(
        "Aplicar"
    )

if aplicar:
    st.write(
        cidade,
        periodo
    )

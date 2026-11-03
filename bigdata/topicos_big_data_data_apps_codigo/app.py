from __future__ import annotations

from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Big Data Analytics",
    page_icon="📊",
    layout="wide",
)

DATASET = Path(__file__).parent / "data" / "supermarket_sales.csv"

st.session_state.setdefault(
    "dataset_path",
    str(DATASET),
)

pages = {
    "Analytics": [
        st.Page(
            "pages/overview.py",
            title="Visão geral",
            icon="📊",
            default=True,
        ),
        st.Page(
            "pages/explorer.py",
            title="Explorador",
            icon="🔎",
        ),
    ],
    "Projeto": [
        st.Page(
            "pages/about.py",
            title="Sobre",
            icon="ℹ️",
        ),
    ],
}

navigation = st.navigation(
    pages
)

navigation.run()

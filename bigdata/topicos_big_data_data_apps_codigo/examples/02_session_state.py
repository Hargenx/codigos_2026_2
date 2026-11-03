import streamlit as st

st.session_state.setdefault(
    "contador",
    0
)

if st.button(
    "Incrementar"
):
    st.session_state["contador"] += 1

st.metric(
    "Contador",
    st.session_state["contador"]
)

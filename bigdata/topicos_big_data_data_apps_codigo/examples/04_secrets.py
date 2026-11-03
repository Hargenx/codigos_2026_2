import streamlit as st

# Configure em .streamlit/secrets.toml
# Nunca publique o arquivo real no repositório.

if "database" in st.secrets:
    host = st.secrets["database"]["host"]
    st.write(
        "Host configurado:",
        host
    )
else:
    st.info(
        "Crie .streamlit/secrets.toml para testar este exemplo."
    )

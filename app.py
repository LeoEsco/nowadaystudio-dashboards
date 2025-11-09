import streamlit as st
import streamlit_authenticator as stauth

config = {
    "credentials": {
        "usernames": {
            "nowadays": {"name": "Nowadays Studio", "password": "1234"},
            "botanerolimon": {"name": "Botanero Limón", "password": "abcd"},
            "nue": {"name": "Nue Lengiere", "password": "5678"},
        }
    },
    "cookie": {"name": "nowadays_cookie", "key": "abc123", "expiry_days": 1},
}

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.login(location="main")

if st.session_state["authentication_status"]:
    authenticator.logout("Salir", location="sidebar")
    st.sidebar.success(f"Bienvenido, {st.session_state['name']}")
    st.write(f"Dashboard privado de {st.session_state['name']}")
elif st.session_state["authentication_status"] is False:
    st.error("Usuario o contraseña incorrectos")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, inicia sesión")
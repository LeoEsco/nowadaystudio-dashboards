import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- Cargar configuración ---
@st.cache_resource
def load_config():
    with open("config.yaml") as file:
        return yaml.load(file, Loader=SafeLoader)

config = load_config()

# --- Autenticación ---
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.login(location="main")

# --- Interfaz principal ---
if st.session_state["authentication_status"]:
    authenticator.logout("Salir", location="sidebar")
    st.sidebar.success(f"Bienvenido, {st.session_state['name']}")

    username = st.session_state["username"]

    # --- Mostrar dashboard correspondiente ---
    if username == "botanerolimon":
        import clientes.botanero_limon as dashboard
        dashboard.show()
    elif username == "nowadays":
        import clientes.nowadays_studio as dashboard
        dashboard.show()
    elif username == "nue":
        import clientes.nue_lingerie as dashboard
        dashboard.show()
    else:
        st.warning("Usuario sin dashboard asignado.")

elif st.session_state["authentication_status"] is False:
    st.error("Usuario o contraseña incorrectos")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, inicia sesión")

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import clientes.nowadays_studio as nowadays_studio

# Cargar configuración
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Autenticación
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login(location='sidebar')

if st.session_state["authentication_status"]:
    authenticator.logout("Salir", location='sidebar')
    st.sidebar.title(f"Bienvenido, {st.session_state['name']}")
    opcion = st.sidebar.selectbox("Sección", ["Dashboard"])
    if opcion == "Dashboard":
        nowadays_studio.mostrar()
elif st.session_state["authentication_status"] is False:
    st.error("Usuario o contraseña incorrectos")
elif st.session_state["authentication_status"] is None:
    st.warning("Ingresa tus credenciales")
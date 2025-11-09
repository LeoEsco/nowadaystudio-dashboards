import streamlit as st

def show():
    st.title("Dashboard - Nowadays Studio")
    st.write("Bienvenido al panel interno de Nowadays Studio.")
    st.metric("Proyectos activos", 5)
    st.metric("Clientes totales", 8)

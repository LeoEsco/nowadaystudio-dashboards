import streamlit as st

def show():
    st.title("Dashboard - Nue Lingerie")
    st.write("Bienvenida al panel de ventas de Nue Lingerie.")
    st.metric("Ventas del mes", "$12,800")
    st.metric("Pedidos pendientes", 9)

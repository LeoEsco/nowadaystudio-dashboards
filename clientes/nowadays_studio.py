# app.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

def mostrar():
    st.set_page_config(page_title="Nowadays Studio — Resumen financiero", layout="wide")

    # --- Paleta de marca ---
    COLOR_INGRESOS = "#af2b2a"
    COLOR_GASTOS = "#28211f"
    COLOR_BG = "#c8c6c4"

    # --- Encabezado ---
    st.markdown(
        f"""
        <div style="padding:16px; border-radius:8px; background:{COLOR_BG};">
            <h1 style="margin:0; color:{COLOR_INGRESOS};">Nowadays Studio</h1>
            <div style="color:{COLOR_GASTOS};">Resumen financiero</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # --- Datos de ejemplo ---
    meses = pd.date_range("2025-01-01", "2025-12-01", freq="MS").strftime("%Y-%m")
    np.random.seed(42)
    ingresos = np.random.randint(1000, 5000, size=len(meses))
    gastos = np.random.randint(1000, 5000, size=len(meses))

    df = pd.DataFrame({
        "Mes": meses,
        "Ingresos": ingresos,
        "Gastos": gastos
    })
    df["Utilidad"] = df["Ingresos"] - df["Gastos"]
    df["mes_dt"] = pd.to_datetime(df["Mes"] + "-01")

    st.session_state.df = df  # solo para mantener consistencia

    # --- Visualizaciones ---
    st.subheader("Visualizaciones")

    left, right = st.columns([2, 1])

    with left:
        base = alt.Chart(df).encode(x=alt.X("mes_dt:T", title="Mes", axis=alt.Axis(format="%b")))
        line_ing = base.mark_line(point=True, color=COLOR_INGRESOS).encode(y="Ingresos:Q")
        line_gas = base.mark_line(point=True, color=COLOR_GASTOS).encode(y="Gastos:Q")
        st.altair_chart((line_ing + line_gas).properties(height=320), use_container_width=True)

        df_melt = df.melt(id_vars=["Mes", "mes_dt"], value_vars=["Ingresos", "Gastos"], var_name="Tipo", value_name="Monto")
        bar = alt.Chart(df_melt).mark_bar().encode(
            x=alt.X("mes_dt:T", title="Mes", axis=alt.Axis(format="%b")),
            y="Monto:Q",
            color=alt.Color("Tipo:N", scale=alt.Scale(domain=["Ingresos","Gastos"], range=[COLOR_INGRESOS, COLOR_GASTOS]))
        ).properties(height=260)
        st.altair_chart(bar, use_container_width=True)

    with right:
        st.subheader("KPIs")
        total_ingresos = df["Ingresos"].sum()
        total_gastos = df["Gastos"].sum()
        utilidad_neta = df["Utilidad"].sum()
        st.metric("Total Ingresos", f"${total_ingresos:,.0f}")
        st.metric("Total Gastos", f"${total_gastos:,.0f}")
        st.metric("Utilidad Neta", f"${utilidad_neta:,.0f}", delta=f"${utilidad_neta:,.0f}")

    # --- Tabla resumen ---
    st.subheader("Tabla resumen")
    df_display = df.copy()

    # Forzar numérico solo por seguridad
    for col in ["Ingresos", "Gastos", "Utilidad"]:
        df_display[col] = pd.to_numeric(df_display[col], errors="coerce")

    # Mostrar sin formato de moneda (evita el error)
    st.dataframe(df_display[["Mes", "Ingresos", "Gastos", "Utilidad"]])

    st.info("Datos generados aleatoriamente entre $1,000 y $5,000 MXN por mes (solo demostración).")

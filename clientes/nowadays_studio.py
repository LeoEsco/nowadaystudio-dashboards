import streamlit as st
import pandas as pd
import altair as alt

def show():
    st.title("Dashboard - Nowadays Studio")
    st.write("Panel financiero interno de Nowadays Studio.")

    # --- PROYECTOS ACTIVOS (TABLA) ---
    st.subheader("Proyectos activos")
    data_proyectos = [
        ["Botanero Limón", "Mantenimiento", "1,000 MXN/mes"],
        ["Nue Lingerie", "En construcción", "3,000 MXN pendientes + 1,500 MXN/mes (desde enero)"],
        ["Pangas", "En negociación", "20,000 MXN inicial + 15,000 MXN/mes (desde enero)"],
        ["Mullix", "En negociación", "5,000 MXN inicial + 1,000 MXN/mes (desde enero)"],
    ]
    df_proyectos = pd.DataFrame(data_proyectos, columns=["Proyecto", "Estado", "Precio"])
    st.dataframe(df_proyectos.style.set_properties(**{
        'font-size': '16px', 'text-align': 'center'
    }), use_container_width=True)

    # --- DATOS DE INGRESOS MENSUALES ---
    meses = pd.date_range("2025-05-01", periods=12, freq="MS").strftime("%B %Y")

    real = [1000]*12

    nue = [1000]*6 + [1000, 1000, 1000, 1000, 4000, 1000]
    nue[6] = 4000      # noviembre ingreso de 3k
    for i in range(8, 12):
        nue[i] = 2500  # mantenimiento desde enero

    mullix = [1000]*6 + [1000, 1000, 1000, 1000, 6000, 1000]
    mullix[6] = 6000
    for i in range(8, 12):
        mullix[i] = 2000

    pangas = [1000]*6 + [1000, 1000, 1000, 1000, 21000, 1000]
    pangas[6] = 21000
    for i in range(8, 12):
        pangas[i] = 16000

    todo = [1000]*6 + [28000, 1000, 18500, 18500, 18500, 18500]  # inyección en nov, baja dic, mantenimiento desde ene

    df = pd.DataFrame({
        "Mes": list(meses)*5,
        "Escenario": (
            ["Real"]*12 +
            ["+ Nue"]*12 +
            ["+ Mullix"]*12 +
            ["+ Pangas"]*12 +
            ["Todo cerrado"]*12
        ),
        "Ingresos": real + nue + mullix + pangas + todo
    })

    # --- COLORES (ajustados para fondo oscuro) ---
    colores = {
        "Real": "#6a5acd",
        "+ Nue": "#ff6b6b",
        "+ Mullix": "#4ecdc4",
        "+ Pangas": "#ffe66d",
        "Todo cerrado": "#ff9ff3"
    }

    # --- GRÁFICA ---
    st.subheader("Proyección de ingresos mensuales por escenario")
    chart = (
        alt.Chart(df)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("Mes:N", sort=None, title="Mes", axis=alt.Axis(labelAngle=0, labelFontSize=14)),
            y=alt.Y("Ingresos:Q", title="MXN", axis=alt.Axis(labelFontSize=14)),
            color=alt.Color("Escenario:N",
                            scale=alt.Scale(domain=list(colores.keys()),
                                            range=list(colores.values())),
                            legend=alt.Legend(title="Escenario")),
            tooltip=["Mes", "Escenario", "Ingresos"]
        )
        .properties(height=450, width=850)
    )

    st.altair_chart(chart, use_container_width=True)

    # --- NOTAS EXPLICATIVAS ---
    st.markdown("""
    **Notas:**
    - **Azul violeta:** Ingresos reales (solo Botanero Limón).  
    - **Rojo coral:** Cierre de *Nue Lingerie* en noviembre (mantenimiento desde enero).  
    - **Turquesa:** Cierre de *Mullix* en noviembre (mantenimiento desde enero).  
    - **Amarillo cálido:** Cierre de *Pangas* en noviembre (mantenimiento desde enero).  
    - **Rosa neón:** Escenario general: todos los proyectos cerrados en noviembre, mantenimientos activos desde enero 2026.
    """)

import streamlit as st
import pandas as pd
import plotly.express as px

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

    nue = [1000]*12
    nue[6] = 4000       # noviembre: ingreso pendiente
    for i in range(8, 12):
        nue[i] = 2500   # mantenimiento desde enero

    mullix = [1000]*12
    mullix[6] = 6000
    for i in range(8, 12):
        mullix[i] = 2000

    pangas = [1000]*12
    pangas[6] = 21000
    for i in range(8, 12):
        pangas[i] = 16000

    todo = [1000]*12
    todo[6] = 28000     # noviembre: cobro total
    todo[7] = 1000      # diciembre: solo Botanero
    for i in range(8, 12):
        todo[i] = 18500 # mantenimiento desde enero

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

    # --- COLORES ---
    colores = {
        "Real": "#6a5acd",
        "+ Nue": "#ff6b6b",
        "+ Mullix": "#4ecdc4",
        "+ Pangas": "#ffe66d",
        "Todo cerrado": "#ff9ff3"
    }

    # --- GRÁFICA (Plotly, responsiva) ---
    st.subheader("Proyección de ingresos mensuales por escenario")

    fig = px.line(
        df,
        x="Mes",
        y="Ingresos",
        color="Escenario",
        color_discrete_map=colores,
        markers=True,
        title="Proyección de ingresos mensuales"
    )

    fig.update_layout(
        template="plotly_dark",
        title_font_size=18,
        legend_title_text="Escenario",
        legend_font_size=12,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified"
    )

    fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig.update_yaxes(title="MXN", tickfont=dict(size=10))

    st.plotly_chart(fig, use_container_width=True)

    # --- NOTAS EXPLICATIVAS ---
    st.markdown("""
    **Notas:**
    - **Azul violeta:** Ingresos reales (solo Botanero Limón).  
    - **Rojo coral:** Cierre de *Nue Lingerie* en noviembre (mantenimiento desde enero).  
    - **Turquesa:** Cierre de *Mullix* en noviembre (mantenimiento desde enero).  
    - **Amarillo cálido:** Cierre de *Pangas* en noviembre (mantenimiento desde enero).  
    - **Rosa neón:** Todos los proyectos cerrados en noviembre; mantenimientos activos desde enero 2026.
    """)

# Para ejecutar directamente (si no usas multipage)
if __name__ == "__main__":
    show()

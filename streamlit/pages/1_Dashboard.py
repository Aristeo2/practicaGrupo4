import pandas as pd
import streamlit as st
import plotly.express as px
import requests

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data(url: str):
    """
    Función para cargar los datos desde la API.
    """
    try:
        r = requests.get(url)
        r.raise_for_status()  # Verifica que la solicitud fue exitosa (status 200)
        listado = r.json()  # Aquí esperamos una lista directamente
        df = pd.DataFrame.from_records(listado)
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # Convertir la columna de fecha
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectarse a la API: {e}")
        return pd.DataFrame()
    except ValueError as e:
        st.error(f"Error al procesar los datos: {e}")
        return pd.DataFrame()

# Cargar datos desde la API
api_url = "http://fastapi:8000/contratos"  # Cambiar si es necesario
df_merged = load_data(api_url)

if df_merged.empty:
    st.error("No se pudieron cargar los datos. Verifica la conexión con la API.")
else:
    # Calcular estadísticas generales
    registros = str(df_merged.shape[0])
    adjudicatarios = str(len(df_merged.adjuducatario.unique()))
    centro = str(len(df_merged.centro_seccion.unique()))
    tipologia = str(len(df_merged.tipo.unique()))
    presupuesto_medio = str(round(df_merged.presupuesto_con_iva.mean(), 2))
    adjudicado_medio = str(round(df_merged.importe_adj_con_iva.mean(), 2))

    st.title("🔎 Dashboard Mejorado de Contratos")
    st.header("📊 Resumen General")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("# Contratos", registros)
    with col2:
        st.metric("# Adjudicatarios", adjudicatarios)
    with col3:
        st.metric("# Centros", centro)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("# Tipologías", tipologia)
    with col5:
        st.metric("Presupuesto Medio", f"{presupuesto_medio} €")
    with col6:
        st.metric("Importe Medio Adjudicado", f"{adjudicado_medio} €")

    st.header("🎨 Visualizaciones")
    fig1 = px.scatter(
        df_merged,
        x='importe_adj_con_iva',
        y='presupuesto_con_iva',
        color='procedimiento',
        title="Relación entre Importe Adjudicado y Presupuesto",
    )
    st.plotly_chart(fig1, use_container_width=True)

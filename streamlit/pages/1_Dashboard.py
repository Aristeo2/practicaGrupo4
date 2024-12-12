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
@st.cache_data
def load_facturas(url: str):
    """
    Función para cargar los datos de facturas desde la API.
    """
    try:
        r = requests.get(url)
        r.raise_for_status()  # Verifica que la solicitud fue exitosa (status 200)
        listado = r.json()  # Aquí esperamos una lista directamente
        df = pd.DataFrame.from_records(listado)

        # Procesar las columnas clave
        df['fecha_cita'] = pd.to_datetime(df['fecha_cita'], errors='coerce')  # Convertir la fecha de la cita
        df['precio'] = pd.to_numeric(df['precio'], errors='coerce')  # Convertir el precio a numérico
        df['id_cliente'] = df['id_cliente'].astype(str)  # Asegurarse de que los IDs de cliente sean cadenas
        df['tratamiento'] = df['tratamiento'].astype(str)  # Convertir tratamiento a texto

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
api_url_facturas = "http://fastapi:8000/facturas"  # Cambiar si es necesario
df_facturas = load_facturas(api_url_facturas)

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
    

    fig2 = px.box(
    df_merged.query("procedimiento == 'Negociado sin publicidad'"),
    x='importe_adj_con_iva',
    title="Distribución del Importe Adjudicado en 'Negociado sin Publicidad'",
    labels={'importe_adj_con_iva': 'Importe Adjudicado (€)'},
    color_discrete_sequence=['#FF6347'],
    template='plotly_white'
)
    fig2.update_traces(boxpoints='all', jitter=0.3, marker_color='#FF5733', line_color='black')


    fig3 = px.bar(
        df_merged.groupby('tipo').agg(total_presupuesto=('presupuesto_con_iva', 'sum')).reset_index(),
        x='tipo',
        y='total_presupuesto',
        color='tipo',
        title="Presupuesto Total por Tipología",
        labels={'tipo': 'Tipología', 'total_presupuesto': 'Presupuesto Total (€)'},
        template='plotly_white',
        text_auto=True
)
if 'fecha' in df_merged.columns and not df_merged['fecha'].isnull().all():
    contratos_por_mes = (
        df_merged.groupby(df_merged['fecha'].dt.to_period('M'))
        .agg(num_contratos=('fecha', 'size'), total_costo=('importe_adj_con_iva', 'sum'))
        .reset_index()
    )
    contratos_por_mes['fecha'] = contratos_por_mes['fecha'].dt.to_timestamp()

    fig4 = px.line(
        contratos_por_mes,
        x='fecha',
        y='num_contratos',
        markers=True,
        title="Evolución Mensual del Número de Contratos",
        labels={'fecha': 'Fecha', 'num_contratos': 'Número de Contratos'},
        hover_data={'total_costo': ':,.2f'},
        color_discrete_sequence=['#8e44ad'],
        template='plotly_white'
    )
else:
    fig4 = None
tabs = st.tabs(["Relación Importe-Presupuesto", "Distribución Negociado", "Presupuesto por Tipologías", "Evolución Mensual"])
with tabs[0]:
    st.plotly_chart(fig1, use_container_width=True)
with tabs[1]:
    st.plotly_chart(fig2, use_container_width=True)
with tabs[2]:
    st.plotly_chart(fig3, use_container_width=True)
if fig4 is not None:
    with tabs[3]:
        st.plotly_chart(fig4, use_container_width=True)
else:
    with tabs[3]:
        st.write("No hay datos disponibles para mostrar la evolución mensual.")

if not df_facturas.empty:
    st.header("📊 Análisis de Facturas")
    
    # Gráfico 1: Ingresos Mensuales
    facturas_por_mes = (
        df_facturas.groupby(df_facturas['fecha_cita'].dt.to_period('M'))
        .agg(total_ingresos=('precio', 'sum'))
        .reset_index()
    )
    facturas_por_mes['fecha_cita'] = facturas_por_mes['fecha_cita'].dt.to_timestamp()

    fig_ingresos_mensuales = px.line(
        facturas_por_mes,
        x='fecha_cita',
        y='total_ingresos',
        title="Evolución de Ingresos Mensuales",
        labels={'fecha_cita': 'Mes', 'total_ingresos': 'Ingresos (€)'},
        markers=True,
        template='plotly_white'
    )

    # Gráfico 2: Distribución de Precios
    fig_distribucion_precios = px.box(
        df_facturas,
        y='precio',
        title="Distribución de Precios de Facturas",
        labels={'precio': 'Precio (€)'},
        template='plotly_white'
    )
    fig_distribucion_precios.update_traces(boxpoints='all', jitter=0.3)

    # Gráfico 3: Facturas por Tratamiento
    facturas_por_tratamiento = (
        df_facturas.groupby('tratamiento')
        .agg(cantidad_facturas=('tratamiento', 'size'))
        .reset_index()
    )
    fig_facturas_tratamiento = px.bar(
        facturas_por_tratamiento,
        x='tratamiento',
        y='cantidad_facturas',
        title="Facturas por Tratamiento",
        labels={'tratamiento': 'Tratamiento', 'cantidad_facturas': 'Cantidad de Facturas'},
        text_auto=True,
        template='plotly_white'
    )

    # Gráfico 4: Top Clientes por Gastos
    top_clientes = (
        df_facturas.groupby('id_cliente')
        .agg(total_gastado=('precio', 'sum'))
        .reset_index()
        .sort_values(by='total_gastado', ascending=False)
        .head(10)
    )
    fig_top_clientes = px.bar(
        top_clientes,
        x='id_cliente',
        y='total_gastado',
        title="Top 10 Clientes por Gastos",
        labels={'id_cliente': 'Cliente', 'total_gastado': 'Gasto Total (€)'},
        text_auto=True,
        template='plotly_white'
    )

    # Mostrar Gráficos
    tabs_facturas = st.tabs(["Ingresos Mensuales", "Distribución de Precios", "Facturas por Tratamiento", "Top Clientes"])
    with tabs_facturas[0]:
        st.plotly_chart(fig_ingresos_mensuales, use_container_width=True)
    with tabs_facturas[1]:
        st.plotly_chart(fig_distribucion_precios, use_container_width=True)
    with tabs_facturas[2]:
        st.plotly_chart(fig_facturas_tratamiento, use_container_width=True)
    with tabs_facturas[3]:
        st.plotly_chart(fig_top_clientes, use_container_width=True)
else:
    st.warning("No hay datos de facturas disponibles para análisis.")
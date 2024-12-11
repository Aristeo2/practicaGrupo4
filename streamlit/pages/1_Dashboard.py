import pandas as pd
import streamlit as st
import plotly.express as px
import requests
import seaborn as sns

# Configuración de estilo general del dashboard
st.set_page_config(
    page_title="Dashboard",
    page_icon="🌟",
    layout="wide",
)

@st.cache_data
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    mijson = r.json()
    listado = mijson['contratos']
    df = pd.DataFrame.from_records(listado)
    df['importe_adj_con_iva'] = df['importe_adj_con_iva'].str.replace('€', '').str.replace('.', '').str.replace(',', '.')
    df['presupuesto_con_iva'] = df['presupuesto_con_iva'].str.replace('€', '').str.replace('.', '').str.replace(',', '.')
    df['presupuesto_con_iva'] = df['presupuesto_con_iva'].astype(float)
    df['importe_adj_con_iva'] = df['importe_adj_con_iva'].astype(float)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # Convertir la columna de fecha
    return df

def info_card(title, value, icon, color):
    st.markdown(
        f"""
        <div style="background-color:{color}; padding: 10px; border-radius: 8px; text-align: center;">
            <h3 style="color:white;">{icon} {title}</h3>
            <p style="font-size: 24px; color:white;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

df_merged = load_data('http://fastapi:8000/retrieve_data')

# Calcular estadísticas generales
registros = str(df_merged.shape[0])
adjudicatarios = str(len(df_merged.adjuducatario.unique()))
centro = str(len(df_merged.centro_seccion.unique()))
tipologia = str(len(df_merged.tipo.unique()))
presupuesto_medio = str(round(df_merged.presupuesto_con_iva.mean(), 2))
adjudicado_medio = str(round(df_merged.importe_adj_con_iva.mean(), 2))

sns.set_palette("pastel")

# Título del dashboard
st.title("🔎 Dashboard Mejorado de Seguimiento ")

# Información general en tarjetas
st.header("📊 Resumen General")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    info_card("# Contratos", registros, "📈", "#3498db")
with col2:
    info_card("# Adjudicatarios", adjudicatarios, "💼", "#2ecc71")
with col3:
    info_card("# Centros", centro, "🏢", "#e74c3c")

with col4:
    info_card("# Tipologías", tipologia, "🔹", "#f39c12")
with col5:
    info_card("Presupuesto Medio", f"{presupuesto_medio} €", "💵", "#9b59b6")
with col6:
    info_card("Importe Medio Adjudicado", f"{adjudicado_medio} €", "💳", "#1abc9c")

# Visualizaciones
st.header("🎨 Visualizaciones Interactivas")

# Relación entre importe adjudicado y presupuesto
fig1 = px.scatter(
    df_merged,
    x='importe_adj_con_iva',
    y='presupuesto_con_iva',
    size='numlicit',
    color='procedimiento',
    title="Relación entre Importe Adjudicado y Presupuesto",
    labels={'importe_adj_con_iva': 'Importe Adjudicado (€)', 'presupuesto_con_iva': 'Presupuesto (€)'},
    hover_data=['tipo'],
    template='plotly_white'
)
fig1.update_traces(marker=dict(opacity=0.6, line=dict(width=0.5, color='DarkSlateGrey')))

# Distribución de importe adjudicado en 'Negociado sin publicidad'
fig2 = px.box(
    df_merged.query("procedimiento == 'Negociado sin publicidad'"),
    x='importe_adj_con_iva',
    title="Distribución del Importe Adjudicado en 'Negociado sin Publicidad'",
    labels={'importe_adj_con_iva': 'Importe Adjudicado (€)'},
    color_discrete_sequence=['#FF6347'],
    template='plotly_white'
)
fig2.update_traces(boxpoints='all', jitter=0.3, marker_color='#FF5733', line_color='black')

# Distribución por tipología
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

# Contratos por mes
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

# Mostrar visualizaciones
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

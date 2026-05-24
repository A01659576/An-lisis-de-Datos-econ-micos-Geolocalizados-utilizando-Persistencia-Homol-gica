import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Salud ZMVM",
    page_icon="🏥",
    layout="wide"
)



# ── Estilos ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.title-block {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
}
.title-block h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.title-block p {
    font-size: 0.95rem;
    opacity: 0.7;
    margin: 0;
}

.metric-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #0f2027;
    line-height: 1;
}
.metric-card .label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.4rem;
}
.metric-card .sub {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f2027;
    border-left: 4px solid #2c5364;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    hosp_cdmx   = pd.read_csv('hospitales_cdmx.csv')
    hosp_edomex = pd.read_csv('hospitales_edomex.csv')
    cons_cdmx   = pd.read_csv('consultorios_cdmx.csv')
    cons_edomex = pd.read_csv('consultorios_edomex.csv')
    return hosp_cdmx, hosp_edomex, cons_cdmx, cons_edomex

hosp_cdmx, hosp_edomex, cons_cdmx, cons_edomex = cargar_datos()
st.write(hosp_cdmx.head())

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
    <h1>🏥 Análisis de Servicios de Salud — ZMVM</h1>
    <p>Sector salud (código 62) · DENUE 2025 · CDMX y Estado de México</p>
</div>
""", unsafe_allow_html=True)

# ── Filtro de entidad ─────────────────────────────────────────────────────────
entidad = st.radio(
    "Entidad",
    ["CDMX", "EdoMex", "Ambas"],
    horizontal=True
)

if entidad == "CDMX":
    hosp   = hosp_cdmx
    cons   = cons_cdmx
    label_mun = "Alcaldía"
elif entidad == "EdoMex":
    hosp   = hosp_edomex
    cons   = cons_edomex
    label_mun = "Municipio"
else:
    hosp   = pd.concat([hosp_cdmx, hosp_edomex])
    cons   = pd.concat([cons_cdmx, cons_edomex])
    label_mun = "Municipio / Alcaldía"

# ── Métricas ──────────────────────────────────────────────────────────────────
hosp_por_mun = hosp['municipio'].value_counts()
cons_por_mun = cons['municipio'].value_counts()

top_hosp_mun  = hosp_por_mun.idxmax()
low_hosp_mun  = hosp_por_mun.idxmin()
top_cons_mun  = cons_por_mun.idxmax()
low_cons_mun  = cons_por_mun.idxmin()

# municipios sin hospitales
dist = pd.concat([
    hosp['municipio'].value_counts().rename('hospitales'),
    cons['municipio'].value_counts().rename('consultorios')
], axis=1).fillna(0).astype(int)
sin_hosp = (dist['hospitales'] == 0).sum()

cols = st.columns(6)
metrics = [
    (f"{len(hosp):,}",        "Hospitales",             ""),
    (f"{len(cons):,}",        "Consultorios",           ""),
    (top_hosp_mun,            "Más hospitales",         f"{hosp_por_mun[top_hosp_mun]}"),
    (low_hosp_mun,            "Menos hospitales",       f"{hosp_por_mun[low_hosp_mun]}"),
    (top_cons_mun,            "Más consultorios",       f"{cons_por_mun[top_cons_mun]}"),
    (f"{sin_hosp}",           "Sin hospitales",         "municipios/alcaldías"),
]
for col, (val, label, sub) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{val}</div>
            <div class="label">{label}</div>
            <div class="sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Mapa ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Distribución geográfica</div>', unsafe_allow_html=True)

# Muestra para el mapa (máx 3000 puntos por capa para que cargue rápido)
MAX_MAPA = 3000
hosp_mapa = hosp[['latitud', 'longitud', 'municipio', 'nombre_act']].dropna().sample(
    n=min(MAX_MAPA, len(hosp)), random_state=42)
cons_mapa = cons[['latitud', 'longitud', 'municipio', 'nombre_act']].dropna().sample(
    n=min(MAX_MAPA, len(cons)), random_state=42)

centro_lat = pd.concat([hosp_mapa['latitud'], cons_mapa['latitud']]).mean()
centro_lon = pd.concat([hosp_mapa['longitud'], cons_mapa['longitud']]).mean()

m = folium.Map(location=[centro_lat, centro_lon], zoom_start=10, tiles='CartoDB positron')

# Capa consultorios
cons_layer = folium.FeatureGroup(name='Consultorios', show=True)
for _, row in cons_mapa.iterrows():
    folium.CircleMarker(
        location=[row['latitud'], row['longitud']],
        radius=3,
        color='#e05252',
        fill=True,
        fill_color='#e05252',
        fill_opacity=0.6,
        weight=0,
        tooltip=f"{row['nombre_act']} — {row['municipio']}"
    ).add_to(cons_layer)
cons_layer.add_to(m)

# Capa hospitales
hosp_layer = folium.FeatureGroup(name='Hospitales', show=True)
for _, row in hosp_mapa.iterrows():
    folium.CircleMarker(
        location=[row['latitud'], row['longitud']],
        radius=6,
        color='#1a56db',
        fill=True,
        fill_color='#1a56db',
        fill_opacity=0.85,
        weight=1,
        tooltip=f"{row['nombre_act']} — {row['municipio']}"
    ).add_to(hosp_layer)
hosp_layer.add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, width="100%", height=480)

# ── Gráficas de distribución ──────────────────────────────────────────────────
st.markdown('<div class="section-title">Distribución por municipio / alcaldía</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    top_n = st.slider("Top N", min_value=5, max_value=30, value=15, key="topn")

    fig_hosp = px.bar(
        hosp_por_mun.sort_values().tail(top_n).reset_index(),
        x='count', y='municipio',
        orientation='h',
        color_discrete_sequence=['#1a56db'],
        title=f'Top {top_n} — Hospitales',
        labels={'count': 'Establecimientos', 'municipio': ''}
    )
    fig_hosp.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='Inter',
        title_font_family='Syne',
        height=420
    )
    st.plotly_chart(fig_hosp, use_container_width=True)

with col2:
    fig_cons = px.bar(
        cons_por_mun.sort_values().tail(top_n).reset_index(),
        x='count', y='municipio',
        orientation='h',
        color_discrete_sequence=['#e05252'],
        title=f'Top {top_n} — Consultorios',
        labels={'count': 'Establecimientos', 'municipio': ''}
    )
    fig_cons.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='Inter',
        title_font_family='Syne',
        height=420
    )
    st.plotly_chart(fig_cons, use_container_width=True)

# ── Municipios sin hospitales ─────────────────────────────────────────────────
st.markdown('<div class="section-title">Municipios sin hospitales</div>', unsafe_allow_html=True)

sin_hosp_df = dist[dist['hospitales'] == 0].sort_values('consultorios')

if len(sin_hosp_df) == 0:
    st.info("No hay municipios/alcaldías sin hospitales en la selección actual.")
else:
    fig_sin = px.bar(
        sin_hosp_df.reset_index(),
        x='consultorios', y='municipio',
        orientation='h',
        color_discrete_sequence=['#f59e0b'],
        title=f'{len(sin_hosp_df)} municipios sin hospitales — solo consultorios',
        labels={'consultorios': 'Consultorios', 'municipio': ''}
    )
    fig_sin.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='Inter',
        title_font_family='Syne',
        height=max(300, len(sin_hosp_df) * 22)
    )
    st.plotly_chart(fig_sin, use_container_width=True)

# ── Tipo de establecimiento ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Tipos de establecimiento</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    top_hosp_tipo = hosp['nombre_act'].value_counts().head(10).reset_index()
    fig_ht = px.bar(
        top_hosp_tipo.sort_values('count'),
        x='count', y='nombre_act',
        orientation='h',
        color_discrete_sequence=['#1a56db'],
        title='Tipos de hospital más frecuentes',
        labels={'count': '', 'nombre_act': ''}
    )
    fig_ht.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                         font_family='Inter', title_font_family='Syne', height=380)
    st.plotly_chart(fig_ht, use_container_width=True)

with col4:
    top_cons_tipo = cons['nombre_act'].value_counts().head(10).reset_index()
    fig_ct = px.bar(
        top_cons_tipo.sort_values('count'),
        x='count', y='nombre_act',
        orientation='h',
        color_discrete_sequence=['#e05252'],
        title='Tipos de consultorio más frecuentes',
        labels={'count': '', 'nombre_act': ''}
    )
    fig_ct.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                         font_family='Inter', title_font_family='Syne', height=380)
    st.plotly_chart(fig_ct, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#94a3b8; font-size:0.8rem'>"
    "Fuente: DENUE 2025 · INEGI &nbsp;|&nbsp; MA2007B — Geometría y Topología para Ciencia de Datos"
    "</p>",
    unsafe_allow_html=True
)
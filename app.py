import streamlit as st
import pandas as pd
import plotly.express as px
from decouple import config

# pathdata = config('PATHDATA')

st.set_page_config(
  page_title='Dashboard',
  page_icon='/home/pc/Documentos/CodigoFacilito/Dashboard/streamlit/image/streamli1.png',
  layout='wide',
  initial_sidebar_state='expanded'
)

with st.sidebar:
  st.title('Dashboard')
  st.write('Ejemplo de prueba')


superTienda_raw = pd.read_csv(
    'data/supertienda.csv')
print(superTienda_raw.columns)

# Quitar valores nulos
superTienda_raw = superTienda_raw[superTienda_raw['Fecha_pedido'].notna()]
superTienda_raw = superTienda_raw.drop(columns=['Unnamed: 20'])
# Convertir a datatime y crear columnas de año y mes
superTienda_raw['Fecha_pedido'] = pd.to_datetime(
    superTienda_raw['Fecha_pedido'])
superTienda_raw['Anho'] = pd.to_datetime(
    superTienda_raw['Fecha_pedido']).dt.year.astype(int)
superTienda_raw['Mes'] = pd.to_datetime(
    superTienda_raw['Fecha_pedido']).dt.month.astype(int)
# Mostrar una fotgrafia de los datos
st.write(superTienda_raw.head(4))
# ContainerPrincipal
with st.container():
  # Titulo
  st.title('Super Tienda Performance Dashboard')
with st.container():
  # Crear Columna para filtros
  filtro_anho, filtro_mes, filtro_region = st.columns(3)
  with filtro_anho:
    list_anho = superTienda_raw['Anho'].unique()
    list_anho.sort()
    anho = st.multiselect('Año', list_anho, list_anho[0])
  with filtro_mes:
    list_meses = superTienda_raw['Mes'].unique()
    list_meses.sort()
    mes = st.multiselect('Mes', list_meses, list_meses[0])
  with filtro_region:
    list_regiones = superTienda_raw['Región'].unique()
    list_regiones.sort()
    region = st.multiselect('Region', list_regiones, list_regiones[0])

# Data Frame filtrado
superTienda_raw_filter = superTienda_raw[
  (superTienda_raw['Anho'].isin(anho)) &
  (superTienda_raw['Mes'].isin(mes)) &
  (superTienda_raw['Región'].isin(region))
]
# Container para 2 kpi
with st.container():
  # Crear 2 columnas
  kpi1, kpi2 = st.columns(2)
  with kpi1:
    st.metric(
      label='Total de ventas',
      value=f"${superTienda_raw_filter['Ventas'].sum():,.0f}"
        )
  with kpi2:
    st.metric(
      label='Total de Productos Vendidos',
      value=f"${superTienda_raw_filter['Cantidad'].sum():,.0f}"
        )
# Container para nuestros dos primeros graficos
st.header('Tendencia de Ventas')
with st.container():
    # creacion de 2 columnas para el grafico de lineas y de pie
    line_chart_total, pie_chart_total = st.columns((2, 1))
    with line_chart_total:
        # grafico de lineas
        data_line = superTienda_raw_filter.groupby(
            'Fecha_pedido')['Ventas'].sum().reset_index()
        line_chart = px.line(data_line,
                            x='Fecha_pedido',
                            y='Ventas',
                            title='Tendencia de Ventas')
        line_chart.update_layout(height=600,
                                width=1000)
        st.plotly_chart(line_chart)

    with pie_chart_total:
        # grafico de pie para ventas totales por pais
        data_pie = superTienda_raw_filter.groupby(
            'País/Región')['Ventas'].sum().reset_index()
        pie_chart = px.pie(data_pie,
                            values='Ventas',
                            names='País/Región',
                            title='Ventas por País')
        # cambiar el tamaño del grafico
        pie_chart.update_traces(textposition='inside',
                                textinfo='percent+label+value')
        pie_chart.update_layout(uniformtext_minsize=12,
                                uniformtext_mode='hide',
                                showlegend=False,
                                height=600,
                                width=600)
        st.plotly_chart(pie_chart)

# Container para nuestros dos ultimos graficos
with st.container():
    # creacion de 2 columnas para el grafico de barras horizontales y de barras verticales
    st.markdown('## Ventas por Categoría')
    bar_chart_total, bar_chart_total2 = st.columns((1, 2))

    with bar_chart_total:
        # grafico de barras horizontales
        data_bar = superTienda_raw_filter.groupby(
            'Categoría')['Ventas'].sum().reset_index()
        bar_chart = px.bar(data_bar,
                            y='Categoría',
                            x='Ventas',
                            title='Ventas por Categoría',
                            color='Categoría',
                            orientation='h',
                            text_auto='.2s')
        bar_chart.update_layout(height=600,
                                width=600)
        st.plotly_chart(bar_chart)

    with bar_chart_total2:
        # grafico de barras verticales
        data_bar2 = superTienda_raw_filter.groupby(
            'Subcategoría')['Ventas'].sum().reset_index()
        bar_chart2 = px.bar(data_bar2,
                            x='Subcategoría',
                            y='Ventas',
                            title='Ventas por Sub-Categoría',
                            color='Subcategoría',
                            text_auto='.2s')
        bar_chart2.update_layout(height=600,
                                width=1000)
        st.plotly_chart(bar_chart2)

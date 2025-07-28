import streamlit as st
import pandas as pd
from utils.database import get_all_incident_records_df, get_all_verifiers_df, get_all_warehouses_df, get_incidents_by_zone, get_incidents_by_verifier, get_incidents_by_warehouse, get_incidents_by_type, get_incidents_by_status, get_assignments_by_verifier

def display_filtered_table(title, df_getter):
    st.subheader(title)
    df = df_getter()
    if df.empty:
        st.warning('No hay datos disponibles.')
        return
    columns = st.multiselect('Seleccionar columnas para filtrar', df.columns)
    filters = {}
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            min_val, max_val = st.slider(f'Filtrar {col}', float(df[col].min()), float(df[col].max()), (float(df[col].min()), float(df[col].max())))
            filters[col] = (min_val, max_val)
        else:
            unique_vals = df[col].unique()
            selected = st.multiselect(f'Filtrar {col}', unique_vals, unique_vals)
            filters[col] = selected
    filtered_df = df.copy()
    for col, vals in filters.items():
        if isinstance(vals, tuple):
            filtered_df = filtered_df[(filtered_df[col] >= vals[0]) & (filtered_df[col] <= vals[1])]
        else:
            filtered_df = filtered_df[filtered_df[col].isin(vals)]
    st.dataframe(filtered_df)

def display_chart(title, df_getter, x_col, y_col='count'):
    st.subheader(title)
    df = df_getter()
    if df.empty:
        st.warning('No hay datos disponibles.')
        return
    st.bar_chart(df.set_index(x_col)[y_col])

def analytics_incidents():
    display_filtered_table('Consulta de Incidencias', get_all_incident_records_df)
    display_chart('Incidencias por Zona', get_incidents_by_zone, 'warehouse_zone')
    display_chart('Incidencias por Verificador', get_incidents_by_verifier, 'causing_verifier')
    display_chart('Incidencias por Bodega', get_incidents_by_warehouse, 'warehouse')
    display_chart('Incidencias por Tipo', get_incidents_by_type, 'incident_type')
    display_chart('Incidencias por Status', get_incidents_by_status, 'status')

def analytics_verifiers():
    display_filtered_table('Consulta de Verificadores', get_all_verifiers_df)
    display_chart('Asignaciones por Verificador', get_assignments_by_verifier, 'causing_verifier')

def analytics_warehouses():
    display_filtered_table('Consulta de Bodegas', get_all_warehouses_df)
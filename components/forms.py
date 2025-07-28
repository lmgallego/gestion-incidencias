import streamlit as st
import pandas as pd
import datetime
from utils.database import insert_coordinator, insert_verifier, insert_warehouse, load_csv_to_verifiers, load_csv_to_warehouses, insert_incident, get_coordinators, get_verifiers, get_warehouses, get_incidents, insert_incident_record, get_incident_records, insert_incident_action, get_incident_actions

def coordinator_form():
    st.subheader('Alta de Coordinador')
    name = st.text_input('Nombre')
    surnames = st.text_input('Apellidos')
    if st.button('Guardar Coordinador'):
        if name and surnames:
            insert_coordinator(name, surnames)
            st.success('Coordinador guardado exitosamente.')
        else:
            st.error('Por favor, complete todos los campos.')

def verifier_form():
    st.subheader('Alta de Verificador')
    name = st.text_input('Nombre')
    surnames = st.text_input('Apellidos')
    phone = st.text_input('Teléfono')
    zone = st.text_input('Zona')
    if st.button('Guardar Verificador'):
        if name and surnames:
            insert_verifier(name, surnames, phone, zone)
            st.success('Verificador guardado exitosamente.')
        else:
            st.error('Por favor, complete nombre y apellidos.')

def warehouse_form():
    st.subheader('Alta de Bodega')
    name = st.text_input('Nombre')
    nif = st.text_input('NIF')
    zone = st.text_input('Zona')
    if st.button('Guardar Bodega'):
        if name and nif:
            insert_warehouse(name, nif, zone)
            st.success('Bodega guardada exitosamente.')
        else:
            st.error('Por favor, complete nombre y NIF.')

def csv_upload(section):
    st.subheader(f'Carga de {section} desde CSV')
    uploaded_file = st.file_uploader(f'Seleccione CSV para {section}', type='csv')
    if uploaded_file is not None:
        if st.button('Cargar CSV'):
            if section == 'Verificadores':
                load_csv_to_verifiers(uploaded_file)
            elif section == 'Bodegas':
                load_csv_to_warehouses(uploaded_file)
            st.success(f'{section} cargados exitosamente desde CSV.')

def incident_form():
    st.subheader('Alta de Incidencia')
    description = st.text_area('Descripción de la Incidencia')
    if st.button('Guardar Incidencia'):
        if description:
            insert_incident(description)
            st.success('Incidencia guardada exitosamente.')
        else:
            st.error('Por favor, ingrese una descripción.')

def incident_record_form():
    st.subheader('Registro de Incidencia')
    date = st.date_input('Fecha', datetime.date.today())
    coordinators = get_coordinators()
    if not coordinators:
        st.warning('No hay coordinadores disponibles. Por favor, registre uno primero.')
        return
    registering_coordinator_id = st.selectbox('Coordinador que registra', options=coordinators, format_func=lambda x: x[1])[0]
    warehouses = get_warehouses()
    if not warehouses:
        st.warning('No hay bodegas disponibles. Por favor, registre una primero.')
        return
    warehouse_id = st.selectbox('Bodega', options=warehouses, format_func=lambda x: x[1])[0]
    verifiers = get_verifiers()
    if not verifiers:
        st.warning('No hay verificadores disponibles. Por favor, registre uno primero.')
        return
    causing_verifier_id = st.selectbox('Verificador que provocó la incidencia', options=verifiers, format_func=lambda x: x[1])[0]
    incidents = get_incidents()
    if not incidents:
        st.warning('No hay incidencias disponibles. Por favor, registre una primero.')
        return
    incident_id = st.selectbox('Incidencia', options=incidents, format_func=lambda x: x[1])[0]
    assigned_coordinator_id = st.selectbox('Coordinador asignado', options=coordinators, format_func=lambda x: x[1])[0]
    explanation = st.text_area('Explicación')
    status = st.selectbox('Status', ['Pendiente', 'En Proceso', 'Solucionado', 'Asignado a Técnicos'])
    responsible = st.selectbox('Responsable', ['Bodega', 'Verificador'])
    if st.button('Guardar Registro de Incidencia'):
        if all([date, registering_coordinator_id, warehouse_id, causing_verifier_id, incident_id, assigned_coordinator_id, status, responsible]):
            insert_incident_record(date, registering_coordinator_id, warehouse_id, causing_verifier_id, incident_id, assigned_coordinator_id, explanation, status, responsible)
            st.success('Registro de incidencia guardado exitosamente.')
        else:
            st.error('Por favor, complete todos los campos obligatorios.')

def manage_incident_actions_form():
    st.subheader('Gestión de Acciones de Incidencia')
    incident_records = get_incident_records()
    if not incident_records:
        st.warning('No hay registros de incidencias disponibles. Por favor, registre uno primero.')
        return
    selected_record = st.selectbox('Seleccionar Registro de Incidencia', options=incident_records, format_func=lambda x: x[1])
    incident_record_id = selected_record[0]
    actions = get_incident_actions(incident_record_id)
    st.subheader('Historial de Acciones')
    for action in actions:
        st.write(f"Fecha: {action['action_date']}, Descripción: {action['action_description']}, Nuevo Status: {action['new_status'] or 'N/A'}, Realizado por: {action['performed_by']}")
    st.subheader('Añadir Nueva Acción')
    action_date = st.date_input('Fecha de la Acción', datetime.date.today())
    action_description = st.text_area('Descripción de la Acción')
    new_status = st.selectbox('Nuevo Status (opcional)', [None, 'Pendiente', 'En Proceso', 'Solucionado', 'Asignado a Técnicos'], index=0)
    coordinators = get_coordinators()
    performed_by = st.selectbox('Realizado por', options=coordinators, format_func=lambda x: x[1])[0]
    if st.button('Guardar Acción'):
        if action_date and action_description and performed_by:
            insert_incident_action(incident_record_id, action_date, action_description, new_status, performed_by)
            st.success('Acción guardada exitosamente.')
            st.experimental_rerun()
        else:
            st.error('Por favor, complete fecha, descripción y realizado por.')
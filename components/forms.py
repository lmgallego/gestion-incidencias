import streamlit as st
import pandas as pd
import datetime
from utils.database import insert_coordinator, insert_verifier, insert_warehouse, load_csv_to_verifiers, load_csv_to_warehouses, insert_incident, get_coordinators, get_verifiers, get_warehouses, get_incidents, insert_incident_record, get_incident_records, insert_incident_action, get_incident_actions

def coordinator_form():
    st.subheader('Alta de Coordinador')
    
    # Inicializar contador si no existe
    if 'coord_form_counter' not in st.session_state:
        st.session_state.coord_form_counter = 0
    
    # Usar el contador en las claves para forzar la recreación de widgets
    name = st.text_input('Nombre', key=f'coord_name_{st.session_state.coord_form_counter}')
    surnames = st.text_input('Apellidos', key=f'coord_surnames_{st.session_state.coord_form_counter}')
    
    if st.button('Guardar Coordinador'):
        if name and surnames:
            insert_coordinator(name, surnames)
            st.success('Coordinador guardado exitosamente.')
            # Incrementar contador para limpiar formulario
            st.session_state.coord_form_counter += 1
            st.rerun()
        else:
            st.error('Por favor, complete todos los campos.')

def verifier_form():
    st.subheader('Alta de Verificador')
    
    if 'verif_form_counter' not in st.session_state:
        st.session_state.verif_form_counter = 0
    
    name = st.text_input('Nombre', key=f'verif_name_{st.session_state.verif_form_counter}')
    surnames = st.text_input('Apellidos', key=f'verif_surnames_{st.session_state.verif_form_counter}')
    phone = st.text_input('Teléfono', key=f'verif_phone_{st.session_state.verif_form_counter}')
    zone = st.text_input('Zona', key=f'verif_zone_{st.session_state.verif_form_counter}')
    
    if st.button('Guardar Verificador'):
        if name and surnames:
            insert_verifier(name, surnames, phone, zone)
            st.success('Verificador guardado exitosamente.')
            st.session_state.verif_form_counter += 1
            st.rerun()
        else:
            st.error('Por favor, complete nombre y apellidos.')

def warehouse_form():
    st.subheader('Alta de Bodega')
    
    # Inicializar contador si no existe
    if 'warehouse_form_counter' not in st.session_state:
        st.session_state.warehouse_form_counter = 0
    
    name = st.text_input('Nombre', key=f'wh_name_{st.session_state.warehouse_form_counter}')
    nif = st.text_input('NIF', key=f'wh_nif_{st.session_state.warehouse_form_counter}')
    zone = st.text_input('Zona', key=f'wh_zone_{st.session_state.warehouse_form_counter}')
    if st.button('Guardar Bodega'):
        if name and nif:
            insert_warehouse(name, nif, zone)
            st.success('Bodega guardada exitosamente.')
            # Incrementar contador para limpiar formulario
            st.session_state.warehouse_form_counter += 1
            st.rerun()
        else:
            st.error('Por favor, complete nombre y NIF.')

def csv_upload(section):
    st.subheader(f'Carga de {section} desde CSV')
    with st.form(key=f'csv_upload_{section}', clear_on_submit=True):
        uploaded_file = st.file_uploader(f'Seleccione CSV para {section}', type='csv')
        separator = st.selectbox('Separador del CSV', [',', ';'], index=0)
        submit = st.form_submit_button('Cargar CSV')
        if submit and uploaded_file is not None:
            try:
                if section == 'Verificadores':
                    df = pd.read_csv(uploaded_file, sep=separator, encoding='latin1')
                    required_columns = ['name', 'surnames']
                    if not all(col in df.columns for col in required_columns):
                        raise ValueError(f'El CSV debe contener las columnas: {', '.join(required_columns)}')
                    load_csv_to_verifiers(uploaded_file, sep=separator)
                elif section == 'Bodegas':
                    df = pd.read_csv(uploaded_file, sep=separator, encoding='latin1')
                    required_columns = ['name', 'nif']
                    if not all(col in df.columns for col in required_columns):
                        raise ValueError(f'El CSV debe contener las columnas: {', '.join(required_columns)}')
                    load_csv_to_warehouses(uploaded_file, sep=separator)
                st.success(f'{section} cargados exitosamente desde CSV.')
            except Exception as e:
                st.error(f'Error al cargar el CSV: {str(e)}')

def incident_form():
    st.subheader('Alta de Incidencia')
    
    # Inicializar contador si no existe
    if 'incident_form_counter' not in st.session_state:
        st.session_state.incident_form_counter = 0
    
    description = st.text_area('Descripción de la Incidencia', key=f'inc_description_{st.session_state.incident_form_counter}')
    if st.button('Guardar Incidencia'):
        if description:
            insert_incident(description)
            st.success('Incidencia guardada exitosamente.')
            # Incrementar contador para limpiar formulario
            st.session_state.incident_form_counter += 1
            st.rerun()
        else:
            st.error('Por favor, ingrese una descripción.')

def incident_record_form():
    st.subheader('Registro de Incidencia')
    
    # Inicializar contador si no existe
    if 'incident_record_counter' not in st.session_state:
        st.session_state.incident_record_counter = 0
    
    date = st.date_input('Fecha', datetime.date.today(), key=f'inc_rec_date_{st.session_state.incident_record_counter}')
    coordinators = get_coordinators()
    if not coordinators:
        st.warning('No hay coordinadores disponibles. Por favor, registre uno primero.')
        return
    registering_coordinator_id = st.selectbox('Coordinador que registra', options=coordinators, format_func=lambda x: x[1], key=f'inc_rec_reg_coord_{st.session_state.incident_record_counter}')[0]
    warehouses = get_warehouses()
    if not warehouses:
        st.warning('No hay bodegas disponibles. Por favor, registre una primero.')
        return
    warehouse_id = st.selectbox('Bodega', options=warehouses, format_func=lambda x: x[1], key=f'inc_rec_warehouse_{st.session_state.incident_record_counter}')[0]
    verifiers = get_verifiers()
    if not verifiers:
        st.warning('No hay verificadores disponibles. Por favor, registre uno primero.')
        return
    causing_verifier_id = st.selectbox('Verificador que provocó la incidencia', options=verifiers, format_func=lambda x: x[1], key=f'inc_rec_verifier_{st.session_state.incident_record_counter}')[0]
    incidents = get_incidents()
    if not incidents:
        st.warning('No hay incidencias disponibles. Por favor, registre una primero.')
        return
    incident_id = st.selectbox('Incidencia', options=incidents, format_func=lambda x: x[1], key=f'inc_rec_incident_{st.session_state.incident_record_counter}')[0]
    assigned_coordinator_id = st.selectbox('Coordinador asignado', options=coordinators, format_func=lambda x: x[1], key=f'inc_rec_assigned_coord_{st.session_state.incident_record_counter}')[0]
    explanation = st.text_area('Explicación', key=f'inc_rec_explanation_{st.session_state.incident_record_counter}')
    status = st.selectbox('Status', ['Pendiente', 'En Proceso', 'Solucionado', 'Asignado a Técnicos'], key=f'inc_rec_status_{st.session_state.incident_record_counter}')
    responsible = st.selectbox('Responsable', ['Bodega', 'Verificador'], key=f'inc_rec_responsible_{st.session_state.incident_record_counter}')
    if st.button('Guardar Registro de Incidencia'):
        if all([date, registering_coordinator_id, warehouse_id, causing_verifier_id, incident_id, assigned_coordinator_id, status, responsible]):
            insert_incident_record(date, registering_coordinator_id, warehouse_id, causing_verifier_id, incident_id, assigned_coordinator_id, explanation, status, responsible)
            st.success('Registro de incidencia guardado exitosamente.')
            # Incrementar contador para limpiar formulario
            st.session_state.incident_record_counter += 1
            st.rerun()
        else:
            st.error('Por favor, complete todos los campos obligatorios.')

def manage_incident_actions_form():
    st.subheader('Gestión de Acciones de Incidencia')
    
    # Inicializar contador si no existe
    if 'incident_actions_counter' not in st.session_state:
        st.session_state.incident_actions_counter = 0
    
    incident_records = get_incident_records()
    if not incident_records:
        st.warning('No hay registros de incidencias disponibles. Por favor, registre uno primero.')
        return
    selected_record = st.selectbox('Seleccionar Registro de Incidencia', options=incident_records, format_func=lambda x: x[1], key=f'inc_act_record_{st.session_state.incident_actions_counter}')
    incident_record_id = selected_record[0]
    actions = get_incident_actions(incident_record_id)
    st.subheader('Historial de Acciones')
    for action in actions:
        st.write(f"Fecha: {action['action_date']}, Descripción: {action['action_description']}, Nuevo Status: {action['new_status'] or 'N/A'}, Realizado por: {action['performed_by']}")
    st.subheader('Añadir Nueva Acción')
    action_date = st.date_input('Fecha de la Acción', datetime.date.today(), key=f'inc_act_date_{st.session_state.incident_actions_counter}')
    action_description = st.text_area('Descripción de la Acción', key=f'inc_act_desc_{st.session_state.incident_actions_counter}')
    new_status = st.selectbox('Nuevo Status (opcional)', [None, 'Pendiente', 'En Proceso', 'Solucionado', 'Asignado a Técnicos'], index=0, key=f'inc_act_status_{st.session_state.incident_actions_counter}')
    coordinators = get_coordinators()
    performed_by = st.selectbox('Realizado por', options=coordinators, format_func=lambda x: x[1], key=f'inc_act_by_{st.session_state.incident_actions_counter}')[0]
    if st.button('Guardar Acción'):
        if action_date and action_description and performed_by:
            insert_incident_action(incident_record_id, action_date, action_description, new_status, performed_by)
            st.success('Acción guardada exitosamente.')
            # Incrementar contador para limpiar formulario
            st.session_state.incident_actions_counter += 1
            st.rerun()
        else:
            st.error('Por favor, complete fecha, descripción y realizado por.')
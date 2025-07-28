import streamlit as st
from streamlit_option_menu import option_menu
from utils.database import init_db
from components.forms import coordinator_form, verifier_form, warehouse_form, csv_upload, incident_form, incident_record_form, manage_incident_actions_form
from components.analytics import analytics_incidents, analytics_verifiers, analytics_warehouses
from components.delete import delete_test_data_form

# Inicializar la base de datos
init_db()

# Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if username == "coordinador" and password == "Cava1234!":
            st.session_state.logged_in = True
            st.rerun()  # Updated from experimental_rerun
        else:
            st.error("Usuario o contraseña incorrectos.")
else:
    # Menú principal
    with st.sidebar:
        main_selected = option_menu(
            menu_title="Menú Principal",
            options=["Altas", "Incidencias", "Consultas y Analítica", "Administración"],
            icons=["plus-circle", "exclamation-triangle", "bar-chart-line"],
            menu_icon="cast",
            default_index=0,
        )

    if main_selected == "Altas":
        with st.sidebar:
            sub_selected = option_menu(
                menu_title="Altas",
                options=["Alta Coordinador", "Alta Verificador", "Alta Bodega", "Cargar Verificadores CSV", "Cargar Bodegas CSV", "Alta Incidencia"],
                icons=["person", "person-check", "building", "file-earmark-spreadsheet", "file-earmark-spreadsheet", "exclamation-triangle"],
                menu_icon="plus",
                default_index=0,
            )

        if sub_selected == "Alta Coordinador":
            coordinator_form()
        elif sub_selected == "Alta Verificador":
            verifier_form()
        elif sub_selected == "Alta Bodega":
            warehouse_form()
        elif sub_selected == "Cargar Verificadores CSV":
            csv_upload("Verificadores")
        elif sub_selected == "Cargar Bodegas CSV":
            csv_upload("Bodegas")
        elif sub_selected == "Alta Incidencia":
            incident_form()

    elif main_selected == "Incidencias":
        with st.sidebar:
            sub_selected = option_menu(
                menu_title="Incidencias",
                options=["Registro de Incidencia", "Gestión de Acciones"],
                icons=["clipboard-plus", "pencil-square"],
                menu_icon="exclamation",
                default_index=0,
            )

        if sub_selected == "Registro de Incidencia":
            incident_record_form()
        elif sub_selected == "Gestión de Acciones":
            manage_incident_actions_form()

    elif main_selected == "Consultas y Analítica":
        with st.sidebar:
            sub_selected = option_menu(
                menu_title="Consultas y Analítica",
                options=["Analítica de Incidencias", "Analítica de Verificadores", "Analítica de Bodegas"],
                icons=["clipboard-data", "person-lines-fill", "building"],
                menu_icon="graph-up",
                default_index=0,
            )

        if sub_selected == "Analítica de Incidencias":
            analytics_incidents()
        elif sub_selected == "Analítica de Verificadores":
            analytics_verifiers()
        elif sub_selected == "Analítica de Bodegas":
            analytics_warehouses()

    elif main_selected == "Administración":
        with st.sidebar:
            sub_selected = option_menu(
                menu_title="Administración",
                options=["Borrar Datos de Prueba"],
                icons=["trash"],
                menu_icon="gear",
                default_index=0,
            )

        if sub_selected == "Borrar Datos de Prueba":
            delete_test_data_form()
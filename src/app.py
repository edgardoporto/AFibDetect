import streamlit as st
import sys
import os

# 1. SOLUCIÓN ABSOLUTA DE ENRUTAMIENTO (Inyección en el Python Path)
# Obtenemos la ruta absoluta de la carpeta 'src' donde viven tus módulos
root_path = os.path.dirname(os.path.abspath(__file__))

# Le decimos a Python que busque módulos directamente dentro de 'src'
if root_path not in sys.path:
    sys.path.insert(0, root_path)
    

# 1. IMPORTAR NUESTROS PROPIOS MÓDULOS
# Importamos las funciones de carga y validación que guardamos en data_loader.py
from modules.data_loader import cargar_archivo_csv, validar_estructura_ecg
from modules.dashboard import graficar_ecg_crudo


# Inicialización y configuración estética de la página web
st.set_page_config(
    page_title="AFibDetect System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. GESTIÓN DE ESTADO (In-Memory State Management con st.session_state)
# Inicializamos las variables en la memoria RAM del servidor para que no se borren al hacer clic
if "df_ecg" not in st.session_state:
    st.session_state["df_ecg"] = None  # Aquí guardaremos el DataFrame del ECG una vez validado

if "mensaje_validacion" not in st.session_state:
    st.session_state["mensaje_validacion"] = ""

# 3. INTERFAZ DE USUARIO: BARRA LATERAL (Sidebar)
with st.sidebar:
    st.title("🩺 AFibDetect v1.0")
    st.markdown("---")
    st.markdown("### Navegación del Sistema")
    
    # Menú de selección para alternar entre las pantallas de la aplicación
    menu_opcion = st.radio(
        "Seleccione un Módulo:",
        ["1. Carga de Señal", "2. Procesamiento", "3. Inferencia y Dashboard"]
    )
    st.markdown("---")
    st.caption("Desarrollado para la clasificación robusta de Fibrilación Auricular.")

# 4. ORQUESTACIÓN DE PANTALLAS (Flujo Reactivo)
if menu_opcion == "1. Carga de Señal":
    st.header("📥 Módulo de Ingreso y Validación de Datos")
    st.write("Cargue el archivo de texto plano (.csv) que contiene el registro de la señal electrocardiográfica.")
    
    # Componente nativo de Streamlit para arrastrar y soltar archivos
    archivo_subido = st.file_uploader("Cargar registro ECG (Formato CSV)", type=["csv"])
    
    if archivo_subido is not None:
        # Ejecutamos la función del módulo data_loader para leer el archivo
        df_temporal = cargar_archivo_csv(archivo_subido)
        
        # Ejecutamos la validación estructural
        es_valido, mensaje = validar_estructura_ecg(df_temporal)
        
        if es_valido:
            # Si el archivo es correcto, lo guardamos en la persistencia de sesión
            st.session_state["df_ecg"] = df_temporal
            st.session_state["mensaje_validacion"] = mensaje
            st.success(st.session_state["mensaje_validacion"])
            
            # Mensaje informativo temporal sobre las dimensiones detectadas
            filas, columnas = df_temporal.shape
            st.info(f"Señal cargada en memoria: {filas} puntos de muestreo distribuidos en {columnas} columna(s).")
        else:
            st.error(mensaje)

elif menu_opcion == "2. Procesamiento":
    st.header("⚡ Módulo de Preprocesamiento de Señales")
    st.write("Sección dedicada al filtrado digital y segmentación.")
    
    # Verificamos si ya hay datos en memoria antes de permitir procesar
    if st.session_state["df_ecg"] is not None:
        st.info("Datos listos para preprocesar detectados en memoria de sesión.")
    else:
        st.warning("Por favor, regrese al Módulo 1 y cargue una señal de ECG válida primero.")

elif menu_opcion == "3. Inferencia y Dashboard":
    st.header("📊 Tablero de Control Estadístico y Diagnóstico")
    st.write("Resultados de clasificación y explicabilidad.")

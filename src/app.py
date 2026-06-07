import streamlit as st
import numpy as np

# Importamos la tabla de códigos desde tu archivo de configuración
from config import SNOMED_MAP
# Importación del módulo gráfico corregido
from modules.dashboard import graficar_derivacion_ecg
# IMPORTACIÓN DEL CARGADOR BIOMÉDICO REAL DE PHYSIONET
from modules.data_loader import cargar_registro_unico_wfdb

# Inicialización y configuración del Layout
st.set_page_config(page_title="AFibDetect System", page_icon="🩺", layout="wide")

# Inicializamos el estado para almacenar un solo paciente de CPSC-2018
if "paciente_activo" not in st.session_state:
    st.session_state["paciente_activo"] = None

# Título Principal
st.title("🩺 AFibDetect v1.0")
st.write("Cargue los archivos de un registro de la CPSC-2018 (Arrastre juntos el archivo de texto .hea y la matriz de señal .mat).")

# 1. COMPONENTE DE CARGA DE ARCHIVOS (.hea y .mat)
archivos_subidos = st.file_uploader(
    "Seleccione o arrastre juntos los archivos .hea y .mat del registro:", 
    type=["hea", "mat"],
    accept_multiple_files=True
)

def traducir_codigo_snomed(codigo_crudo):
    """
    Traduce el código SNOMED de PhysioNet al estándar del proyecto.
    Si no es AF ni NSR, lo encapsula como 'Other (Nombre_Real)'.
    """
    codigo_str = str(codigo_crudo).strip()
    
    if codigo_str in SNOMED_MAP:
        nombre_real = SNOMED_MAP[codigo_str]
        if nombre_real in ["AF", "NSR", "Noise"]:
            return nombre_real
        else:
            return f"Other ({nombre_real})"
    else:
        return "Other (Unknown)"

# 2. PROCESAMIENTO Y PARSEO DE SEÑALES REALES DESDE EL BUS BUFFER
if archivos_subidos and len(archivos_subidos) == 2:
    if st.session_state["paciente_activo"] is None:
        with st.spinner("Parseando matriz binaria de Matlab en memoria RAM..."):
            # Llamamos al cargador real que guarda los archivos por un milisegundo en disco temporal
            registro_real, mensaje = cargar_registro_unico_wfdb(archivos_subidos)
            
            if registro_real:
                # Traducimos dinámicamente el código SNOMED extraído de la cabecera real
                registro_real["etiqueta_referencia"] = traducir_codigo_snomed(registro_real["codigo_snomed"])
                
                # Campos complementarios estéticos fijos requeridos por tu interfaz
                registro_real["resolución_adc"] = "16-bit"
                registro_real["ganancia_base"] = "1000 adu/mV"
                registro_real["formato_almacenamiento"] = "Matlab v4 (Format 16)"
                registro_real["metadatos_clinicos"] = "Registro Clínico CPSC-2018"
                
                st.session_state["paciente_activo"] = registro_real
                st.success(mensaje)
            else:
                st.error(mensaje)

# 3. DESPLIEGUE EXHAUSTIVO DE TODOS LOS METADATOS CLÍNICOS
if st.session_state["paciente_activo"] is not None:
    st.markdown("---")
    st.subheader("📊 Panel Integral de Metadatos (Estándar PhysioNet)")
    
    paciente = st.session_state["paciente_activo"]
    duracion_segundos = paciente["total_muestras"] / paciente["frecuencia_muestreo"]
    
    # Fila 1: Métricas Principales de Diagnóstico e Infraestructura
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Nombre del Registro", value=paciente["id_registro"])
    with col2:
        st.metric(label="Frecuencia de Muestreo", value=f"{paciente['frecuencia_muestreo']} Hz")
    with col3:
        st.metric(label="Duración del Registro", value=f"{duracion_segundos:.2f} s")
    with col4:
        st.metric(label="Diagnóstico de Referencia", value=paciente["etiqueta_referencia"])
        
    # Fila 2: Información Técnica del Archivo y Canales
    st.markdown("###") 
    col_tech1, col_tech2, col_tech3 = st.columns(3)
    
    with col_tech1:
        st.info(f"**Estructura Digital:**\n\n* **N° de Derivaciones:** {paciente['num_derivaciones']} canales\n* **Puntos Totales:** {paciente['total_muestras']} muestras")
    
    with col_tech2:
        st.info(f"**Convertidor Análogo-Digital (ADC):**\n\n* **Resolución:** {paciente['resolución_adc']}\n* **Ganancia Base:** {paciente['ganancia_base']}")
        
    with col_tech3:
        st.info(f"**Formato de Almacenamiento:**\n\n* **Módulo Lector:** {paciente['formato_almacenamiento']}\n* **Datos Clínicos:** {paciente['metadatos_clinicos']}")

    st.markdown("**Matriz de Canales Detectados:**")
    st.code(" | ".join(paciente["derivaciones"]), language="text")

    st.markdown("---")
    st.subheader("📈 Visualización Interactiva Multiderivación")
    st.write("Seleccione los canales electrocardiográficos que desea inspeccionar en paralelo:")
    
    # 4. DISEÑO DE LA MATRIZ COMPACTA DE CHECKBOXES (6 Columnas)
    cols_check = st.columns(6)
    derivaciones_seleccionadas = []
    
    for idx, derivacion in enumerate(paciente["derivaciones"]):
        col_actual = cols_check[idx % 6]
        with col_actual:
            if st.checkbox(derivacion, value=False, key=f"chk_{derivacion}"):
                derivaciones_seleccionadas.append(derivacion)
                
    # 5. RENDERIZADO REACTIVO DE GRÁFICOS REALES DE PLOTLY
    if derivaciones_seleccionadas:
        st.markdown("###") # Pequeño espacio de separación
        for derivacion_activa in derivaciones_seleccionadas:
            # Llamamos a Plotly pasando la matriz de voltajes del paciente real
            graficar_derivacion_ecg(paciente, derivacion_activa)
    else:
        st.warning("Seleccione al menos una derivación de la matriz superior para desplegar su análisis gráfico.")

# 6. INYECCIÓN DE CÓDIGO CSS (Control estético de fuentes y márgenes)
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 0rem;
            margin-top: 0rem;
        }
        h1 {
            font-size: 2.0rem !important; 
            font-weight: 700;
            padding-bottom: 0.2rem;
            margin-top: 0rem;
        }
        h2, h3 {
            font-size: 1.3rem !important;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        .stText, p, li {
            font-size: 0.95rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

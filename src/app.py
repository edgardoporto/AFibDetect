import streamlit as st

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

# Simulador de datos expandido con TODOS los metadatos de PhysioNet
if archivos_subidos and len(archivos_subidos) == 2:
    if st.session_state["paciente_activo"] is None:
        st.session_state["paciente_activo"] = {
            "id_registro": "A0001.mat",
            "frecuencia_muestreo": 300,
            "total_muestras": 15000,
            "num_derivaciones": 12,
            "derivaciones": ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"],
            "etiqueta_referencia": "AF (Atrial Fibrillation)",
            "resolución_adc": "16-bit",
            "ganancia_base": "1000 adu/mV",
            "formato_almacenamiento": "Matlab v4 (Format 16)",
            "metadatos_clinicos": "Edad: 68 | Sexo: Masculino | Tipo: Registro Clínico Estándar"
        }
        st.success("Validación e ingesta biomédica completada con éxito.")

# 2. DESPLIEGUE EXHAUSTIVO DE TODOS LOS METADATOS
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
        
    # Fila 2: Información Técnica del Archivo y Canales (Organizado en columnas secundarias)
    st.markdown("###") # Pequeño espacio de separación
    col_tech1, col_tech2, col_tech3 = st.columns(3)
    
    with col_tech1:
        st.info(f"**Estructura Digital:**\n* **N° de Derivaciones:** {paciente['num_derivaciones']} canales\n* **Puntos Totales por Canal:** {paciente['total_muestras']} muestras")
    
    with col_tech2:
        st.info(f"**Especificaciones del Convertidor (ADC):**\n* **Resolución:** {paciente['resolución_adc']}\n* **Ganancia Digital:** {paciente['ganancia_base']}")
        
    with col_tech3:
        st.info(f"**Formato de Archivo:**\n* **Módulo Lector:** {paciente['formato_almacenamiento']}\n* **Datos Clínicos Extrayibles:** {paciente['metadatos_clinicos']}")

    # Despliegue explícito del mapa de derivaciones presentes
    st.markdown("**Matriz de Canales Detectados:**")
    st.code(" | ".join(paciente["derivaciones"]), language="text")

    st.markdown("---")
    st.subheader("📈 Visualización Interactiva")
    
    # Selector de derivación acoplado al mapa de canales
    derivacion_seleccionada = st.selectbox(
        "Seleccione la derivación electrocardiográfica a graficar de la matriz anterior:", 
        paciente["derivaciones"],
        index=1  # Preselecciona la derivación II
    )
    
    st.warning(f"Estructura lista. Esperando confirmación para renderizar la onda de la derivación {derivacion_seleccionada}...")

# 3. INYECCIÓN DE CÓDIGO CSS (Márgenes y Fuentes)
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

import streamlit as st

# Inicialización y configuración del Layout
st.set_page_config(page_title="AFibDetect System", page_icon="🩺", layout="wide")

# Inicializamos el estado para almacenar un solo paciente de CPSC-2018
if "paciente_activo" not in st.session_state:
    st.session_state["paciente_activo"] = None

# Título Principal
st.title("🩺 AFibDetect v1.0")
st.write("Cargue los archivos binarios (.hea y .dat) de un registro CPSC-2018 para su análisis.")

# 1. COMPONENTE DE CARGA DE ARCHIVOS (GUI)
# Modificado para aceptar múltiples archivos y filtrar por las extensiones de PhysioNet
archivos_subidos = st.file_uploader(
    "Seleccione o arrastre juntos los archivos .hea y .dat del registro:", 
    type=["hea", "dat"], 
    accept_multiple_files=True
)

# Simulador temporal de datos para ver la GUI bonita antes de conectar el lector real
if archivos_subidos and len(archivos_subidos) == 2:
    if st.session_state["paciente_activo"] is None:
        # Simulamos que leímos con éxito el registro A0001 para poder diseñar la interfaz
        st.session_state["paciente_activo"] = {
            "id_registro": "A0001",
            "frecuencia_muestreo": 300,
            "total_muestras": 3000,
            "derivaciones": ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"],
            "etiqueta_referencia": "AF"
        }
        st.success("Validación e ingesta biomédica completada con éxito.")

# 2. DESPLIEGUE DE METADATOS (Solo si el paciente ya está cargado en memoria)
if st.session_state["paciente_activo"] is not None:
    st.markdown("---")
    st.subheader("📊 Metadatos del Registro Seleccionado")
    
    # Extraemos el perfil del paciente activo
    paciente = st.session_state["paciente_activo"]
    
    # Calculamos la duración teórica (Muestras / Frecuencia)
    duracion_segundos = paciente["total_muestras"] / paciente["frecuencia_muestreo"]
    
    # Creamos 4 columnas visuales bonitas para presentar los datos clave
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="ID del Paciente", value=paciente["id_registro"])
    with col2:
        st.metric(label="Frecuencia de Muestreo", value=f"{paciente['frecuencia_muestreo']} Hz")
    with col3:
        st.metric(label="Duración del Registro", value=f"{duracion_segundos:.2f} s")
    with col4:
        st.metric(label="Etiqueta Cardiológica", value=paciente["etiqueta_referencia"])
        
    st.markdown("---")
    st.subheader("📈 Visualización de Derivaciones")
    
    # Selector desplegable para que el usuario elija cuál de las 12 derivaciones inspeccionar
    derivacion_seleccionada = st.selectbox(
        "Seleccione la derivación electrocardiográfica a graficar:", 
        paciente["derivaciones"],
        index=1  # Preselecciona la derivación II por defecto
    )
    
    # AQUÍ CONECTAREMOS EL GRÁFICO EN EL SIGUIENTE PASO
    st.info(f"Listo para renderizar la señal de la derivación {derivacion_seleccionada}...")

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
            font-size: 1.4rem !important;
            font-weight: 600;
        }
        .stText, p {
            font-size: 0.95rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

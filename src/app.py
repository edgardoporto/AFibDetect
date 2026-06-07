import streamlit as st
# Importamos la tabla de códigos desde tu archivo de configuración
from config import SNOMED_MAP

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
    "Seleccione o arrastre juntos los archivos .hea y .dat del registro:", 
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

# Simulador de datos de PhysioNet modificado con códigos reales
if archivos_subidos and len(archivos_subidos) == 2:
    if st.session_state["paciente_activo"] is None:
        # Simulamos que leímos el código "59118001" (RBBB) de la cabecera .hea
        codigo_snomed_detectado = "59118001" 
        
        # El traductor procesará dinámicamente la etiqueta según tu requerimiento
        etiqueta_procesada = traducir_codigo_snomed(codigo_snomed_detectado)
        
        st.session_state["paciente_activo"] = {
            "id_registro": "A0001.mat",
            "frecuencia_muestreo": 300,
            "total_muestras": 15000,
            "num_derivaciones": 12,
            "derivaciones": ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"],
            "etiqueta_referencia": etiqueta_procesada,  # <--- GUARDADO CON EL NUEVO FORMATO
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
    st.subheader("📈 Visualización Interactiva")
    




    st.markdown("---")
    st.subheader("📈 Visualización Interactiva Multiderivación")
    st.write("Seleccione los canales electrocardiográficos que desea inspeccionar en paralelo:")
    
    # 1. DISEÑO DE LA MATRIZ COMPACTA (Solo las siglas de los canales)
    cols_check = st.columns(6)
    derivaciones_seleccionadas = []
    
    for idx, derivacion in enumerate(paciente["derivaciones"]):
        col_actual = cols_check[idx % 6]
        with col_actual:
            # CORRECCIÓN: Eliminamos la palabra 'Derivación ' del texto visual para mayor compacidad
            if st.checkbox(derivacion, value=False, key=f"chk_{derivacion}"):
                derivaciones_seleccionadas.append(derivacion)

                
    # 2. RENDERIZADO REACTIVO DE GRÁFICOS (Abajo de la matriz)
    if derivaciones_seleccionadas:
        st.markdown("###") # Pequeño espacio de separación
        
        # Iteramos únicamente sobre los canales que el usuario activó
        for derivacion_activa in derivaciones_seleccionadas:
            
            # --- AQUÍ INVOCAREMOS PRÓXIMAMENTE LA FUNCIÓN GRÁFICA REAL DE Plotly ---
            # Por ahora, dejamos un contenedor visual informativo por cada canal seleccionado
            st.info(f"📈 [Espacio Reservado] Renderizando la señal en tiempo real para la **Derivación {derivacion_activa}**...")
            
    else:
        # Mensaje informativo si el usuario desmarcó todo
        st.warning("Seleccione al menos una derivación de la matriz superior para desplegar su análisis gráfico.")








# 3. INYECCIÓN DE CÓDIGO CSS
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



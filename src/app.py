import streamlit as st
import numpy as np

# 1. IMPORTACIÓN DE CONFIGURACIONES Y MÓDULOS DE PROCESAMIENTO
from config import SNOMED_MAP
from modules.data_loader import cargar_registro_unico_wfdb
from modules.dashboard import graficar_derivacion_ecg, graficar_comparativa_preprocesamiento
from modules.preprocessor import ejecutar_pipeline_preprocesamiento
from modules.inference import ejecutar_inferencia_segmentos
from modules.dashboard import graficar_derivacion_ecg, graficar_comparativa_preprocesamiento, graficar_ecg_coloreado_por_clase


# Inicialización y configuración del Layout
st.set_page_config(page_title="AFibDetect System", page_icon="🩺", layout="wide")

# 2. GESTIÓN DE ESTADO (In-Memory State Management)
if "paciente_activo" not in st.session_state:
    st.session_state["paciente_activo"] = None

if "datos_preprocesados" not in st.session_state:
    st.session_state["datos_preprocesados"] = None

# 3. INTERFAZ DE USUARIO: BARRA LATERAL (Menú de Navegación Estricto)
with st.sidebar:
    st.title("🩺 AFibDetect v1.0")
    st.markdown("---")
    st.markdown("### Navegación de Capas")
    
    # El menú izquierdo solo sirve como selector de pestañas del sistema
    menu_opcion = st.radio(
        "Seleccione un Módulo:",
        ["1. Carga de Señal", "2. Preprocesamiento", "3. Inferencia y Dashboard"]
    )
    st.markdown("---")
    st.caption("Arquitectura modular para la clasificación de arritmias.")

def traducir_codigo_snomed(codigo_crudo):
    codigo_str = str(codigo_crudo).strip()
    if codigo_str in SNOMED_MAP:
        nombre_real = SNOMED_MAP[codigo_str]
        return nombre_real if nombre_real in ["AF", "NSR", "Noise"] else f"Other ({nombre_real})"
    return "Other (Unknown)"

# ==============================================================================
# PANTALLA 1: MODULO DE INGRESO Y VALIDACIÓN DE DATOS
# ==============================================================================
# ==============================================================================
# PANTALLA 1: MODULO DE INGRESO Y VALIDACIÓN DE DATOS (VERSION HÍBRIDA)
# ==============================================================================
if menu_opcion == "1. Carga de Señal":
    st.header("📥 Módulo de Ingreso y Validación de Datos")
    st.write("Seleccione el método de ingreso de datos electrocardiográficos de la CPSC-2018:")
    
    # 1. SELECTOR DEL MODO DE INGESTA (GUI)
    modo_ingreso = st.radio(
        "Método de Ingesta:",
        ["🔬 Cargar Archivos Propios (.hea + .mat)", "🚀 Usar Registro de Demostración (Para Pruebas Rápidas)"],
        horizontal=True
    )
    
    st.markdown("###") # Pequeño espacio de separación
    
    # --- CASO A: EL USUARIO SUBE SUS PROPIOS ARCHIVOS ---
    if modo_ingreso == "🔬 Cargar Archivos Propios (.hea + .mat)":
        archivos_subidos = st.file_uploader(
            "Seleccione o arrastre juntos los archivos .hea y .mat del registro:", 
            type=["hea", "mat"],
            accept_multiple_files=True
        )

        if archivos_subidos and len(archivos_subidos) == 2:
            if st.session_state["paciente_activo"] is None:
                with st.spinner("Parseando matriz binaria de Matlab en memoria RAM..."):
                    registro_real, mensaje = cargar_registro_unico_wfdb(archivos_subidos)
                    
                    if registro_real:
                        registro_real["etiqueta_referencia"] = traducir_codigo_snomed(registro_real["codigo_snomed"])
                        registro_real["resolución_adc"] = "16-bit"
                        registro_real["ganancia_base"] = "1000 adu/mV"
                        registro_real["formato_almacenamiento"] = "Matlab v4 (Format 16)"
                        registro_real["metadatos_clinicos"] = "Registro Clínico CPSC-2018"
                        
                        st.session_state["paciente_activo"] = registro_real
                        st.session_state["datos_preprocesados"] = None 
                        st.success(mensaje)
                    else:
                        st.error(mensaje)
                        
    # --- CASO B: EL USUARIO ELIGE UN EJEMPLO DE LA BASE DE DATOS INTERNA ---
    else:
        st.write("Seleccione uno de los casos reales pre-cargados en el servidor para auditar el pipeline:")
        demo_seleccionado = st.selectbox(
            "Casos de Estudio Disponibles:",
            [
                "Caso 1: Ritmo Sinusal Normal de Referencia (NSR)",
                "Caso 2: Episodio Aguto de Fibrilación Auricular (AF)",
                "Caso 3: Patología de Bloqueo de Rama Derecha (Other - RBBB)"
            ]
        )
        
        # Mapeamos la selección de la GUI con los nombres reales de los archivos en disco
        mapa_demos = {
            "Caso 1: Ritmo Sinusal Normal de Referencia (NSR)": "ejemplo_NSR",
            "Caso 2: Episodio Aguto de Fibrilación Auricular (AF)": "ejemplo_AF",
            "Caso 3: Patología de Bloqueo de Rama Derecha (Other - RBBB)": "ejemplo_RBBB"
        }
        
        # Botón de carga instantánea
        if st.button("🚀 Inicializar Caso de Estudio Seleccionado", type="secondary"):
            with st.spinner("Cargando registro clínico desde el repositorio interno..."):
                from modules.data_loader import cargar_registro_ejemplo_interno
                
                archivo_base = mapa_demos[demo_seleccionado]
                registro_demo = cargar_registro_ejemplo_interno(archivo_base)
                
                if registro_demo:
                    registro_demo["etiqueta_referencia"] = traducir_codigo_snomed(registro_demo["codigo_snomed"])
                    registro_demo["resolución_adc"] = "16-bit"
                    registro_demo["ganancia_base"] = "1000 adu/mV"
                    registro_demo["formato_almacenamiento"] = "Matlab v4 (Format 16)"
                    registro_demo["metadatos_clinicos"] = "Caso de Estudio Pre-cargado CPSC-2018"
                    
                    st.session_state["paciente_activo"] = registro_demo
                    st.session_state["datos_preprocesados"] = None 
                    st.success(f"¡Éxito! {demo_seleccionado} cargado correctamente en memoria RAM.")
                else:
                    st.error("Error crítico: No se encontraron los archivos de ejemplo en la carpeta 'data/examples/'. Por favor verifique el repositorio de GitHub.")










    if st.session_state["paciente_activo"] is not None:
        st.markdown("---")
        st.subheader("📊 Panel Integral de Metadatos (Estándar PhysioNet)")
        
        paciente = st.session_state["paciente_activo"]
        duracion_segundos = paciente["total_muestras"] / paciente["frecuencia_muestreo"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Nombre del Registro", value=paciente["id_registro"])
        with col2:
            st.metric(label="Frecuencia de Muestreo", value=f"{paciente['frecuencia_muestreo']} Hz")
        with col3:
            st.metric(label="Duración del Registro", value=f"{duracion_segundos:.2f} s")
        with col4:
            st.metric(label="Diagnóstico de Referencia", value=paciente["etiqueta_referencia"])
            
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
        
        cols_check = st.columns(6)
        derivaciones_seleccionadas = []
        for idx, derivacion in enumerate(paciente["derivaciones"]):
            col_actual = cols_check[idx % 6]
            with col_actual:
                if st.checkbox(derivacion, value=False, key=f"chk_{derivacion}"):
                    derivaciones_seleccionadas.append(derivacion)
                    
        if derivaciones_seleccionadas:
            st.markdown("###")
            for derivacion_activa in derivaciones_seleccionadas:
                graficar_derivacion_ecg(paciente, derivacion_activa)
        else:
            st.warning("Seleccione al menos una derivación de la matriz superior para desplegar su análisis gráfico.")







# ==============================================================================
# PANTALLA 2: MODULO DE PREPROCESAMIENTO DE SEÑALES
# ==============================================================================
elif menu_opcion == "2. Preprocesamiento":
    st.header("⚡ Módulo de Preprocesamiento de Señales")
    st.write("Este módulo ejecuta la limpieza macro de la bioseñal y su fraccionamiento en tensores aptos para la red neuronal.")
    
    # Bloque de seguridad de software: Evita procesar si el usuario no cargó datos
    if st.session_state["paciente_activo"] is not None:
        paciente = st.session_state["paciente_activo"]
        
        st.markdown("---")
        st.markdown("### 🦾 Ejecución del Pipeline Analítico")
        st.write("El sistema procesará de forma estandarizada la **Derivación II** (canal de referencia clínico de diseño para el modelo) aplicando:")
        st.markdown("* **Filtro Butterworth Pasabanda:** 0.5 a 40.0 Hz\n* **Remuestreo Polifásico:** Reducción analítica de 300 Hz a **250 Hz**\n* **Normalización Global:** Estandarización por Z-score\n* **Corte Arquitectural:** Segmentación rígida en ventanas fijas de **10 segundos**")
        
        # BOTÓN CENTRAL DE ACCIÓN EN LA INTERFAZ
        if st.button("⚡ Ejecutar Pipeline de Preprocesamiento", type="primary"):
            with st.spinner("Ejecutando transformaciones matemáticas en segundo plano..."):
                # Invocamos la función orquestadora de preprocessor.py pasándole la matriz real
                resultados, mensaje = ejecutar_pipeline_preprocesamiento(
                    matriz_multiderivacion=paciente["senal_cruda"],
                    nombres_derivaciones=paciente["derivaciones"],
                    derivacion_objetivo="II",
                    fs_original=paciente["frecuencia_muestreo"]
                )
                
                if resultados:
                    st.session_state["datos_preprocesados"] = resultados
                    st.success(mensaje)
                else:
                    st.error(mensaje)
                    
        # Si el pipeline ya se corrió con éxito, desplegamos las tarjetas de control y la curva
        if st.session_state["datos_preprocesados"] is not None:
            proc = st.session_state["datos_preprocesados"]
            
            st.markdown("###")
            st.subheader("📊 Resultados del Pipeline de Diseño")
            
            # Mostramos el impacto numérico de la guillotina de segmentación
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.metric(label="Derivación Elegida", value=proc["derivacion_processed"] if "derivacion_processed" in proc else proc.get("derivacion_procesada", "II"))
            with col_p2:
                st.metric(label="Nueva Frecuencia (Destino)", value=f"{proc['fs_nueva']} Hz")
            with col_p3:
                st.metric(label="Segmentos de 10s Obtenidos", value=proc["cantidad_segmentos"])
                
            st.info(f"💡 Cada uno de los **{proc['cantidad_segmentos']} segmentos** cuenta con un vector exacto de **2,500 puntos de datos** (250 Hz x 10s) con Media = 0 y Varianza = 1, listos para la inyección de tensores.")
            

# 1. PRIMERO CALCULAMOS LOS VECTORES Y VALORES EN MEMORIA
            idx_ii = paciente["derivaciones"].index("II")
            senal_cruda_ii = paciente["senal_cruda"][idx_ii]
            tiempo_crudo = np.arange(len(senal_cruda_ii)) / paciente["frecuencia_muestreo"]
            
            # Calculamos la duración máxima ANTES de llamarla en el Slider
            duracion_maxima_segundos = float(len(proc["senal_continua_procesada"]) / proc["fs_nueva"])
            tiempo_procesado = np.arange(len(proc["senal_continua_procesada"])) / proc["fs_nueva"]
            
            st.markdown("###")
            st.subheader("🎛️ Selector de Ventana Temporal")
            st.write("Desplace el controlador para aislar e inspeccionar un tramo específico del registro continuo:")
            
            # 2. AHORA SÍ CREAMOS EL SLIDER (Ya conoce 'duracion_maxima_segundos')
            intervalo_seleccionado = st.slider(
                "Intervalo de inspección (Segundos):",
                min_value=0.0,
                max_value=duracion_maxima_segundos,
                value=(0.0, min(10.0, duracion_maxima_segundos)),
                step=0.5
            )
            
            # 3. FINALMENTE PINTAMOS EL GRÁFICO COMPARATIVO
            graficar_comparativa_preprocesamiento(
                tiempo_crudo=tiempo_crudo,
                senal_cruda=senal_cruda_ii,
                tiempo_procesado=tiempo_procesado,
                senal_procesada=proc["senal_continua_procesada"],
                nombre_lead="II",
                intervalo_tiempo=intervalo_seleccionado
            )


            
    else:
        st.warning("⚠️ No se han detectado datos en la memoria RAM del servidor. Por favor, regrese al Módulo 1 e ingrese un registro biomédico válido primero.")

# ==============================================================================
# PANTALLA 3: INFERENCIA Y DASHBOARD (MARCO DE TRABAJO PARA EL SIGUIENTE PASO)
# ==============================================================================
# ==============================================================================
# PANTALLA 3: INFERENCIA Y DASHBOARD (DISEÑO CENTRALIZADO)
# ==============================================================================
elif menu_opcion == "3. Inferencia y Dashboard":
    st.header("📊 Tablero de Control Estadístico y Diagnóstico")
    st.write("Evaluación computacional por segmentos temporales a través del clasificador profundo de arritmias.")
    
    # Bloque de seguridad de software: Verifica que existan tensores preprocesados
    if st.session_state["datos_preprocesados"] is not None:
        proc = st.session_state["datos_preprocesados"]
        paciente = st.session_state["paciente_activo"]
        
        st.markdown("---")
        st.markdown("### 🧠 Clasificación Computacional del Registro")
        st.write(f"El sistema alimentará el modelo utilizando los **{proc['cantidad_segmentos']} segmentos** de 10 segundos extraídos de la **Derivación {proc['derivacion_procesada']}**.")
        
        # BOTÓN CENTRAL DE ACCIÓN PARA LA INFERENCIA
        if st.button("🧠 Ejecutar Inferencia Computacional", type="primary"):
            with st.spinner("Inyectando tensores en la arquitectura del modelo..."):
                # Ejecutamos el motor analítico pasándole las ventanas y la etiqueta real
                predicciones_calculadas = ejecutar_inferencia_segmentos(
                    lista_segmentos=proc["lista_segmentos"],
                    etiqueta_referencia_global=paciente["etiqueta_referencia"]
                )
                # Guardamos los resultados de la red en la memoria de la sesión
                st.session_state["resultados_inferencia"] = predicciones_calculadas
                st.success("🤖 Clasificación completada de forma exitosa sobre el registro continuo.")
                
        # Si el usuario ya presionó el botón y las predicciones existen, desplegamos la tabla analítica
        if "resultados_inferencia" in st.session_state and st.session_state["resultados_inferencia"] is not None:
            st.markdown("###")
            st.subheader("📋 Reporte Diagnóstico por Segmento (Ventanas de 10s)")
            
            # Formateamos los diccionarios como una tabla/DataFrame estético para el usuario
            import pandas as pd
            df_reporte = pd.DataFrame(st.session_state["resultados_inferencia"])
            
            # Renombramos las columnas para que luzcan formales en la pantalla
            df_reporte.columns = ["Segmento", "Diagnóstico Predicho", "Prob NSR", "Prob AF", "Prob Other", "Prob Noise"]
            
            # Desplegamos la tabla interactiva de alta densidad informativa
            st.dataframe(
                df_reporte.style.format({
                    "Prob NSR": "{:.4f}",
                    "Prob AF": "{:.4f}",
                    "Prob Other": "{:.4f}",
                    "Prob Noise": "{:.4f}"
                }),
                use_container_width=True,
                hide_index=True
            )
            
  
# --- NUEVO CONTROLLER: SLIDER DUAL ARRASTRABLE Y ENSANCHABLE ---
            st.markdown("---")
            st.subheader("🎛️ Visor Temporal del Diagnóstico")
            st.write("Ajuste los extremos del bloque para ensanchar/reducir el rango de análisis, o arrástrelo completo para desplazarse:")
            
            # Calculamos la duración máxima real del registro en segundos
            duracion_maxima_segundos = float(len(proc["senal_continua_procesada"]) / proc["fs_nueva"])
            tiempo_procesado = np.arange(len(proc["senal_continua_procesada"])) / proc["fs_nueva"]
            
            # EL SECRETO DEL SLIDER DUAL: Pasamos una tupla (0.0, 10.0) en el parámetro 'value'
            # Esto crea un bloque de rango flotante seleccionable con dos manijas ajustables
            rango_seleccionado = st.slider(
                "Rango de Inspección Clínica (Segundos):",
                min_value=0.0,
                max_value=duracion_maxima_segundos,
                value=(0.0, min(10.0, duracion_maxima_segundos)), # Visor inicial por defecto de 10s
                step=0.5,
                key="slider_dual_diagnostico"
            )
            
            # Mapeo Informativo: Calculamos qué número de segmentos caen dentro de la ventana seleccionada
            seg_ini, seg_fin = rango_seleccionado
            idx_segmento_inicio = int(seg_ini // 10) + 1
            idx_segmento_fin = int((seg_fin - 0.01) // 10) + 1
            
            # Formateamos el reporte descriptivo para el usuario
            if idx_segmento_inicio == idx_segmento_fin:
                st.info(f"🔍 Inspeccionando morfológicamente el **Segmento {idx_segmento_inicio}** de la Inteligencia Artificial.")
            else:
                st.info(f"🔍 Inspeccionando una ventana ensanchada que abarca desde el **Segmento {idx_segmento_inicio}** hasta el **Segmento {idx_segmento_fin}**.")
            
            # Invocamos la gráfica coloreada pasándole el rango seleccionado
            graficar_ecg_coloreado_por_clase(
                tiempo_procesado=tiempo_procesado,
                senal_procesada=proc["senal_continua_procesada"],
                resultados_inferencia=st.session_state["resultados_inferencia"],
                intervalo_tiempo=rango_seleccionado, # Inyección de la tupla [inicio, fin]
                fs_nueva=proc["fs_nueva"]
            )





    else:
        st.warning("⚠️ Falta completar pasos previos. Asegúrese de haber cargado el archivo en el Módulo 1 y haber presionado el botón de preprocesamiento en el Módulo 2.")







# 4. INYECCIÓN DE CÓDIGO CSS (Control estético de fuentes y márgenes)
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


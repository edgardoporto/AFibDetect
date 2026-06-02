import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página (Debe ser la primera línea de Streamlit)
st.set_page_config(page_title="AFDetect - UNMSM", layout="wide")

st.header("🔬 AFDetect: Cross-Domain Multi-Class Classifier for AFib")
st.write("Cargue sus señales biomédicas, ajuste los parámetros del algoritmo y visualice los resultados en tiempo real.")

# --- 1. BARRA LATERAL: PARÁMETROS DEL ALGORITMO ---
with st.sidebar:
    st.header("⚙️ Parámetros del Algoritmo")
    
    # Aumentamos el rango máximo del umbral a 10000 para que se adapte a variables como 'pressure' o 'temperature'
    umbral = st.slider("Umbral de Detección (Threshold)", min_value=0.0, max_value=10000.0, value=30.0, step=0.5)
    frecuencia_muestreo = st.number_input("Frecuencia de Muestreo (Hz)", min_value=1, max_value=2000, value=250)
    
    # Caja de selección para el tipo de filtro
    tipo_filtro = st.selectbox("Filtro de Preprocesamiento", ["Ninguno", "Pasa-banda Butterworth", "Filtro Notch (50/60 Hz)", "Media Móvil"])

# --- 2. ÁREA PRINCIPAL: CARGA DE ARCHIVOS ---
st.subheader("📂 1. Carga de Datos")
archivo_cargado = st.file_uploader("Seleccione un archivo de señal (Formatos soportados: CSV, TXT)", type=["csv", "txt"])

# --- 3. PROCESAMIENTO Y VISUALIZACIÓN ---
if archivo_cargado is not None:
    try:
        # Leer el archivo con punto y coma como separador
        df = pd.read_csv(archivo_cargado, sep=';')
        
        st.success("¡Archivo cargado con éxito!")
        
        # Mostrar una vista previa de la tabla de datos en un contenedor colapsable
        with st.expander("Ver tabla de datos crudos"):
            st.dataframe(df.head(10))
        
        # Verificar si hay columnas numéricas para graficar
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(columnas) > 0:
            st.header("📊 2. Visualización y Procesamiento de la Señal")
            
            # Selector para que el usuario elija qué columna graficar
            columna_seleccionada = st.selectbox("Seleccione la columna de la señal a analizar:", columnas)
            
            # Extraer la señal para el procesamiento global
            señal_original = df[columna_seleccionada].values
            
            # Lógica de detección basada en el umbral configurado
            indices_detectados = np.where(señal_original > umbral)[0]
            total_eventos = len(indices_detectados)
            
            # Crear métricas de resumen en pantalla
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Muestras", len(señal_original))
            with col2:
                st.metric("Filtro Aplicado", tipo_filtro)
            with col3:
                st.metric("Eventos Detectados", total_eventos)
            
            st.subheader(f"Gráfico de la señal: {columna_seleccionada}")
            
            # CONTROL DE RENDIMIENTO: Selector de rango numérico interactivo
            # Por defecto selecciona las primeras 2,000 muestras para no colapsar la PC
            rango = st.slider(
                "Seleccione el rango de muestras a visualizar en la gráfica:", 
                min_value=0, 
                max_value=len(df), 
                value=(0, min(2000, len(df)))
            )
            
            # Extraer únicamente el segmento seleccionado por el usuario
            datos_segmento = df[columna_seleccionada].iloc[rango[0]:rango[1]]
            
            # Renderizar el gráfico con datos livianos
            st.line_chart(datos_segmento)
            
        else:
            st.error("El archivo cargado no contiene columnas numéricas válidas para graficar.")
            
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    # Mensaje de espera si no hay archivo
    st.info("Por favor, cargue un archivo en el panel de arriba para activar las gráficas y el análisis.")

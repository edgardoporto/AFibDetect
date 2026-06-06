import streamlit as st
import pandas as pd
import numpy as np
import os

# 1. CONFIGURACIÓN DE LA PÁGINA (¡Obligatoriamente debe ser la primera línea de Streamlit!)
st.set_page_config(page_title="AFDetect - UNMSM", layout="wide")

st.header("🔬 AFDetect: Cross-Domain Multi-Class Classifier for AFib")
st.write("Cargue sus señales biomédicas, ajuste los parámetros del algoritmo y visualice los resultados en tiempo real.")

# --- 2. BARRA LATERAL: PARÁMETROS DEL ALGORITMO ---
with st.sidebar:
    st.header("⚙️ Parámetros del Algoritmo")
    
    # Rango máximo del umbral a 10000 para adaptarse a variables como 'pressure' o 'temperature'
    umbral = st.slider("Umbral de Detección (Threshold)", min_value=0.0, max_value=10000.0, value=30.0, step=0.5)
    frecuencia_muestreo = st.number_input("Frecuencia de Muestreo (Hz)", min_value=1, max_value=2000, value=250)
    
    # Caja de selección para el tipo de filtro
    tipo_filtro = st.selectbox("Filtro de Preprocesamiento", ["Ninguno", "Pasa-banda Butterworth", "Filtro Notch (50/60 Hz)", "Media Móvil"])

# --- 3. ÁREA PRINCIPAL: CARGA DE ARCHIVOS ---
st.subheader("📂 1. Carga de Datos")
archivo_cargado = st.file_uploader("Seleccione un archivo de señal (Formatos soportados: CSV, TXT)", type=["csv", "txt"])

# --- 4. PROCESAMIENTO Y VISUALIZACIÓN ---
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


# --- 5. SECCIÓN DE APRENDIZAJE (AL FINAL ABSOLUTO DEL ARCHIVO) ---
st.markdown("---") 
st.title("📚 Códigos de ejemplo")

carpeta_paginas = "pages"

# Leer dinámicamente los archivos reales de la carpeta pages
if os.path.exists(carpeta_paginas):
    archivos_ejemplo = [f for f in os.listdir(carpeta_paginas) if f.endswith(".py")]
else:
    archivos_ejemplo = []

if not archivos_ejemplo:
    archivos_ejemplo = ["No se encontraron archivos .py"]

archivo_seleccionado = st.selectbox(
    "Selecciona un código de ejemplo para revisar cómo funciona:", 
    archivos_ejemplo
)

# Buscar y mostrar el archivo seleccionado dentro de la carpeta pages
if archivo_seleccionado != "No se encontraron archivos .py":
    ruta_completa = os.path.join(carpeta_paginas, archivo_seleccionado)
    if os.path.exists(ruta_completa):
        with open(ruta_completa, "r", encoding="utf-8") as f:
            codigo_fuente = f.read()
        
        st.subheader(f"📄 Archivo: {archivo_seleccionado}")
        st.code(codigo_fuente, language="python")
    else:
        st.error(f"No se pudo cargar el archivo {archivo_seleccionado}")
else:
    st.info("Coloque archivos .py dentro de la carpeta 'pages' para verlos aquí.")

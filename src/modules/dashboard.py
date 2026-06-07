# pip install plotly

import plotly.graph_objects as go
import streamlit as st
import numpy as np

def graficar_derivacion_ecg(paciente, nombre_derivacion):
    """
    Extrae los datos de voltaje de una derivación específica del paciente
    y renderiza un gráfico interactivo con zoom utilizando Plotly.
    """
    # 1. Localizamos el índice de la fila que corresponde al nombre de la derivación
    idx_canal = paciente["derivaciones"].index(nombre_derivacion)
    
    # 2. Extraemos el vector de voltaje [Muestras] y su frecuencia de muestreo
    voltaje = paciente["senal_cruda"][idx_canal]
    fs = paciente["frecuencia_muestreo"]
    
    # 3. Construimos el eje x en segundos reales (Muestra / Frecuencia)
    tiempo_segundos = np.arange(len(voltaje)) / fs
    
    # 4. Diseñamos la figura de Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=tiempo_segundos,
        y=voltaje,
        mode='lines',
        name=f"Canal {nombre_derivacion}",
        line=dict(color='#FF4B4B', width=1.2) # Rojo clínico estandarizado
    ))
    
    # Configuración de diseño con estándares estéticos para papers Q1
    fig.update_layout(
        title=f"Señal Electrocardiográfica: Derivación {nombre_derivacion}",
        xaxis_title="Tiempo (Segundos)",
        yaxis_title="Amplitud (mV)",
        template="plotly_white", # Fondo blanco limpio para publicaciones
        height=320,              # Altura compacta para permitir visualizaciones múltiples en paralelo
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        dragmode="zoom"          # Habilita el zoom por recuadro de forma nativa
    )
    
    # Desplegamos el gráfico dentro de la interfaz web de Streamlit
    st.plotly_chart(fig, use_container_width=True, key=f"plot_{nombre_derivacion}")




def graficar_comparativa_preprocesamiento(tiempo_crudo, senal_cruda, tiempo_procesado, senal_procesada, nombre_lead):
    """
    Genera dos trazas en un mismo gráfico interactivo de Plotly para comparar el ECG
    antes (crudo) y después (procesado) del pipeline de limpieza.
    """
    fig = go.Figure()
    
    # Traza 1: Señal Cruda (Graficamos solo los primeros 10 segundos para que se aprecien las ondas)
    fig.add_trace(go.Scatter(
        x=tiempo_crudo[:3000], # Primeros 10s a 300Hz
        y=senal_cruda[:3000],
        mode='lines',
        name='ECG Crudo Original (300 Hz)',
        line=dict(color='#BDC3C7', width=1.0, dash='dash') # Gris punteado
    ))
    
    # Traza 2: Señal Procesada
    fig.add_trace(go.Scatter(
        x=tiempo_procesado[:2500], # Primeros 10s a 250Hz
        y=senal_normalizada_plot := senal_procesada[:2500],
        mode='lines',
        name='ECG Procesado Destino (250 Hz, Filtrado y Normalizado)',
        line=dict(color='#2ECC71', width=1.3) # Verde limpio
    ))
    
    fig.update_layout(
        title=f"Impacto del Pipeline de Preprocesamiento — Derivación {nombre_lead} (Primeras Ventanas)",
        xaxis_title="Tiempo (Segundos)",
        yaxis_title="Amplitud Normalizada / Voltaje",
        template="plotly_white",
        height=380,
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True, key=f"comp_{nombre_lead}")

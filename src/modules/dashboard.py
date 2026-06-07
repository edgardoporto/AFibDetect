import plotly.graph_objects as go
import streamlit as st
import numpy as np

def graficar_derivacion_ecg(paciente, nombre_derivacion):
    """
    Extrae los datos de voltaje de una derivación específica del paciente
    y renderiza un gráfico interactivo con zoom utilizando Plotly.
    """
    idx_canal = paciente["derivaciones"].index(nombre_derivacion)
    voltaje = paciente["senal_cruda"][idx_canal]
    fs = paciente["frecuencia_muestreo"]
    
    tiempo_segundos = np.arange(len(voltaje)) / fs
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tiempo_segundos,
        y=voltaje,
        mode='lines',
        name=f"Canal {nombre_derivacion}",
        line=dict(color='#FF4B4B', width=1.2)
    ))
    
    fig.update_layout(
        title=f"Señal Electrocardiográfica: Derivación {nombre_derivacion}",
        xaxis_title="Tiempo (Segundos)",
        yaxis_title="Amplitud (mV)",
        template="plotly_white",
        height=320,
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
        dragmode="zoom"
    )
    st.plotly_chart(fig, use_container_width=True, key=f"plot_{nombre_derivacion}")


def graficar_comparativa_preprocesamiento(tiempo_crudo, senal_cruda, tiempo_procesado, senal_procesada, nombre_lead):
    """
    Genera un gráfico interactivo de Plotly para comparar el ECG
    antes (crudo) y después (procesado) del pipeline de limpieza.
    """
    fig = go.Figure()
    
    # Traza 1: Señal Cruda (Primeros 10 segundos a 300Hz = 3000 muestras)
    fig.add_trace(go.Scatter(
        x=tiempo_crudo[:3000],
        y=senal_cruda[:3000],
        mode='lines',
        name='ECG Crudo Original (300 Hz)',
        line=dict(color='#BDC3C7', width=1.0, dash='dash')
    ))
    
    # Traza 2: Señal Procesada (Primeros 10 segundos a 250Hz = 2500 muestras)
    fig.add_trace(go.Scatter(
        x=tiempo_procesado[:2500],
        y=senal_procesada[:2500],
        mode='lines',
        name='ECG Procesado Destino (250 Hz, Filtrado y Normalizado)',
        line=dict(color='#2ECC71', width=1.3)
    ))
    
    fig.update_layout(
        title=f"Impacto del Pipeline de Preprocesamiento — Derivación {nombre_lead} (Primeras Ventanas)",
        xaxis_title="Tiempo (Segundos)",
        yaxis_title="Amplitud / Voltaje Normalizado",
        template="plotly_white",
        height=380,
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True, key=f"comp_{nombre_lead}")

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






from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import numpy as np

def graficar_comparativa_preprocesamiento(tiempo_crudo, senal_cruda, tiempo_procesado, senal_procesada, nombre_lead, fs_original=500, fs_nueva=250):
    """
    Genera un gráfico interactivo con doble eje Y para comparar con absoluta nitidez
    el ECG crudo frente al procesado, escalando cada traza de forma independiente.
    """
    muestras_10s_crudo = int(10 * fs_original)     # 5000 muestras a 500 Hz
    muestras_10s_procesado = int(10 * fs_nueva)   # 2500 muestras a 250 Hz
    
    # Creamos una figura especial con un eje Y secundario habilitado
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Traza 1: Señal Cruda (Asociada al eje Y Izquierdo - Original)
    fig.add_trace(
        go.Scatter(
            x=tiempo_crudo[:muestras_10s_crudo],
            y=senal_cruda[:muestras_10s_crudo],
            mode='lines',
            name=f'ECG Crudo ({fs_original} Hz)',
            line=dict(color='#A0AEC0', width=1.2, dash='dash') # Gris más oscuro y nítido
        ),
        secondary_y=False # Se dibuja usando la escala de la izquierda
    )
    
    # Traza 2: Señal Procesada (Asociada al eje Y Derecho - Secundario)
    fig.add_trace(
        go.Scatter(
            x=tiempo_procesado[:muestras_10s_procesado],
            y=senal_procesada[:muestras_10s_procesado],
            mode='lines',
            name=f'ECG Procesado ({fs_nueva} Hz)',
            line=dict(color='#2ECC71', width=1.4) # Verde brillante
        ),
        secondary_y=True # Se dibuja usando la escala de la derecha
    )
    
    # Configuración estética y de títulos de los ejes independientes
    fig.update_layout(
        title=f"Impacto del Pipeline de Preprocesamiento — Derivación {nombre_lead} (Primeros 10 Segundos)",
        xaxis_title="Tiempo (Segundos)",
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified"
    )
    
    # Títulos individuales para cada eje vertical
    fig.update_yaxes(title_text="<b>Amplitud Cruda (Voltaje Original)</b>", secondary_y=False, color='#718096')
    fig.update_yaxes(title_text="<b>Amplitud Normalizada (Z-score)</b>", secondary_y=True, color='#2ECC71')
    
    st.plotly_chart(fig, use_container_width=True, key=f"comp_{nombre_lead}")


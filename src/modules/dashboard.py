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


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import numpy as np

def graficar_comparativa_preprocesamiento(tiempo_crudo, senal_cruda, tiempo_procesado, senal_procesada, nombre_lead, fs_original=500, fs_nueva=250):
    """
    Genera un gráfico interactivo con doble eje Y, optimizando el ancho total de la pantalla
    al reubicar la leyenda en la parte inferior y aplicando un color rojo tenue a la señal cruda.
    """
    muestras_10s_crudo = int(10 * fs_original)     # 5000 muestras a 500 Hz
    muestras_10s_procesado = int(10 * fs_nueva)   # 2500 muestras a 250 Hz
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Traza 1: Señal Cruda (Asociada al eje Y Izquierdo - Rojo Tenue)
    fig.add_trace(
        go.Scatter(
            x=tiempo_crudo[:muestras_10s_crudo],
            y=senal_cruda[:muestras_10s_crudo],
            mode='lines',
            name=f'ECG Crudo Original ({fs_original} Hz)',
            line=dict(color='#FCA5A5', width=1.1, dash='dash') # <-- AJUSTE: Rojo suave punteado
        ),
        secondary_y=False
    )
    
    # Traza 2: Señal Procesada (Asociada al eje Y Derecho - Verde Brillante)
    fig.add_trace(
        go.Scatter(
            x=tiempo_procesado[:muestras_10s_procesado],
            y=senal_procesada[:muestras_10s_procesado],
            mode='lines',
            name=f'ECG Procesado Destino ({fs_nueva} Hz)',
            line=dict(color='#2ECC71', width=1.4)
        ),
        secondary_y=True
    )
    
    # Configuración de diseño con la leyenda abajo en formato horizontal
    fig.update_layout(
        title=f"Impacto del Pipeline de Preprocesamiento — Derivación {nombre_lead} (Primeros 10 Segundos)",
        xaxis_title="Tiempo (Segundos)",
        template="plotly_white",
        height=420,
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        # --- AJUSTE: Reubicación de la leyenda abajo ---
        legend=dict(
            orientation="h",       # Orientación horizontal
            yanchor="bottom",
            y=-0.25,               # Desplazamiento hacia abajo (afuera del gráfico)
            xanchor="center",
            x=0.5                  # Centrado horizontalmente
        )
    )
    
    # Títulos de los ejes verticales
    fig.update_yaxes(title_text="<b>Amplitud Cruda (Voltaje Original)</b>", secondary_y=False, color='#E53E3E')
    fig.update_yaxes(title_text="<b>Amplitud Normalizada (Z-score)</b>", secondary_y=True, color='#2ECC71')
    
    st.plotly_chart(fig, use_container_width=True, key=f"comp_{nombre_lead}")



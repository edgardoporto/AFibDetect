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




from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import numpy as np

def graficar_comparativa_preprocesamiento(tiempo_crudo, senal_cruda, tiempo_procesado, senal_procesada, nombre_lead, fs_original=500, fs_nueva=250):
    """
    Genera un gráfico interactivo con doble eje Y, asegurando que el ECG procesado
    esté en primer plano, el crudo como traza continua detrás, y los íconos limpios.
    """
    muestras_10s_crudo = int(10 * fs_original)     # 5000 muestras a 500 Hz
    muestras_10s_procesado = int(10 * fs_nueva)   # 2500 muestras a 250 Hz
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # CAPA 1 (FONDO): TRAZA ROJA EN LÍNEA CONTINUA
    # Al declararse primero, Python la dibuja atrás en el lienzo digital
    fig.add_trace(
        go.Scatter(
            x=tiempo_crudo[:muestras_10s_crudo],
            y=senal_cruda[:muestras_10s_crudo],
            mode='lines',
            name=f'ECG Crudo Original ({fs_original} Hz)',
            line=dict(color='#FCA5A5', width=1.1) # <-- CORREGIDO: Trazo continuo suave
        ),
        secondary_y=False
    )
    
    # CAPA 2 (PRIMER PLANO): TRAZA VERDE EN LÍNEA CONTINUA ENFÁTICA
    # Al declararse después, se sobrepone de forma limpia sobre los trazos que coincidan
    fig.add_trace(
        go.Scatter(
            x=tiempo_procesado[:muestras_10s_procesado],
            y=senal_procesada[:muestras_10s_procesado],
            mode='lines',
            name=f'ECG Procesado Destino ({fs_nueva} Hz)',
            line=dict(color='#2ECC71', width=1.4) # Verde nítido predominante
        ),
        secondary_y=True
    )
    
    # Configuración avanzada del Layout arquitectural
    fig.update_layout(
        title=f"Impacto del Pipeline de Preprocesamiento — Derivación {nombre_lead} (Primeros 10 Segundos)",
        xaxis_title="Tiempo (Segundos)",
        template="plotly_white",
        height=440,
        margin=dict(l=40, r=40, t=80, b=40), # <-- AJUSTE: Ampliamos margen superior para los íconos
        hovermode="x unified",
        
        # Reubicación estética de la leyenda horizontal abajo
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        )
    )
    
    # AJUSTE DE LA BARRA DE HERRAMIENTAS: Evita que flote encima de las letras del título
    # Forzamos a que aparezca debajo o de forma más integrada en el marco gráfico
    fig.update_layout(modebar=dict(orientation='v', bgcolor='rgba(0,0,0,0)'))
    
    # Títulos individuales y colores de los ejes verticales de referencia
    fig.update_yaxes(title_text="<b>Amplitud Cruda (Voltaje Original)</b>", secondary_y=False, color='#E53E3E')
    fig.update_yaxes(title_text="<b>Amplitud Normalizada (Z-score)</b>", secondary_y=True, color='#2ECC71')
    
    st.plotly_chart(fig, use_container_width=True, key=f"comp_{nombre_lead}")


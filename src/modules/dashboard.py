import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots

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







def graficar_comparativa_preprocesamiento(tiempo_crudo, senal_cruda, tiempo_procesado, senal_procesada, nombre_lead, intervalo_tiempo, fs_original=500, fs_nueva=250):
    """
    Genera un gráfico interactivo con doble eje Y, acotando la vista inicial al 
    intervalo de segundos (ej:) seleccionado dinámicamente por el usuario.
    """
    seg_inicio, seg_fin = intervalo_tiempo
    
    # Traducimos los segundos seleccionados a índices exactos según la frecuencia de muestreo
    idx_inicio_crudo = int(seg_inicio * fs_original)
    idx_fin_crudo = int(seg_fin * fs_original)
    
    idx_inicio_proc = int(seg_inicio * fs_nueva)
    idx_fin_proc = int(seg_fin * fs_nueva)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # CAPA 1 (FONDO): TRAZA ROJA EN LÍNEA CONTINUA (Recortada al intervalo activo)
    fig.add_trace(
        go.Scatter(
            x=tiempo_crudo[idx_inicio_crudo:idx_fin_crudo],
            y=senal_cruda[idx_inicio_crudo:idx_fin_crudo],
            mode='lines',
            name=f'ECG Crudo Original ({fs_original} Hz)',
            line=dict(color='#FCA5A5', width=1.1)
        ),
        secondary_y=False
    )
    
    # CAPA 2 (PRIMER PLANO): TRAZA VERDE (Recortada al intervalo activo)
    fig.add_trace(
        go.Scatter(
            x=tiempo_procesado[idx_inicio_proc:idx_fin_proc],
            y=senal_procesada[idx_inicio_proc:idx_fin_proc],
            mode='lines',
            name=f'ECG Procesado Destino ({fs_nueva} Hz)',
            line=dict(color='#2ECC71', width=1.4)
        ),
        secondary_y=True
    )
    
    # Configuración de Layout Estándar
    fig.update_layout(
        title=f"Impacto del Pipeline de Preprocesamiento — Derivación {nombre_lead} (Ventana: {seg_inicio}s - {seg_fin}s)",
        xaxis_title="Tiempo (Segundos)",
        template="plotly_white",
        height=440,
        margin=dict(l=40, r=40, t=90, b=40), 
        hovermode="x unified",
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        )
    )
    
    fig.update_yaxes(title_text="<b>Amplitud Cruda (Voltaje Original)</b>", secondary_y=False, color='#E53E3E')
    fig.update_yaxes(title_text="<b>Amplitud Normalizada (Z-score)</b>", secondary_y=True, color='#2ECC71')
    
    config_grafico = {
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    }
    
    st.plotly_chart(fig, use_container_width=True, key=f"comp_{nombre_lead}", config=config_grafico)

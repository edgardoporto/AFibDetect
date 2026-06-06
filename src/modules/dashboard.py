# pip install plotly
import plotly.graph_objects as go
import streamlit as st

def graficar_ecg_crudo(df):
    """Genera un gráfico interactivo de la señal de ECG cruda usando Plotly."""
    senal = df.iloc[:, 0]
    tiempo = senal.index
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tiempo, y=senal, mode='lines', name='ECG Crudo',
        line=dict(color='#FF4B4B', width=1.5)
    ))
    fig.update_layout(
        title="Visualización Preliminar del Registro Electrocardiográfico (Crudo)",
        xaxis_title="Muestras", yaxis_title="Amplitud",
        template="plotly_white", height=400
    )
    st.plotly_chart(fig, use_container_width=True)

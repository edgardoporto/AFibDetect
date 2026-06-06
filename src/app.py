import streamlit as st

# Importaciones directas aprovechando la jerarquía de tu repositorio
from modules.data_loader import cargar_archivo_csv, validar_estructura_ecg
from modules.dashboard import graficar_ecg_crudo

st.set_page_config(page_title="AFibDetect System", page_icon="🩺", layout="wide")

if "df_ecg" not in st.session_state:
    st.session_state["df_ecg"] = None

st.title("🩺 AFibDetect v1.0")

archivo_subido = st.file_uploader("Cargar registro ECG (Formato CSV)", type=["csv"])

if archivo_subido is not None:
    df_temporal = cargar_archivo_csv(archivo_subido)
    es_valido, mensaje = validar_estructura_ecg(df_temporal)
    
    if es_valido:
        st.session_state["df_ecg"] = df_temporal
        st.success(mensaje)
        graficar_ecg_crudo(st.session_state["df_ecg"])
    else:
        st.error(mensaje)



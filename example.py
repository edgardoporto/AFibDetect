import streamlit as st
import pandas as pd

st.title("Mi primera App con Streamlit")
st.write("Aquí se visualizará los datos y resultados de forma interactiva")

# Crear un slider
n_filas = st.slider("Selecciona el número de filas a mostrar", 1, 100)

# Generar datos aleatorios y mostrarlos
df = pd.DataFrame({'Columna A': range(n_filas)})
st.line_chart(df)


# Ejemplo visual de cómo se estructura la GUI en código
# 1. Configurar barra lateral
with st.sidebar:
    st.header("Configuración")
    opcion = st.selectbox("Elige una opción", ["A", "B"])

# 2. Configurar el cuerpo principal en columnas
col1, col2 = st.columns(2)

with col1:
    st.header("Columna Izquierda")
    st.button("Botón Acción")

with col2:
    st.header("Columna Derecha")
    st.metric(label="Temperatura", value="24 °C", delta="1.2 °C")

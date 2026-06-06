import pandas as pd
import numpy as np

def cargar_archivo_csv(uploaded_file):
    """Lee un archivo CSV. Devuelve un DataFrame de Pandas o None."""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return None

def validar_estructura_ecg(df):
    """Verifica que los datos cargados sean correctos."""
    if df is None or df.empty:
        return False, "El archivo está vacío o no se pudo procesar."
    primera_columna = df.iloc[:, 0]
    if not np.issubdtype(primera_columna.dtype, np.number):
        return False, "Los datos del archivo no son numéricos."
    return True, "Validación exitosa. Señal lista para procesamiento."

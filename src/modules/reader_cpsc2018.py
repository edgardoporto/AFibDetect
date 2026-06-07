import wfdb
import os
import numpy as np
import scipy.io

def leer_registro_cpsc2018(ruta_base_registro):
    """
    Lector híbrido de alta robustez para registros CPSC-2018.
    Intenta leer con WFDB; si falla por restricciones de Linux, lee la matriz .mat directamente.
    """
    try:
        # Intento estándar con la librería oficial de PhysioNet
        record, header = wfdb.rdsamp(ruta_base_registro)
        matriz_multiderivacion = record.T
        nombres_canales = header['sig_name']
        frecuencia_muestreo = header['fs']
        codigo_snomed = "Unknown"
        comentarios = header.get('comments', [])
        for comentario in comentarios:
            if "Dx:" in comentario:
                codigo_snomed = comentario.split(":")[-1].strip()
                break
    except Exception:
        # PLAN DE RESPALDO (FALLBACK): Lectura directa de la matriz de MATLAB si WFDB colapsa en Linux
        try:
            ruta_mat = ruta_base_registro + ".mat"
            ruta_hea = ruta_base_registro + ".hea"
            
            # Cargamos la estructura .mat usando SciPy
            mat_data = scipy.io.loadmat(ruta_mat)
            # En CPSC-2018, la señal siempre se guarda dentro de una variable llamada 'val'
            matriz_cruda = mat_data['val'] 
            
            # Las señales crudas de la CPSC vienen en formato entero; las convertimos a milivoltios (mV)
            # dividiendo entre la ganancia estándar de PhysioNet (1000 adu/mV)
            matriz_multiderivacion = matriz_cruda / 1000.0
            
            # Valores por defecto del estándar CPSC-2018 si no se puede parsear el texto del .hea
            frecuencia_muestreo = 500
            nombres_canales = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
            codigo_snomed = "Unknown"
            
            # Intentamos extraer el código SNOMED-CT real leyendo el archivo de texto plano .hea
            if os.path.exists(ruta_hea):
                with open(ruta_hea, "r") as f:
                    for linea in f:
                        if "Dx:" in linea:
                            codigo_snomed = linea.split(":")[-1].strip()
                            break
        except Exception as e:
            print(f"Error crítico en lector híbrido: {e}")
            return None
            
    # Estructura del Contrato Unificado de Memoria
    return {
        "id_registro": os.path.basename(ruta_base_registro) + ".mat",
        "frecuencia_muestreo": frecuencia_muestreo,
        "total_muestras": matriz_multiderivacion.shape,
        "num_derivaciones": len(nombres_canales),
        "derivaciones": nombres_canales,
        "senal_cruda": matriz_multiderivacion,
        "codigo_snomed": codigo_snomed
    }

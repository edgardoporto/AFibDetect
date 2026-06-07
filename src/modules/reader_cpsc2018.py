import wfdb
import os
import numpy as np

def leer_registro_cpsc2018(ruta_base_registro):
    """
    Lee un registro multiderivación real en formato WFDB (MATLAB .mat + .hea)
    y lo unifica bajo la estructura estricta del proyecto.
    """
    try:
        # wfdb.rdsamp extrae simultáneamente la matriz de voltajes y los metadatos de cabecera
        record, header = wfdb.rdsamp(ruta_base_registro)
        
        # Transponemos la matriz desde [Muestras, Canales] hacia el estándar [Canales, Muestras]
        matriz_multiderivacion = record.T
        nombres_canales = header['sig_name']
        frecuencia_muestreo = header['fs']
        puntos_totales = record.shape[0]
        
        # Extracción de la etiqueta diagnóstica (SNOMED-CT) contenida en los comentarios
        codigo_snomed = "Unknown"
        comentarios = header.get('comments', [])
        for comentario in comentarios:
            if "Dx:" in comentario:
                # Extrae el código después de los dos puntos (ej: "# Dx: 164889003" -> "164889003")
                codigo_snomed = comentario.split(":")[-1].strip()
                break
                
        # Estructura limpia de memoria
        return {
            "id_registro": os.path.basename(ruta_base_registro) + ".mat",
            "frecuencia_muestreo": frecuencia_muestreo,
            "total_muestras": puntos_totales,
            "num_derivaciones": len(nombres_canales),
            "derivaciones": nombres_canales,
            "senal_cruda": matriz_multiderivacion, # <-- VOLTAJES REALES DE MATLAB
            "codigo_snomed": codigo_snomed
        }
    except Exception as e:
        print(f"Error interno en lector de CPSC-2018: {e}")
        return None

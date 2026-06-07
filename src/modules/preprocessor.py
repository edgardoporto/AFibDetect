import numpy as np
from scipy.signal import butter, filtfilt, resample_poly

def filtro_butterworth_pasabanda(senal, lowcut=0.5, highcut=40.0, fs=300.0, order=4):
    """
    Aplica un filtro Butterworth pasabanda de fase cero (filtfilt) 
    para eliminar la línea base errante (<0.5 Hz) y el ruido de alta frecuencia (>40 Hz).
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, senal)

def remuestrear_senal(senal, fs_original=300, fs_nueva=250):
    """
    Cambia la frecuencia de muestreo de la señal utilizando interpolación polifásica (resample_poly),
    que es la forma más limpia y precisa en señales biomédicas para evitar aliasing.
    """
    if fs_original == fs_nueva:
        return senal
    # Calcula la relación matemática de conversión
    return resample_poly(senal, fs_nueva, fs_original)

def normalizar_zscore(senal):
    """
    Normaliza globalmente la señal restando la media y dividiendo por la desviación estándar.
    Garantiza que el vector tenga media 0 y varianza 1, estabilizando la convergencia de la red neuronal.
    """
    media = np.mean(senal)
    desviacion = np.std(senal)
    # Evitamos división por cero en señales muertas o planas
    if desviacion == 0:
        return senal
    return (senal - media) / desviacion

def segmentar_senal(senal, fs=250, duracion_segmento_seg=10):
    """
    Fracciona la señal continua en bloques independientes de 10 segundos.
    Devuelve una lista con los fragmentos de voltaje numérico.
    """
    muestras_por_segmento = int(duracion_segmento_seg * fs)
    total_muestras = len(senal)
    
    segmentos = []
    # Iteramos a lo largo del vector saltando el tamaño exacto del bloque
    for i in range(0, total_muestras, muestras_por_segmento):
        fin = i + muestras_por_segmento
        # Solo guardamos el segmento si está completo (requisito estricto de tensores)
        if fin <= total_muestras:
            segmentos.append(senal[i:fin])
            
    return segmentos

def ejecutar_pipeline_preprocesamiento(matriz_multiderivacion, nombres_derivaciones, derivacion_objetivo="II", fs_original=300):
    """
    Función orquestadora que ejecuta los 4 pasos secuencialmente sobre la derivación seleccionada.
    """
    try:
        # 1. Extraemos la fila de la matriz correspondiente a la derivación seleccionada
        idx_canal = nombres_derivaciones.index(derivacion_objetivo)
        senal_cruda = matriz_multiderivacion[idx_canal]
        
        # 2. Aplicamos Filtrado Pasabanda (0.5 a 40 Hz)
        senal_filtrada = filtro_butterworth_pasabanda(senal_cruda, lowcut=0.5, highcut=40.0, fs=fs_original)
        
        # 3. Aplicamos Resampling a la nueva frecuencia de diseño (250 Hz)
        fs_nueva = 250
        senal_resampleada = remuestrear_senal(senal_filtrada, fs_original=fs_original, fs_nueva=fs_nueva)
        
        # 4. Aplicamos Normalización Z-score sobre el registro completo
        senal_normalizada = normalizar_zscore(senal_resampleada)
        
        # 5. Aplicamos Segmentación final en bloques de 10 segundos
        segmentos_finales = segmentar_senal(senal_normalizada, fs=fs_nueva, duracion_segmento_seg=10)
        
        # Empaquetamos los resultados en un diccionario para la persistencia de sesión
        resultados_preprocesamiento = {
            "derivacion_procesada": derivacion_objetivo,
            "fs_nueva": fs_nueva,
            "senal_continua_procesada": senal_normalizada,
            "lista_segmentos": segmentos_finales,
            "cantidad_segmentos": len(segmentos_finales)
        }
        
        return resultados_preprocesamiento, "Pipeline completado con éxito."
    except Exception as e:
        return None, f"Fallo en la matriz de procesamiento: {str(e)}"



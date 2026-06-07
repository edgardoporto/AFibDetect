import numpy as np

def ejecutar_inferencia_segmentos(lista_segmentos, etiqueta_referencia_global):
    """
    Simula el comportamiento de una red neuronal profunda con capa Softmax.
    Procesa cada tensor de 10 segundos (2,500 muestras) y calcula probabilidades.
    """
    resultados_inferencia = []
    clases = ["NSR", "AF", "Other", "Noise"]
    
    for idx, segmento in enumerate(lista_segmentos):
        # 1. Creamos una simulación inteligente basada en la etiqueta real del .hea
        # Si el registro global es AF, le damos mayor probabilidad a la clase AF en los segmentos
        valores_crudos = np.random.rand(4)
        
        if "AF" in etiqueta_referencia_global:
            valores_crudos[1] += 2.0  # Sesgamos positivamente hacia Atrial Fibrillation
        elif "NSR" in comentario or "Normal" in etiqueta_referencia_global:
            valores_crudos[0] += 2.0  # Sesgamos hacia Normal Sinus Rhythm
        elif "Other" in etiqueta_referencia_global:
            valores_crudos[2] += 2.0  # Sesgamos hacia Otras Arritmias
            
        # 2. Aplicamos Softmax matemática para que las probabilidades sumen exactamente 1.0
        probabilidades = np.exp(valores_crudos) / np.sum(np.exp(valores_crudos))
        
        # 3. Identificamos el índice de la clase ganadora (Argmax)
        idx_ganador = np.argmax(probabilidades)
        clase_predicha = clases[idx_ganador]
        
        # Guardamos el reporte detallado por segmento
        resultados_inferencia.append({
            "num_segmento": idx + 1,
            "diagnostico_ganador": clase_predicha,
            "probabilidades": {
                "NSR": float(probabilidades[0]),
                "AF": float(probabilidades[1]),
                "Other": float(probabilidades[2]),
                "Noise": float(probabilidades[3])
            }
        })
        
    return resultados_inferencia

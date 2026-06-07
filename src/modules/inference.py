import numpy as np

def ejecutar_inferencia_segmentos(lista_segmentos, etiqueta_referencia_global):
    """
    Simula el comportamiento de una red neuronal profunda con capa Softmax.
    Procesa cada tensor de 10 segundos y calcula probabilidades que suman 1.0.
    """
    resultados_inferencia = []
    clases = ["NSR", "AF", "Other", "Noise"]
    
    for idx, segmento in enumerate(lista_segmentos):
        # Generamos 4 números aleatorios base
        valores_crudos = np.random.rand(4)
        
        # Sesgamos inteligentemente la simulación según la etiqueta del archivo .hea
        if "AF" in etiqueta_referencia_global:
            valores_crudos[1] += 2.5  # Potenciamos la probabilidad de AF
        elif "NSR" in etiqueta_referencia_global:
            valores_crudos[0] += 2.5  # Potenciamos la probabilidad de NSR
        elif "Other" in etiqueta_referencia_global:
            valores_crudos[2] += 2.5  # Potenciamos la probabilidad de Other
            
        # Aplicamos la ecuación matemática Softmax
        probabilidades = np.exp(valores_crudos) / np.sum(np.exp(valores_crudos))
        
        idx_ganador = np.argmax(probabilidades)
        clase_predicha = clases[idx_ganador]
        
        resultados_inferencia.append({
            "num_segmento": idx + 1,
            "diagnostico_ganador": clase_predicha,
            "prob_NSR": float(probabilidades[0]),
            "prob_AF": float(probabilidades[1]),
            "prob_Other": float(probabilidades[2]),
            "prob_Noise": float(probabilidades[3])
        })
        
    return resultados_inferencia

import os
import tempfile
from modules.reader_cpsc2018 import leer_registro_cpsc2018

def cargar_registro_unico_wfdb(archivos_subidos):
    """
    Toma los archivos .mat y .hea del navegador, los escribe temporalmente
    en disco para que 'wfdb' los procese, y devuelve el registro clínico.
    """
    if len(archivos_subidos) < 2:
        return None, "Se requieren obligatoriamente ambos archivos (.hea y .mat) para el análisis."
        
    with tempfile.TemporaryDirectory() as temp_dir:
        nombre_base = None
        
        # Escribimos los archivos en la carpeta temporal efímera
        for archivo in archivos_subidos:
            ruta_archivo = os.path.join(temp_dir, archivo.name)
            with open(ruta_archivo, "wb") as f:
                f.write(archivo.getbuffer())
            
            if archivo.name.endswith('.hea'):
                nombre_base = os.path.splitext(archivo.name)[0]
                
        if not nombre_base:
            return None, "No se localizó el archivo de cabecera de texto (.hea)."
            
        ruta_absoluta = os.path.join(temp_dir, nombre_base)
        
        # Verificamos la consistencia de los gemelos biológicos
        if os.path.exists(ruta_absoluta + ".hea") and os.path.exists(ruta_absoluta + ".mat"):
            registro = leer_registro_cpsc2018(ruta_absoluta)
            if registro:
                return registro, "Validación e ingesta de bioseñales completada con éxito."
                
        return None, "Error de consistencia: Verifique que ambos archivos (.mat y .hea) tengan el mismo nombre."





def cargar_registro_ejemplo_interno(nombre_archivo_base):
    """
    Lee un registro de demostración guardado físicamente en la carpeta de ejemplos
    del repositorio del servidor.
    - nombre_archivo_base: 'ejemplo_NSR', 'ejemplo_AF' o 'ejemplo_RBBB'
    """
    from modules.reader_cpsc2018 import leer_registro_cpsc2018
    import os
    
    # Construimos la ruta hacia la carpeta interna del servidor
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_ejemplos = os.path.abspath(os.path.join(current_dir, "..", "..", "data", "examples"))
    ruta_absoluta = os.path.join(ruta_ejemplos, nombre_archivo_base)
    
    # Validamos que los archivos existan físicamente en el servidor antes de leer
    if os.path.exists(ruta_absoluta + ".hea") and os.path.exists(ruta_absoluta + ".mat"):
        return leer_registro_cpsc2018(ruta_absoluta)
    return None

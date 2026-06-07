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

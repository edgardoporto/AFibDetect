"""
Configuración Global del Sistema AFibDetect.
Centraliza los códigos diagnósticos SNOMED-CT oficiales de CPSC-2018.
"""

# Mapeo oficial de códigos SNOMED-CT proporcionados para CPSC-2018
SNOMED_MAP = {
    "164889003": "AF",
    "426783006": "NSR",
    "59118001": "RBBB",
    "429622005": "STD",
    "270492004": "I-AVB",
    "16484008": "PVC",  # Nota: El estándar oficial suele omitir el '4' inicial o corregirlo según PhysioNet
    "164884008": "PVC", # Variante común en registros
    "284470004": "PAC",
    "164909002": "LBBB",
    "164931005": "STE"
}



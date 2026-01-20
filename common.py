"""
Módulo común con utilidades compartidas para Iyari-ear.

Este módulo centraliza constantes, validaciones y funciones auxiliares
que son reutilizadas por múltiples módulos del proyecto, eliminando
la duplicación de código y facilitando el mantenimiento.

Módulos que usan este módulo:
- image_tool.py: CLI para manipulación de imágenes
- webui.py: Interfaz web Gradio para manipulación de imágenes

Contenido:
- Constantes: MAX_DIMENSION, MAX_PIXELS, PRESETS
- Validaciones: validate_dimensions(), validate_aspect_ratio()
- Utilidades: list_presets()
"""
from typing import Dict, Tuple, Union, List

# ==============================================================================
# Constantes globales para procesamiento de imágenes
# ==============================================================================

# Límite máximo de dimensiones para evitar consumo excesivo de memoria
MAX_DIMENSION = 20000
MAX_PIXELS = 100_000_000  # 100 megapíxeles

# ==============================================================================
# Presets de tamaños para redes sociales y otros usos
# ==============================================================================

PRESETS: Dict[str, Dict[str, Union[Tuple[int, int], List[int], int]]] = {
    "spotify_avatar":   {"size": (750, 750)},
    "spotify_header":   {"size": (2660, 1140)},
    "facebook_post":    {"size": (1080, 1080)},
    "instagram_square": {"size": (1080, 1080)},
    "instagram_story":  {"size": (1080, 1920)},
    "fiverr_gig":       {"size": (1280, 769)},
    "square_3000":      {"size": (3000, 3000)},
    "panoramic_2x1":    {"aspect_ratio": (2, 1), "width": 2000},
    "panoramic_3x1":    {"aspect_ratio": (3, 1), "width": 3000},
    "story_9x16":       {"size": (1080, 1920)},  # Alias for instagram_story
}


# ==============================================================================
# Funciones de validación
# ==============================================================================

def validate_dimensions(width: int, height: int) -> Tuple[bool, str]:
    """
    Valida que las dimensiones estén dentro de límites seguros.
    
    Args:
        width: Ancho en píxeles
        height: Alto en píxeles
    
    Returns:
        Tuple[bool, str]: (es_válido, mensaje_error)
    """
    if width <= 0 or height <= 0:
        return False, f"Las dimensiones deben ser mayores a 0 (recibido: {width}x{height})."
    
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        return False, f"Las dimensiones exceden el límite máximo de {MAX_DIMENSION}px."
    
    if width * height > MAX_PIXELS:
        return False, f"El total de píxeles ({width * height:,}) excede el límite de {MAX_PIXELS:,}."
    
    return True, ""


def validate_aspect_ratio(ratio_w: int, ratio_h: int) -> Tuple[bool, str]:
    """
    Valida que los valores de proporción sean válidos.
    
    Args:
        ratio_w: Ancho de la proporción
        ratio_h: Alto de la proporción
    
    Returns:
        Tuple[bool, str]: (es_válido, mensaje_error)
    """
    if ratio_w <= 0 or ratio_h <= 0:
        return False, "Los valores de proporción deben ser mayores a 0."
    
    return True, ""


def list_presets() -> str:
    """
    Retorna una cadena formateada con los presets disponibles.
    
    Returns:
        str: Lista formateada de presets
    """
    available_presets = "\n".join([f"  - {name}" for name in PRESETS.keys()])
    return f"Presets disponibles:\n{available_presets}"

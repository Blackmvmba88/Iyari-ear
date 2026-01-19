import gradio as gr  # type: ignore
from PIL import Image, ImageOps
from typing import Dict, Tuple, Union, List, Optional, cast

# Importar constantes y utilidades desde el módulo común
from common import PRESETS, MAX_DIMENSION, MAX_PIXELS

# ---- Tipos ----
PresetDict = Dict[str, Dict[str, Union[Tuple[int, int], List[int], int]]]


def validate_dimensions(width: int, height: int) -> None:
    """Valida que las dimensiones estén dentro de límites seguros."""
    if width <= 0 or height <= 0:
        raise gr.Error(f"Las dimensiones deben ser mayores a 0 (recibido: {width}x{height}).")
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise gr.Error(f"Las dimensiones exceden el límite máximo de {MAX_DIMENSION}px.")
    if width * height > MAX_PIXELS:
        raise gr.Error(f"El total de píxeles ({width * height:,}) excede el límite de {MAX_PIXELS:,}.")


# ---- Helpers de tamaño/ratio ----
def resize_with_preset(image: Optional[Image.Image], preset: str) -> Image.Image:
    if image is None:
        raise gr.Error("Sube una imagen primero.")
    if not preset:
        raise gr.Error("Selecciona un preset.")
    if preset not in PRESETS:
        raise gr.Error(f"Preset inválido: {preset}")

    data = PRESETS[preset]
    if not isinstance(data, dict):
        raise gr.Error("Configuración de preset inválida.")
    
    # 1) Caso A: 'size' directa (w, h)
    target_size = data.get("size", (0, 0))
    if not isinstance(target_size, tuple):
        raise gr.Error("Formato de tamaño inválido en preset.")
    if target_size != (0, 0):
        pass
    else:
        # 2) Caso B: construir desde 'width' + 'aspect_ratio'=[rw, rh]
        rw, rh = (1, 1)
        if "aspect_ratio" in data:
            ratio_data = data["aspect_ratio"]
            if not isinstance(ratio_data, (list, tuple)):
                raise gr.Error("Formato de ratio inválido en preset.")
            if len(ratio_data) == 2:
                rw, rh = int(ratio_data[0]), int(ratio_data[1])

        width_val = data.get("width")
        w = int(width_val) if isinstance(width_val, int) else 0
        height_val = data.get("height")
        h = int(height_val) if isinstance(height_val, int) else 0  # opcional por si el preset lo trae

        if w and rw and rh and not h:
            h = int(round(w * rh / rw))
        if h and rw and rh and not w:
            w = int(round(h * rw / rh))

        if not (w and h):
            raise gr.Error("Preset incompleto: define 'size' o ('width' y 'aspect_ratio').")

        target_size = (w, h)

    validate_dimensions(target_size[0], target_size[1])
    return ImageOps.fit(image, target_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def resize_to_size(image: Optional[Image.Image], width: int, height: int) -> Image.Image:
    if image is None:
        raise gr.Error("Sube una imagen primero.")
    w, h = int(width), int(height)
    validate_dimensions(w, h)
    return image.resize((w, h), Image.Resampling.LANCZOS)


def resize_to_aspect_ratio(image: Optional[Image.Image], rw: int, rh: int) -> Image.Image:
    if image is None:
        raise gr.Error("Sube una imagen primero.")
    if rw <= 0 or rh <= 0:
        raise gr.Error("El ratio debe ser positivo.")

    w, h = image.size
    img_ratio = w / h
    target_ratio = rw / rh

    if target_ratio > img_ratio:
        # recortamos altura
        h2 = int(round(w / target_ratio))
        w2 = w
    else:
        # recortamos ancho
        w2 = int(round(h * target_ratio))
        h2 = h

    target_size = (w2, h2)
    return ImageOps.fit(image, target_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def crop_box(image: Optional[Image.Image], x: int, y: int, width: int, height: int) -> Image.Image:
    if image is None:
        raise gr.Error("Sube una imagen primero.")
    x, y, width, height = int(x), int(y), int(width), int(height)

    # Validar valores de entrada
    if width <= 0 or height <= 0:
        raise gr.Error("El ancho y alto del recorte deben ser mayores a 0.")
    if x < 0 or y < 0:
        raise gr.Error("Las coordenadas X e Y deben ser >= 0.")

    box = (x, y, x + width, y + height)

    # Clamp dentro de la imagen
    left   = max(0, box[0])
    top    = max(0, box[1])
    right  = min(image.width, box[2])
    bottom = min(image.height, box[3])

    if right <= left or bottom <= top:
        raise gr.Error("La caja de recorte es inválida o está fuera de la imagen.")
    return image.crop((left, top, right, bottom))


def tile_mosaic(tile_img: Optional[Image.Image], final_width: int, final_height: int) -> Image.Image:
    """
    Crea un mosaico llenando (final_width x final_height) repitiendo la 'tile'.
    Maneja bordes que no son múltiplos exactos del tamaño del azulejo.
    """
    if tile_img is None:
        raise gr.Error("Sube un azulejo (tile) primero.")
    final_width, final_height = int(final_width), int(final_height)

    # Validar dimensiones
    validate_dimensions(final_width, final_height)

    base_mode = "RGBA" if tile_img and tile_img.mode == "RGBA" else "RGB"
    out = Image.new(base_mode, (final_width, final_height))
    tile = tile_img.convert(base_mode)
    tw, th = tile.size

    if tw <= 0 or th <= 0:
        raise gr.Error("El azulejo tiene tamaño inválido.")

    for y in range(0, final_height, th):
        for x in range(0, final_width, tw):
            # recortar si nos pasamos del borde
            crop_w = min(tw, final_width - x)
            crop_h = min(th, final_height - y)
            if crop_w < tw or crop_h < th:
                out.paste(tile.crop((0, 0, crop_w, crop_h)), (x, y))
            else:
                out.paste(tile, (x, y))

    return out


def mirror_img(image: Optional[Image.Image]) -> Image.Image:
    if image is None:
        raise gr.Error("Sube una imagen primero.")
    return ImageOps.mirror(image)


def ocr_img(image: Optional[Image.Image]) -> str:
    if image is None:
        return ""
    try:
        import pytesseract  # type: ignore
        text = cast(str, pytesseract.image_to_string(image))  # type: ignore
        text = text.strip()
        return text if text else "Sin texto detectado."
    except ImportError:
        return "Instala pytesseract: pip install pytesseract. En macOS: brew install tesseract"
    except Exception as e:
        return f"Error OCR: {e}"


# ---- UI ----
with gr.Blocks(title="Iyari-ear Image Tool - WebUI") as demo:
    gr.Markdown("## Iyari-ear Image Tool - WebUI")

    with gr.Tab("Resize (Preset)"):
        inp = gr.Image(type="pil", label="Imagen")
        preset = gr.Dropdown(choices=list(PRESETS.keys()), label="Preset")  # type: ignore
        out = gr.Image(type="pil", label="Salida")
        gr.Button("Aplicar").click(resize_with_preset, inputs=[inp, preset], outputs=out)

    with gr.Tab("Resize (Tamaño fijo)"):
        inp2 = gr.Image(type="pil", label="Imagen")
        w = gr.Number(value=1080, label="Ancho")
        h = gr.Number(value=1080, label="Alto")
        out2 = gr.Image(type="pil", label="Salida")
        gr.Button("Aplicar").click(resize_to_size, inputs=[inp2, w, h], outputs=out2)

    with gr.Tab("Resize (Proporción)"):
        inp3 = gr.Image(type="pil", label="Imagen")
        rw = gr.Number(value=16, label="Ratio W")
        rh = gr.Number(value=9, label="Ratio H")
        out3 = gr.Image(type="pil", label="Salida")
        gr.Button("Aplicar").click(resize_to_aspect_ratio, inputs=[inp3, rw, rh], outputs=out3)

    with gr.Tab("Crop"):
        inp4 = gr.Image(type="pil", label="Imagen")
        cx = gr.Number(value=0, label="X")
        cy = gr.Number(value=0, label="Y")
        cw = gr.Number(value=200, label="Ancho")
        ch = gr.Number(value=200, label="Alto")
        out4 = gr.Image(type="pil", label="Salida")
        gr.Button("Recortar").click(crop_box, inputs=[inp4, cx, cy, cw, ch], outputs=out4)

    with gr.Tab("Tile"):
        tile_in = gr.Image(type="pil", label="Azulejo")
        fw = gr.Number(value=1080, label="Ancho final")
        fh = gr.Number(value=1080, label="Alto final")
        tile_out = gr.Image(type="pil", label="Salida")
        gr.Button("Crear mosaico").click(tile_mosaic, inputs=[tile_in, fw, fh], outputs=tile_out)

    with gr.Tab("Mirror"):
        inp5 = gr.Image(type="pil", label="Imagen")
        out5 = gr.Image(type="pil", label="Salida")
        gr.Button("Espejo").click(mirror_img, inputs=inp5, outputs=out5)

    with gr.Tab("OCR"):
        ocr_in = gr.Image(type="pil", label="Imagen")
        ocr_out = gr.Textbox(lines=8, label="Texto")
        gr.Button("Extraer texto").click(ocr_img, inputs=ocr_in, outputs=ocr_out)

if __name__ == "__main__":
    demo.launch()

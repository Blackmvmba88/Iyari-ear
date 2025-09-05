import gradio as gr  # type: ignore
from PIL import Image, ImageOps
from typing import Dict, Any, Tuple, Union, List
from image_tool import PRESETS  # type: ignore

# Define PRESETS type
PresetDict = Dict[str, Dict[str, Union[Tuple[int, int], List[int], int]]]

def resize_with_preset(image: Image.Image, preset: str) -> Image.Image:
    data: Dict[str, Any] = PRESETS[preset]
    target_size: Tuple[int, int] = data.get("size", (0, 0))  # type: ignore
    if not target_size and "aspect_ratio" in data:
        ratio_data = data["aspect_ratio"]
        rw, rh = ratio_data if isinstance(ratio_data, list) else (1, 1)  # type: ignore
        w = int(data.get("width", 0))
        h = int(w * rh / rw)
        target_size = (w, h)
        rw, rh = data["aspect_ratio"]  # type: ignore
        w = int(data.get("width", 0))
        h = int(w * rh / rw)
        target_size = (w, h)
    return ImageOps.fit(image, target_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))

def resize_to_size(image: Image.Image, width: int, height: int) -> Image.Image:
    if not image:
        return image
    return image.resize((int(width), int(height)), Image.Resampling.LANCZOS)

def resize_to_aspect_ratio(image: Image.Image, rw: int, rh: int) -> Image.Image:
    if not image:
        return image
    w, h = image.size
    img_ratio = w / h
    target_ratio = rw / rh
    if target_ratio > img_ratio:
        h2 = int(w / target_ratio)
        w2 = w
    else:
        w2 = int(h * target_ratio)
        h2 = h
    target_size = (w2, h2)
    return ImageOps.fit(image, target_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))

def crop_box(image: Image.Image, x: int, y: int, width: int, height: int) -> Image.Image:
    if not image:
        return image
    x, y, width, height = int(x), int(y), int(width), int(height)
    box = (x, y, x + width, y + height)
    # Clamp dentro de la imagen
    left   = max(0, box[0])
    top    = max(0, box[1])
    right  = min(image.width, box[2])
    bottom = min(image.height, box[3])
    if right <= left or bottom <= top:
        raise gr.Error("La caja de recorte es inválida.")
    return image.crop((left, top, right, bottom))

def tile_mosaic(tile_img: Image.Image, final_width: int, final_height: int) -> Image.Image:
    if not tile_img:
        return tile_img
    final_width, final_height = int(final_width), int(final_height)
    out = Image.new(tile_img.mode, (final_width, final_height))
    tw, th = tile_img.size
def mirror_img(image: Image.Image) -> Image.Image:
    if not image:
        return image
    return ImageOps.mirror(image)

def ocr_img(image: Image.Image) -> str:
    if not image:
        return ""
    try:
        import pytesseract  # type: ignore
    except ImportError:
        return "Instala pytesseract: pip install pytesseract. En macOS: brew install tesseract"
    try:
        result = pytesseract.image_to_string(image)
        return result if result else "Sin texto detectado."
    except Exception as e:
        return f"Error OCR: {e}"
        return "Instala pytesseract: pip install pytesseract. En macOS: brew install tesseract"
    try:
        return pytesseract.image_to_string(image) or "Sin texto detectado."
    except Exception as e:
        return f"Error OCR: {e}"
        preset = gr.Dropdown(choices=list(PRESETS.keys()), label="Preset")  # type: ignore
with gr.Blocks(title="Iyari-ear Image Tool - WebUI") as demo:
    gr.Markdown("## Iyari-ear Image Tool - WebUI")

    with gr.Tab("Resize (Preset)"):
        inp = gr.Image(type="pil", label="Imagen")
        preset = gr.Dropdown(choices=list(PRESETS.keys()), label="Preset")
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
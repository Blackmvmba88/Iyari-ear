import argparse
import os
import sys
from PIL import Image, ImageOps

# ==============================================================================
# Constants
# ==============================================================================

# Límite máximo de dimensiones para evitar consumo excesivo de memoria
MAX_DIMENSION = 20000
MAX_PIXELS = 100_000_000  # 100 megapíxeles

# ==============================================================================
# Logic Functions
# ==============================================================================

PRESETS = {
    "spotify_avatar":   {"size": (750, 750)},
    "spotify_header":   {"size": (2660, 1140)},
    "facebook_post":    {"size": (1080, 1080)},
    "instagram_square": {"size": (1080, 1080)},
    "instagram_story":  {"size": (1080, 1920)},
    "fiverr_gig":       {"size": (1280, 769)},
    "square_3000":      {"size": (3000, 3000)},
    "panoramic_2x1":    {"aspect_ratio": (2, 1), "width": 2000},
    "panoramic_3x1":    {"aspect_ratio": (3, 1), "width": 3000},
    "story_9x16":       {"size": (1080, 1920)}, # Alias for instagram_story
}

def list_presets():
    """Returns a formatted string with available presets."""
    available_presets = "\n".join([f"  - {name}" for name in PRESETS.keys()])
    return f"Presets disponibles:\n{available_presets}"


def validate_dimensions(width: int, height: int) -> bool:
    """Valida que las dimensiones estén dentro de límites seguros."""
    if width <= 0 or height <= 0:
        print(f"Error: Las dimensiones deben ser mayores a 0 (recibido: {width}x{height}).")
        return False
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        print(f"Error: Las dimensiones exceden el límite máximo de {MAX_DIMENSION}px.")
        return False
    if width * height > MAX_PIXELS:
        print(f"Error: El total de píxeles ({width * height:,}) excede el límite de {MAX_PIXELS:,}.")
        return False
    return True


def validate_input_file(path: str) -> bool:
    """Valida que el archivo de entrada exista y sea legible."""
    if not os.path.exists(path):
        print(f"Error: No se encontró el archivo '{path}'.")
        return False
    if not os.path.isfile(path):
        print(f"Error: '{path}' no es un archivo válido.")
        return False
    if not os.access(path, os.R_OK):
        print(f"Error: No se tiene permiso de lectura para '{path}'.")
        return False
    return True


def validate_output_path(path: str) -> bool:
    """Valida que se pueda escribir en la ruta de salida."""
    output_dir = os.path.dirname(path) or '.'
    if not os.path.exists(output_dir):
        print(f"Error: El directorio de salida '{output_dir}' no existe.")
        return False
    if not os.access(output_dir, os.W_OK):
        print(f"Error: No se tiene permiso de escritura en '{output_dir}'.")
        return False
    return True

def resize_image(args):
    """Logic for the resize command."""
    # Validar archivos de entrada y salida
    if not validate_input_file(args.input_path):
        return
    if not validate_output_path(args.output_path):
        return

    try:
        with Image.open(args.input_path) as img:
            output_img = None

            if args.preset:
                if args.preset not in PRESETS:
                    print(f"Error: Preset '{args.preset}' no válido.\n{list_presets()}")
                    return

                preset = PRESETS[args.preset]
                target_size = preset.get("size")

                if not target_size and "aspect_ratio" in preset:
                    ratio_w, ratio_h = preset["aspect_ratio"]
                    target_width = preset["width"]
                    target_height = int(target_width * ratio_h / ratio_w)
                    target_size = (target_width, target_height)

                if not validate_dimensions(target_size[0], target_size[1]):
                    return

                print(f"Aplicando preset '{args.preset}' con tamaño final {target_size}...")
                output_img = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))

            elif args.size:
                target_size = tuple(args.size)
                if not validate_dimensions(target_size[0], target_size[1]):
                    return
                print(f"Redimensionando a tamaño fijo {target_size} (puede distorsionar)...")
                output_img = img.resize(target_size, Image.Resampling.LANCZOS)

            elif args.aspect_ratio:
                target_w_ratio, target_h_ratio = args.aspect_ratio
                if target_w_ratio <= 0 or target_h_ratio <= 0:
                    print("Error: Los valores de proporción deben ser mayores a 0.")
                    return

                print(f"Ajustando a proporción {target_w_ratio}:{target_h_ratio}...")

                final_w, final_h = img.size
                img_ratio = final_w / final_h
                target_ratio = target_w_ratio / target_h_ratio

                if target_ratio > img_ratio:
                    final_h = int(final_w / target_ratio)
                else:
                    final_w = int(final_h * target_ratio)

                target_size = (final_w, final_h)
                if not validate_dimensions(target_size[0], target_size[1]):
                    return
                output_img = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))

            if output_img:
                output_img.save(args.output_path)
                print(f"¡Éxito! Imagen guardada en '{args.output_path}' con tamaño {output_img.size}.")
            else:
                print("Error: No se pudo procesar la imagen. Revisa los argumentos.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.input_path}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def crop_image(args):
    """Lógica para el comando crop."""
    # Validar archivos de entrada y salida
    if not validate_input_file(args.input_path):
        return
    if not validate_output_path(args.output_path):
        return

    # Validar dimensiones de recorte
    if args.width <= 0 or args.height <= 0:
        print("Error: El ancho y alto del recorte deben ser mayores a 0.")
        return
    if args.x < 0 or args.y < 0:
        print("Error: Las coordenadas X e Y deben ser >= 0.")
        return

    try:
        with Image.open(args.input_path) as img:
            # Las coordenadas para crop son (left, upper, right, lower)
            box = (args.x, args.y, args.x + args.width, args.y + args.height)

            # Validar que la caja de recorte esté dentro de los límites de la imagen
            if box[0] < 0 or box[1] < 0 or box[2] > img.width or box[3] > img.height:
                print(f"Error: La caja de recorte ({box}) está fuera de los límites de la imagen (ancho: {img.width}, alto: {img.height}).")
                return

            print(f"Recortando la imagen a la caja: {box}...")
            cropped_img = img.crop(box)
            cropped_img.save(args.output_path)
            print(f"¡Éxito! Imagen recortada guardada en '{args.output_path}'.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.input_path}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def tile_image(args):
    """Lógica para el comando tile."""
    # Validar archivos de entrada y salida
    if not validate_input_file(args.input_path):
        return
    if not validate_output_path(args.output_path):
        return

    # Validar dimensiones del mosaico final
    if not validate_dimensions(args.final_width, args.final_height):
        return

    try:
        with Image.open(args.input_path) as tile_img:
            target_w, target_h = args.final_width, args.final_height
            tile_w, tile_h = tile_img.size

            if tile_w <= 0 or tile_h <= 0:
                print("Error: La imagen del azulejo tiene dimensiones inválidas.")
                return

            print(f"Creando un mosaico de {target_w}x{target_h} usando un 'azulejo' de {tile_w}x{tile_h}...")

            # Crear la nueva imagen en blanco
            output_img = Image.new(tile_img.mode, (target_w, target_h))

            # Pegar el azulejo en un patrón de mosaico
            for x in range(0, target_w, tile_w):
                for y in range(0, target_h, tile_h):
                    # Calculate the region to fill
                    paste_w = min(tile_w, target_w - x)
                    paste_h = min(tile_h, target_h - y)
                    if paste_w < tile_w or paste_h < tile_h:
                        # Crop the tile to fit the remaining space
                        cropped_tile = tile_img.crop((0, 0, paste_w, paste_h))
                        output_img.paste(cropped_tile, (x, y))
                    else:
                        output_img.paste(tile_img, (x, y))

            output_img.save(args.output_path)
            print(f"¡Éxito! Imagen de mosaico guardada en '{args.output_path}'.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.input_path}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def mirror_image(args):
    """Lógica para el comando mirror."""
    # Validar archivos de entrada y salida
    if not validate_input_file(args.input_path):
        return
    if not validate_output_path(args.output_path):
        return

    try:
        with Image.open(args.input_path) as img:
            print(f"Creando efecto espejo (volteo horizontal) de '{args.input_path}'...")
            # Usamos FLIP_LEFT_RIGHT para el efecto espejo
            mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            mirrored_img.save(args.output_path)
            print(f"¡Éxito! Imagen reflejada guardada en '{args.output_path}'.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.input_path}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def ocr_image(args):
    """Lógica para el comando ocr."""
    # Validar archivo de entrada
    if not validate_input_file(args.input_path):
        return

    try:
        # Pytesseract es una dependencia opcional, la importamos aquí.
        import pytesseract

        print(f"Extrayendo texto de '{args.input_path}'...")
        # Abrimos la imagen aquí para pasar el objeto a pytesseract
        with Image.open(args.input_path) as img:
            text = pytesseract.image_to_string(img)

        if text.strip():
            print("\n--- Texto extraído ---")
            print(text)
            print("--------------------")
        else:
            print("No se encontró texto en la imagen.")

    except ImportError:
        print("Error: La librería 'pytesseract' no está instalada.")
        print("Por favor, instálala con: pip install pytesseract")
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract no está instalado o no se encuentra en el PATH del sistema.")
        print("Por favor, visita el sitio oficial de Tesseract para ver las instrucciones de instalación.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{args.input_path}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


# ==============================================================================
# Argument Configuration and Main Script
# ==============================================================================

def main():
    """Función principal que configura y ejecuta el parser de argumentos."""
    parser = argparse.ArgumentParser(
        description="A command-line tool for image manipulation.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos disponibles")

    # --- Comando Resize ---
    parser_resize = subparsers.add_parser("resize", help="Redimensionar una imagen a un tamaño o proporción.")
    parser_resize.add_argument("input_path", help="Ruta de la imagen de entrada.")
    parser_resize.add_argument("output_path", help="Ruta para guardar la imagen de salida.")
    group = parser_resize.add_mutually_exclusive_group(required=True)
    group.add_argument("--preset", help="Usa un preset de tamaño (ej: spotify_avatar, instagram_square).")
    group.add_argument("--size", nargs=2, type=int, metavar=("ANCHO", "ALTO"), help="Define un tamaño específico.")
    group.add_argument("--aspect-ratio", nargs=2, type=int, metavar=("RATIO_W", "RATIO_H"), help="Define una proporción (ej: 16 9).")
    parser_resize.set_defaults(func=resize_image)

    # --- Comando Crop ---
    parser_crop = subparsers.add_parser("crop", help="Recortar una sección de una imagen.")
    parser_crop.add_argument("input_path", help="Ruta de la imagen de entrada.")
    parser_crop.add_argument("output_path", help="Ruta para guardar la imagen de salida.")
    parser_crop.add_argument("x", type=int, help="Coordenada X de la esquina superior izquierda.")
    parser_crop.add_argument("y", type=int, help="Coordenada Y de la esquina superior izquierda.")
    parser_crop.add_argument("width", type=int, help="Ancho del recorte.")
    parser_crop.add_argument("height", type=int, help="Alto del recorte.")
    parser_crop.set_defaults(func=crop_image)

    # --- Comando Tile ---
    parser_tile = subparsers.add_parser("tile", help="Crear un mosaico repitiendo una imagen.")
    parser_tile.add_argument("input_path", help="Ruta de la imagen de entrada (el 'azulejo').")
    parser_tile.add_argument("output_path", help="Ruta para guardar la imagen de salida.")
    parser_tile.add_argument("final_width", type=int, help="Ancho final de la imagen de mosaico.")
    parser_tile.add_argument("final_height", type=int, help="Alto final de la imagen de mosaico.")
    parser_tile.set_defaults(func=tile_image)

    # --- Comando Mirror ---
    parser_mirror = subparsers.add_parser("mirror", help="Crear un efecto espejo (volteo horizontal).")
    parser_mirror.add_argument("input_path", help="Ruta de la imagen de entrada.")
    parser_mirror.add_argument("output_path", help="Ruta para guardar la imagen de salida.")
    parser_mirror.set_defaults(func=mirror_image)

    # --- Comando OCR ---
    parser_ocr = subparsers.add_parser("ocr", help="Extraer texto de una imagen (requiere Tesseract).")
    parser_ocr.add_argument("input_path", help="Ruta de la imagen de entrada.")
    parser_ocr.set_defaults(func=ocr_image)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

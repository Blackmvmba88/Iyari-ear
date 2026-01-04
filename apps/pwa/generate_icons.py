#!/usr/bin/env python3
"""
Script para generar iconos de PWA para Iyari-ear
Genera iconos en múltiples tamaños con el emoji 🎤
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_pwa_icons():
    """Genera iconos PWA en diferentes tamaños"""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    output_dir = "apps/pwa/icons"
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    for size in sizes:
        # Crear imagen con fondo
        img = Image.new('RGBA', (size, size), (26, 26, 26, 255))  # Fondo oscuro
        draw = ImageDraw.Draw(img)
        
        # Dibujar círculo de fondo con color acento
        margin = size // 8
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=(0, 255, 159, 255)  # Verde acento #00ff9f
        )
        
        # Añadir texto del emoji (🎤)
        # Nota: esto funciona mejor con fuentes del sistema que soporten emojis
        try:
            # Intentar usar una fuente de emoji del sistema
            font_size = int(size * 0.5)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            # Fallback a fuente por defecto
            font = ImageFont.load_default()
        
        # Dibujar el símbolo de micrófono
        text = "🎤"
        # Calcular posición centrada
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((size - text_width) // 2, (size - text_height) // 2 - size // 10)
        
        try:
            draw.text(position, text, font=font, fill=(255, 255, 255, 255))
        except:
            # Si falla el emoji, dibujar un micrófono simple
            # Dibujar cuerpo del micrófono
            mic_width = size // 6
            mic_height = size // 3
            mic_x = (size - mic_width) // 2
            mic_y = size // 3
            draw.rounded_rectangle(
                [mic_x, mic_y, mic_x + mic_width, mic_y + mic_height],
                radius=mic_width // 2,
                fill=(255, 255, 255, 255)
            )
            # Dibujar base
            base_y = mic_y + mic_height + size // 20
            draw.line([size // 2, mic_y + mic_height, size // 2, base_y], 
                     fill=(255, 255, 255, 255), width=size // 30)
            draw.arc([mic_x, mic_y + mic_height - size // 12, 
                     mic_x + mic_width, mic_y + mic_height + size // 12],
                    0, 180, fill=(255, 255, 255, 255), width=size // 30)
        
        # Guardar icono
        output_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
        img.save(output_path, "PNG")
        print(f"✓ Generado: {output_path}")
    
    print(f"\n✅ {len(sizes)} iconos generados exitosamente en {output_dir}/")

if __name__ == "__main__":
    create_pwa_icons()

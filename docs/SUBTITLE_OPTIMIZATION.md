# Guía de Optimización y Validación de Subtítulos

## Descripción

El módulo de optimización de subtítulos de Iyari-ear procesa archivos de subtítulos para mejorar su legibilidad y compatibilidad con reproductores de video como VLC. El sistema valida y optimiza automáticamente:

- ✅ Duraciones de subtítulos (muy cortos o muy largos)
- ✅ Superposiciones entre subtítulos
- ✅ Longitud de líneas de texto
- ✅ Número de líneas por subtítulo
- ✅ Espaciado entre subtítulos

## Formatos Soportados

### Entrada
- **SRT** (SubRip Text) - `.srt`
- **VTT** (WebVTT) - `.vtt`
- **ASS/SSA** (Advanced SubStation Alpha) - `.ass`, `.ssa`

### Salida
- **SRT** (SubRip Text) - `.srt`
- **VTT** (WebVTT) - `.vtt`

## Uso

### 1. CLI (Línea de Comandos)

#### Procesar y Optimizar Subtítulos

```bash
# Procesar un archivo con optimización automática
iyari-ear process-subtitle input.srt output.srt

# Procesar sin validación
iyari-ear process-subtitle input.srt output.srt --no-validate

# Procesar sin optimización (solo validar)
iyari-ear process-subtitle input.srt output.srt --no-optimize

# Cambiar formato de salida
iyari-ear process-subtitle input.srt output.vtt --format vtt
```

#### Ejemplos Prácticos

```bash
# Optimizar subtítulos de una película
iyari-ear process-subtitle pelicula.srt pelicula.optimized.srt

# Convertir ASS a SRT optimizado
iyari-ear process-subtitle anime.ass anime.srt --format srt

# Solo validar sin guardar cambios
iyari-ear process-subtitle serie_s01e01.srt --no-optimize
```

### 2. Python API

```python
from subtitle_processor import SubtitleProcessor, process_subtitle_file

# Método 1: Función de conveniencia
success, results = process_subtitle_file(
    input_path='input.srt',
    output_path='output.srt',
    validate=True,
    optimize=True
)

print(f"Subtítulos procesados: {results['stats']['total']}")
print(f"Problemas encontrados: {len(results['validation_issues'])}")
print(f"Optimizaciones aplicadas: {results['optimization_changes']}")

# Método 2: Uso avanzado con clase
processor = SubtitleProcessor()

# Cargar archivo
processor.load_from_file('input.srt')

# Validar
issues = processor.validate()
for issue in issues:
    print(f"{issue['severity'].upper()}: {issue['message']}")

# Optimizar
changes = processor.optimize(
    fix_overlaps=True,
    fix_durations=True,
    split_long_lines=True
)

# Guardar
processor.save_to_file('output.srt', format='srt')

# Obtener estadísticas
stats = processor.get_stats()
print(f"Total: {stats['total']} subtítulos")
print(f"Duración promedio: {stats['avg_duration']:.0f}ms")
```

### 3. API REST

#### Procesar Subtítulos

```bash
# Usando curl
curl -X POST http://localhost:8000/api/subtitles/process \
  -F "file=@input.srt" \
  -F "validate=true" \
  -F "optimize=true" \
  -F "output_format=srt"
```

**Respuesta:**
```json
{
  "success": true,
  "stats": {
    "total": 150,
    "total_duration": 450.5,
    "avg_duration": 3003,
    "min_duration": 500,
    "max_duration": 7000
  },
  "validation_issues": [
    {
      "index": 42,
      "type": "duration_too_short",
      "message": "Subtítulo #42: Duración muy corta (300ms)",
      "severity": "warning"
    }
  ],
  "optimization_changes": 8,
  "download_url": "/api/subtitles/download/abc123-def456"
}
```

#### Descargar Subtítulos Procesados

```bash
curl -O http://localhost:8000/api/subtitles/download/abc123-def456
```

#### Solo Validar

```bash
curl -X GET http://localhost:8000/api/subtitles/validate \
  -F "file=@input.srt"
```

## Reglas de Optimización

### Duraciones

| Regla | Valor | Acción |
|-------|-------|--------|
| Duración mínima | 500ms | Extender subtítulo |
| Duración máxima | 7000ms | Acortar subtítulo |
| Espacio mínimo entre subtítulos | 100ms | Ajustar timing |

### Texto

| Regla | Valor | Acción |
|-------|-------|--------|
| Caracteres máximos por línea | 42 | Dividir línea |
| Líneas máximas por subtítulo | 2 | Limitar líneas |

### Validaciones

El sistema detecta y reporta:

- ❌ **Errores**: Superposiciones entre subtítulos
- ⚠️ **Advertencias**: Duraciones anormales (muy corto/largo)
- ℹ️ **Info**: Líneas largas, muchas líneas

## Ejemplos de Optimización

### Antes
```srt
1
00:00:00,000 --> 00:00:00,200
Muy corto

2
00:00:01,000 --> 00:00:15,000
Este subtítulo es extremadamente largo y permanece en pantalla demasiado tiempo lo cual hace difícil la lectura

3
00:00:14,000 --> 00:00:16,000
Se superpone con el anterior
```

### Después
```srt
1
00:00:00,000 --> 00:00:00,500
Muy corto

2
00:00:01,000 --> 00:00:08,000
Este subtítulo es extremadamente largo y
permanece en pantalla demasiado tiempo

3
00:00:08,100 --> 00:00:16,000
Se superpone con el anterior
```

## Solución de Problemas

### "Módulo de procesamiento de subtítulos no disponible"

Asegúrate de tener el archivo `subtitle_processor.py` en el directorio raíz:

```bash
cd /ruta/a/Iyari-ear
ls subtitle_processor.py
```

### "Error al cargar archivo de subtítulos"

- Verifica que el archivo existe
- Comprueba que el formato es soportado (.srt, .vtt, .ass, .ssa)
- Asegúrate de que el archivo tiene codificación UTF-8

```bash
# Convertir a UTF-8 si es necesario
iconv -f LATIN1 -t UTF-8 input.srt > input_utf8.srt
```

### "Formato no soportado"

Usa uno de los formatos soportados:

```bash
# Ver extensión del archivo
file input.sub

# Renombrar si es SRT con extensión incorrecta
mv input.sub input.srt
```

## Configuración Avanzada

### Personalizar Reglas de Optimización

```python
from subtitle_processor import SubtitleProcessor

processor = SubtitleProcessor()

# Modificar límites
processor.MIN_DURATION_MS = 700  # Default: 500
processor.MAX_DURATION_MS = 6000  # Default: 7000
processor.MAX_CHARS_PER_LINE = 50  # Default: 42
processor.MAX_LINES = 3  # Default: 2

# Procesar con configuración personalizada
processor.load_from_file('input.srt')
processor.optimize()
processor.save_to_file('output.srt')
```

### Procesamiento por Lotes

```bash
#!/bin/bash
# Procesar todos los archivos SRT en un directorio

for file in *.srt; do
    echo "Procesando: $file"
    iyari-ear process-subtitle "$file" "${file%.srt}.optimized.srt"
done
```

```python
# Python script para procesamiento masivo
import os
from subtitle_processor import process_subtitle_file

input_dir = './subtitulos'
output_dir = './subtitulos_optimizados'

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith('.srt'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        success, results = process_subtitle_file(
            input_path,
            output_path,
            validate=True,
            optimize=True
        )
        
        if success:
            print(f"✅ {filename}: {results['optimization_changes']} cambios")
        else:
            print(f"❌ {filename}: Error")
```

## Integración con Flujos de Trabajo

### FFmpeg + Iyari-ear

```bash
# Extraer subtítulos de un video
ffmpeg -i video.mkv -map 0:s:0 subtitles.srt

# Optimizar subtítulos
iyari-ear process-subtitle subtitles.srt subtitles.optimized.srt

# Incrustar subtítulos optimizados
ffmpeg -i video.mkv -i subtitles.optimized.srt -c copy -c:s mov_text output.mp4
```

### Automatización con Python

```python
import subprocess
from subtitle_processor import process_subtitle_file

def process_video_subtitles(video_path):
    """Extrae, optimiza y reintegra subtítulos de un video"""
    
    # Extraer subtítulos
    subprocess.run([
        'ffmpeg', '-i', video_path,
        '-map', '0:s:0', 'temp.srt'
    ])
    
    # Optimizar
    success, results = process_subtitle_file(
        'temp.srt',
        'temp.optimized.srt',
        validate=True,
        optimize=True
    )
    
    if success:
        print(f"Optimizaciones: {results['optimization_changes']}")
        return 'temp.optimized.srt'
    
    return None

# Uso
optimized_srt = process_video_subtitles('pelicula.mkv')
```

## Mejores Prácticas

1. **Siempre haz backup**: Guarda una copia del archivo original
2. **Valida antes de usar**: Ejecuta validación primero para ver qué cambios se harán
3. **Verifica el resultado**: Reproduce el video con los subtítulos optimizados
4. **Usa formato apropiado**: SRT para compatibilidad, VTT para web
5. **Revisa manualmente**: La optimización automática puede no ser perfecta

## Recursos Adicionales

- [Especificación SRT](https://en.wikipedia.org/wiki/SubRip)
- [Especificación WebVTT](https://www.w3.org/TR/webvtt1/)
- [Guía de subtitulado](https://www.rev.com/blog/resources/subtitling-guide)

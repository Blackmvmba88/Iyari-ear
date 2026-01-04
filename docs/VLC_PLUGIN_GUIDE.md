# Plugin de VLC para Optimización de Subtítulos

## Descripción

El plugin de Iyari-ear para VLC Media Player optimiza automáticamente los subtítulos mientras reproduces videos. Los subtítulos se pre-procesan y se almacenan en caché para mejorar la legibilidad sin interrupciones.

## Características

- ✨ **Optimización automática**: Detecta y optimiza subtítulos al cargar el video
- 💾 **Sistema de caché**: Los subtítulos procesados se guardan para usos futuros
- 🔄 **Integración transparente**: Funciona en segundo plano sin intervención
- 🎯 **Compatible con múltiples formatos**: SRT, VTT, ASS/SSA

## Requisitos

- **VLC Media Player** 3.0 o superior
- **Servidor de Iyari-ear** ejecutándose en background
- **Python 3.7+** para generar e instalar el plugin

## Instalación

### Método 1: Instalación Automática (Recomendado)

```bash
# Desde el directorio de Iyari-ear
iyari-ear install-vlc-plugin
```

El comando:
1. Genera el archivo del plugin Lua
2. Detecta la ubicación de VLC en tu sistema
3. Instala el plugin automáticamente
4. Muestra instrucciones de uso

### Método 2: Instalación Manual

#### 1. Generar el Plugin

```bash
# Generar el archivo del plugin
python vlc_plugin_generator.py --output iyari_ear_optimizer.lua

# O con configuración personalizada
python vlc_plugin_generator.py \
  --api-url http://192.168.1.100:8000 \
  --output iyari_ear_optimizer.lua
```

#### 2. Localizar Directorio de Plugins VLC

**Windows:**
```
%APPDATA%\vlc\lua\extensions\
```
Ejemplo: `C:\Users\TuUsuario\AppData\Roaming\vlc\lua\extensions\`

**macOS:**
```
~/Library/Application Support/org.videolan.vlc/lua/extensions/
```

**Linux:**
```
~/.local/share/vlc/lua/extensions/
```

#### 3. Copiar el Plugin

```bash
# Windows (PowerShell)
Copy-Item iyari_ear_optimizer.lua "$env:APPDATA\vlc\lua\extensions\"

# macOS/Linux
cp iyari_ear_optimizer.lua ~/.local/share/vlc/lua/extensions/

# Crear directorio si no existe
mkdir -p ~/.local/share/vlc/lua/extensions/
```

#### 4. Reiniciar VLC

Cierra completamente VLC y vuelve a abrirlo para cargar el plugin.

## Configuración

### Verificar Instalación

1. Abre VLC
2. Ve a `Ver` → `Extensiones y complementos` (o `Herramientas` → `Plugins y extensiones`)
3. Busca "Iyari-ear Subtitle Optimizer"

### Iniciar Servidor de Iyari-ear

El plugin requiere que el servidor esté corriendo:

```bash
# Iniciar servidor
iyari-ear start

# O manualmente
python main.py
```

El servidor debe estar accesible en `http://localhost:8000` (o la URL configurada).

### Configuración Avanzada

Edita el archivo `iyari_ear_optimizer.lua` para personalizar:

```lua
-- Configuración
local config = {
    api_url = "http://localhost:8000",  -- URL del servidor
    cache_dir = "~/.cache/iyari-ear/subtitles",  -- Directorio de caché
    auto_optimize = true,  -- Optimización automática
    max_cache_size_mb = 100  -- Tamaño máximo del caché
}
```

#### Parámetros de Configuración

| Parámetro | Descripción | Valor por Defecto |
|-----------|-------------|-------------------|
| `api_url` | URL del servidor de Iyari-ear | `http://localhost:8000` |
| `cache_dir` | Directorio para subtítulos procesados | Sistema específico |
| `auto_optimize` | Optimizar automáticamente | `true` |
| `max_cache_size_mb` | Tamaño máximo del caché en MB | `100` |

## Uso

### Uso Básico

1. **Inicia el servidor de Iyari-ear**:
   ```bash
   iyari-ear start
   ```

2. **Abre VLC y reproduce un video con subtítulos**:
   - El plugin detectará automáticamente los subtítulos
   - Si es la primera vez, los procesará y guardará en caché
   - En reproducciones futuras, usará la versión optimizada del caché

3. **Verifica los logs** (opcional):
   - Ve a `Herramientas` → `Mensajes` en VLC
   - Busca mensajes de "Iyari-ear Subtitle Optimizer"

### Flujo de Trabajo

```
┌──────────────────┐
│ Abrir video      │
│ en VLC           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Plugin detecta   │◄─── Si está en caché
│ subtítulos       │     └─► Usar versión optimizada
└────────┬─────────┘
         │ No está en caché
         ▼
┌──────────────────┐
│ Enviar a API     │
│ para procesar    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Guardar en       │
│ caché            │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Usar subtítulos  │
│ optimizados      │
└──────────────────┘
```

## Ejemplos de Uso

### Reproducir Video con Subtítulos

```bash
# 1. Inicia el servidor
iyari-ear start &

# 2. Abre VLC con un video
vlc pelicula.mkv

# Los subtítulos se optimizarán automáticamente
```

### Usar con Subtítulos Externos

```bash
# VLC con archivo de subtítulos separado
vlc pelicula.mp4 --sub-file subtitulos.srt

# El plugin optimizará subtitulos.srt
```

### Pre-procesar Subtítulos

```bash
# Procesar subtítulos antes de reproducir
iyari-ear process-subtitle subtitulos.srt subtitulos.optimized.srt

# Reproducir con subtítulos pre-optimizados
vlc pelicula.mp4 --sub-file subtitulos.optimized.srt
```

## Verificación

### Ver Mensajes del Plugin

En VLC:
1. Ve a `Herramientas` → `Mensajes` (o presiona `Ctrl+M`)
2. Establece verbosidad a "2 - Debug"
3. Busca líneas como:
   ```
   [lua] Iyari-ear Subtitle Optimizer activado
   [lua] Medio cargado: file:///path/to/video.mkv
   [lua] Pista de subtítulos detectada: Spanish
   [lua] Auto-optimización habilitada - procesando...
   ```

### Verificar Caché

```bash
# Linux/macOS
ls -lh ~/.cache/iyari-ear/subtitles/

# Windows
dir %LOCALAPPDATA%\iyari-ear\subtitle-cache\

# Ver archivos en caché
find ~/.cache/iyari-ear/subtitles/ -name "*.optimized.srt"
```

### Probar Conectividad con API

```bash
# Verificar que el servidor responde
curl http://localhost:8000/health

# Respuesta esperada:
# {"status":"ok","active_connections":0,"subtitle_support":true}
```

## Solución de Problemas

### El plugin no aparece en VLC

**Solución:**
1. Verifica que el archivo esté en el directorio correcto:
   ```bash
   # Linux
   ls ~/.local/share/vlc/lua/extensions/iyari_ear_optimizer.lua
   
   # Windows
   dir %APPDATA%\vlc\lua\extensions\iyari_ear_optimizer.lua
   ```

2. Cierra **completamente** VLC (no solo la ventana, sino el proceso)
3. Vuelve a abrir VLC

### Los subtítulos no se optimizan

**Diagnóstico:**

1. **Verificar que el servidor está corriendo:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Ver logs de VLC:**
   - `Herramientas` → `Mensajes`
   - Buscar errores relacionados con Iyari-ear

3. **Verificar URL en el plugin:**
   - Abre `iyari_ear_optimizer.lua`
   - Confirma que `api_url` es correcta

**Soluciones comunes:**

```bash
# Reiniciar el servidor
pkill -f "python main.py"
iyari-ear start

# Regenerar el plugin con URL correcta
python vlc_plugin_generator.py --api-url http://localhost:8000 --install
```

### Error "Servidor saturado"

El servidor tiene un límite de 100 conexiones simultáneas.

**Solución:**
- Cierra otras instancias de VLC
- Reinicia el servidor
- Si usas múltiples dispositivos, considera aumentar el límite en `main.py`

### Subtítulos en caché desactualizados

Para forzar re-procesamiento:

```bash
# Limpiar caché
rm -rf ~/.cache/iyari-ear/subtitles/*

# Regenerar optimizaciones
iyari-ear process-subtitle input.srt output.srt
```

### Plugin funciona pero subtítulos no mejoran

- Verifica que `auto_optimize = true` en la configuración
- Algunos subtítulos ya pueden estar bien formateados
- Revisa los logs para ver si hay errores de procesamiento

## Desinstalación

### Remover Plugin

```bash
# Linux/macOS
rm ~/.local/share/vlc/lua/extensions/iyari_ear_optimizer.lua

# Windows (PowerShell)
Remove-Item "$env:APPDATA\vlc\lua\extensions\iyari_ear_optimizer.lua"
```

### Limpiar Caché

```bash
# Linux/macOS
rm -rf ~/.cache/iyari-ear/

# Windows
rmdir /s %LOCALAPPDATA%\iyari-ear\
```

## Limitaciones Conocidas

- ⚠️ El plugin requiere que el servidor esté corriendo localmente o en red
- ⚠️ Subtítulos incrustados en el video no se procesan (solo externos)
- ⚠️ Primera reproducción puede tener pequeño retraso mientras se procesan
- ⚠️ Formatos de subtítulos propietarios no son soportados

## Seguridad y Privacidad

- 🔒 Los subtítulos se procesan localmente en tu red
- 🔒 No se envían datos a servidores externos
- 🔒 El caché es local y solo accesible por tu usuario
- 🔒 No se guardan registros de lo que reproduces

## Rendimiento

- ⚡ Subtítulos en caché se cargan instantáneamente
- ⚡ Primera optimización: ~0.5-2 segundos (dependiendo del tamaño)
- ⚡ Caché típico: 1-5 MB por archivo de subtítulos
- ⚡ Impacto en CPU: Mínimo durante reproducción

## Desarrollo

### Generar Plugin con Configuración Personalizada

```python
from vlc_plugin_generator import VLCPluginGenerator

# Crear generador
generator = VLCPluginGenerator(
    api_url='http://192.168.1.100:9000',
    cache_dir='/custom/cache/path'
)

# Generar con opciones
plugin_path = generator.generate_plugin(
    output_path='custom_plugin.lua',
    auto_optimize=True,
    max_cache_size=200  # MB
)

# Instalar
generator.install_plugin(plugin_path)

# Generar README
generator.generate_readme('CUSTOM_README.md')
```

### Estructura del Plugin Lua

El plugin implementa:
- `descriptor()`: Metadata del plugin
- `activate()`: Inicialización
- `input_changed()`: Callback cuando se carga un medio
- `deactivate()`: Limpieza al desactivar

### Extender Funcionalidad

Para añadir funciones personalizadas, edita `vlc_plugin_generator.py`:

```python
# Añadir nuevas funciones al template
VLC_PLUGIN_TEMPLATE = '''
-- Tu código Lua personalizado aquí

function custom_function()
    -- Implementación
end
'''
```

## Recursos

- [VLC Lua API](https://wiki.videolan.org/Documentation:Building_Lua_Playlist_Scripts/)
- [Documentación de Subtítulos](./SUBTITLE_OPTIMIZATION.md)
- [Repositorio de Iyari-ear](https://github.com/Blackmvmba88/Iyari-ear)

## Contribuir

¿Encontraste un bug o tienes una mejora? Abre un issue en GitHub:
https://github.com/Blackmvmba88/Iyari-ear/issues

# Apps Directory

Este directorio contiene configuraciones y recursos para empaquetar Iyari-ear como aplicación en diferentes plataformas.

## Estructura

### `/pwa` - Progressive Web App
Recursos para la PWA (Progressive Web App) instalable desde el navegador.

- `manifest.json` - Manifiesto de la aplicación PWA
- `sw.js` - Service Worker para funcionamiento offline
- `icons/` - Iconos en múltiples tamaños (72x72 a 512x512)
- `generate_icons.py` - Script para generar iconos

**Uso:**
La PWA se instala automáticamente cuando visitas la aplicación en Chrome/Edge/Safari. Busca el ícono de instalación en la barra de direcciones.

### `/desktop` (Futuro)
Configuraciones para empaquetado de aplicación de escritorio con Electron o Tauri.

## Instalación de la PWA

1. Inicia el servidor: `iyari-ear start`
2. Abre Chrome/Edge: `http://localhost:8000`
3. Click en el ícono "Instalar" (➕) en la barra de direcciones
4. ¡Listo! La app estará en tu menú de aplicaciones

## Generación de Iconos

Para regenerar los iconos de la PWA:

```bash
python apps/pwa/generate_icons.py
```

Esto creará iconos en 8 tamaños diferentes (72x72, 96x96, 128x128, 144x144, 152x152, 192x192, 384x384, 512x512).

## Service Worker

El Service Worker (`sw.js`) permite:
- ✅ Funcionamiento parcial offline
- ✅ Caché de recursos estáticos
- ✅ Instalación como aplicación
- ✅ Actualizaciones automáticas

**Nota:** El WebSocket siempre requiere conexión a internet para la transcripción en tiempo real.

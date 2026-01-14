# 🎨 Biblioteca Visual — Iyari-ear

> **"Assets visuales para comunicar con coherencia y significado"**

Este documento cataloga todos los recursos visuales del proyecto Iyari-ear, organizados por propósito y contexto.

---

## 📚 Índice

1. [Iconografía](#-iconografía)
2. [Paleta de Color](#-paleta-de-color)
3. [Tipografía](#-tipografía)
4. [Logos y Marcas](#-logos-y-marcas)
5. [Posters Narrativos](#-posters-narrativos)
6. [Screenshots](#-screenshots)
7. [Diagramas](#-diagramas)
8. [Badges](#-badges)

---

## 🎯 Iconografía

### Emojis Canónicos

Cada emoji tiene un **significado semántico específico** en Iyari-ear.

#### Sistema y Funcionalidad
```
🎤 — Subtítulos / Audio / Voz
🔧 — Diagnóstico / Reparación / Técnico
⚙️ — Sistema / Arquitectura / Backend
📱 — App / Móvil / PWA
💻 — CLI / Terminal / Desarrollo
🌐 — Web / Browser / Internet
```

#### Emociones y Propósito
```
❤️  — Empatía / Humano / Comunidad
💝 — Manifiesto / Filosofía / Cariño
🤝 — Colaboración / Conexión
🌉 — Puente / Accesibilidad
💡 — Idea / Insight / Tip
✨ — Especial / Destacado / Nuevo
```

#### Plataformas
```
🪟 — Windows
🐧 — Linux
🍎 — macOS / Apple
🤖 — Android
🦊 — Firefox
```

#### Estados y Acciones
```
✅ — Sí / Correcto / Completado
❌ — No / Error / Prohibido
⚠️  — Warning / Importante
🔒 — Privacidad / Seguridad
⚡ — Rápido / Acción / Inicio
🎬 — Demo / Video / Visual
📖 — Documentación / Lectura
🎯 — Objetivo / Foco
📌 — Pin / Importante
🔍 — Buscar / Diagnosticar
```

#### Releases y Versiones
```
👑 — Coronación / Milestone
🌅 — Futuro / Visión / Roadmap
🚀 — Launch / Release
🎉 — Celebración / Achievement
```

### Uso Correcto

**✅ Hacer:**
```markdown
## 🎤 Sistema de Subtítulos
## 🔧 Diagnóstico Electrónico
## ❤️  Historias Reales
```

**❌ No Hacer:**
```markdown
Hola 👋 este 📝 es 🎨 un 🌟 ejemplo 💫 malo 😅
```

---

## 🎨 Paleta de Color

### Sistema Tripartito

#### ❤️ Emocional — Rosa/Magenta
```css
--color-empathy-primary: #ff0080;
--color-empathy-light: #ff66b3;
--color-empathy-dark: #cc0066;
```

**Uso:** Manifiesto, historias, testimonios, comunidad

**Visual:**
```
███████████ #ff0080
███████████ #ff66b3
███████████ #cc0066
```

#### ⚙️ Técnico — Verde/Cyan
```css
--color-technical-primary: #00ff9f;
--color-technical-cyan: #00bfff;
--color-technical-dark: #00cc7f;
```

**Uso:** Código, arquitectura, API, sistema

**Visual:**
```
███████████ #00ff9f
███████████ #00bfff
███████████ #00cc7f
```

#### 📚 Institucional — Naranja
```css
--color-institutional-primary: #ff6b00;
--color-institutional-light: #ffa500;
--color-institutional-dark: #cc5500;
```

**Uso:** Documentación, instalación, guías oficiales

**Visual:**
```
███████████ #ff6b00
███████████ #ffa500
███████████ #cc5500
```

### Colores de Soporte

#### Fondos
```css
--background-dark: #1a1a2e
--background-darker: #16213e
--background-card: rgba(30, 30, 50, 0.8)
```

#### Texto
```css
--text-primary: #ffffff
--text-secondary: #e0e0e0
--text-muted: #b0b0b0
--text-dim: #808080
```

#### Estados
```css
--success: #00ff9f
--warning: #ffa500
--error: #ff4444
--info: #00bfff
```

---

## 📝 Tipografía

### Jerarquía

```
# Títulos (H1)       — 2.5rem — Bold (700) — Color contextual
## Subtítulos (H2)   — 1.75rem — SemiBold (600) — Color contextual
### Subsección (H3)  — 1.25rem — Medium (500) — Text secondary
Párrafos            — 1rem — Normal (400) — Text secondary
> Callouts          — 1rem — Varies — Emphasized
`code`              — 0.9rem — Monospace — Technical green
```

### Fuentes

**Sans-serif (General):**
```
-apple-system, BlinkMacSystemFont, 'Segoe UI', 
Roboto, 'Helvetica Neue', Arial, sans-serif
```

**Monospace (Código):**
```
'Courier New', Courier, monospace, 
'SF Mono', Monaco, Consolas
```

---

## 🏷️ Logos y Marcas

### Logo Principal

**Emoji-based:**
```
🎤 Iyari-ear
```

**Variantes por contexto:**
```
🎤 — Subtítulos (default)
🔧 — Diagnóstico
❤️  — Comunidad
```

### Tagline Oficial

```
"Para que nadie quede fuera de la conversación"
```

### Tagline Técnico

```
"Un puente de empatía técnica"
```

---

## 📊 Posters Narrativos

**Ubicación:** `docs/NARRATIVE_POSTERS.md`

### Catálogo

1. **Para Quién Existe** — Audiencias y escenarios
2. **Qué Dolor Repara** — Problemas que resuelve
3. **Casos Reales** — 4 historias de impacto
4. **Filosofía del Sistema** — Principios éticos
5. **Coronación 1.0** — Milestone v1.0

**Formato:** ASCII art en bloques de código Markdown

**Uso:**
```markdown
Embeber en documentos o exportar como imagen
```

---

## 📸 Screenshots

### Screenshots Requeridos

#### Subtítulos
- [ ] `subtitle-demo-desktop.png` — Vista desktop
- [ ] `subtitle-demo-mobile.png` — Vista móvil
- [ ] `subtitle-demo-tablet.png` — Vista tablet
- [ ] `subtitle-demo-active.png` — Escuchando activo

#### Diagnóstico
- [x] `diagnostic-dashboard.png` — Dashboard inicial
- [ ] `diagnostic-upload.png` — Subida de foto
- [ ] `diagnostic-analysis.png` — Análisis en progreso
- [ ] `diagnostic-report.png` — Reporte completo

#### Instalación
- [ ] `install-pwa.gif` — Animación instalación PWA
- [ ] `install-windows.png` — Setup Windows
- [ ] `install-linux.png` — Terminal Linux

### Especificaciones

**Resolución:** Mínimo 1920x1080 para desktop, 750x1334 para móvil
**Formato:** PNG para statics, GIF para animaciones
**Fondo:** Dark mode preferido
**Marca de agua:** Opcional, esquina inferior derecha

---

## 📐 Diagramas

### Diagramas Arquitectónicos

#### Flujo de Subtítulos
```
┌─────────────┐
│  Micrófono  │
└──────┬──────┘
       │ Audio PCM
       ▼
┌─────────────┐
│  WebSocket  │
└──────┬──────┘
       │ Binary chunks
       ▼
┌─────────────┐
│   Backend   │ Google Speech API
│   (Python)  │
└──────┬──────┘
       │ Transcript JSON
       ▼
┌─────────────┐
│  Frontend   │
│   (HTML)    │
└──────┬──────┘
       │ Rendered
       ▼
┌─────────────┐
│  Subtítulos │
│   Display   │
└─────────────┘
```

#### Flujo de Diagnóstico
```
┌──────────┐
│   Foto   │
└────┬─────┘
     │ Upload
     ▼
┌──────────┐
│  Vision  │ Componente recognition
│   API    │
└────┬─────┘
     │ Components list
     ▼
┌──────────┐
│  Engine  │ Razonamiento causal
│  (Local) │
└────┬─────┘
     │ Diagnóstico
     ▼
┌──────────┐
│ Reporte  │
│   3 Cap  │
└──────────┘
```

### Diagramas de Datos

**Ver:** `ARCHITECTURE.md` para diagramas completos

---

## 🏅 Badges

### Badges Actuales

```markdown
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platforms-Windows|Linux|macOS|Android-blue)
![PWA](https://img.shields.io/badge/PWA-Ready-green)
![Python](https://img.shields.io/badge/python-3.7+-blue)
```

### Badges Propuestos v2.0

```markdown
![Empathy](https://img.shields.io/badge/built_with-empathy-ff0080)
![Privacy](https://img.shields.io/badge/privacy-by_design-00ff9f)
![No Tracking](https://img.shields.io/badge/tracking-none-00ff9f)
![Ethical Tech](https://img.shields.io/badge/ethical-tech-ff6b00)
```

### Estilo de Badges

**Color scheme:**
- **Blue** — Información técnica (versión, plataforma)
- **Green** — Estados positivos (PWA ready, tests passing)
- **Orange** — Documentación y guías
- **Pink** — Comunidad y empatía
- **Red** — Warnings o estados críticos

---

## 🎬 Assets de Video/GIF

### Demos Requeridos

1. **Subtítulos en acción** — 30s
   - Mesa con celular
   - Persona habla
   - Texto aparece en tiempo real
   - Sin edición, raw footage

2. **Diagnóstico rápido** — 60s
   - Foto de ESP32
   - Upload a sistema
   - Análisis en progreso
   - Reporte final

3. **Instalación PWA** — 45s
   - Abrir en browser
   - Click en "Instalar"
   - App instalada
   - Uso desde menú

### Especificaciones Video

- **Formato:** MP4 (H.264)
- **Resolución:** 1920x1080 o 1080x1920 (mobile)
- **Duración:** 30-90 segundos
- **Audio:** Opcional, subtítulos recomendados
- **Tamaño:** < 10MB por video

---

## 📦 Organización de Assets

### Estructura de Carpetas

```
docs/
├── assets/
│   ├── screenshots/
│   │   ├── subtitle-demo-desktop.png
│   │   ├── subtitle-demo-mobile.png
│   │   └── diagnostic-dashboard.png
│   ├── videos/
│   │   ├── subtitle-demo-30s.mp4
│   │   └── diagnostic-demo-60s.mp4
│   ├── diagrams/
│   │   ├── architecture-flow.svg
│   │   └── data-flow.svg
│   └── logos/
│       ├── iyari-ear-icon.svg
│       └── iyari-ear-banner.png
```

---

## 🎨 Guidelines de Creación

### Screenshots

**Antes de capturar:**
1. Usa modo oscuro
2. Limpia la UI de elementos de debug
3. Usa datos de ejemplo realistas (no "lorem ipsum")
4. Muestra casos de uso reales

**Durante captura:**
- Tamaño de ventana estándar
- Sin overlays de sistema (notificaciones)
- Barra de URL limpia
- Zoom 100%

### Videos/GIFs

**Preparación:**
1. Guión claro de 3-5 pasos
2. Sin música de fondo (distractora)
3. Movimientos lentos y deliberados
4. Zoom en áreas importantes

**Post-producción:**
- Comprimir sin pérdida de calidad
- Añadir subtítulos si hay voz
- Recortar espacios muertos
- Exportar en múltiples resoluciones

---

## 🔄 Versioning de Assets

### Nomenclatura

```
{componente}-{contexto}-{version}.{ext}

Ejemplos:
subtitle-demo-desktop-v1.0.png
diagnostic-flow-v2.0.svg
logo-iyari-ear-2026.svg
```

### Change Log Visual

**v1.0 (Enero 2025)**
- Logo emoji-based
- Screenshots diagnóstico
- Posters narrativos (ASCII art)
- Diagramas arquitectónicos

**v2.0 (Propuesto 2026)**
- Sistema de color tripartito implementado
- Video demos completos
- Landing page assets
- Logos vectoriales SVG

---

## 🌐 Assets Web-Ready

### Formatos Recomendados

**Imágenes:**
- **PNG** — Screenshots con transparencia
- **JPEG** — Fotos sin transparencia
- **SVG** — Logos, iconos, diagramas
- **WebP** — Optimizado para web (fallback a PNG)

**Videos:**
- **MP4** — Compatibilidad universal
- **WebM** — Tamaño reducido (fallback a MP4)
- **GIF** — Animaciones cortas < 5s

### Optimización

**Imágenes:**
```bash
# Comprimir PNG
pngquant image.png --output compressed.png

# Convertir a WebP
cwebp -q 80 image.png -o image.webp

# Resize para web
convert image.png -resize 1920x1080 resized.png
```

**Videos:**
```bash
# Comprimir MP4
ffmpeg -i input.mp4 -crf 23 output.mp4

# Crear GIF optimizado
ffmpeg -i input.mp4 -vf "fps=10,scale=800:-1" output.gif
```

---

## 📋 Checklist de Asset Completo

Antes de publicar un asset, verificar:

- [ ] Nomenclatura correcta
- [ ] Resolución adecuada
- [ ] Formato optimizado
- [ ] Tamaño de archivo < 5MB (imágenes) / < 10MB (videos)
- [ ] Usa paleta de color canónica
- [ ] Representa caso de uso real
- [ ] Sin información sensible
- [ ] Metadata correcto (alt text, título)
- [ ] Versionado en nombre de archivo
- [ ] Documentado en este catálogo

---

## 🤝 Contribuir Assets

¿Quieres crear assets para Iyari-ear?

1. **Lee las guidelines** de este documento
2. **Usa la paleta de color** canónica
3. **Crea assets con significado**, no solo decorativos
4. **Abre un PR** con el asset y documentación
5. **Sigue la nomenclatura** establecida

**Preguntas frecuentes:**

**¿Puedo usar IA para generar assets?**
Sí, pero deben representar casos de uso reales y seguir las guidelines visuales.

**¿Necesito permiso para crear assets?**
No, pero abre un Issue primero para coordinar y evitar duplicados.

**¿Qué licencia tienen los assets?**
Misma que el código: libre uso manteniendo el espíritu del proyecto.

---

<div align="center">

**"Los mejores assets visuales son invisibles.  
Solo transmiten el mensaje sin ruido."**

*Iyari-ear Visual Library v2.0*

</div>

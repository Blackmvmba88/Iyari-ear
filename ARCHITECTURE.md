# 🏗️ Arquitectura Técnica — Iyari-ear

> **"Un mapa cognitivo para que los demás no se pierdan"**

## Vista General del Sistema

Iyari-ear es un sistema **multiplataforma** que combina dos funcionalidades principales:
1. **Subtítulos en tiempo real** para conversaciones cara a cara
2. **Diagnóstico electrónico profesional** para reparación de placas

---

## 🎯 Diagrama de Arquitectura

### Sistema de Subtítulos en Tiempo Real

```
┌─────────────────┐
│   Navegador     │
│   (Frontend)    │
│                 │
│  ┌───────────┐  │
│  │ Micrófono │  │
│  │  Browser  │  │
│  └─────┬─────┘  │
│        │        │
│   Audio Chunks  │
│        │        │
│  ┌─────▼─────┐  │
│  │ WebSocket │  │
│  │  Cliente  │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │
    Internet
         │
┌────────▼────────┐
│  FastAPI Server │
│   (Backend)     │
│                 │
│  ┌───────────┐  │
│  │ WebSocket │  │
│  │  Handler  │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │  Speech   │  │
│  │Recognition│  │
│  │  (Google) │  │
│  └─────┬─────┘  │
│        │        │
│   Texto transcrito
│        │        │
│  ┌─────▼─────┐  │
│  │ WebSocket │  │
│  │  Respuesta│  │
│  └───────────┘  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   Navegador     │
│  Muestra texto  │
│  en pantalla    │
└─────────────────┘
```

### Sistema de Diagnóstico Electrónico

```
┌──────────────────────────────────────────┐
│         Frontend (diagnostic.html)        │
│                                           │
│  ┌────────────┐      ┌────────────┐      │
│  │  Drag &    │      │  Session   │      │
│  │  Drop UI   │      │  Manager   │      │
│  └──────┬─────┘      └──────┬─────┘      │
│         │                   │             │
│    Imágenes            WebSocket          │
│         │                   │             │
└─────────┼───────────────────┼─────────────┘
          │                   │
          │              Real-time
     HTTP POST            Updates
          │                   │
┌─────────▼───────────────────▼─────────────┐
│         FastAPI Backend (main.py)         │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │   REST API Endpoints                 │ │
│  │   /api/diagnostic/*                  │ │
│  └────────────┬─────────────────────────┘ │
│               │                            │
│  ┌────────────▼─────────────────────────┐ │
│  │   Diagnostic Engine                  │ │
│  │   (diagnostic_engine.py)             │ │
│  │                                      │ │
│  │  ┌────────────────────────────────┐ │ │
│  │  │  Capa 1: Localización          │ │ │
│  │  │  (¿Dónde está la falla?)       │ │ │
│  │  │  - Rail de voltaje             │ │ │
│  │  │  - Componente específico       │ │ │
│  │  │  - Bloque funcional            │ │ │
│  │  └────────────┬───────────────────┘ │ │
│  │               │                      │ │
│  │  ┌────────────▼───────────────────┐ │ │
│  │  │  Capa 2: Causa Raíz            │ │ │
│  │  │  (¿Por qué existe la falla?)   │ │ │
│  │  │  - Análisis causal             │ │ │
│  │  │  - Evidencia recopilada        │ │ │
│  │  │  - Razonamiento técnico        │ │ │
│  │  └────────────┬───────────────────┘ │ │
│  │               │                      │ │
│  │  ┌────────────▼───────────────────┐ │ │
│  │  │  Capa 3: Consecuencia          │ │ │
│  │  │  (¿Qué rompe funcionalmente?)  │ │ │
│  │  │  - Impacto en el sistema       │ │ │
│  │  │  - Funciones afectadas         │ │ │
│  │  │  - Efectos en cascada          │ │ │
│  │  └────────────────────────────────┘ │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │   3 Estilos de Diagnóstico:          │ │
│  │   • Técnico (práctico)               │ │
│  │   • Ingeniero (causal)               │ │
│  │   • Forense (exhaustivo)             │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

---

## 📁 Estructura de Módulos

```
Iyari-ear/
│
├── 🎤 Subtítulos en Tiempo Real
│   ├── index.html              # Frontend principal (PWA)
│   ├── js/
│   │   └── matrix.js           # Lógica del cliente WebSocket
│   ├── styles/
│   │   └── style.css           # Estilos de la UI
│   └── main.py                 # Servidor FastAPI con WebSocket
│
├── 🔧 Sistema de Diagnóstico Electrónico
│   ├── diagnostic.html         # Frontend de diagnóstico
│   ├── diagnostic_engine.py    # Motor de 3 capas
│   └── main.py                 # API REST + WebSocket para diagnóstico
│
├── 🎬 Optimizador de Subtítulos
│   ├── subtitle-optimizer.html # Frontend del optimizador
│   ├── subtitle_processor.py   # Procesador de SRT/VTT/ASS
│   └── vlc_plugin_generator.py # Generador de plugin VLC
│
├── 💻 CLI (Interfaz de Línea de Comandos)
│   ├── cli/
│   │   └── iyari_ear_cli.py    # Comandos: doctor, test-mic, start
│   └── setup.py                # Instalador del CLI
│
├── 📱 PWA (Progressive Web App)
│   ├── apps/pwa/
│   │   ├── manifest.json       # Manifiesto PWA
│   │   ├── service-worker.js   # Service worker para offline
│   │   └── icons/              # Íconos de la app
│   └── generate_icons.py       # Generador de íconos
│
├── 📖 Documentación
│   ├── README.md               # Documentación principal
│   ├── ARCHITECTURE.md         # Este archivo
│   ├── API.md                  # Contratos de API
│   ├── CONTRIBUTING.md         # Guía de contribución
│   ├── MANIFIESTO.md           # Alma del proyecto
│   ├── IMPACT.md               # Impacto técnico
│   ├── TESTIMONIOS.md          # Historias reales
│   └── docs/
│       ├── DIAGNOSTIC_SYSTEM.md
│       ├── DIAGNOSTIC_STYLES.md
│       ├── SUBTITLE_OPTIMIZATION.md
│       ├── VLC_PLUGIN_GUIDE.md
│       ├── INSTALLATION.md
│       └── PLATFORMS.md
│
├── 🧪 Tests
│   └── tests/                  # (Futuro: tests unitarios)
│
└── 🛠️ Configuración
    ├── requirements.txt        # Dependencias Python
    ├── setup.py               # Instalación del paquete
    ├── .gitignore             # Archivos ignorados
    └── VERSION                # Versión actual
```

---

## 🔄 Flujos de Datos

### Flujo 1: Subtítulos en Tiempo Real

```
1. Usuario abre navegador → index.html
2. Usuario presiona "Iniciar"
3. Browser pide permiso de micrófono → Usuario acepta
4. Browser captura audio en chunks (cada ~500ms)
5. Cliente WebSocket envía audio binario → Servidor
6. Servidor (main.py) recibe audio → speech_recognition
7. Google Speech API transcribe audio → texto
8. Servidor envía texto → Cliente WebSocket
9. Cliente muestra texto en pantalla en tiempo real
10. Repite desde paso 4 mientras el micrófono esté activo
```

**Características clave:**
- ✅ Sin almacenamiento (el audio desaparece después de transcribir)
- ✅ Latencia baja (~1-2 segundos)
- ✅ Soporte multi-idioma (español, inglés)

### Flujo 2: Diagnóstico Electrónico (Modo Asíncrono)

```
1. Técnico abre diagnostic.html
2. Crea sesión → Ingresa modelo de placa + estilo de diagnóstico
3. Sube 1-5 fotos (frontal, backside, closeup, etc.)
4. Presiona "Analizar"
5. Backend recibe imágenes → diagnostic_engine.py
6. Motor analiza:
   a. Identifica rails de voltaje (3V3, 5V, etc.)
   b. Detecta componentes (reguladores, capacitores)
   c. Genera hipótesis de Capa 1 (localización)
   d. Genera hipótesis de Capa 2 (causa raíz)
   e. Genera hipótesis de Capa 3 (impacto funcional)
7. WebSocket envía actualizaciones en tiempo real → Frontend
8. Frontend muestra diagnóstico completo con:
   - Localización de falla
   - Causa probable
   - Impacto funcional
   - Próximos pasos
   - Puntos de prueba
9. Técnico puede exportar reporte (JSON/TXT)
```

**Características clave:**
- ✅ Multi-shot (múltiples fotos por sesión)
- ✅ 3 estilos de diagnóstico
- ✅ Razonamiento causal, no solo reconocimiento visual
- ✅ Modo ticket: Foto → Procesa → Diagnóstico

### Flujo 3: Optimización de Subtítulos

```
1. Usuario sube archivo .srt / .vtt / .ass
2. subtitle_processor.py procesa:
   a. Valida timing y formato
   b. Detecta problemas (superposiciones, líneas largas)
   c. Optimiza duración y espaciado
3. Usuario descarga archivo optimizado
4. (Opcional) Plugin VLC lo hace automáticamente
```

---

## 🧩 Componentes Clave

### 1. Backend (FastAPI + WebSocket)
**Archivo:** `main.py`

**Responsabilidades:**
- Servir archivos estáticos (HTML, CSS, JS)
- Manejar WebSocket para transcripción en tiempo real
- API REST para diagnóstico electrónico
- API REST para procesamiento de subtítulos
- Rate limiting y validación de seguridad

**Tecnologías:**
- FastAPI (framework web)
- Uvicorn (servidor ASGI)
- speech_recognition (STT)
- WebSockets (comunicación bidireccional)

### 2. Motor de Diagnóstico
**Archivo:** `diagnostic_engine.py`

**Responsabilidades:**
- Gestión de sesiones de diagnóstico
- Análisis de 3 capas (Localización → Causa → Consecuencia)
- Generación de hipótesis con diferentes estilos
- Exportación de reportes

**Tecnologías:**
- Python dataclasses
- Enums para tipos y causas
- JSON para exportación

### 3. Procesador de Subtítulos
**Archivo:** `subtitle_processor.py`

**Responsabilidades:**
- Parseo de SRT, VTT, ASS
- Validación de timing y formato
- Optimización automática
- Conversión entre formatos

### 4. CLI
**Archivo:** `cli/iyari_ear_cli.py`

**Comandos:**
```bash
iyari-ear doctor          # Verifica sistema
iyari-ear test-mic        # Prueba micrófono
iyari-ear start           # Inicia servidor
iyari-ear process-subtitle # Procesa subtítulos
iyari-ear install-vlc-plugin # Instala plugin VLC
```

### 5. Frontend (HTML + JavaScript)

**Archivos principales:**
- `index.html` - Subtítulos en tiempo real
- `diagnostic.html` - Sistema de diagnóstico
- `subtitle-optimizer.html` - Optimizador de subtítulos

**Características:**
- PWA (Progressive Web App) instalable
- Modo oscuro
- Drag & drop
- WebSocket cliente
- Responsive design

---

## 🔐 Seguridad y Privacidad

### Principios de Diseño Seguro

1. **No almacenamiento de audio**
   - El audio se transcribe y desaparece inmediatamente
   - No hay logs de conversaciones
   - No hay bases de datos de audio

2. **Rate limiting**
   - Límite de 30 solicitudes por minuto por IP
   - Protección contra abuso de API

3. **Validación de entrada**
   - Tamaño máximo de audio: 10 MB
   - Validación de formatos de archivo
   - Sanitización de paths para prevenir directory traversal

4. **Conexiones seguras**
   - WebSocket con validación de origen
   - Límite de 100 conexiones simultáneas

5. **Sesiones temporales**
   - Las sesiones de diagnóstico son temporales
   - Limpieza automática de archivos antiguos (>24h)

---

## 🚀 Stack Tecnológico

### Backend
- **Python 3.7+**
- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI
- **speech_recognition** - Biblioteca para STT
- **Pillow** - Procesamiento de imágenes (para diagnóstico)

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos (con variables CSS para theming)
- **JavaScript Vanilla** - Lógica del cliente
- **WebSocket API** - Comunicación en tiempo real
- **MediaRecorder API** - Captura de audio

### Infraestructura
- **Git** - Control de versiones
- **GitHub** - Hosting del código
- **PWA** - Progressive Web App para instalación

### APIs Externas
- **Google Speech Recognition API** - Transcripción de voz

---

## 📊 Escalabilidad

### Capacidad Actual
- **Conexiones simultáneas:** 100 usuarios
- **Throughput:** ~30 solicitudes/minuto por usuario
- **Latencia:** 1-2 segundos para transcripción

### Cómo Escalar
1. **Horizontal:** Múltiples instancias detrás de un load balancer
2. **Caché:** Redis para sesiones y rate limiting
3. **CDN:** Servir archivos estáticos desde CDN
4. **WebSocket:** Usar Redis Pub/Sub para WebSocket distribuido
5. **STT:** Migrar a Whisper local o servicios dedicados

---

## 🔧 Patrones de Diseño Utilizados

### 1. WebSocket Bidireccional
- Comunicación full-duplex entre cliente y servidor
- Ideal para transcripción en tiempo real

### 2. REST API
- CRUD para sesiones de diagnóstico
- Endpoints claros y documentados

### 3. Dataclasses
- Estructuras de datos tipadas para diagnóstico
- Facilita serialización/deserialización

### 4. Enum para Estados
- Tipos de componentes, causas de fallas, niveles de impacto
- Evita "magic strings"

### 5. Modular Architecture
- Separación clara entre:
  - Transcripción (speech_recognition)
  - Diagnóstico (diagnostic_engine)
  - Subtítulos (subtitle_processor)
  - CLI (iyari_ear_cli)

---

## 🧪 Testing (Futuro)

### Estrategia de Testing
```
tests/
├── unit/
│   ├── test_diagnostic_engine.py
│   ├── test_subtitle_processor.py
│   └── test_api_endpoints.py
├── integration/
│   ├── test_websocket_flow.py
│   └── test_diagnostic_flow.py
└── e2e/
    └── test_user_flows.py
```

### Herramientas Sugeridas
- **pytest** - Framework de testing
- **pytest-asyncio** - Tests asíncronos
- **httpx** - Cliente HTTP para tests
- **pytest-cov** - Cobertura de código

---

## 🎯 Decisiones Arquitectónicas Clave

### ¿Por qué FastAPI?
- Moderno, rápido, con soporte nativo para async/await
- Documentación automática con OpenAPI
- Type hints nativos
- WebSocket out-of-the-box

### ¿Por qué Google Speech API?
- Precisión alta
- Soporte multi-idioma
- Sin necesidad de entrenar modelos
- Gratis para uso moderado

### ¿Por qué No se Almacena Audio?
- **Privacidad por diseño**
- El proyecto existe para ayudar, no para vigilar
- Cumple con la filosofía del Manifiesto

### ¿Por qué 3 Capas en Diagnóstico?
- Localización + Causa + Consecuencia = Diagnóstico completo
- Los técnicos necesitan saber DÓNDE, POR QUÉ y QUÉ IMPACTO
- Es la metodología profesional real

### ¿Por qué PWA?
- Instalable sin App Store
- Funciona en cualquier dispositivo
- Actualizaciones automáticas
- Acceso offline parcial

---

## 🌐 Deployment

### Opción 1: Local
```bash
python main.py
# Acceder a http://localhost:8000
```

### Opción 2: Cloud (Render, Railway, etc.)
```bash
# 1. Configurar variables de entorno
HOST=0.0.0.0
PORT=8000

# 2. Comando de inicio
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Opción 3: Docker (Futuro)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔮 Roadmap Arquitectónico

### Corto Plazo (v1.1)
- [ ] Tests unitarios básicos
- [ ] CI/CD con GitHub Actions
- [ ] Logs estructurados

### Medio Plazo (v1.2)
- [ ] Migrar a Whisper local (eliminar dependencia de Google)
- [ ] Caché Redis para sesiones
- [ ] Docker Compose para desarrollo

### Largo Plazo (v2.0)
- [ ] ML/CV real para diagnóstico de placas
- [ ] Soporte para más idiomas
- [ ] Plugin system para extensiones
- [ ] Modo offline completo

---

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [PWA Best Practices](https://web.dev/progressive-web-apps/)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)

---

<div align="center">

**Iyari-ear** — *Un puente de empatía técnica*

**Creado con cariño para una amiga. Compartido con amor para el mundo.**

✨ 2025 ✨

</div>

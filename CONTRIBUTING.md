# 🤝 Guía de Contribución — Iyari-ear

> **"Defender el alma del proyecto desde el código"**

Bienvenido a Iyari-ear. Esta guía te ayudará a contribuir manteniendo el espíritu y la calidad del proyecto.

---

## 📋 Índice

1. [Filosofía del Proyecto](#filosofía-del-proyecto)
2. [Estilo Técnico](#estilo-técnico)
3. [Estilo Humano (Decisiones Prohibidas)](#estilo-humano-decisiones-prohibidas)
4. [Estilo de Comunicación](#estilo-de-comunicación)
5. [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
6. [Proceso de Contribución](#proceso-de-contribución)
7. [Code Review](#code-review)
8. [Tipos de Contribuciones](#tipos-de-contribuciones)

---

## Filosofía del Proyecto

**Iyari-ear no es un producto. Es una herramienta de empatía.**

Antes de contribuir, lee el [Manifiesto](./MANIFIESTO.md) para entender el alma del proyecto.

### Pregunta Guía

Cada decisión técnica se hace preguntando:

> *"¿Esto ayuda a conectar o complica la vida?"*

Si complica la vida, probablemente no pertenece aquí.

### Principios Fundamentales

1. **Privacidad por Diseño** - No grabar, no guardar, no vigilar
2. **Simplicidad sobre Features** - Menos es más
3. **Empatía sobre Eficiencia** - A veces lo humano es más importante que lo óptimo
4. **Código Legible > Código Clever** - Prefiere claridad sobre ingenio
5. **Documentación es Código** - Explica el por qué, no solo el qué

---

## Estilo Técnico

### Python

#### Convenciones Generales

```python
# ✅ CORRECTO: Type hints, docstrings, nombres descriptivos
def process_audio_chunk(
    audio_data: bytes, 
    language: str = "es-ES"
) -> Optional[str]:
    """
    Transcribe un chunk de audio a texto.
    
    Args:
        audio_data: Audio en formato WAV (bytes)
        language: Código de idioma (ej: "es-ES", "en-US")
    
    Returns:
        Texto transcrito o None si no se pudo transcribir
    
    Raises:
        ValueError: Si el formato de audio es inválido
    """
    if len(audio_data) == 0:
        raise ValueError("Audio chunk vacío")
    
    # Lógica aquí
    return transcribed_text

# ❌ INCORRECTO: Sin tipos, sin docstring, nombres crípticos
def proc(ad, l="es"):
    if len(ad)==0:
        raise ValueError("empty")
    return txt
```

#### Nombres de Variables

```python
# ✅ CORRECTO: Nombres descriptivos en inglés o español consistente
session_id = "session_123"
diagnostic_engine = DiagnosticEngine()
voltage_rail = "3V3"

# ❌ INCORRECTO: Nombres crípticos o inconsistentes
sid = "s123"
de = DiagnosticEngine()
vr = "3V3"
```

#### Manejo de Errores

```python
# ✅ CORRECTO: Errores específicos, mensajes claros
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"Error al procesar datos: {e}")
    raise HTTPException(
        status_code=400,
        detail=f"Datos inválidos: {str(e)}"
    )

# ❌ INCORRECTO: Catch genérico, sin contexto
try:
    result = process_data(data)
except:
    raise Exception("Error")
```

#### Logging

```python
# ✅ CORRECTO: Niveles apropiados, contexto útil
logger.info(f"Sesión de diagnóstico creada: {session_id}")
logger.warning(f"Chunk de audio grande: {len(audio_chunk)} bytes")
logger.error(f"Error al procesar imagen: {e}")
logger.debug(f"Audio chunk recibido: {len(audio_chunk)} bytes")

# ❌ INCORRECTO: Nivel incorrecto, sin contexto
print("sesion creada")
logger.info(f"Error: {e}")  # Error debería ser logger.error
```

#### Estructura de Clases

```python
# ✅ CORRECTO: Dataclasses para estructuras de datos
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DiagnosticSession:
    """Sesión completa de diagnóstico de una placa"""
    session_id: str
    board_model: str
    creation_time: datetime = field(default_factory=datetime.now)
    images: List[BoardImage] = field(default_factory=list)
    status: str = "iniciada"
    
    def add_image(self, image: BoardImage) -> None:
        """Añade una imagen a la sesión"""
        self.images.append(image)
```

#### Validación de Entrada

```python
# ✅ CORRECTO: Validación exhaustiva con mensajes claros
def validate_session_id(session_id: str) -> bool:
    """
    Valida formato de session_id para prevenir directory traversal
    
    Formato esperado: session_YYYYMMDD_HHMMSS_hash
    """
    import re
    pattern = r'^session_[0-9]{8}_[0-9]{6}_[a-f0-9]{8,16}$'
    if not re.match(pattern, session_id):
        raise ValueError(f"Formato de session_id inválido: {session_id}")
    return True

# ❌ INCORRECTO: Sin validación o validación débil
def validate_session_id(session_id):
    if "/" in session_id:
        raise ValueError("Invalid")
```

### JavaScript

#### Estilo General

```javascript
// ✅ CORRECTO: const/let, nombres claros, comentarios útiles
const connectWebSocket = (url, onMessage) => {
    const ws = new WebSocket(url);
    
    ws.onopen = () => {
        console.log('WebSocket conectado');
    };
    
    ws.onmessage = (event) => {
        onMessage(event.data);
    };
    
    return ws;
};

// ❌ INCORRECTO: var, nombres crípticos, sin comentarios
var cws = function(u, om) {
    var w = new WebSocket(u);
    w.onopen = function() { console.log('ok'); };
    w.onmessage = function(e) { om(e.data); };
    return w;
};
```

#### Manejo de Promesas

```javascript
// ✅ CORRECTO: async/await, manejo de errores
const uploadImage = async (file, sessionId) => {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', sessionId);
        
        const response = await fetch('/api/diagnostic/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error al subir imagen:', error);
        throw error;
    }
};

// ❌ INCORRECTO: callback hell, sin manejo de errores
function uploadImage(file, sessionId, callback) {
    var formData = new FormData();
    formData.append('file', file);
    fetch('/api/diagnostic/upload', {
        method: 'POST',
        body: formData
    }).then(function(r) {
        r.json().then(function(d) {
            callback(d);
        });
    });
}
```

### HTML/CSS

#### HTML Semántico

```html
<!-- ✅ CORRECTO: Semántico, accesible -->
<main>
    <section class="transcription-container">
        <h1>Subtítulos en Tiempo Real</h1>
        <button 
            id="start-button" 
            aria-label="Iniciar transcripción"
            class="primary-button">
            Iniciar
        </button>
        <div 
            class="subtitle-display" 
            role="region" 
            aria-live="polite">
        </div>
    </section>
</main>

<!-- ❌ INCORRECTO: Div soup, sin semántica -->
<div>
    <div class="container">
        <div class="title">Subtítulos en Tiempo Real</div>
        <div id="start">Iniciar</div>
        <div class="display"></div>
    </div>
</div>
```

#### CSS

```css
/* ✅ CORRECTO: Variables CSS, nombres BEM, comentarios */
:root {
    --color-primary: #00ff9f;
    --color-background: #1a1a1a;
    --font-family: 'Inter', sans-serif;
}

.subtitle-display {
    background-color: var(--color-background);
    color: var(--color-primary);
    font-family: var(--font-family);
    /* Texto grande y legible para accesibilidad */
    font-size: 2rem;
    line-height: 1.5;
}

/* ❌ INCORRECTO: Valores hardcodeados, sin comentarios */
.display {
    background-color: #1a1a1a;
    color: #00ff9f;
    font-size: 32px;
}
```

### Comentarios en Código

```python
# ✅ CORRECTO: Explica el POR QUÉ, no el QUÉ
# Limitamos a 30 req/min para prevenir abuso del STT API (limitado por Google)
RATE_LIMIT_REQUESTS = 30

# Usamos session_id con timestamp y hash para evitar colisiones
# y facilitar identificación en logs
session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

# ❌ INCORRECTO: Explica lo obvio
# Asigna 30 a la variable RATE_LIMIT_REQUESTS
RATE_LIMIT_REQUESTS = 30

# Crea un session_id
session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
```

### Testing

```python
# ✅ CORRECTO: Tests claros, casos edge, nombres descriptivos
import pytest
from diagnostic_engine import DiagnosticEngine, DiagnosticStyle

def test_create_session_generates_valid_id():
    """El ID de sesión debe tener formato correcto"""
    engine = DiagnosticEngine()
    session_id = engine.create_session("ESP32-DevKitC")
    
    assert session_id.startswith("session_")
    assert len(session_id.split("_")) == 3
    assert session_id in engine.sessions

def test_create_session_with_custom_id():
    """Se debe permitir session_id personalizado"""
    engine = DiagnosticEngine()
    custom_id = "session_20250113_120000_abc12345"
    session_id = engine.create_session("ESP32", session_id=custom_id)
    
    assert session_id == custom_id

def test_add_image_to_nonexistent_session_raises_error():
    """Añadir imagen a sesión inexistente debe fallar"""
    engine = DiagnosticEngine()
    
    with pytest.raises(ValueError, match="Sesión .* no encontrada"):
        engine.add_image("nonexistent", "/path/to/image.jpg")

# ❌ INCORRECTO: Tests vagos, sin contexto
def test1():
    e = DiagnosticEngine()
    s = e.create_session("ESP32")
    assert s
```

---

## Estilo Humano (Decisiones Prohibidas)

Estas decisiones están **PROHIBIDAS** porque van contra el alma del proyecto:

### 🚫 Nunca Agregues

#### 1. Grabación de Audio
```python
# ❌ PROHIBIDO
with open("conversation.wav", "wb") as f:
    f.write(audio_data)

# ✅ PERMITIDO
# El audio se transcribe y desaparece
text = recognize_speech(audio_data)
# audio_data se descarta aquí
```

**Razón:** Privacidad por diseño. No vigilamos.

#### 2. Almacenamiento de Conversaciones
```python
# ❌ PROHIBIDO
db.insert("conversations", {
    "text": transcribed_text,
    "timestamp": datetime.now()
})

# ✅ PERMITIDO
# El texto se muestra y desaparece
websocket.send(transcribed_text)
# No hay persistencia
```

**Razón:** No guardamos conversaciones privadas.

#### 3. Métricas de Usuario / Analytics
```python
# ❌ PROHIBIDO
analytics.track("user_engagement", {
    "duration": session_time,
    "words_spoken": word_count
})

# ✅ PERMITIDO (solo métricas técnicas)
logger.info(f"WebSocket conectado. Conexiones activas: {active_connections}")
```

**Razón:** No medimos personas, medimos sistema.

#### 4. Gamificación
```python
# ❌ PROHIBIDO
user.add_achievement("spoke_1000_words")
user.increment_points(10)

# ✅ PERMITIDO
# Sin sistemas de puntos, logros, streaks, etc.
```

**Razón:** No convertimos conversaciones en juego.

#### 5. Autenticación Obligatoria (para funcionalidad básica)
```python
# ❌ PROHIBIDO (para subtítulos básicos)
@app.get("/")
@requires_auth
async def index():
    return FileResponse("index.html")

# ✅ PERMITIDO
@app.get("/")
async def index():
    return FileResponse("index.html")
```

**Razón:** Acceso sin barreras. Si en el futuro se agrega auth, debe ser opcional.

#### 6. Publicidad / Monetización Directa
```html
<!-- ❌ PROHIBIDO -->
<script src="google-ads.js"></script>

<!-- ✅ PERMITIDO -->
<!-- Ninguna publicidad -->
```

**Razón:** No es un producto comercial.

#### 7. Recopilación de Datos Personales
```python
# ❌ PROHIBIDO
user_data = {
    "name": request.form.get("name"),
    "email": request.form.get("email"),
    "location": request.headers.get("X-Forwarded-For")
}

# ✅ PERMITIDO (solo datos técnicos necesarios)
rate_limit_check(request.client.host)  # IP solo para rate limiting temporal
```

**Razón:** Minimización de datos.

---

## Estilo de Comunicación

### Pull Requests

#### Título
```
✅ CORRECTO:
feat: Agregar soporte para idioma francés en transcripción
fix: Corregir superposición de subtítulos en modo oscuro
docs: Actualizar guía de instalación para macOS
refactor: Simplificar lógica de diagnóstico capa 2

❌ INCORRECTO:
update
fixed bug
changes
PR #123
```

**Formato:** `tipo: Descripción clara y específica`

**Tipos:**
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Documentación
- `refactor:` - Refactorización sin cambio de funcionalidad
- `test:` - Agregar o mejorar tests
- `chore:` - Mantenimiento (dependencias, config)
- `style:` - Formato de código (no afecta funcionalidad)

#### Descripción del PR

```markdown
## ✅ CORRECTO

### Resumen
Agrega soporte para transcripción en francés (fr-FR).

### Cambios
- Añadido `fr-FR` a SUPPORTED_LANGUAGES
- Actualizado selector de idioma en frontend
- Agregados tests para validación de idioma francés

### Motivación
Un usuario francés solicitó esta funcionalidad para usar la app en París.

### Testing
- [ ] Tests unitarios pasan
- [ ] Probado manualmente con audio en francés
- [ ] Interfaz muestra correctamente el nuevo idioma

### Screenshots
![Selector de idioma](link-to-image.png)

### Checklist
- [x] Código sigue las guías de estilo
- [x] Documentación actualizada
- [x] Tests agregados
- [x] No rompe funcionalidad existente
```

```markdown
## ❌ INCORRECTO

cambios varios
```

### Issues

#### Para Bugs

```markdown
## ✅ CORRECTO

### Descripción del Bug
Los subtítulos no aparecen cuando el navegador está en modo incógnito.

### Pasos para Reproducir
1. Abrir Chrome en modo incógnito
2. Ir a http://localhost:8000
3. Presionar "Iniciar"
4. Hablar al micrófono
5. Los subtítulos no aparecen

### Comportamiento Esperado
Los subtítulos deberían aparecer incluso en modo incógnito.

### Comportamiento Actual
La pantalla queda en blanco, sin subtítulos.

### Entorno
- OS: Windows 11
- Navegador: Chrome 120.0.6099.109
- Versión Iyari-ear: v1.0.0

### Logs/Screenshots
```
Error: WebSocket connection failed
```

### Contexto Adicional
Funciona bien en modo normal, solo falla en incógnito.
```

#### Para Features

```markdown
## ✅ CORRECTO

### Propuesta de Feature
Agregar botón de "Pausa" para detener transcripción temporalmente.

### Motivación
A veces el usuario necesita hablar en privado (ej: recibir llamada) 
sin cerrar completamente la app.

### Propuesta de Implementación
- Botón "Pausa" junto al botón "Iniciar"
- Al pausar: detener envío de audio pero mantener WebSocket abierto
- Al reanudar: continuar transcripción desde donde se dejó

### Alternativas Consideradas
1. Cerrar y reabrir: Más fricción para el usuario
2. Mute automático: Menos control explícito

### Impacto
- Código: Moderado (cambio en frontend y lógica de audio)
- UX: Mejora la flexibilidad sin complicar interfaz

### Pregunta Guía
¿Esto ayuda a conectar o complica la vida?
**Respuesta:** Ayuda, da más control sin complejidad.
```

### Code Review

#### Al Revisar Código

```markdown
✅ CORRECTO:

> Línea 42: Considera usar `logger.error()` en lugar de `print()` para 
> mantener consistencia con el resto del código.

> ¿Por qué elegiste guardar el audio en disco? Esto va contra nuestra 
> filosofía de privacidad. ¿Podemos procesarlo en memoria?

> Gran implementación! Solo una sugerencia: ¿podrías agregar un test 
> para el caso donde session_id es None?

❌ INCORRECTO:

> esto esta mal

> no me gusta

> cambia todo
```

**Tono:** Constructivo, específico, explicativo

#### Al Recibir Review

```markdown
✅ CORRECTO:

> Gracias por la observación. Tienes razón, cambié a logger.error().

> Buen punto sobre la privacidad. Refactoricé para procesar en memoria.

> No había pensado en ese edge case. Agregué el test.

❌ INCORRECTO:

> no, esta bien asi

> es solo temporal

> ya funciona
```

---

## Configuración del Entorno de Desarrollo

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clone tu fork
git clone https://github.com/TU_USUARIO/Iyari-ear.git
cd Iyari-ear
```

### 2. Crear Rama

```bash
git checkout -b feature/mi-mejora
```

**Nombres de rama:**
- `feature/nombre-feature` - Nueva funcionalidad
- `fix/nombre-bug` - Corrección de bug
- `docs/tema` - Documentación
- `refactor/componente` - Refactorización

### 3. Instalar Dependencias

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Instalar en modo desarrollo
pip install -e .
```

### 4. Configurar VS Code (Opcional)

El repo incluye `.vscode/settings.json` con configuración recomendada:
- Type checking estricto
- Auto-format con Black (si está instalado)
- Linting con Pylint

### 5. Ejecutar Tests (cuando existan)

```bash
pytest tests/
```

### 6. Ejecutar en Modo Desarrollo

```bash
# Servidor con auto-reload
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

## Proceso de Contribución

### 1. Antes de Escribir Código

- [ ] Lee el [Manifiesto](./MANIFIESTO.md)
- [ ] Lee esta guía completa
- [ ] Busca si ya existe un issue relacionado
- [ ] Si es feature grande, crea issue para discutir primero

### 2. Durante el Desarrollo

- [ ] Escribe código claro y documentado
- [ ] Sigue las guías de estilo
- [ ] Agrega tests para nueva funcionalidad
- [ ] Actualiza documentación si es necesario
- [ ] Haz commits pequeños y frecuentes

#### Mensajes de Commit

```bash
✅ CORRECTO:
git commit -m "feat: Agregar soporte para idioma francés"
git commit -m "fix: Corregir bug de WebSocket en Chrome"
git commit -m "docs: Actualizar README con instrucciones macOS"

❌ INCORRECTO:
git commit -m "update"
git commit -m "fix"
git commit -m "wip"
```

### 3. Antes de Abrir PR

- [ ] Sincroniza con main:
  ```bash
  git fetch upstream
  git rebase upstream/main
  ```
- [ ] Ejecuta tests (si existen)
- [ ] Ejecuta linter
- [ ] Prueba manualmente los cambios
- [ ] Revisa tu propio código

### 4. Abrir Pull Request

```bash
git push origin feature/mi-mejora
```

Luego en GitHub:
1. Click en "New Pull Request"
2. Llena la plantilla del PR
3. Agrega screenshots si hay cambios visuales
4. Espera review

### 5. Durante el Review

- Responde a comentarios constructivamente
- Haz cambios solicitados
- Empuja cambios adicionales a la misma rama
- Marca conversaciones como resueltas

### 6. Después del Merge

- Elimina tu rama local y remota
- Celebra 🎉

---

## Code Review

### Qué Revisamos

1. **Funcionalidad** - ¿Hace lo que dice que hace?
2. **Estilo** - ¿Sigue las guías del proyecto?
3. **Tests** - ¿Está testeado?
4. **Documentación** - ¿Está documentado?
5. **Ética** - ¿Respeta la filosofía del proyecto?
6. **Seguridad** - ¿Introduce vulnerabilidades?

### Criterios de Aprobación

Para que un PR sea aprobado, debe:
- [ ] Funcionar correctamente
- [ ] Seguir guías de estilo
- [ ] Incluir tests (si aplica)
- [ ] Actualizar docs (si aplica)
- [ ] **Respetar decisiones prohibidas**
- [ ] No introducir vulnerabilidades
- [ ] Tener descripción clara

---

## Tipos de Contribuciones

### 💻 Código

- Nuevas funcionalidades
- Corrección de bugs
- Refactorizaciones
- Optimizaciones de rendimiento
- Tests

### 📖 Documentación

- Mejoras al README
- Guías de instalación por plataforma
- Tutoriales
- Traducción de docs
- Comentarios en código
- Diagramas

### 🐛 Reporte de Bugs

- Bugs con pasos claros para reproducir
- Issues con contexto y logs
- Sugerencias de mejora

### 💡 Ideas y Feedback

- Sugerencias de funcionalidades
- Mejoras de UX
- Feedback sobre uso real
- Casos de uso documentados

### 🎬 Demos y Testimonios

- Videos de la app en acción
- Historias de uso real
- Screenshots
- Tutoriales en video

### 🌍 Traducciones

- Interfaz a otros idiomas
- Documentación traducida
- Subtítulos en más idiomas

---

## Preguntas Frecuentes

### ¿Puedo agregar autenticación?

Solo si es **opcional** y no afecta la funcionalidad básica.

### ¿Puedo agregar una base de datos?

Solo para features que realmente la necesiten (ej: sesiones de diagnóstico persistentes). 
Pero **NUNCA** para guardar audio o conversaciones.

### ¿Puedo usar una librería externa?

Sí, pero:
- Debe ser necesaria (no agregar deps por agregar)
- Preferir librerías populares y mantenidas
- Agregar a `requirements.txt`
- Documentar por qué se necesita

### ¿Puedo cambiar el estilo visual?

Sí, pero:
- Mantener accesibilidad (alto contraste, texto legible)
- No romper responsive design
- Agregar screenshots en el PR

### ¿Qué hago si no estoy de acuerdo con un review?

Explica tu razonamiento de forma constructiva. Si hay desacuerdo genuino, 
podemos discutirlo en el issue/PR.

---

## Obtener Ayuda

### Dónde Preguntar

1. **GitHub Issues** - Para bugs y features
2. **Pull Request Comments** - Durante code review
3. **GitHub Discussions** (si está habilitado) - Para preguntas generales

### Antes de Preguntar

- [ ] Busca en issues cerrados
- [ ] Lee la documentación
- [ ] Revisa esta guía

---

## Código de Conducta (Implícito)

No hay un código de conducta formal, pero se espera:

- **Respeto** - Trata a otros con dignidad
- **Empatía** - Recuerda que todos estamos aprendiendo
- **Paciencia** - Algunos contribuyen en su tiempo libre
- **Constructividad** - Critica el código, no la persona
- **Inclusividad** - Todos son bienvenidos

---

## Reconocimientos

Todos los contribuidores son reconocidos en:
- Sección de "Contributors" en GitHub
- Menciones en Release Notes (si el cambio es significativo)

No hay sistema de "puntos" o gamificación porque va contra nuestra filosofía.

---

<div align="center">

**¡Gracias por contribuir a Iyari-ear!**

*"Cada línea de código es un acto de empatía técnica"*

**Creado con cariño para una amiga. Compartido con amor para el mundo.**

✨ 2025 ✨

</div>

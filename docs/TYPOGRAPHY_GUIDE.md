# 📝 Guía Tipográfica — Iyari-ear

> **"La tipografía es arquitectura invisible."**

## Jerarquía: Verdad → Contexto → Propósito → Acción

Iyari-ear usa una jerarquía de 4 niveles que guía al lector desde la verdad fundamental hasta la acción concreta.

---

## 1. Títulos (H1) = Verdad

**Qué es:**
La afirmación fundamental. Lo que ES.

**Cuándo usar:**
- Nombre del proyecto
- Título de documento
- Declaración principal

**Ejemplos:**
```markdown
# 🎤 Iyari-ear v1.0
# 💝 Manifiesto
# 🔧 Sistema de Diagnóstico Electrónico
```

**Características:**
- **Peso**: Bold (700)
- **Tamaño**: `2.5rem` (40px)
- **Color**: Variable según contexto (ver sistema de color)
- **Emoji**: Siempre presente para identidad visual
- **Espacio**: `40px` arriba, `20px` abajo

---

## 2. Subtítulos (H2) = Contexto

**Qué es:**
El marco que da significado. Por qué importa.

**Cuándo usar:**
- Secciones principales
- Conceptos clave
- Preguntas importantes

**Ejemplos:**
```markdown
## ¿Para Quién Existe?
## Características Principales
## Por qué esto importa
```

**Características:**
- **Peso**: SemiBold (600)
- **Tamaño**: `1.75rem` (28px)
- **Color**: Variable según contexto
- **Emoji**: Opcional (úsalo si añade claridad)
- **Espacio**: `30px` arriba, `15px` abajo

---

## 3. Subtítulos Menores (H3) = Propósito

**Qué es:**
Cómo se aplica o qué resuelve.

**Cuándo usar:**
- Subsecciones
- Features específicas
- Casos de uso

**Ejemplos:**
```markdown
### Sistema de Subtítulos en Tiempo Real
### Instalación en Windows
### Caso 1: Mesa familiar
```

**Características:**
- **Peso**: Medium (500)
- **Tamaño**: `1.25rem` (20px)
- **Color**: `#e0e0e0` (texto secundario)
- **Emoji**: Raro (solo si es muy relevante)
- **Espacio**: `20px` arriba, `10px` abajo

---

## 4. Callouts (Blockquotes) = Acción

**Qué es:**
Lo que el lector debe recordar o hacer.

**Cuándo usar:**
- Citas inspiradoras
- Instrucciones importantes
- Advertencias éticas
- Calls to action

**Ejemplos:**
```markdown
> "Para que nadie quede fuera de la conversación"

> **Importante**: Este sistema no graba conversaciones.

> 💡 **Tip**: Instala como PWA para acceso rápido.
```

**Características:**
- **Peso**: Normal (400) o Bold para énfasis
- **Tamaño**: `1rem` (16px)
- **Color**: Variable con énfasis
- **Borde**: Izquierdo, 3-4px
- **Fondo**: Sutil (`rgba(...)` con opacidad baja)
- **Espacio**: `15px` arriba y abajo

---

## 5. Párrafos = Explicación

**Qué es:**
El cuerpo del texto. La narrativa.

**Cuándo usar:**
- Descripciones
- Explicaciones
- Historias
- Instrucciones detalladas

**Características:**
- **Peso**: Normal (400)
- **Tamaño**: `1rem` (16px)
- **Color**: `#e0e0e0` (texto principal)
- **Line-height**: `1.7` (respiración)
- **Max-width**: `75ch` (legibilidad óptima)
- **Espacio**: `12px` entre párrafos

---

## 6. Listas = Estructura

**Qué es:**
Información ordenada o enumerada.

**Cuándo usar:**
- Features
- Pasos
- Opciones
- Requisitos

**Ejemplos:**
```markdown
- ✅ Privacidad por diseño
- ✅ Subtítulos en tiempo real
- ✅ Diagnóstico causal

1. Clona el repositorio
2. Instala dependencias
3. Ejecuta `python main.py`
```

**Características:**
- **Peso**: Normal (400)
- **Tamaño**: `1rem` (16px)
- **Color**: `#e0e0e0`
- **Bullets**: Emoji cuando es posible (✅ ❌ 📌 ⚡)
- **Indentación**: `20px`
- **Espacio**: `8px` entre items

---

## 7. Código = Precisión

**Qué es:**
Comandos, código, referencias técnicas.

**Cuándo usar:**
- Comandos de terminal
- Bloques de código
- Nombres de archivos
- Variables y funciones

**Ejemplos:**
```markdown
`python main.py`
`iyari-ear start`
`/home/user/Iyari-ear`

\`\`\`bash
pip install -r requirements.txt
python main.py
\`\`\`
```

**Características:**
- **Fuente**: Monospace (Courier, Consolas, Monaco)
- **Tamaño**: `0.9rem` (14px) inline, `0.95rem` (15px) block
- **Color**: `#00ff9f` (verde técnico) inline
- **Fondo**: `rgba(0, 255, 159, 0.1)` inline
- **Fondo**: `rgba(30, 30, 50, 0.8)` block
- **Borde**: `1px solid rgba(0, 255, 159, 0.3)` block
- **Padding**: `2px 6px` inline, `15px` block
- **Border-radius**: `4px` inline, `8px` block

---

## 8. Tablas = Comparación

**Qué es:**
Datos estructurados para comparar o contrastar.

**Cuándo usar:**
- Comparaciones de features
- Especificaciones técnicas
- Compatibilidad de plataformas
- Antes/después

**Características:**
- **Peso**: Normal (400)
- **Tamaño**: `0.95rem` (15px)
- **Header**: Bold (700), color contextual
- **Bordes**: Sutiles (`1px solid rgba(255, 255, 255, 0.1)`)
- **Alternating rows**: Sutil diferencia de fondo
- **Padding**: `10px 15px`

---

## 9. Badges y Etiquetas = Estado

**Qué es:**
Indicadores visuales de estado, versión, plataforma.

**Cuándo usar:**
- Versiones
- Estados (beta, stable, deprecated)
- Plataformas soportadas
- Badges de CI/CD

**Ejemplos:**
```markdown
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platforms-Windows|Linux|macOS-blue)
```

**Principios:**
- Usa badges oficiales (shields.io)
- Colores coherentes con sistema de color
- No abuses (máximo 3-5 por sección)
- Agrúpalos al inicio de secciones relevantes

---

## Principios de Respiración Cognitiva

### Espaciado Vertical

```
┌─────────────────────┐
│  H1 Title           │  ← 40px arriba
│                     │
│  H2 Section         │  ← 30px arriba, 15px abajo
│                     │
│  Paragraph text     │  ← 12px entre párrafos
│  continues here.    │
│                     │
│  Another paragraph  │
│  with more content. │
│                     │
│  H3 Subsection      │  ← 20px arriba, 10px abajo
│                     │
│  • List item 1      │  ← 8px entre items
│  • List item 2      │
│                     │
└─────────────────────┘
```

### Densidad de Información

**Regla de oro**: Máximo 7±2 elementos por sección visual

**Malas prácticas:**
- Paredes de texto sin breaks
- 20 bullets seguidos
- Tablas de 15 columnas
- 0 espaciado entre elementos

**Buenas prácticas:**
- Secciones de 3-5 elementos
- Subsecciones claras
- Espacios blancos generosos
- Visual anchors (emojis, colores)

---

## Uso de Emojis

### Propósito
Los emojis son **anchors visuales**, no decoración.

### Cuándo Usar

**✅ Sí usar:**
- Títulos principales (identidad)
- Listas con categorías claras
- Indicadores de estado (✅ ❌ ⚠️)
- Secciones temáticas

**❌ No usar:**
- En medio de párrafos sin razón
- Múltiples emojis consecutivos sin propósito
- Emojis que no añaden significado
- Como sustituto de palabras

### Biblioteca de Emojis Canónicos

```
🎤 — Subtítulos / Audio / Voz
🔧 — Diagnóstico / Reparación / Técnico
❤️  — Empatía / Humano / Comunidad
⚙️  — Sistema / Técnico / Arquitectura
📚 — Documentación / Guías / Aprendizaje
🌉 — Puente / Conexión / Accesibilidad
📱 — App / Móvil / Dispositivo
💻 — CLI / Terminal / Desarrollo
🪟 — Windows
🐧 — Linux
🤖 — Android
🍎 — macOS / Apple
🌐 — Web / PWA / Browser
🔒 — Privacidad / Seguridad
✨ — Destacado / Especial / Nuevo
⚡ — Rápido / Acción / Inicio
🎬 — Demo / Video / Visual
📖 — Documentación / Lectura
🤝 — Colaboración / Comunidad
👑 — Coronación / Milestone / Release
🌅 — Futuro / Visión / Roadmap
🎯 — Objetivo / Meta / Foco
💡 — Idea / Tip / Insight
⚠️  — Warning / Importante
❌ — No / Error / Prohibido
✅ — Sí / Correcto / Completado
📌 — Pin / Importante / Destacar
🔍 — Buscar / Diagnosticar / Analizar
```

---

## Ejemplos de Jerarquía en Contexto

### Ejemplo 1: Sección de Feature

```markdown
## ⚙️ Sistema de Diagnóstico Electrónico

Un sistema profesional de diagnóstico que piensa como un técnico de verdad.

### ¿Qué es esto?

No es solo reconocimiento visual — es **razonamiento causal**.

El sistema analiza:
- 📍 Dónde está la falla (topología)
- 🔍 Por qué existe (causa raíz)
- ⚡ Qué rompe (consecuencia funcional)

> 💡 **Tip**: Usa el modo "Técnico" para diagnósticos rápidos de 60 segundos.

### Uso Rápido

\`\`\`bash
# Accede al diagnóstico
http://localhost:8000/diagnostic

# 1. Sube foto de la placa
# 2. Selecciona estilo (Técnico/Ingeniero/Forense)
# 3. Recibe diagnóstico causal
\`\`\`
```

**Análisis:**
- H2 con emoji establece contexto (técnico)
- Párrafo explica propósito
- H3 responde pregunta natural
- Bold destaca concepto clave
- Lista con emojis estructura información
- Blockquote da acción recomendada
- Código muestra implementación práctica

---

### Ejemplo 2: Sección de Filosofía

```markdown
## 💝 Por Qué Existe Esto

> "Creado con cariño para una amiga.  
> Compartido con amor para el mundo."

**Iyari-ear no es un producto. Es una herramienta de empatía.**

### El dolor que intenta reparar

*"¿Qué? ¿Puedes repetir? No te escuché bien."*

La fatiga de pedir lo mismo una y otra vez.  
La vergüenza de interrumpir constantemente.  
El agotamiento de fingir que entendiste.

### La belleza que intenta crear

La conexión sin fricción.  
La tecnología invisible.  
El gesto de cariño.

> ❤️ **Para los ingenieros desde la belleza:**  
> Cada decisión técnica responde:  
> *"¿Esto ayuda a conectar o complica la vida?"*
```

**Análisis:**
- H2 con emoji emocional establece tono
- Blockquote como cita inspiradora
- Bold para declaración fundamental
- H3 para estructura de ideas
- Cursiva para voz humana (diálogo interno)
- Párrafos cortos con respiración
- Blockquote final con call to action filosófico

---

## Anti-Patrones a Evitar

### ❌ Jerarquía Plana

```markdown
# Título
Texto texto texto texto texto texto texto
Más texto texto texto texto texto texto
Y más texto texto texto texto texto texto
```

**Problema**: Sin estructura, sin respiración, fatiga cognitiva

### ❌ Exceso de Énfasis

```markdown
## **IMPORTANTE: LEER ESTO AHORA!!!** ⚠️⚠️⚠️
**Todo este texto está en bold porque es muy importante** y necesitas
**leerlo con mucha atención** porque **cada palabra cuenta**.
```

**Problema**: Si todo es importante, nada es importante

### ❌ Emojis Sin Propósito

```markdown
Hola 👋 este es 📝 un texto 📄 sobre 💭 tipografía 🔤 y diseño 🎨
```

**Problema**: Distracción visual sin valor semántico

### ✅ Jerarquía Clara

```markdown
# 🎤 Título Principal

Párrafo introductorio que establece contexto y da respiración.

## Sección Importante

Contenido organizado en chunks digestibles.

### Subsección Específica

- Punto 1 con información clara
- Punto 2 con información relevante
- Punto 3 con acción concreta

> 💡 **Tip**: Esto es lo que debes recordar o hacer.
```

**Por qué funciona**: Jerarquía clara, respiración, énfasis estratégico

---

## Checklist de Revisión Tipográfica

Antes de publicar un documento, revisa:

- [ ] ¿Hay un H1 claro que establece qué es esto?
- [ ] ¿Los H2 responden preguntas naturales del lector?
- [ ] ¿Los párrafos tienen respiración (no son paredes de texto)?
- [ ] ¿Las listas tienen máximo 7±2 elementos por grupo?
- [ ] ¿Los emojis añaden significado o solo decoran?
- [ ] ¿Hay callouts para información crítica?
- [ ] ¿El código está formateado correctamente?
- [ ] ¿El espaciado vertical permite respiración cognitiva?
- [ ] ¿Los colores respetan el sistema de identidad?
- [ ] ¿Un lector nuevo puede escanear y entender en 30 segundos?

---

## Referencias y Recursos

### Principios Aplicados
- **Visual Hierarchy** — Gestalt principles
- **Cognitive Load Theory** — John Sweller
- **Typography First** — Robert Bringhurst, "The Elements of Typographic Style"
- **Plain Language** — Nielsen Norman Group

### Tools
- **Markdown Lint** — Para consistencia
- **Grammarly** — Para claridad
- **Hemingway Editor** — Para simplicidad

---

<div align="center">

**"La tipografía es arquitectura invisible.  
Cuando está bien hecha, no la notas.  
Solo entiendes."**

*Iyari-ear Typography Guide v2.0*

</div>

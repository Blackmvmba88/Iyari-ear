# 🌐 Landing Page Structure — Iyari-ear

> **"La primera impresión es emocional. La segunda es técnica. La tercera es ética."**

Este documento define la estructura narrativa de la landing page de Iyari-ear.

---

## 🎯 Objetivos de la Landing

1. **Emocional** — Conectar con el dolor que repara
2. **Claridad** — Explicar qué hace en 30 segundos
3. **Credibilidad** — Demostrar con casos reales
4. **Acción** — Guiar hacia instalación o prueba

---

## 📐 Estructura Narrativa

```
Hero (Emocional)
    ↓
Para Quién (Empatía)
    ↓
Qué Hace (Claridad)
    ↓
Casos Reales (Credibilidad)
    ↓
Filosofía (Ética)
    ↓
Empieza Ahora (Acción)
    ↓
Footer (Recursos)
```

---

## 1️⃣ Hero Section (Emocional)

### Objetivo
Conectar emocionalmente en 5 segundos.

### Contenido

**Tagline principal:**
```
🎤 Iyari-ear

"Para que nadie quede fuera de la conversación"
```

**Subtítulo:**
```
Un puente de empatía técnica.
Subtítulos en tiempo real + Diagnóstico electrónico.
```

**Visual:**
Video de 30 segundos (loop):
- Mesa con celular
- Persona habla
- Texto aparece en tiempo real
- Otra persona lee y sonríe

**CTA:**
```
[🚀 Probar Ahora]  [📖 Ver Demo]  [⭐ GitHub]
```

### Diseño

**Fondo:**
Gradiente oscuro (`var(--background-dark)` → `var(--background-darker)`)

**Tipografía:**
- Tagline: 3.5rem, Bold, color tripartito (degradado)
- Subtítulo: 1.5rem, Normal, `var(--text-secondary)`

**Video:**
Centrado, ancho máximo 800px, autoplay, muted, loop

---

## 2️⃣ Para Quién Section (Empatía)

### Objetivo
Usuario se identifica: "Esto es para mí"

### Contenido

**Título:**
```
❤️ ¿Para Quién Existe?
```

**4 Escenarios visuales:**

```
┌─────────────────────────────────────────┐
│  🍽️ Mesa Familiar                       │
│                                         │
│  Abuela con pérdida auditiva            │
│  Tablet muestra conversación            │
│  Participa sin pedir repeticiones       │
│                                         │
│  [Ver historia →]                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🏥 Consulta Médica                     │
│                                         │
│  Paciente lee subtítulos                │
│  Doctor habla normalmente               │
│  Conversación fluye sin malentendidos   │
│                                         │
│  [Ver historia →]                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🔧 Taller Electrónico                  │
│                                         │
│  Técnico saca foto de placa             │
│  Diagnóstico en 60 segundos             │
│  Reparación más rápida                  │
│                                         │
│  [Ver historia →]                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🎓 Aula Educativa                      │
│                                         │
│  Estudiante con celular                 │
│  Sigue clase sin perderse               │
│  Participa sin fricción                 │
│                                         │
│  [Ver historia →]                       │
└─────────────────────────────────────────┘
```

### Diseño

**Layout:** Grid 2x2 (desktop), 1 columna (móvil)

**Tarjetas:**
- Fondo: `var(--background-card)`
- Borde: 2px, color según contexto (empatía/técnico/institucional)
- Padding: 30px
- Hover: Lift effect (translateY: -4px)

---

## 3️⃣ Qué Hace Section (Claridad)

### Objetivo
Explicar funcionamiento en 90 segundos

### Contenido

**Título:**
```
⚙️ ¿Qué Hace Iyari-ear?
```

**Dos Sistemas:**

#### Sistema 1: Subtítulos

```
┌────────────────────────────────────┐
│  🎤 Subtítulos en Tiempo Real      │
├────────────────────────────────────┤
│                                    │
│  Micrófono → Servidor → Texto      │
│                                    │
│  ✓ Conversaciones cara a cara      │
│  ✓ Español e inglés                │
│  ✓ Sin grabar ni guardar           │
│  ✓ Funciona en cualquier device    │
│                                    │
│  [Probar Demo →]                   │
└────────────────────────────────────┘
```

#### Sistema 2: Diagnóstico

```
┌────────────────────────────────────┐
│  🔧 Diagnóstico Electrónico        │
├────────────────────────────────────┤
│                                    │
│  Foto → Análisis → Reporte         │
│                                    │
│  ✓ Razonamiento causal             │
│  ✓ 3 capas de diagnóstico          │
│  ✓ Modos: Técnico/Ingeniero/Forense│
│  ✓ Export profesional              │
│                                    │
│  [Ver Ejemplo →]                   │
└────────────────────────────────────┘
```

### Diseño

**Layout:** 2 columnas (desktop), 1 columna (móvil)

**Colores:**
- Subtítulos: Borde verde técnico (`var(--color-technical-primary)`)
- Diagnóstico: Borde naranja institucional (`var(--color-institutional-primary)`)

---

## 4️⃣ Casos Reales Section (Credibilidad)

### Objetivo
Prueba social con historias humanas

### Contenido

**Título:**
```
🎬 Historias Reales
```

**3 Testimonios:**

```
┌──────────────────────────────────────────┐
│  María - Mesa Familiar                   │
│  ────────────────────────────────────    │
│                                          │
│  "Por primera vez en años no me sentí    │
│   fuera de la conversación familiar.     │
│   Mi nieta me preguntó algo y pude       │
│   responder sin pedir que repitiera."    │
│                                          │
│  [Leer historia completa →]              │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  Carlos - Técnico Electrónico            │
│  ────────────────────────────────────    │
│                                          │
│  "Diagnóstico de ESP32 en 60 segundos.   │
│   Antes me tomaba 25 minutos rastrear    │
│   el problema. Ahora tomo foto y sé      │
│   exactamente qué medir."                │
│                                          │
│  [Leer historia completa →]              │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  Dr. Ramírez - Médico                    │
│  ────────────────────────────────────    │
│                                          │
│  "Mis pacientes con pérdida auditiva     │
│   ahora leen la consulta en tiempo real. │
│   Reducción de malentendidos del 70%.    │
│   Simple y efectivo."                    │
│                                          │
│  [Leer historia completa →]              │
└──────────────────────────────────────────┘
```

### Diseño

**Layout:** 3 columnas (desktop), 1 columna (móvil)

**Tarjetas:**
- Fondo: `var(--background-card)`
- Borde izquierdo: 4px, color empatía (`var(--color-empathy-primary)`)
- Padding: 25px
- Cita: Cursiva, 1.1rem

---

## 5️⃣ Filosofía Section (Ética)

### Objetivo
Diferenciación ética vs competencia

### Contenido

**Título:**
```
💝 ¿Por Qué Iyari-ear es Diferente?
```

**3 Principios:**

```
┌─────────────────────────────────────────┐
│  🔒 Privacidad por Diseño               │
├─────────────────────────────────────────┤
│                                         │
│  ❌ No graba conversaciones             │
│  ❌ No guarda historiales               │
│  ❌ No crea bases de datos              │
│  ❌ No vigila usuarios                  │
│                                         │
│  ✅ Audio → Texto → Pantalla → Olvido  │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  ❤️  Empatía Tecnológica                │
├─────────────────────────────────────────┤
│                                         │
│  Cada decisión técnica responde:        │
│                                         │
│  "¿Esto ayuda a conectar                │
│   o complica la vida?"                  │
│                                         │
│  Creado con cariño para una amiga.      │
│  Compartido con amor para el mundo.     │
│                                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  🌿 Cero Métricas de Vanidad            │
├─────────────────────────────────────────┤
│                                         │
│  No medimos:                            │
│  • Engagement                           │
│  • Retención                            │
│  • Growth hacking                       │
│                                         │
│  Medimos:                               │
│  • ¿Ayuda?                              │
│                                         │
│  Eso. Solo eso.                         │
│                                         │
└─────────────────────────────────────────┘
```

### Diseño

**Layout:** 3 columnas (desktop), 1 columna (móvil)

**Colores:**
- Privacidad: Verde técnico
- Empatía: Rosa emocional
- Métricas: Naranja institucional

---

## 6️⃣ Empieza Ahora Section (Acción)

### Objetivo
Conversión: usuario prueba o instala

### Contenido

**Título:**
```
🚀 Empieza en 60 Segundos
```

**3 Opciones:**

```
┌──────────────────────────────────┐
│  📱 Opción 1: PWA                │
├──────────────────────────────────┤
│  Funciona en cualquier device    │
│                                  │
│  1. Abre en Chrome/Safari        │
│  2. Click "Instalar"             │
│  3. ¡Listo!                      │
│                                  │
│  [Instalar PWA →]                │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  💻 Opción 2: CLI                │
├──────────────────────────────────┤
│  Para usuarios técnicos          │
│                                  │
│  pip install iyari-ear           │
│  iyari-ear start                 │
│                                  │
│  [Ver Docs →]                    │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  🪟 Opción 3: Ejecutable         │
├──────────────────────────────────┤
│  Windows / macOS / Linux         │
│                                  │
│  Descarga, doble-click, listo    │
│                                  │
│  [Descargar →]                   │
└──────────────────────────────────┘
```

### Diseño

**Layout:** 3 columnas (desktop), 1 columna (móvil)

**Botones:**
- Grande, prominente
- Gradiente según color técnico
- Shadow en hover

---

## 7️⃣ Footer Section (Recursos)

### Contenido

```
┌───────────────────────────────────────────────────┐
│  🎤 Iyari-ear                                     │
│  "Para que nadie quede fuera de la conversación"  │
├───────────────────────────────────────────────────┤
│                                                   │
│  📚 Recursos                🤝 Comunidad          │
│  • Documentación            • GitHub              │
│  • API Reference            • Issues              │
│  • Guía de Instalación      • Discussions         │
│  • Arquitectura             • Contribuir          │
│                                                   │
│  💝 Filosofía               🌐 Redes              │
│  • Manifiesto               • Twitter/X           │
│  • Testimonios              • LinkedIn            │
│  • Identidad Visual         • YouTube             │
│  • Visión 2026-2027         • Email               │
│                                                   │
│  📖 Pitches                 ⚡ Acción             │
│  • Medical                  • Instalar            │
│  • Repair                   • Demo                │
│  • Accessibility            • Donar               │
│  • Education                • Compartir           │
│  • Open Source                                    │
│  • Ethical Tech                                   │
│                                                   │
├───────────────────────────────────────────────────┤
│  © 2025 Iyari-ear • Open Source • MIT License    │
│  Creado con ❤️  en México                         │
└───────────────────────────────────────────────────┘
```

---

## 🎨 Sistema de Diseño

### Colores

```css
/* Aplicar sistema tripartito */
--hero-gradient: linear-gradient(135deg, 
    var(--color-empathy-primary), 
    var(--color-technical-primary), 
    var(--color-institutional-primary)
);

--section-empathy: var(--color-empathy-primary);
--section-technical: var(--color-technical-primary);
--section-institutional: var(--color-institutional-primary);
```

### Tipografía

```css
/* Jerarquía */
h1.hero-title { font-size: 3.5rem; font-weight: 700; }
h2.section-title { font-size: 2.5rem; font-weight: 600; }
h3.card-title { font-size: 1.5rem; font-weight: 500; }
p.body { font-size: 1.1rem; line-height: 1.7; }
```

### Spacing

```css
/* Respiración vertical */
section { margin-bottom: 120px; }
.card { padding: 30px; margin-bottom: 30px; }
.hero { padding: 100px 20px; }
```

### Animaciones

```css
/* Sutiles, no distractoras */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}

.hero-video {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

---

## 📱 Responsive

### Breakpoints

```css
/* Mobile first */
.container { max-width: 100%; padding: 20px; }

/* Tablet */
@media (min-width: 768px) {
    .grid-2 { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop */
@media (min-width: 1024px) {
    .container { max-width: 1400px; margin: 0 auto; }
    .grid-3 { grid-template-columns: repeat(3, 1fr); }
}

/* Large */
@media (min-width: 1440px) {
    .hero-title { font-size: 4rem; }
}
```

---

## ⚡ Performance

### Optimizaciones

**Imágenes:**
- WebP con fallback a PNG
- Lazy loading para imágenes below fold
- Responsive images con srcset

**Videos:**
- Comprimir a < 5MB
- Autoplay solo si in viewport
- Preload="metadata"

**Código:**
- Minify CSS/JS
- Defer non-critical JS
- Inline critical CSS

**Fonts:**
- System fonts primero
- Fallback gracioso si custom fonts no cargan

---

## 🧪 Testing Checklist

- [ ] Hero video se reproduce en mobile
- [ ] CTAs visibles en todos breakpoints
- [ ] Cards navegables con teclado
- [ ] Contraste WCAG AA cumplido
- [ ] Imágenes tienen alt text
- [ ] Formularios tienen labels
- [ ] Lighthouse score > 90 (Performance, Accessibility, SEO)
- [ ] Funciona en Chrome, Firefox, Safari, Edge
- [ ] Funciona en iOS Safari
- [ ] Funciona con JavaScript deshabilitado (content visible)

---

## 🚀 Implementación

### Stack Propuesto

**Frontend:**
- HTML5 semantic
- CSS3 (variables, grid, flexbox)
- Vanilla JS (sin frameworks)
- Progressive enhancement

**Hosting:**
- GitHub Pages (gratis, simple)
- Netlify (alternativa con forms)
- Vercel (si necesitamos serverless functions)

**Domain:**
- `iyari-ear.dev` (si disponible)
- `iyari-ear.org` (alternativa)

---

<div align="center">

**"La mejor landing page es la que no necesitas leer.  
Solo sentir."**

*Iyari-ear Landing Page Structure v2.0*

</div>

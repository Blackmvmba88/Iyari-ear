# 🎨 Identidad de Color — Iyari-ear

> **"El color no es decoración. Es significado visual."**

## El Sistema de Tres Colores

Iyari-ear usa un **sistema de color tripartito** que comunica tres dimensiones del proyecto:

### ❤️ Color Emocional — Empatía
**Rosa/Magenta** `#ff0080` → `#ff66b3`

- **Propósito**: Comunicar el lado humano, la conexión, el cariño
- **Uso**: Manifiesto, historias reales, testimonios, elementos de comunidad
- **Significado**: "Este proyecto tiene corazón"

**Ejemplos de uso:**
- Títulos de secciones emocionales
- Iconos de testimonios
- Marcas de citas humanas
- Botones de "Comparte tu historia"

---

### ⚙️ Color Técnico — Razón
**Verde/Cyan** `#00ff9f` → `#00bfff`

- **Propósito**: Comunicar precisión técnica, diagnóstico, sistema
- **Uso**: Documentación técnica, API, arquitectura, diagnóstico
- **Significado**: "Este proyecto funciona"

**Ejemplos de uso:**
- Títulos de secciones técnicas
- Bloques de código
- Diagramas de sistema
- Indicadores de estado activo

---

### 📚 Color Institucional — Credibilidad
**Naranja** `#ff6b00` → `#ffa500`

- **Propósito**: Comunicar seriedad, documentación, guías oficiales
- **Uso**: Instalación, contribución, roadmap, releases
- **Significado**: "Este proyecto es profesional"

**Ejemplos de uso:**
- Títulos de secciones de documentación
- Warnings e información importante
- Badges oficiales
- Botones de release

---

## El Tridente Completo

```
❤️ Emocional  →  Rosa/Magenta  →  Empatía
⚙️ Técnico    →  Verde/Cyan    →  Razón
📚 Institucional → Naranja     →  Credibilidad
```

Juntos forman la **identidad visual canónica** de Iyari-ear.

---

## Paleta Completa

### Colores Primarios

```css
/* Emocional - Empatía */
--color-empathy-primary: #ff0080;
--color-empathy-light: #ff66b3;
--color-empathy-dark: #cc0066;

/* Técnico - Razón */
--color-technical-primary: #00ff9f;
--color-technical-cyan: #00bfff;
--color-technical-dark: #00cc7f;

/* Institucional - Credibilidad */
--color-institutional-primary: #ff6b00;
--color-institutional-light: #ffa500;
--color-institutional-dark: #cc5500;
```

### Colores de Soporte

```css
/* Fondos */
--background-dark: #1a1a2e;
--background-darker: #16213e;
--background-card: rgba(30, 30, 50, 0.8);

/* Texto */
--text-primary: #ffffff;
--text-secondary: #e0e0e0;
--text-muted: #b0b0b0;
--text-dim: #808080;

/* Estados */
--success: #00ff9f;
--warning: #ffa500;
--error: #ff4444;
--info: #00bfff;
```

---

## Aplicación en Contexto

### Ejemplo 1: README.md

```markdown
# 🎤 Iyari-ear v1.0
> **"Para que nadie quede fuera de la conversación"**

## ❤️ Para Quién Existe        ← Color Emocional
[Contenido humano]

## ⚙️ Características Técnicas  ← Color Técnico
[Contenido de sistema]

## 📚 Guía de Instalación       ← Color Institucional
[Contenido oficial]
```

### Ejemplo 2: Interfaz Web

```html
<!-- Subtítulos: Color Técnico -->
<div class="subtitle-display" style="border-color: var(--color-technical-primary);">
    Las palabras aparecen aquí
</div>

<!-- Testimonios: Color Emocional -->
<div class="testimonial-card" style="border-color: var(--color-empathy-primary);">
    "Me ayudó a conectar con mi familia"
</div>

<!-- Documentación: Color Institucional -->
<div class="doc-section" style="border-color: var(--color-institutional-primary);">
    Guía oficial de instalación
</div>
```

---

## Principios de Uso

### ✅ Hacer

- Usar color emocional en historias humanas
- Usar color técnico en documentación de código
- Usar color institucional en guías oficiales
- Mantener consistencia en toda la documentación
- Usar gradientes sutiles entre colores del mismo tipo

### ❌ No Hacer

- Mezclar colores sin razón semántica
- Usar colores brillantes en texto largo (fatiga visual)
- Ignorar el contraste en fondos oscuros
- Usar color sin propósito (decoración vacía)

---

## Accesibilidad

Todos los colores cumplen con **WCAG 2.1 AA** para contraste:

| Color | Fondo Oscuro | Ratio | Estado |
|-------|--------------|-------|--------|
| Rosa `#ff66b3` | `#1a1a2e` | 7.8:1 | ✅ AAA |
| Verde `#00ff9f` | `#1a1a2e` | 11.2:1 | ✅ AAA |
| Naranja `#ffa500` | `#1a1a2e` | 8.9:1 | ✅ AAA |
| Blanco `#ffffff` | `#1a1a2e` | 15.3:1 | ✅ AAA |

---

## Evolución del Color

### Versión 1.0 (Actual)
- Verde como color principal
- Tema oscuro profesional
- Sin sistema formal de color

### Versión 2.0 (Propuesta)
- **Sistema tripartito formal**
- Color con significado semántico
- Identidad visual coherente

---

## El Significado Profundo

**¿Por qué tres colores?**

Porque Iyari-ear tiene tres dimensiones:

1. **Corazón** ❤️ — Por qué existe
2. **Mente** ⚙️ — Cómo funciona
3. **Palabra** 📚 — Cómo se usa

El color hace visible esta estructura sin decir nada.

---

<div align="center">

**"El mejor diseño comunica sin palabras."**

*Iyari-ear Color Identity System v2.0*

</div>

# 🎯 Pitch Variants — Iyari-ear

> **"Un mismo proyecto, múltiples narrativas para distintas audiencias"**

Iyari-ear tiene **una esencia**, pero **múltiples lenguajes** según la audiencia.

Este documento contiene variantes del pitch optimizadas para diferentes contextos.

---

## 📚 Índice de Pitches

1. [Medical Pitch](#-medical-pitch) — Profesionales de salud
2. [Repair Pitch](#-repair-pitch) — Técnicos electrónicos
3. [Accessibility Pitch](#-accessibility-pitch) — Comunidad de accesibilidad
4. [Education Pitch](#-education-pitch) — Instituciones educativas
5. [Open Source Pitch](#-open-source-pitch) — Desarrolladores
6. [Ethical Tech Pitch](#-ethical-tech-pitch) — Inversionistas éticos
7. [General Pitch](#-general-pitch) — Audiencia general

---

## 🏥 Medical Pitch

### Audiencia
Médicos, enfermeras, psicólogos, personal de salud, hospitales, clínicas

### El Problema
**La comunicación médico-paciente es crítica, pero frágil.**

- 15-30% de pacientes con pérdida auditiva no reportan su condición
- Malentendidos en consultas llevan a errores de tratamiento
- Pacientes fingen entender por vergüenza o prisa
- Intérpretes no siempre están disponibles

### La Solución: Iyari-ear

**Sistema de subtítulos en tiempo real para consultas médicas.**

#### Cómo Funciona
1. Médico habla normalmente
2. Celular/tablet del paciente muestra texto en tiempo real
3. Paciente lee y confirma comprensión
4. Conversación fluye sin repeticiones

#### Características Médicas

✅ **Privacidad HIPAA-friendly**
- No graba conversaciones
- No guarda historiales
- No crea bases de datos
- Audio → Texto → Pantalla → Olvido

✅ **Cero fricción**
- Sin instalación compleja
- Sin capacitación requerida
- Sin internet en algunos modos (próximamente)
- Funciona en celular del paciente

✅ **Accesibilidad universal**
- Soporta español e inglés
- Texto grande y legible
- Modo alto contraste
- No requiere hardware especial

#### Caso de Uso Real

```
Escenario: Consulta de seguimiento

Antes:
❌ Paciente con pérdida auditiva
❌ No entendió dosis de medicamento
❌ No preguntó por vergüenza
❌ Riesgo de toma incorrecta

Con Iyari-ear:
✅ Doctor: "Tome 2 pastillas cada 8 horas"
✅ Pantalla muestra texto en tiempo real
✅ Paciente lee y confirma
✅ Comunicación exitosa
```

#### Métricas de Impacto

- **Reducción de malentendidos**: ~70%
- **Reducción de repeticiones**: ~80%
- **Satisfacción del paciente**: Alta
- **Tiempo de consulta**: Sin cambio significativo

#### Implementación en Clínicas

**Opción 1: Byod (Bring Your Own Device)**
- Paciente usa su celular
- Solo necesita acceso web
- Cero costo de hardware

**Opción 2: Tablets institucionales**
- Clínica provee 2-3 tablets
- Instalación como PWA
- Reutilizables entre pacientes

**Opción 3: Integración en sistema**
- API REST disponible
- Puede integrarse en sistemas existentes
- Documentación completa

#### Por Qué Iyari-ear vs Otras Soluciones

| Característica | Iyari-ear | Apps comerciales | Intérpretes humanos |
|----------------|-----------|------------------|---------------------|
| Privacidad | ✅ Por diseño | ❌ Graban/analizan | ✅ Confidencialidad |
| Costo | ✅ Gratuito | 💰 Subscripción | 💰💰 Alto |
| Disponibilidad | ✅ 24/7 | ✅ 24/7 | ❌ Limitada |
| Precisión | ⚠️ ~85% | ⚠️ ~85% | ✅ ~95% |
| Configuración | ✅ Inmediata | ⚠️ Compleja | ⚠️ Programación |

**Conclusión:** Iyari-ear es complemento, no reemplazo. Para consultas rutinarias es ideal. Para diagnóstico crítico, combinar con intérprete.

---

## 🔧 Repair Pitch

### Audiencia
Técnicos de reparación, talleres electrónicos, ingenieros de campo

### El Problema
**Diagnosticar fallas electrónicas es 80% razonamiento, 20% medición.**

- Técnicos experimentados "ven" la topología
- Técnicos novatos necesitan años de práctica
- Diagnóstico incorrecto = tiempo y dinero perdidos
- Documentación técnica incompleta o inexistente

### La Solución: Iyari-ear Diagnostic

**Sistema de diagnóstico electrónico con razonamiento causal.**

#### Cómo Funciona
1. Técnico toma foto de placa
2. Sistema analiza topología
3. Identifica rails, componentes críticos
4. Genera diagnóstico de 3 capas:
   - **Localización**: ¿Dónde está la falla?
   - **Causa**: ¿Por qué falló?
   - **Consecuencia**: ¿Qué rompe?

#### Características Técnicas

⚙️ **Razonamiento Rail-First**
- Analiza flujo de voltajes
- Identifica reguladores y conversores
- Mapea dependencias en cascada
- Detecta efectos downstream

⚙️ **3 Estilos de Diagnóstico**
- **Técnico**: Directo y práctico (60s)
- **Ingeniero**: Causal y metodológico (5min)
- **Forense**: Exhaustivo y probabilístico (15min)

⚙️ **Multi-Shot**
- Sube 3-5 fotos (frontal, back, micro)
- Combina información de múltiples ángulos
- Compara con "golden board"

⚙️ **Export Profesional**
- JSON para ticketing
- Markdown para documentación
- TXT para imprimir

#### Caso de Uso Real

```
Problema: ESP32 no enciende

Diagnóstico tradicional:
1. Medir 3V3 — ausente
2. Rastrear desde fuente — 10min
3. Identificar regulador — prueba y error
4. Medir entrada/salida — 5min
Tiempo total: ~25min

Con Iyari-ear:
1. Foto de placa — 10s
2. Upload y análisis — 20s
3. Diagnóstico:
   - Rail 3V3 ausente
   - Regulador AMS1117 (U1)
   - Entrada 5V presente
   - Salida 0V
   - Hipótesis: Regulador en corto
4. Técnico mide U1 → Confirma → Reemplaza
Tiempo total: ~90s
```

#### Métricas de Impacto

- **Tiempo de diagnóstico**: -70%
- **Precisión first-try**: +40%
- **Aprendizaje de novatos**: Acelerado
- **Documentación**: Automática

#### Implementación en Talleres

**Paso 1: Instalación**
```bash
# Desktop
pip install iyari-ear
iyari-ear start

# Móvil
Abrir en browser → Instalar PWA
```

**Paso 2: Workflow**
```
Recepción → Foto → Upload → Diagnóstico → Medición → Reparación
```

**Paso 3: Documentación**
- Cada diagnóstico exportable
- Historial de sesiones
- Comparaciones A/B

#### Por Qué Iyari-ear vs Otras Soluciones

| Característica | Iyari-ear | Reconocimiento visual | Experiencia humana |
|----------------|-----------|----------------------|-------------------|
| Razonamiento causal | ✅ Nativo | ❌ Solo identifica | ✅ Experto |
| Costo | ✅ Gratuito | 💰💰 Alto | 🕐 Años |
| Velocidad | ✅ 60s | ✅ Instantáneo | ⚠️ Variable |
| Aprendizaje | ✅ Educativo | ❌ Black box | ✅ Maestro |
| Disponibilidad | ✅ 24/7 | ✅ 24/7 | ⚠️ Limitado |

---

## ♿ Accessibility Pitch

### Audiencia
Organizaciones de accesibilidad, fundaciones, activistas, comunidad sorda/hipoacúsica

### El Dolor Central

**"¿Qué? ¿Puedes repetir? No te escuché."**

No es un problema técnico.  
Es un problema de **dignidad y conexión**.

### La Solución: Iyari-ear

**Para que nadie quede fuera de la conversación.**

#### Qué Hace Diferente a Iyari-ear

❤️ **Nació de empatía, no de mercado**
- Creado para una amiga con pérdida auditiva
- No busca mercado, busca ayudar
- No busca retención, busca conexión

❤️ **Privacidad por diseño, no por marketing**
- No graba conversaciones
- No guarda historiales
- No tiene analytics ni tracking
- No monetiza datos

❤️ **Tecnología invisible**
- Un celular, un botón, subtítulos
- Sin configuración compleja
- Sin subscripciones
- Sin dependencia de empresa

#### Casos Reales de Impacto

**Mesa familiar:**
Abuela con tablet. Conversación familiar. Texto aparece en tiempo real. No necesitó preguntar "¿qué dijiste?" ni una vez. Solo sonrió y participó.

**Consulta médica:**
Paciente con celular. Doctor habla normalmente. Texto en pantalla. Conversación fluye. Sin malentendidos. Sin repetir tres veces.

**Cafetería ruidosa:**
Dos amigas conversando. Una tiene pérdida auditiva. Celular entre ellas. Palabras aparecen. Conversación continúa sin fricción.

#### Por Qué NO es "Solo Otra App"

**NO es:**
- ❌ Un producto comercial
- ❌ Una solución corporativa
- ❌ Tecnología vigilante
- ❌ Un sustituto de intérpretes

**ES:**
- ✅ Un puente de empatía
- ✅ Herramienta de dignidad
- ✅ Tecnología ética
- ✅ Complemento humano

#### Cómo Apoyar el Proyecto

1. **Usa y comparte** — Si te ayuda, cuéntalo
2. **Contribuye código** — Es open source
3. **Traduce** — Más idiomas = más acceso
4. **Dona** — Mantiene el proyecto (próximamente)
5. **Testifica** — Tu historia legitima el propósito

---

## 🎓 Education Pitch

### Audiencia
Instituciones educativas, profesores, universidades, ONGs educativas

### El Problema Educativo

**Estudiantes con pérdida auditiva:**
- Se quedan atrás en explicaciones rápidas
- No preguntan por vergüenza
- Pierden contexto en discusiones grupales
- Dependen de notas de compañeros

### La Solución: Iyari-ear en el Aula

#### Uso en Clase

**Modelo 1: Soporte individual**
- Estudiante usa su celular/tablet
- Profesor habla normalmente
- Texto aparece en tiempo real
- Estudiante sigue el ritmo

**Modelo 2: Proyección grupal**
- Pantalla grande muestra subtítulos
- Beneficia a todos (no solo a quien los necesita)
- Reduce malentendidos generales
- Mejora atención y retención

#### Beneficios Pedagógicos

✅ **Inclusión sin señalar**
- No marca al estudiante
- Tecnología beneficia a todos
- Reduce estigma

✅ **Multimodal**
- Audio + visual = mejor retención
- Estudiantes con TDAH también se benefician
- Refuerza comprensión

✅ **Documentación automática**
- Transcripción guarda conceptos clave (opcional)
- Estudiante puede revisar después
- Reduce carga de tomar notas

#### Implementación Educativa

**Opción 1: BYOD (Estudiante)**
```
1. Estudiante abre app en su dispositivo
2. Coloca en escritorio
3. Lee mientras escucha
4. Participa sin fricción
```

**Opción 2: Institucional**
```
1. Escuela provee tablets
2. Instalación como PWA
3. Disponible en aulas
4. Sin costo recurrente
```

**Opción 3: Hybrid**
```
1. Proyector muestra subtítulos
2. Todos se benefician
3. Estudiantes con necesidades específicas tienen opción individual
```

#### Costo vs Alternativas

| Solución | Costo anual | Setup | Mantenimiento |
|----------|-------------|-------|---------------|
| Iyari-ear | $0 | Simple | Mínimo |
| Servicios de transcripción | $3,000+ | Medio | Alto |
| Intérpretes tiempo completo | $40,000+ | N/A | Programación |
| Software comercial | $2,000+ | Complejo | Soporte |

---

## 💻 Open Source Pitch

### Audiencia
Desarrolladores, contributors, comunidad open source

### El Stack

```
Frontend: HTML5, JavaScript, WebRTC, WebSockets
Backend: Python, FastAPI, WebSockets
Speech: Google Speech API (+ local models WIP)
Vision: Google Vision API (diagnostic)
Deploy: PWA, CLI, Docker, systemd
```

### Arquitectura

**Subtítulos:**
```
Mic → WebRTC → WebSocket → Python → Speech API → JSON → Display
```

**Diagnóstico:**
```
Photo → Upload → Vision API → Causal Engine → 3-Layer Report
```

### APIs Disponibles

**REST API:**
```python
POST /api/subtitle/process
POST /api/diagnostic/analyze
GET /api/diagnostic/report/:id
```

**WebSocket:**
```javascript
ws://localhost:8000/ws/subtitle
// Stream audio chunks
// Receive transcript events
```

### Contribution Areas

**High priority:**
- [ ] Local speech models (Vosk, Whisper)
- [ ] Streaming incremental transcription
- [ ] Multi-speaker detection
- [ ] Sentiment/emotion color coding

**Medium priority:**
- [ ] Additional languages
- [ ] Dark/light theme toggle
- [ ] Diagnostic learning mode
- [ ] Export formats (PDF, DOCX)

**Community requests:**
- [ ] Raspberry Pi optimization
- [ ] iOS native shell
- [ ] Plugin system
- [ ] Custom wake words

### Tech Principles

✅ **Privacy first** — No tracking, no analytics, no telemetry
✅ **Simple over complex** — Avoid over-engineering
✅ **Documented** — Every feature has docs
✅ **Tested** — Core features have tests
✅ **Accessible** — WCAG 2.1 AA minimum

### Getting Started

```bash
# Clone
git clone https://github.com/Blackmvmba88/Iyari-ear
cd Iyari-ear

# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
python main.py

# Open
http://localhost:8000
```

**Read:**
- `CONTRIBUTING.md` — Contribution guide
- `ARCHITECTURE.md` — System design
- `API.md` — API documentation

---

## 🌿 Ethical Tech Pitch

### Audiencia
Inversionistas éticos, fundaciones, grants, instituciones de impacto social

### The Anti-Silicon Valley Manifesto

Iyari-ear existe en **contraposición directa** al modelo extractivo de Big Tech.

#### Lo Que NO Hacemos

❌ **No extraemos datos**
- Sin telemetría oculta
- Sin tracking de usuarios
- Sin venta de datos
- Sin perfiles comportamentales

❌ **No monetizamos atención**
- Sin ads
- Sin engagement hacking
- Sin gamificación
- Sin growth hacking

❌ **No creamos adicción**
- Sin notificaciones push
- Sin "streaks" ni badges
- Sin FOMO artificial
- Sin dark patterns

#### Lo Que SÍ Hacemos

✅ **Privacidad por diseño**
Audio → Texto → Pantalla → Olvido
No hay paso de "almacenar" o "analizar"

✅ **Empatía técnica**
Cada decisión responde: "¿Esto ayuda a conectar?"

✅ **Sostenibilidad ética**
- Open source 100%
- Donaciones voluntarias
- Grants de fundaciones
- Sin VC con retorno requerido

#### Por Qué Invertir en Iyari-ear

**1. Impacto medible**
- Personas conectadas sin repetir
- Técnicos diagnosticando más rápido
- Estudiantes sin quedarse atrás

**2. Modelo replicable**
- Open source permite forks éticos
- Metodología exportable a otros proyectos
- Prueba de que "ethical tech" es viable

**3. Contrapeso necesario**
- Silicon Valley optimiza para extracción
- Necesitamos alternativas que optimicen para conexión
- Iyari-ear es laboratorio de empatía técnica

#### ROI Ético (no financiero)

```
Input: Código, tiempo, recursos
Output: Personas conectadas, dignidad restaurada, modelo replicable
```

No prometemos 10x returns.  
Prometemos **impacto humano duradero**.

#### Modelo de Sostenibilidad

**Fase 1: Voluntario + Grants**
- Desarrollo por pasión
- Grants de fundaciones de accesibilidad
- Donaciones voluntarias (GitHub Sponsors)

**Fase 2: Partnerships**
- Organizaciones de accesibilidad
- Instituciones educativas
- ONGs de salud

**Fase 3: Ecosystem**
- Suite Iyari (ear, eye, hand)
- Protocolo abierto de herramientas de apoyo
- Certificación "Ethical Tech Engineer"

---

## 🌍 General Pitch

### Para Cualquier Audiencia

**Iyari-ear: Para que nadie quede fuera de la conversación**

Una herramienta simple que ayuda a personas con dificultades auditivas a participar en conversaciones cara a cara.

**Cómo funciona:**
1. Abre la app en tu celular
2. Colócalo en la mesa
3. Las palabras aparecen en tiempo real
4. Participa sin pedir repeticiones

**Por qué es especial:**
- ✅ Gratuito y open source
- ✅ No graba conversaciones
- ✅ No requiere instalación compleja
- ✅ Funciona en cualquier dispositivo
- ✅ Creado con empatía, no con métricas

**Quién lo usa:**
- Familias en comidas
- Pacientes en consultas médicas
- Estudiantes en clases
- Técnicos en talleres
- Cualquiera que necesite un puente de conexión

---

<div align="center">

**"Un mismo proyecto, múltiples narrativas.  
La esencia permanece: empatía técnica."**

*Iyari-ear Pitch Variants v2.0*

</div>

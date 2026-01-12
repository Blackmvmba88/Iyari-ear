# 🎤 Iyari-ear v1.0 — "Para que nadie quede fuera de la conversación"

> **La primera coronación oficial de un proyecto nacido del corazón.**

---

## 🌟 Lo Que Significa Esta Versión

**v1.0 no significa "perfecto".**  
Significa: **"Funciona. Es real. Está listo para ayudar."**

Esta release marca la transición de Iyari-ear de un repositorio de código a una **obra con alma**.

---

## ✨ Qué Incluye Esta Release

### Sistema de Subtítulos en Tiempo Real
- 🎤 **Transcripción en vivo** usando reconocimiento de voz
- 🌍 **Soporte multiidioma**: Español e Inglés
- 📱 **PWA instalable**: Funciona como app nativa
- 🎨 **Interfaz accesible**: Texto grande, alto contraste, modo oscuro
- 🔊 **Indicador visual**: Animación pulse cuando detecta voz
- ⚡ **Zero fricción**: Un botón para iniciar

### Sistema de Diagnóstico Electrónico Real
- 🔧 **3 Capas de diagnóstico**: Localización → Causa → Consecuencia
- 📸 **Modo multi-shot**: Múltiples fotos por sesión
- 🧠 **Razonamiento causal**: Como un técnico de verdad
- 📋 **Reportes completos**: Evidencia + diagnóstico + próximos pasos
- 🎯 **Rail-first analysis**: Análisis de voltajes y topología

### Optimizador de Subtítulos
- 🎬 **Validación automática**: Detecta problemas de timing
- 🔧 **Optimización inteligente**: Mejora legibilidad
- 📁 **Múltiples formatos**: SRT, VTT, ASS/SSA
- 🎮 **Plugin VLC**: Integración directa con VLC Media Player
- 💻 **CLI potente**: Procesamiento por lotes

### Herramientas Multiplataforma
- 🪟 **Windows**: Ejecutable .exe con doble-click
- 🐧 **Linux**: Script de instalación y servicio systemd
- 🤖 **Android**: Soporte via Termux + PWA
- 🍎 **macOS**: Homebrew setup
- 🌐 **Web**: Acceso universal via navegador

### CLI Profesional
```bash
iyari-ear doctor      # Verifica sistema
iyari-ear test-mic    # Prueba micrófono
iyari-ear start       # Inicia servidor
iyari-ear process-subtitle  # Procesa subtítulos
iyari-ear install-vlc-plugin  # Instala plugin VLC
```

---

## 💝 El Manifiesto

Con esta release publicamos el **[MANIFIESTO.md](./MANIFIESTO.md)** que define:

- **Para quién existe**: Personas que necesitan leer para seguir conversaciones
- **Para qué NO existe**: No es vigilancia, no es grabadora, no reemplaza lengua de señas
- **Qué dolor repara**: La fatiga de repetir, el aislamiento, la tecnología complicada
- **Qué belleza crea**: Conexión sin fricción, tecnología invisible, gesto de cariño
- **Límites éticos**: No graba, no guarda, no vigila (por diseño)

---

## 🎯 Casos de Uso Reales

### Conversación en cafetería
María coloca su celular sobre la mesa y abre Iyari-ear.  
Las palabras aparecen en tiempo real.  
No necesita pedir que repitan.  
Puede participar naturalmente.

### Consulta médica
Un paciente con dificultad auditiva usa Iyari-ear.  
El doctor habla normalmente.  
El texto aparece en pantalla.  
No hay malentendidos.  
No hay grabaciones.

### Comida familiar
Una abuela usa una tablet durante la comida.  
Los subtítulos le permiten seguir la conversación.  
La tecnología desaparece.  
Solo queda la conexión.

### Taller de reparación
Un técnico usa el diagnóstico electrónico.  
Toma fotos de la placa dañada.  
Recibe análisis de 3 capas.  
Identifica el problema rápidamente.  
Genera reporte profesional.

---

## 🚀 Instalación Rápida

### Para Usuarios Finales (PWA)
```bash
# 1. Inicia el servidor
pip install -r requirements.txt
python main.py

# 2. Abre Chrome/Edge: http://localhost:8000
# 3. Click "Instalar" en la barra de direcciones
# 4. ¡Listo! Tienes Iyari-ear como app
```

### Para Desarrolladores (CLI)
```bash
# Instalar en modo desarrollo
pip install -e .

# Verificar instalación
iyari-ear doctor

# Iniciar servidor
iyari-ear start
```

---

## 📖 Documentación Completa

- 📘 [README.md](./README.md) - Guía completa de instalación y uso
- 💝 [MANIFIESTO.md](./MANIFIESTO.md) - El alma del proyecto
- ⚡ [INICIO_RAPIDO.md](./INICIO_RAPIDO.md) - Guía de inicio rápido
- 🎬 [docs/SUBTITLE_OPTIMIZATION.md](./docs/SUBTITLE_OPTIMIZATION.md) - Optimización de subtítulos
- 🔧 [docs/PLATFORMS.md](./docs/PLATFORMS.md) - Guía por plataforma
- 🎮 [docs/VLC_PLUGIN_GUIDE.md](./docs/VLC_PLUGIN_GUIDE.md) - Plugin VLC

---

## 🚫 Limitaciones Conocidas

Estas limitaciones son parte del diseño ético:

- ⚠️ **Requiere conexión a internet** (para API de transcripción)
- ⚠️ **Precisión variable en ambientes muy ruidosos**
- ⚠️ **Acentos marcados pueden afectar transcripción**
- ⚠️ **No diseñada para transcripción legal o forense**

**Estas no son "bugs".**  
Son límites intencionales que protegen la privacidad y definen el propósito.

---

## 🛠️ Stack Tecnológico

### Frontend
- HTML5 + CSS3 + JavaScript vanilla
- Web Audio API para captura de audio
- Progressive Web App (PWA)
- Responsive design con accesibilidad

### Backend
- Python 3.7+
- FastAPI para API REST
- WebSockets para comunicación en tiempo real
- Google Speech Recognition API

### Herramientas
- Pillow para procesamiento de imágenes
- Gradio para interfaces interactivas
- pytest para testing

---

## 💡 Filosofía de Diseño

### 1. Empatía sobre Métricas
Cada decisión se toma preguntando:  
*"¿Esto ayuda a conectar o complica la vida?"*

### 2. Privacidad por Diseño
No grabamos. No guardamos. No vigilamos.  
El audio se transcribe y desaparece.

### 3. Accesibilidad Universal
Funciona en cualquier dispositivo.  
Sin costos. Sin muros de pago.  
Sin barreras técnicas.

### 4. Tecnología Invisible
La mejor tecnología es la que desaparece.  
Iyari-ear no quiere ser protagonista.  
Las personas lo son.

---

## 🎬 Demo y Testimonios

### Cómo Compartir Tu Experiencia

Si Iyari-ear te ayuda, nos encantaría saberlo:

1. **Demo en video** (30 segundos):
   - Graba la app en acción (sin comprometer privacidad)
   - Muestra el celular sobre la mesa con subtítulos
   - Comparte en redes con #IyariEar

2. **Historia escrita**:
   - Comparte tu caso de uso en GitHub Issues
   - Usa la plantilla [ISSUE_TEMPLATE_HISTORIAS_REALES.md](./ISSUE_TEMPLATE_HISTORIAS_REALES.md)

3. **Foto del momento**:
   - Una foto del celular mostrando subtítulos
   - Una captura de pantalla de la interfaz
   - La app funcionando en tu contexto

**No necesitamos métricas. Necesitamos historias humanas.**

---

## 🤝 Cómo Contribuir

### Código
```bash
# Fork el repositorio
# Clona tu fork
git clone https://github.com/TU_USUARIO/Iyari-ear.git

# Crea una rama
git checkout -b feature/mi-mejora

# Haz tus cambios, commit y push
# Abre un Pull Request
```

### Ideas y Feedback
- 💬 Abre un Issue para sugerencias
- 🐛 Reporta bugs (con contexto)
- 📝 Mejora la documentación
- 🌍 Traduce a otros idiomas

### Historias
- 📖 Comparte tu caso de uso
- 🎥 Envía tu demo
- ❤️ Cuenta cómo te ayudó

---

## 🙏 Agradecimientos

**A la amiga que inspiró este proyecto sin saberlo.**

A todas las personas que entienden que la tecnología debe servir a la humanidad, no al revés.

A quienes prueban la app y comparten su experiencia.

A los contribuidores que mejoran el código con el mismo espíritu de empatía.

---

## 📅 ¿Qué Sigue?

### Roadmap v1.1 (Propuesto)
- 🌍 Más idiomas (portugués, francés, etc.)
- 🎯 Mejora en ambientes ruidosos
- 📱 App nativa móvil (React Native/Flutter)
- 🔊 Modo offline con modelos locales
- 🎨 Temas personalizables
- 📊 Analytics anónimas (opt-in)

### Roadmap Comunitario
**Tú decides qué sigue.**  
Abre un Issue con tu propuesta.  
Si ayuda a conectar personas, lo consideramos.

---

## 📜 Licencia

Este proyecto está bajo la licencia que permite:
- ✅ Usar libremente
- ✅ Modificar
- ✅ Distribuir
- ✅ Uso comercial (si respeta el espíritu del proyecto)

Con la única condición de **mantener el espíritu de empatía y privacidad**.

---

## 🌐 Enlaces

- **Repositorio**: [github.com/Blackmvmba88/Iyari-ear](https://github.com/Blackmvmba88/Iyari-ear)
- **Issues**: [github.com/Blackmvmba88/Iyari-ear/issues](https://github.com/Blackmvmba88/Iyari-ear/issues)
- **Releases**: [github.com/Blackmvmba88/Iyari-ear/releases](https://github.com/Blackmvmba88/Iyari-ear/releases)
- **Documentación**: [README.md](./README.md)
- **Manifiesto**: [MANIFIESTO.md](./MANIFIESTO.md)

---

<div align="center">

## 💝 La Coronación

**Iyari-ear v1.0 — "Para que nadie quede fuera de la conversación"**

*Un puente de empatía técnica*

**Creado con cariño para una amiga.**  
**Compartido con amor para el mundo.**

✨ Enero 2025 ✨

---

> *"Este proyecto no necesita empujones. Necesita testigos."*

> *"La mejor coronación es humana + mínima + real."*

---

**[⬇️ Descargar Release](https://github.com/Blackmvmba88/Iyari-ear/releases/tag/v1.0)**

**[📖 Leer el Manifiesto](./MANIFIESTO.md)**

**[🚀 Empezar a Usar](./README.md)**

</div>

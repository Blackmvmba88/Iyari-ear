# 🎤 Iyari-ear

> **Subtítulos en tiempo real para que nadie se quede fuera de la conversación.**

*Creado con cariño para una amiga.*

**Ahora disponible como aplicación multiplataforma** 🚀

[![Platform Support](https://img.shields.io/badge/platforms-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-blue)]()
[![PWA Ready](https://img.shields.io/badge/PWA-Ready-green)]()
[![Python](https://img.shields.io/badge/python-3.7+-blue)]()

---

## 🚀 Instalación Rápida

### Opción 1: PWA (Recomendado) - Funciona en todos los dispositivos

```bash
# 1. Inicia el servidor
pip install -r requirements.txt
python main.py

# 2. Abre Chrome/Edge en: http://localhost:8000
# 3. Click en "Instalar" (ícono ➕ en la barra de direcciones)
# 4. ¡Listo! Ahora tienes Iyari-ear como app
```

### Opción 2: CLI (Para usuarios técnicos)

```bash
# Instalar
pip install -e .

# Comandos disponibles
iyari-ear doctor      # Verifica sistema
iyari-ear test-mic    # Prueba micrófono
iyari-ear start       # Inicia servidor
```

### Opción 3: Ver guías específicas por plataforma

- **Windows**: [Ejecutable .exe](docs/PLATFORMS.md#-windows)
- **Linux**: [Script de instalación](docs/PLATFORMS.md#-linux)
- **Android (Termux)**: [Guía de instalación](docs/PLATFORMS.md#-android)
- **macOS**: [Homebrew setup](docs/PLATFORMS.md#-macos)

📖 **[Guía completa de instalación](docs/INSTALLATION.md)** | **[Matriz de compatibilidad](docs/PLATFORMS.md)**

---

<div align="center">

## 📱 Visualización de la Aplicación

<!-- TODO: Reemplazar esta imagen placeholder con una foto real -->
<!-- Ver PASO_3_GUIA_IMAGEN.md para instrucciones de cómo generar la imagen -->
<!-- Debe mostrar: Un celular sobre la mesa con subtítulos en pantalla -->

![Iyari-ear Demo - Subtítulos en tiempo real](https://via.placeholder.com/800x450/2a2a2a/00ff9f?text=Iyari-ear+%7C+Subtítulos+en+Tiempo+Real)

*Subtítulos en tiempo real en tu celular. Sin fricción. Solo conexión.*

</div>

---

<div align="center">

```text
📱 Un celular sobre la mesa
🗣️ Alguien habla
✨ Las palabras aparecen

Sin ruido. Sin fricción. Solo conexión.
```

</div>

---

## Pruébalo en 60 segundos ⚡

```bash
# Método 1: CLI (si ya lo instalaste)
iyari-ear start

# Método 2: Python directo
pip install -r requirements.txt
python main.py

# Visita: http://localhost:8000
# Presiona "Iniciar" → Habla → Ve el texto
```

**💡 Nuevo:** Instala como PWA para acceso rápido desde tu menú de apps

---

## ¿Qué es esto? 💡

Una **aplicación multiplataforma** para generar subtítulos en tiempo real. Captura audio desde el micrófono del navegador, lo envía a un servidor backend que lo transcribe a texto, y muestra los subtítulos en la pantalla.

Es una herramienta pensada para ayudar a personas con dificultades auditivas en conversaciones cara a cara, usando un celular, tablet o computadora como pantalla de apoyo.

### ✨ Características Nuevas

- 📱 **PWA**: Instálala como app en cualquier dispositivo
- 🎨 **Dashboard Colorido**: Diseño profesional con modo oscuro y tema rainbow
- 🔊 **Animación Pulse**: Indicador visual cuando detecta voz
- ♿ **Accesibilidad**: Modo alto contraste, texto ultra legible
- 🖥️ **CLI Completo**: Comandos `doctor`, `test-mic`, `start`
- 🪟 **Ejecutable Windows**: Doble-click y listo
- 🤖 **Soporte Android**: Via Termux o PWA
- 🐧 **Servicio Linux**: systemd para auto-inicio
- 🎬 **Optimizador de Subtítulos**: Valida y optimiza archivos de subtítulos (SRT, VTT, ASS)
- 🎮 **Plugin VLC**: Integración con VLC Media Player para optimización automática
- 🌐 **API REST**: Endpoints para procesamiento de subtítulos vía HTTP

## Cómo funciona

La aplicación tiene dos partes principales:
1.  **Frontend**: Una página web (HTML, CSS, JavaScript) que se ejecuta en el navegador. Se encarga de pedir permiso para el micrófono, grabar el audio y enviarlo al backend. También recibe el texto transcrito y lo muestra.
2.  **Backend**: Un servidor en Python (FastAPI, WebSockets) que recibe los fragmentos de audio, utiliza la API de reconocimiento de voz de Google para transcribirlos a texto y los devuelve al frontend.

## Ejemplos de Uso Real 🌍

### Ejemplo 1: Conversación cara a cara

María tiene pérdida auditiva parcial. Está sentada con una amiga en una cafetería ruidosa.
Coloca su celular frente a la mesa y abre Iyari-ear.

La app muestra en tiempo real:

```
— ¿Quieres café o té?
— Café, por favor.
— ¿Azúcar?
— No, gracias.
```

María no necesita pedir que repitan. Lee y participa.

### Ejemplo 2: Consulta médica

Un paciente con dificultad auditiva asiste al doctor.

El doctor habla normalmente.
El celular del paciente muestra:

```
Doctor: Vamos a ajustar la dosis.
Doctor: ¿Has tenido mareos últimamente?
Paciente: No, solo un poco de cansancio.
```

No hay grabaciones.
No hay almacenamiento.
Solo texto en tiempo real.

### Ejemplo 3: Apoyo familiar

Una abuela con problemas auditivos usa una tablet durante la comida familiar.

La conversación aparece como subtítulos grandes y claros:

```
— El pastel es de chocolate.
— Cumples 8 años mañana.
— ¿Te gustó la escuela?
```

La tecnología desaparece.
Solo queda la conversación.

## Por qué existe esto ❤️

**"Creado con cariño para una amiga."**

Iyari-ear no es un producto. Es una herramienta de empatía.

- Ayudar a escuchar sin invadir.
- Apoyar sin vigilar.
- Mostrar palabras, no juzgar voces.

La tecnología al servicio de la conexión humana.

## Flujo de la Aplicación 🔄

```
Micrófono del navegador
        ↓
Fragmentos de audio
        ↓
Servidor Python (WebSockets)
        ↓
API de reconocimiento de voz
        ↓
Texto transcrito
        ↓
Subtítulos en pantalla
```

Todo ocurre en segundos.

## Optimización de Subtítulos 🎬

Iyari-ear ahora incluye un potente sistema de optimización de subtítulos que mejora la legibilidad y compatibilidad de archivos de subtítulos.

### Características del Optimizador

- ✅ **Validación automática**: Detecta problemas de timing, superposiciones y formato
- 🔧 **Optimización inteligente**: Corrige duraciones, divide líneas largas, ajusta espaciado
- 📁 **Múltiples formatos**: Soporta SRT, VTT, ASS/SSA
- 🎮 **Plugin VLC**: Integración directa con VLC Media Player
- 🌐 **Interfaz web**: Interfaz drag-and-drop en el navegador
- 💻 **CLI potente**: Procesamiento por lotes desde línea de comandos
- 🔌 **API REST**: Integración con otros sistemas

### Uso Rápido

```bash
# Optimizar subtítulos desde CLI
iyari-ear process-subtitle pelicula.srt pelicula.optimized.srt

# Instalar plugin para VLC
iyari-ear install-vlc-plugin

# Acceder a interfaz web
# Visita: http://localhost:8000/subtitle-optimizer
```

### Documentación Completa

- 📖 [Guía de Optimización de Subtítulos](docs/SUBTITLE_OPTIMIZATION.md)
- 🎮 [Guía del Plugin VLC](docs/VLC_PLUGIN_GUIDE.md)

## Qué Iyari-ear NO es 🚫

- **No es una grabadora de audio**
- **No es un sistema de vigilancia**
- **No guarda conversaciones**
- **No reemplaza intérpretes de lengua de señas**
- **No es perfecto en ambientes extremadamente ruidosos**

Es una herramienta de apoyo, no de control.

## Limitaciones Conocidas ⚠️

- **Requiere conexión a internet**
- **La precisión depende del ruido ambiental**
- **Acentos muy marcados pueden afectar la transcripción**
- **No está pensada para transcripción legal o forense**

Estas limitaciones son parte del diseño ético del proyecto.

## Requisitos

- Python 3.7 o superior.
- Un micrófono conectado al dispositivo donde se abrirá la página web.
- Conexión a internet (ya que se usa la API de Google para la transcripción).

## Instrucciones de Instalación y Uso

Sigue estos pasos para poner en marcha la aplicación.

### 1. Preparar el Backend (El Servidor)

Primero, necesitamos instalar las dependencias de Python y ejecutar el servidor.

```bash
# 1. (Opcional pero recomendado) Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\\Scripts\\activate

# 2. Instala las librerías necesarias desde requirements.txt
pip install -r requirements.txt

# 3. Inicia el servidor
python main.py
```

Si todo va bien, verás un mensaje como este en tu terminal, lo que significa que el servidor está escuchando:
`Servidor de WebSockets iniciado en ws://0.0.0.0:8000`

**Deja esta terminal abierta mientras usas la aplicación.**

### 2. Usar la Aplicación (El Frontend)

Ahora que el servidor está corriendo, puedes abrir la interfaz.

**Opción A: En la misma computadora**

1.  Abre el archivo `index.html` directamente en tu navegador web (Firefox, Chrome, etc.).
2.  La página se cargará. Presiona el botón "Iniciar".
3.  El navegador te pedirá permiso para usar el micrófono. Debes aceptarlo.
4.  ¡Habla y los subtítulos aparecerán en la pantalla!

**Opción B: En tu celular (o cualquier otro dispositivo)**

Esta es la forma más práctica de usarlo.

1.  Asegúrate de que tu celular y la computadora donde corre el servidor estén **conectados a la misma red Wi-Fi**.
2.  Busca la dirección IP local de tu computadora.
    - **En Windows:** Abre `cmd` y escribe `ipconfig`. Busca la dirección "IPv4 Address".
    - **En macOS o Linux:** Abre una terminal y escribe `hostname -I` o `ifconfig`.
    - Será un número como `192.168.1.10` o `10.0.0.5`.
3.  En el navegador de tu celular, introduce la siguiente dirección:
    `http://<LA_IP_DE_TU_COMPUTADORA>:8000`
    (Reemplaza `<LA_IP_DE_TU_COMPUTADORA>` con el número que encontraste).

4.  La página cargará. Presiona "Iniciar", acepta el permiso del micrófono y ¡listo! El servidor de Python se encarga de todo.

---

## Solución de Problemas

### Error al instalar `PyAudio` en Linux

Si durante la instalación (`pip install -r requirements.txt`) ves un error relacionado con `PyAudio` y `portaudio.h`, significa que te falta una librería del sistema.

Puedes solucionarlo instalando el paquete de desarrollo de PortAudio. En sistemas basados en Debian/Ubuntu, el comando es:

```bash
sudo apt-get update && sudo apt-get install -y portaudio19-dev
```

Después de instalarlo, vuelve a ejecutar `pip install -r requirements.txt`.

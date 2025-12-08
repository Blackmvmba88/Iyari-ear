# Visualización viva de audio en tiempo real
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

fs = 44100  # Frecuencia de muestreo
duration = 0.05  # Duración de cada bloque en segundos

fig, ax = plt.subplots()
line, = ax.plot([], [], linewidth=2)
ax.set_xlim(0, int(fs * duration))
ax.set_ylim(-1, 1)
ax.set_title('Audio en tiempo real - Colores electromagnéticos')
ax.set_xlabel('Muestras')
ax.set_ylabel('Amplitud')

def update_plot(indata):
    y = indata[:, 0]
    x = np.arange(len(y))
    # Color según amplitud media
    amp = np.abs(y).mean()
    color = plt.cm.rainbow(amp)
    line.set_data(x, y)
    line.set_color(color)
    fig.canvas.draw()
    fig.canvas.flush_events()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    update_plot(indata)

plt.ion()
with sd.InputStream(channels=1, samplerate=fs, blocksize=int(fs * duration), callback=audio_callback):
    print('Presiona Ctrl+C para salir')
    while True:
        plt.pause(0.01)
# Onda sinusoidal con línea arcoíris
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la onda
amplitud = 1
frecuencia = 1
fase = 0
t = np.linspace(0, 2 * np.pi, 500)
y = amplitud * np.sin(frecuencia * t + fase)

# Graficar con línea arcoíris
colores = plt.cm.rainbow(np.linspace(0, 1, len(t)-1))
for i in range(len(t)-1):
    plt.plot(t[i:i+2], y[i:i+2], color=colores[i], linewidth=2)

plt.title('Onda Sinusoidal - Línea Rainbow')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.show()
import asyncio
import speech_recognition as sr
import io
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(title="Iyari-ear - Subtítulos en Tiempo Real")

# Límites de seguridad
MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10 MB límite para chunks de audio
MAX_CONNECTIONS = 100  # Límite de conexiones simultáneas

# Port configuration
MIN_PORT = 1
MAX_PORT = 65535
DEFAULT_PORT = 8000

# Contador de conexiones activas
active_connections = 0

# Verificar que los directorios existan antes de montar
js_dir = os.path.abspath("js")
styles_dir = os.path.abspath("styles")

if os.path.isdir(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")
else:
    logger.warning(f"Directorio 'js' no encontrado en: {js_dir}")

if os.path.isdir(styles_dir):
    app.mount("/styles", StaticFiles(directory=styles_dir), name="styles")
else:
    logger.warning(f"Directorio 'styles' no encontrado en: {styles_dir}")

# Inicializar el reconocedor de voz
r = sr.Recognizer()


@app.get("/")
async def read_root():
    """Sirve el archivo index.html como la página principal."""
    index_path = 'index.html'
    if not os.path.isfile(index_path):
        logger.error(f"Archivo index.html no encontrado: {index_path}")
        return {"error": "Archivo index.html no encontrado"}
    return FileResponse(index_path)


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando."""
    return {"status": "ok", "active_connections": active_connections}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint de WebSocket para la transcripción de audio.
    """
    global active_connections

    # Verificar límite de conexiones
    if active_connections >= MAX_CONNECTIONS:
        logger.warning("Límite de conexiones alcanzado. Rechazando nueva conexión.")
        await websocket.close(code=1013, reason="Servidor saturado")
        return

    await websocket.accept()
    active_connections += 1
    logger.info(f"Cliente WebSocket conectado. Conexiones activas: {active_connections}")

    # Default language is Spanish
    current_language = 'es-ES'

    try:
        while True:
            # Espera recibir datos del cliente (puede ser audio binario o mensaje JSON)
            try:
                # Try to receive as text first (for JSON messages)
                message = await websocket.receive()
                
                # Check if it's a text message (language selection)
                if 'text' in message:
                    try:
                        import json
                        data = json.loads(message['text'])
                        if data.get('type') == 'language':
                            current_language = data.get('language', 'es-ES')
                            logger.info(f"Idioma cambiado a: {current_language}")
                            continue
                    except json.JSONDecodeError:
                        logger.warning("Mensaje de texto no es JSON válido")
                        continue
                
                # If it's bytes, process as audio
                if 'bytes' not in message:
                    continue
                    
                audio_chunk = message['bytes']
            except Exception as e:
                logger.error(f"Error al recibir mensaje: {e}")
                continue

            # Validar tamaño del chunk de audio
            if len(audio_chunk) > MAX_AUDIO_SIZE:
                logger.warning(f"Chunk de audio demasiado grande: {len(audio_chunk)} bytes")
                await websocket.send_text("[Error: Audio demasiado grande]")
                continue

            if len(audio_chunk) == 0:
                logger.debug("Chunk de audio vacío recibido, ignorando.")
                continue

            # Creamos un archivo de audio en memoria
            audio_file = io.BytesIO(audio_chunk)

            try:
                with sr.AudioFile(audio_file) as source:
                    audio_data = r.record(source)
            except Exception as e:
                logger.error(f"Error al procesar archivo de audio: {e}")
                await websocket.send_text("[Error: Formato de audio no soportado]")
                continue

            try:
                # Transcribir usando la API de Google con el idioma seleccionado
                text = r.recognize_google(audio_data, language=current_language)
                logger.info(f"Texto reconocido ({current_language}): {text}")
                await websocket.send_text(text)

            except sr.UnknownValueError:
                logger.debug("Audio no reconocido.")
                await websocket.send_text("[Audio no reconocido]")
            except sr.RequestError as e:
                logger.error(f"Error en la API de Google: {e}")
                await websocket.send_text("[Error del servicio de transcripción]")

    except WebSocketDisconnect:
        logger.info("Cliente WebSocket desconectado.")
    except Exception as e:
        logger.error(f"Ocurrió un error en el WebSocket: {e}")
    finally:
        active_connections -= 1
        logger.info(f"Conexiones activas: {active_connections}")


if __name__ == "__main__":
    # Iniciar el servidor Uvicorn
    # El host y el puerto pueden configurarse mediante variables de entorno.
    host = os.environ.get("HOST", "127.0.0.1")
    try:
        port = int(os.environ.get("PORT", DEFAULT_PORT))
        if port < MIN_PORT or port > MAX_PORT:
            raise ValueError(f"Puerto fuera de rango ({MIN_PORT}-{MAX_PORT})")
    except ValueError as e:
        logger.error(f"Puerto inválido: {e}. Usando puerto {DEFAULT_PORT}.")
        port = DEFAULT_PORT

    logger.info(f"Iniciando servidor en {host}:{port}")
    uvicorn.run(app, host=host, port=port)

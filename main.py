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
# Crear la aplicación FastAPI
app = FastAPI()

# Montar los directorios de archivos estáticos (js, styles)
app.mount("/js", StaticFiles(directory=os.path.abspath("js")), name="js")
app.mount("/styles", StaticFiles(directory=os.path.abspath("styles")), name="styles")

# Inicializar el reconocedor de voz
r = sr.Recognizer()

@app.get("/")
async def read_root():
    """Sirve el archivo index.html como la página principal."""
    return FileResponse('index.html')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint de WebSocket para la transcripción de audio.
    """
    await websocket.accept()
    print("Cliente WebSocket conectado.")
    try:
        while True:
            # Espera recibir datos de audio del cliente
            audio_chunk = await websocket.receive_bytes()

            # Creamos un archivo de audio en memoria
            audio_file = io.BytesIO(audio_chunk)

            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)

            try:
                # Transcribir usando la API de Google
                text = r.recognize_google(audio_data, language='es-ES')
                print(f"Texto reconocido: {text}")
                await websocket.send_text(text)

            except sr.UnknownValueError:
                print("Audio no reconocido.")
                await websocket.send_text("[Audio no reconocido]")
            except sr.RequestError as e:
                print(f"Error en la API de Google: {e}")
                await websocket.send_text("[Error del servicio de transcripción]")

    except WebSocketDisconnect:
        print("Cliente WebSocket desconectado.")
    except Exception as e:
        print(f"Ocurrió un error en el WebSocket: {e}")

if __name__ == "__main__":
    # Iniciar el servidor Uvicorn
    # El host y el puerto pueden configurarse mediante variables de entorno.
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host=host, port=port)

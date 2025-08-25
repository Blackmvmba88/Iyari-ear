import asyncio
import speech_recognition as sr
import io
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

# Crear la aplicación FastAPI
app = FastAPI()

# Montar los directorios de archivos estáticos (js, styles)
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/styles", StaticFiles(directory="styles"), name="styles")

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
    # Escuchará en todas las interfaces de red en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

import asyncio
import speech_recognition as sr
import io
import json
import uvicorn
from fastapi import (
    FastAPI, 
    WebSocket, 
    WebSocketDisconnect, 
    UploadFile, 
    File, 
    HTTPException
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import logging
import tempfile
from typing import Optional

# Importar módulos de subtítulos
try:
    from subtitle_processor import SubtitleProcessor, process_subtitle_file
    SUBTITLE_SUPPORT = True
except ImportError:
    SUBTITLE_SUPPORT = False
    logging.warning("Módulo de procesamiento de subtítulos no disponible")

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

# Supported languages for speech recognition
SUPPORTED_LANGUAGES = {'es-ES', 'en-US'}
DEFAULT_LANGUAGE = 'es-ES'

# Contador de conexiones activas
active_connections = 0

# Verificar que los directorios existan antes de montar
js_dir = os.path.abspath("js")
styles_dir = os.path.abspath("styles")
apps_dir = os.path.abspath("apps")

if os.path.isdir(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")
else:
    logger.warning(f"Directorio 'js' no encontrado en: {js_dir}")

if os.path.isdir(styles_dir):
    app.mount("/styles", StaticFiles(directory=styles_dir), name="styles")
else:
    logger.warning(f"Directorio 'styles' no encontrado en: {styles_dir}")

if os.path.isdir(apps_dir):
    app.mount("/apps", StaticFiles(directory=apps_dir), name="apps")
else:
    logger.warning(f"Directorio 'apps' no encontrado en: {apps_dir}")

# Inicializar el reconocedor de voz
r = sr.Recognizer()

# Modelos Pydantic para API de subtítulos
class SubtitleProcessRequest(BaseModel):
    """Solicitud de procesamiento de subtítulos"""
    validate: bool = True
    optimize: bool = True
    output_format: Optional[str] = None


class SubtitleProcessResponse(BaseModel):
    """Respuesta de procesamiento de subtítulos"""
    success: bool
    stats: dict
    validation_issues: list
    optimization_changes: int
    download_url: Optional[str] = None


@app.get("/")
async def read_root():
    """Sirve el archivo index.html como la página principal."""
    index_path = 'index.html'
    if not os.path.isfile(index_path):
        logger.error(f"Archivo index.html no encontrado: {index_path}")
        return {"error": "Archivo index.html no encontrado"}
    return FileResponse(index_path)


@app.get("/subtitle-optimizer")
async def subtitle_optimizer_page():
    """Sirve la página del optimizador de subtítulos."""
    page_path = 'subtitle-optimizer.html'
    if not os.path.isfile(page_path):
        logger.error(f"Archivo subtitle-optimizer.html no encontrado: {page_path}")
        return {"error": "Página no encontrada"}
    return FileResponse(page_path)


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando."""
    return {
        "status": "ok", 
        "active_connections": active_connections,
        "subtitle_support": SUBTITLE_SUPPORT
    }


@app.post("/api/subtitles/process")
async def process_subtitle_endpoint(
    file: UploadFile = File(...),
    validate: bool = True,
    optimize: bool = True,
    output_format: Optional[str] = None
):
    """
    Endpoint para procesar y optimizar archivos de subtítulos
    
    Args:
        file: Archivo de subtítulos (SRT, VTT, ASS)
        validate: Si se debe validar el archivo
        optimize: Si se debe optimizar el archivo
        output_format: Formato de salida (srt, vtt)
    
    Returns:
        JSON con resultados del procesamiento y URL de descarga
    """
    if not SUBTITLE_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de procesamiento de subtítulos no disponible"
        )
    
    # Validar extensión
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in ['.srt', '.vtt', '.ass', '.ssa']:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado: {ext}. Usa .srt, .vtt, .ass o .ssa"
        )
    
    # Crear archivos temporales
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_input:
        content = await file.read()
        tmp_input.write(content)
        tmp_input_path = tmp_input.name
    
    # Determinar formato de salida
    if output_format is None:
        output_format = 'srt' if ext != '.vtt' else 'vtt'
    
    # Procesar archivo
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=f'.{output_format}',
            mode='w'
        ) as tmp_output:
            tmp_output_path = tmp_output.name
        
        success, results = process_subtitle_file(
            tmp_input_path,
            tmp_output_path,
            validate=validate,
            optimize=optimize,
            output_format=output_format
        )
        
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Error al procesar archivo de subtítulos"
            )
        
        # Generar URL de descarga temporal
        # Guardar en directorio temporal con nombre único
        import uuid
        download_id = str(uuid.uuid4())
        download_dir = tempfile.gettempdir()
        final_path = os.path.join(download_dir, f"subtitle_{download_id}.{output_format}")
        
        import shutil
        shutil.move(tmp_output_path, final_path)
        
        # Guardar metadata para descarga posterior
        metadata_path = os.path.join(download_dir, f"subtitle_{download_id}.json")
        with open(metadata_path, 'w') as f:
            json.dump({
                'original_filename': filename,
                'format': output_format,
                'processed_at': str(os.path.getmtime(final_path))
            }, f)
        
        return {
            "success": True,
            "stats": results['stats'],
            "validation_issues": results['validation_issues'],
            "optimization_changes": results['optimization_changes'],
            "download_url": f"/api/subtitles/download/{download_id}"
        }
        
    except Exception as e:
        logger.error(f"Error procesando subtítulo: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Limpiar archivo temporal de entrada
        if os.path.exists(tmp_input_path):
            os.unlink(tmp_input_path)


@app.get("/api/subtitles/download/{download_id}")
async def download_subtitle(download_id: str):
    """
    Descarga un archivo de subtítulos procesado
    
    Args:
        download_id: ID único del archivo procesado
    
    Returns:
        Archivo de subtítulos procesado
    """
    download_dir = tempfile.gettempdir()
    
    # Buscar archivo con diferentes extensiones
    for ext in ['srt', 'vtt']:
        file_path = os.path.join(download_dir, f"subtitle_{download_id}.{ext}")
        metadata_path = os.path.join(download_dir, f"subtitle_{download_id}.json")
        
        if os.path.exists(file_path):
            # Leer metadata
            original_filename = f"optimized.{ext}"
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        original_filename = metadata.get('original_filename', original_filename)
                        # Cambiar extensión al formato procesado
                        original_filename = os.path.splitext(original_filename)[0] + f'.optimized.{ext}'
                except:
                    pass
            
            return FileResponse(
                file_path,
                media_type='text/plain',
                filename=original_filename
            )
    
    raise HTTPException(status_code=404, detail="Archivo no encontrado o expirado")


@app.post("/api/subtitles/validate")
async def validate_subtitle_endpoint(file: UploadFile = File(...)):
    """
    Valida un archivo de subtítulos sin modificarlo
    
    Note: Uses POST (not GET) because it accepts file uploads,
    following RESTful conventions for requests with body content.
    
    Args:
        file: Archivo de subtítulos a validar
    
    Returns:
        Lista de problemas encontrados
    """
    if not SUBTITLE_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de procesamiento de subtítulos no disponible"
        )
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        processor = SubtitleProcessor()
        if not processor.load_from_file(tmp_path):
            raise HTTPException(
                status_code=400,
                detail="Error al cargar archivo de subtítulos"
            )
        
        issues = processor.validate()
        stats = processor.get_stats()
        
        return {
            "success": True,
            "stats": stats,
            "issues": issues,
            "total_issues": len(issues),
            "errors": len([i for i in issues if i['severity'] == 'error']),
            "warnings": len([i for i in issues if i['severity'] == 'warning']),
            "info": len([i for i in issues if i['severity'] == 'info'])
        }
    
    except Exception as e:
        logger.error(f"Error validando subtítulo: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


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
    current_language = DEFAULT_LANGUAGE

    try:
        while True:
            # Espera recibir datos del cliente (puede ser audio binario o mensaje JSON)
            try:
                # Try to receive as text first (for JSON messages)
                message = await websocket.receive()
                
                # Check if it's a text message (language selection)
                if 'text' in message:
                    try:
                        data = json.loads(message['text'])
                        if isinstance(data, dict) and data.get('type') == 'language':
                            requested_language = data.get('language', DEFAULT_LANGUAGE)
                            # Validate language is supported
                            if requested_language in SUPPORTED_LANGUAGES:
                                current_language = requested_language
                                logger.info(f"Idioma cambiado a: {current_language}")
                            else:
                                logger.warning(f"Idioma no soportado: {requested_language}. Usando {DEFAULT_LANGUAGE}")
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

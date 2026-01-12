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
    HTTPException,
    Request
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import logging
import tempfile
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict

# Importar módulos de subtítulos
try:
    from subtitle_processor import SubtitleProcessor, process_subtitle_file
    SUBTITLE_SUPPORT = True
except ImportError:
    SUBTITLE_SUPPORT = False
    logging.warning("Módulo de procesamiento de subtítulos no disponible")

# Importar motor de diagnóstico
try:
    from diagnostic_engine import DiagnosticEngine, DiagnosticStyle
    DIAGNOSTIC_SUPPORT = True
except ImportError:
    DIAGNOSTIC_SUPPORT = False
    logging.warning("Módulo de diagnóstico electrónico no disponible")

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

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 30  # Número de solicitudes permitidas
RATE_LIMIT_WINDOW = 60  # Ventana de tiempo en segundos
rate_limit_storage = defaultdict(list)  # IP -> lista de timestamps

# Port configuration
MIN_PORT = 1
MAX_PORT = 65535
DEFAULT_PORT = 8000

# Supported languages for speech recognition
SUPPORTED_LANGUAGES = {'es-ES', 'en-US'}
DEFAULT_LANGUAGE = 'es-ES'

# Contador de conexiones activas
active_connections = 0


# Rate limiting helper
def check_rate_limit(client_ip: str) -> bool:
    """
    Verifica si el cliente ha excedido el límite de solicitudes
    
    Args:
        client_ip: Dirección IP del cliente
    
    Returns:
        True si el cliente está dentro del límite, False si lo excedió
    """
    now = datetime.now()
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    
    # Limpiar timestamps antiguos
    rate_limit_storage[client_ip] = [
        ts for ts in rate_limit_storage[client_ip] if ts > cutoff
    ]
    
    # Verificar límite
    if len(rate_limit_storage[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    
    # Agregar timestamp actual
    rate_limit_storage[client_ip].append(now)
    return True


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

# Inicializar motor de diagnóstico si está disponible
diagnostic_engine = None
if DIAGNOSTIC_SUPPORT:
    diagnostic_engine = DiagnosticEngine(style=DiagnosticStyle.TECHNICIAN)
    logger.info("Motor de diagnóstico electrónico inicializado")

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


# Modelos Pydantic para API de diagnóstico
class DiagnosticSessionRequest(BaseModel):
    """Solicitud de creación de sesión de diagnóstico"""
    board_model: str
    diagnostic_style: str = "técnico"
    session_id: Optional[str] = None


class DiagnosticImageUpload(BaseModel):
    """Metadata para subida de imagen de diagnóstico"""
    session_id: str
    image_type: str = "frontal"


class DiagnosticAnalyzeRequest(BaseModel):
    """Solicitud de análisis de diagnóstico"""
    session_id: str


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


@app.get("/diagnostic")
async def diagnostic_page():
    """Sirve la página del sistema de diagnóstico electrónico."""
    page_path = 'diagnostic.html'
    if not os.path.isfile(page_path):
        logger.error(f"Archivo diagnostic.html no encontrado: {page_path}")
        return {"error": "Página no encontrada"}
    return FileResponse(page_path)


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que el servidor está funcionando."""
    return {
        "status": "ok", 
        "active_connections": active_connections,
        "subtitle_support": SUBTITLE_SUPPORT,
        "diagnostic_support": DIAGNOSTIC_SUPPORT
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


# ============================================================================
# API DE DIAGNÓSTICO ELECTRÓNICO
# ============================================================================

@app.post("/api/diagnostic/session")
async def create_diagnostic_session(request: DiagnosticSessionRequest, http_request: Request):
    """
    Crea una nueva sesión de diagnóstico electrónico
    
    Args:
        request: Datos de la sesión (modelo de placa, estilo)
        http_request: Solicitud HTTP para obtener IP del cliente
    
    Returns:
        ID de la sesión creada
    """
    if not DIAGNOSTIC_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de diagnóstico no disponible"
        )
    
    # Rate limiting
    client_ip = http_request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Demasiadas solicitudes. Por favor, espera un momento."
        )
    
    try:
        # Mapear estilo al enum
        style_map = {
            "técnico": DiagnosticStyle.TECHNICIAN,  # Spanish: "technician"
            "ingeniero": DiagnosticStyle.ENGINEER,
            "forense": DiagnosticStyle.FORENSIC
        }
        
        diagnostic_engine.style = style_map.get(
            request.diagnostic_style,
            DiagnosticStyle.TECHNICIAN
        )
        
        # Crear sesión
        session_id = diagnostic_engine.create_session(
            board_model=request.board_model,
            session_id=request.session_id
        )
        
        logger.info(f"Sesión de diagnóstico creada: {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "board_model": request.board_model,
            "style": request.diagnostic_style
        }
        
    except Exception as e:
        logger.error(f"Error al crear sesión de diagnóstico: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/diagnostic/upload")
async def upload_diagnostic_image(
    file: UploadFile = File(...),
    session_id: str = "",
    image_type: str = "frontal"
):
    """
    Sube una imagen a la sesión de diagnóstico
    
    Args:
        file: Archivo de imagen
        session_id: ID de la sesión
        image_type: Tipo de imagen
    
    Returns:
        ID de la imagen subida
    """
    if not DIAGNOSTIC_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de diagnóstico no disponible"
        )
    
    if not session_id:
        raise HTTPException(
            status_code=400,
            detail="Se requiere session_id"
        )
    
    # Validate session_id format to prevent directory traversal
    import re
    if not re.match(r'^session_[0-9]{8}_[0-9]{6}_[a-f0-9]{8,16}$', session_id):
        raise HTTPException(
            status_code=400,
            detail=f"Formato de session_id inválido: {session_id}"
        )
    
    # Validar tipo de archivo
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen"
        )
    
    try:
        # Crear directorio temporal para imágenes de diagnóstico (seguro)
        import uuid
        diagnostic_dir = os.path.join(tempfile.gettempdir(), f"diagnostic_{session_id}")
        os.makedirs(diagnostic_dir, exist_ok=True)
        
        # Guardar archivo con nombre único y seguro
        file_ext = os.path.splitext(file.filename)[1]
        safe_filename = f"{image_type}_{uuid.uuid4().hex[:8]}{file_ext}"
        file_path = os.path.join(diagnostic_dir, safe_filename)
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Añadir a la sesión
        image_id = diagnostic_engine.add_image(
            session_id=session_id,
            image_path=file_path,
            image_type=image_type
        )
        
        logger.info(f"Imagen subida: {image_id} para sesión {session_id}")
        
        return {
            "success": True,
            "image_id": image_id,
            "session_id": session_id,
            "image_type": image_type
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al subir imagen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/diagnostic/analyze")
async def analyze_diagnostic_session(request: DiagnosticAnalyzeRequest):
    """
    Inicia el análisis de diagnóstico de una sesión
    
    Args:
        request: Contiene session_id
    
    Returns:
        Confirmación de inicio del análisis
    """
    if not DIAGNOSTIC_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de diagnóstico no disponible"
        )
    
    try:
        # Verificar que la sesión existe
        if request.session_id not in diagnostic_engine.sessions:
            raise HTTPException(
                status_code=404,
                detail=f"Sesión {request.session_id} no encontrada"
            )
        
        session = diagnostic_engine.sessions[request.session_id]
        
        if len(session.images) == 0:
            raise HTTPException(
                status_code=400,
                detail="La sesión no tiene imágenes para analizar"
            )
        
        # Marcar sesión como en progreso
        session.status = "en_progreso"
        
        # Generar hipótesis de ejemplo (en producción usaría ML/CV)
        # Hipótesis 1: Problema en rail 3V3
        hyp1 = diagnostic_engine.generate_full_hypothesis(
            session_id=request.session_id,
            rail="3V3"
        )
        session.hypotheses.append(hyp1)
        
        # Marcar como completada
        session.status = "completada"
        
        logger.info(f"Análisis completado para sesión {request.session_id}")
        
        return {
            "success": True,
            "session_id": request.session_id,
            "status": "analysis_started",
            "message": "El análisis ha comenzado. Conéctate vía WebSocket para recibir actualizaciones."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al iniciar análisis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/diagnostic/session/{session_id}")
async def get_diagnostic_session(session_id: str):
    """
    Obtiene el estado y resultados de una sesión de diagnóstico
    
    Args:
        session_id: ID de la sesión
    
    Returns:
        Datos completos de la sesión
    """
    if not DIAGNOSTIC_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de diagnóstico no disponible"
        )
    
    try:
        if session_id not in diagnostic_engine.sessions:
            raise HTTPException(
                status_code=404,
                detail=f"Sesión {session_id} no encontrada"
            )
        
        # Exportar sesión
        session_data = diagnostic_engine.export_session(session_id)
        
        # Generar reporte de texto
        report_text = diagnostic_engine.format_diagnostic_report(session_id)
        session_data['report_text'] = report_text
        
        return session_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener sesión: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/diagnostic/sessions")
async def list_diagnostic_sessions():
    """
    Lista todas las sesiones de diagnóstico
    
    Returns:
        Lista de resúmenes de sesiones
    """
    if not DIAGNOSTIC_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de diagnóstico no disponible"
        )
    
    try:
        sessions = []
        for session_id in diagnostic_engine.sessions:
            summary = diagnostic_engine.get_diagnostic_summary(session_id)
            sessions.append(summary)
        
        return {
            "success": True,
            "count": len(sessions),
            "sessions": sessions
        }
        
    except Exception as e:
        logger.error(f"Error al listar sesiones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/diagnostic/session/{session_id}")
async def delete_diagnostic_session(session_id: str):
    """
    Elimina una sesión de diagnóstico y limpia archivos temporales
    
    Args:
        session_id: ID de la sesión a eliminar
    
    Returns:
        Confirmación de eliminación
    """
    if not DIAGNOSTIC_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de diagnóstico no disponible"
        )
    
    try:
        if session_id not in diagnostic_engine.sessions:
            raise HTTPException(
                status_code=404,
                detail=f"Sesión {session_id} no encontrada"
            )
        
        # Limpiar archivos temporales de la sesión
        diagnostic_dir = os.path.join(tempfile.gettempdir(), f"diagnostic_{session_id}")
        if os.path.exists(diagnostic_dir):
            import shutil
            shutil.rmtree(diagnostic_dir)
            logger.info(f"Directorio temporal eliminado: {diagnostic_dir}")
        
        # Eliminar sesión de memoria
        del diagnostic_engine.sessions[session_id]
        
        return {
            "success": True,
            "message": f"Sesión {session_id} eliminada correctamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar sesión: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/diagnostic/cleanup")
async def cleanup_old_diagnostic_sessions(max_age_hours: int = 24):
    """
    Limpia sesiones y archivos temporales antiguos
    
    Args:
        max_age_hours: Edad máxima en horas (por defecto 24 horas)
    
    Returns:
        Número de sesiones y archivos eliminados
    """
    if not DIAGNOSTIC_SUPPORT:
        raise HTTPException(
            status_code=503,
            detail="Módulo de diagnóstico no disponible"
        )
    
    try:
        from datetime import timedelta
        import shutil
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        sessions_removed = 0
        files_removed = 0
        
        # Limpiar sesiones antiguas
        sessions_to_remove = []
        for session_id, session in diagnostic_engine.sessions.items():
            if session.creation_time < cutoff_time:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            # Limpiar archivos
            diagnostic_dir = os.path.join(tempfile.gettempdir(), f"diagnostic_{session_id}")
            if os.path.exists(diagnostic_dir):
                shutil.rmtree(diagnostic_dir)
                files_removed += 1
            
            # Eliminar sesión
            del diagnostic_engine.sessions[session_id]
            sessions_removed += 1
        
        logger.info(f"Limpieza completada: {sessions_removed} sesiones, {files_removed} directorios")
        
        return {
            "success": True,
            "sessions_removed": sessions_removed,
            "directories_removed": files_removed,
            "cutoff_time": cutoff_time.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en limpieza: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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


@app.websocket("/ws/diagnostic/{session_id}")
async def diagnostic_websocket(websocket: WebSocket, session_id: str):
    """
    WebSocket para actualizaciones en tiempo real del diagnóstico
    
    Envía mensajes de progreso y resultados mientras se analiza
    """
    if not DIAGNOSTIC_SUPPORT:
        await websocket.close(code=1008, reason="Diagnóstico no disponible")
        return
    
    if session_id not in diagnostic_engine.sessions:
        await websocket.close(code=1008, reason="Sesión no encontrada")
        return
    
    await websocket.accept()
    logger.info(f"Cliente WebSocket de diagnóstico conectado: {session_id}")
    
    try:
        session = diagnostic_engine.sessions[session_id]
        
        # Simular progreso de análisis
        progress_messages = [
            "✔ Identificando rails...",
            "✔ 3V3 encontrado",
            "✔ 5V encontrado",
            "✔ Región RF detectada",
            "✔ Posible regulador AMS1117",
            "✔ Analizando topología...",
            "✔ Generando hipótesis..."
        ]
        
        for msg in progress_messages:
            await websocket.send_json({
                "type": "progress",
                "message": msg
            })
            await asyncio.sleep(0.5)  # Simular procesamiento
        
        # Enviar hipótesis
        for hypothesis in session.hypotheses:
            await websocket.send_json({
                "type": "hypothesis",
                "hypothesis": {
                    "hypothesis_id": hypothesis.hypothesis_id,
                    "overall_confidence": hypothesis.overall_confidence,
                    "layer1": {
                        "voltage_rail": hypothesis.layer1.voltage_rail,
                        "component_id": hypothesis.layer1.component_id,
                        "functional_block": hypothesis.layer1.functional_block
                    },
                    "layer2": {
                        "fault_cause": hypothesis.layer2.fault_cause.value,
                        "reasoning": hypothesis.layer2.reasoning,
                        "evidence": hypothesis.layer2.evidence
                    },
                    "layer3": {
                        "functional_impact": hypothesis.layer3.functional_impact,
                        "impact_level": hypothesis.layer3.impact_level.value,
                        "affected_features": hypothesis.layer3.affected_features
                    },
                    "next_steps": hypothesis.next_steps,
                    "test_points": hypothesis.test_points
                }
            })
            await asyncio.sleep(0.3)
        
        # Enviar mensaje de completación con reporte
        report_text = diagnostic_engine.format_diagnostic_report(session_id)
        session_data = diagnostic_engine.export_session(session_id)
        session_data['report_text'] = report_text
        
        await websocket.send_json({
            "type": "complete",
            "results": session_data
        })
        
    except WebSocketDisconnect:
        logger.info(f"Cliente WebSocket de diagnóstico desconectado: {session_id}")
    except Exception as e:
        logger.error(f"Error en WebSocket de diagnóstico: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except Exception:
            # WebSocket already closed
            pass


if __name__ == "__main__":
    # Leer versión del archivo VERSION
    version = "unknown"
    version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            version = f.read().strip()
    
    # Banner de inicio
    logger.info("=" * 60)
    logger.info("🎤 Iyari-ear v%s", version)
    logger.info('"Para que nadie quede fuera de la conversación"')
    logger.info("Un puente de empatía técnica")
    logger.info("=" * 60)
    
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
    logger.info("Accede a la aplicación en: http://%s:%d", host if host != "0.0.0.0" else "localhost", port)
    logger.info("Presiona Ctrl+C para detener el servidor")
    logger.info("=" * 60)
    uvicorn.run(app, host=host, port=port)

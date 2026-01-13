# 🌐 API Reference — Iyari-ear

> **"Contratos claros para que cualquiera pueda construir encima"**

Esta guía documenta todos los endpoints REST y WebSocket de Iyari-ear, con ejemplos, códigos de error y formatos de respuesta.

---

## 📋 Índice

1. [Información General](#información-general)
2. [WebSocket API](#websocket-api)
3. [REST API - Salud del Sistema](#rest-api---salud-del-sistema)
4. [REST API - Subtítulos](#rest-api---subtítulos)
5. [REST API - Diagnóstico Electrónico](#rest-api---diagnóstico-electrónico)
6. [Códigos de Error](#códigos-de-error)
7. [Rate Limiting](#rate-limiting)
8. [Ejemplos de Integración](#ejemplos-de-integración)

---

## Información General

### Base URL
```
http://localhost:8000
```

### Content Type
- REST API: `application/json`
- File uploads: `multipart/form-data`
- WebSocket: Binary (audio) o Text (JSON)

### Autenticación
**Ninguna** - El sistema es abierto para uso local

### Rate Limits
- **30 solicitudes por minuto** por IP
- **100 conexiones WebSocket simultáneas**

---

## WebSocket API

### 🎤 WebSocket de Transcripción

**Endpoint:** `ws://localhost:8000/ws`

**Propósito:** Transcripción de audio en tiempo real

#### Flujo de Conexión

```javascript
// 1. Conectar
const ws = new WebSocket('ws://localhost:8000/ws');

// 2. Esperar conexión
ws.onopen = () => {
    console.log('Conectado al servidor de transcripción');
    
    // 3. (Opcional) Enviar selección de idioma
    ws.send(JSON.stringify({
        type: 'language',
        language: 'es-ES'  // o 'en-US'
    }));
};

// 4. Enviar audio
ws.send(audioBlob);  // Binary data

// 5. Recibir texto transcrito
ws.onmessage = (event) => {
    const text = event.data;
    console.log('Transcrito:', text);
};

// 6. Manejar errores
ws.onerror = (error) => {
    console.error('Error WebSocket:', error);
};

// 7. Cerrar conexión
ws.close();
```

#### Mensajes Soportados

##### 1. Selección de Idioma (Cliente → Servidor)
```json
{
    "type": "language",
    "language": "es-ES"
}
```

**Idiomas soportados:**
- `es-ES` - Español (por defecto)
- `en-US` - Inglés

##### 2. Audio Chunk (Cliente → Servidor)
- **Formato:** Binary (Blob/ArrayBuffer)
- **Codec:** WAV o formato compatible con SpeechRecognition
- **Tamaño máximo:** 10 MB por chunk
- **Frecuencia recomendada:** Enviar cada ~500ms

##### 3. Texto Transcrito (Servidor → Cliente)
```
"Hola, ¿cómo estás?"
```

**Mensajes especiales:**
- `[Audio no reconocido]` - No se pudo transcribir
- `[Error: Audio demasiado grande]` - Chunk > 10 MB
- `[Error: Formato de audio no soportado]` - Formato inválido
- `[Error del servicio de transcripción]` - Error en Google API

#### Códigos de Cierre

| Código | Razón                     |
|--------|---------------------------|
| 1000   | Cierre normal             |
| 1013   | Servidor saturado (>100 conexiones) |

---

### 🔧 WebSocket de Diagnóstico

**Endpoint:** `ws://localhost:8000/ws/diagnostic/{session_id}`

**Propósito:** Actualizaciones en tiempo real durante diagnóstico

#### Ejemplo de Uso

```javascript
const sessionId = 'session_20250113_161145_a1b2c3d4';
const ws = new WebSocket(`ws://localhost:8000/ws/diagnostic/${sessionId}`);

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'progress':
            console.log('Progreso:', data.message);
            break;
        case 'hypothesis':
            console.log('Hipótesis:', data.hypothesis);
            break;
        case 'complete':
            console.log('Diagnóstico completo:', data.results);
            break;
        case 'error':
            console.error('Error:', data.message);
            break;
    }
};
```

#### Mensajes del Servidor

##### 1. Mensaje de Progreso
```json
{
    "type": "progress",
    "message": "✔ Identificando rails..."
}
```

##### 2. Hipótesis Generada
```json
{
    "type": "hypothesis",
    "hypothesis": {
        "hypothesis_id": "hyp_20250113_161200_123456",
        "overall_confidence": 0.78,
        "layer1": {
            "voltage_rail": "3V3",
            "component_id": "U1",
            "functional_block": "Power"
        },
        "layer2": {
            "fault_cause": "sin_voltaje",
            "reasoning": "3V3 ausente → Regulador falló...",
            "evidence": ["Rail 3V3 identificado", "Regulador probable: AMS1117"]
        },
        "layer3": {
            "functional_impact": "Radio no enciende, placa no arranca",
            "impact_level": "crítico",
            "affected_features": ["WiFi", "Bluetooth", "RF", "MCU"]
        },
        "next_steps": [
            "Medir voltaje en rail 3V3",
            "Verificar continuidad desde fuente",
            "Revisar regulador de voltaje"
        ],
        "test_points": ["TP3", "TP_3V3", "Salida del regulador U1"]
    }
}
```

##### 3. Diagnóstico Completo
```json
{
    "type": "complete",
    "results": {
        "session_id": "session_20250113_161145_a1b2c3d4",
        "board_model": "ESP32-DevKitC",
        "hypotheses": [...],
        "report_text": "═══════════════════...",
        "status": "completada"
    }
}
```

##### 4. Error
```json
{
    "type": "error",
    "message": "Descripción del error"
}
```

---

## REST API - Salud del Sistema

### GET /health

**Propósito:** Verificar que el servidor está funcionando

#### Request
```bash
curl http://localhost:8000/health
```

#### Response
```json
{
    "status": "ok",
    "active_connections": 5,
    "subtitle_support": true,
    "diagnostic_support": true
}
```

**Campos:**
- `status`: Estado del servidor (`ok`)
- `active_connections`: Número de conexiones WebSocket activas
- `subtitle_support`: Si el módulo de subtítulos está disponible
- `diagnostic_support`: Si el módulo de diagnóstico está disponible

---

## REST API - Subtítulos

### POST /api/subtitles/process

**Propósito:** Procesar y optimizar archivos de subtítulos

#### Request

```bash
curl -X POST http://localhost:8000/api/subtitles/process \
  -F "file=@movie.srt" \
  -F "validate=true" \
  -F "optimize=true" \
  -F "output_format=srt"
```

**Parámetros:**
- `file` (required): Archivo de subtítulos (SRT, VTT, ASS, SSA)
- `validate` (optional, default: `true`): Validar el archivo
- `optimize` (optional, default: `true`): Optimizar el archivo
- `output_format` (optional, default: `srt`): Formato de salida (`srt` o `vtt`)

#### Response (Success)

```json
{
    "success": true,
    "stats": {
        "total_subtitles": 250,
        "total_duration_seconds": 3600,
        "average_duration": 2.5,
        "format": "srt"
    },
    "validation_issues": [
        {
            "severity": "warning",
            "subtitle_index": 42,
            "message": "Línea muy larga (>42 caracteres)"
        }
    ],
    "optimization_changes": 15,
    "download_url": "/api/subtitles/download/a1b2c3d4-5678-90ef"
}
```

#### Response (Error)

```json
{
    "detail": "Formato no soportado: .txt. Usa .srt, .vtt, .ass o .ssa"
}
```

**Códigos de estado:**
- `200` - Éxito
- `400` - Formato no soportado o error de procesamiento
- `500` - Error interno del servidor
- `503` - Módulo no disponible

---

### GET /api/subtitles/download/{download_id}

**Propósito:** Descargar archivo de subtítulos procesado

#### Request

```bash
curl -O -J http://localhost:8000/api/subtitles/download/a1b2c3d4-5678-90ef
```

#### Response
- **Success:** Archivo de subtítulos (Content-Type: `text/plain`)
- **Error 404:** `{"detail": "Archivo no encontrado o expirado"}`

---

### POST /api/subtitles/validate

**Propósito:** Validar archivo de subtítulos sin modificarlo

#### Request

```bash
curl -X POST http://localhost:8000/api/subtitles/validate \
  -F "file=@movie.srt"
```

#### Response

```json
{
    "success": true,
    "stats": {
        "total_subtitles": 250,
        "total_duration_seconds": 3600,
        "average_duration": 2.5,
        "format": "srt"
    },
    "issues": [
        {
            "severity": "error",
            "subtitle_index": 10,
            "message": "Superposición de subtítulos"
        },
        {
            "severity": "warning",
            "subtitle_index": 42,
            "message": "Línea muy larga"
        }
    ],
    "total_issues": 2,
    "errors": 1,
    "warnings": 1,
    "info": 0
}
```

---

## REST API - Diagnóstico Electrónico

### POST /api/diagnostic/session

**Propósito:** Crear una nueva sesión de diagnóstico

#### Request

```bash
curl -X POST http://localhost:8000/api/diagnostic/session \
  -H "Content-Type: application/json" \
  -d '{
    "board_model": "ESP32-DevKitC",
    "diagnostic_style": "técnico"
  }'
```

**Parámetros:**
- `board_model` (required): Modelo de la placa (ej: "ESP32-DevKitC", "Arduino Uno")
- `diagnostic_style` (optional, default: "técnico"): Estilo de diagnóstico
  - `"técnico"` - Directo y práctico
  - `"ingeniero"` - Causal y metodológico
  - `"forense"` - Exhaustivo y detallado
- `session_id` (optional): ID personalizado para la sesión

#### Response

```json
{
    "success": true,
    "session_id": "session_20250113_161145_a1b2c3d4",
    "board_model": "ESP32-DevKitC",
    "style": "técnico"
}
```

**Códigos de estado:**
- `200` - Sesión creada exitosamente
- `429` - Rate limit excedido (demasiadas solicitudes)
- `500` - Error interno
- `503` - Módulo de diagnóstico no disponible

---

### POST /api/diagnostic/upload

**Propósito:** Subir imagen a una sesión de diagnóstico

#### Request

```bash
curl -X POST http://localhost:8000/api/diagnostic/upload \
  -F "file=@board_front.jpg" \
  -F "session_id=session_20250113_161145_a1b2c3d4" \
  -F "image_type=frontal"
```

**Parámetros:**
- `file` (required): Imagen de la placa (JPG, PNG)
- `session_id` (required): ID de la sesión
- `image_type` (optional, default: "frontal"): Tipo de imagen
  - `"frontal"` - Vista frontal
  - `"backside"` - Vista trasera
  - `"closeup"` - Acercamiento
  - `"microscope"` - Microscopio
  - `"rf_area"` - Área RF
  - `"power_area"` - Área de potencia

#### Response

```json
{
    "success": true,
    "image_id": "img_1",
    "session_id": "session_20250113_161145_a1b2c3d4",
    "image_type": "frontal"
}
```

**Códigos de estado:**
- `200` - Imagen subida exitosamente
- `400` - Parámetros inválidos o formato de imagen incorrecto
- `404` - Sesión no encontrada
- `500` - Error interno

---

### POST /api/diagnostic/analyze

**Propósito:** Iniciar análisis de diagnóstico

#### Request

```bash
curl -X POST http://localhost:8000/api/diagnostic/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_20250113_161145_a1b2c3d4"
  }'
```

**Parámetros:**
- `session_id` (required): ID de la sesión a analizar

#### Response

```json
{
    "success": true,
    "session_id": "session_20250113_161145_a1b2c3d4",
    "status": "analysis_started",
    "message": "El análisis ha comenzado. Conéctate vía WebSocket para recibir actualizaciones."
}
```

**Nota:** Para recibir actualizaciones en tiempo real, conectarse al WebSocket:
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/diagnostic/${session_id}`);
```

---

### GET /api/diagnostic/session/{session_id}

**Propósito:** Obtener resultados completos de una sesión

#### Request

```bash
curl http://localhost:8000/api/diagnostic/session/session_20250113_161145_a1b2c3d4
```

#### Response

```json
{
    "session_id": "session_20250113_161145_a1b2c3d4",
    "board_model": "ESP32-DevKitC",
    "creation_time": "2025-01-13T16:11:45.123456",
    "images": [
        {
            "image_id": "img_1",
            "path": "/tmp/diagnostic_session_xxx/frontal_abc123.jpg",
            "type": "frontal",
            "timestamp": "2025-01-13T16:12:00.000000"
        }
    ],
    "hypotheses": [
        {
            "hypothesis_id": "hyp_20250113_161200_123456",
            "confidence": 0.78,
            "layer1": {
                "rail": "3V3",
                "component": "U1"
            },
            "layer2": {
                "cause": "sin_voltaje",
                "reasoning": "3V3 ausente → Regulador falló..."
            },
            "layer3": {
                "impact": "Radio no enciende, placa no arranca",
                "level": "crítico"
            },
            "next_steps": [
                "Medir voltaje en rail 3V3",
                "Verificar continuidad desde fuente"
            ],
            "test_points": ["TP3", "TP_3V3", "Salida del regulador U1"]
        }
    ],
    "status": "completada",
    "style": "técnico",
    "report_text": "═══════════════════\n   REPORTE DE DIAGNÓSTICO...\n═══════════════════"
}
```

---

### GET /api/diagnostic/sessions

**Propósito:** Listar todas las sesiones de diagnóstico

#### Request

```bash
curl http://localhost:8000/api/diagnostic/sessions
```

#### Response

```json
{
    "success": true,
    "count": 3,
    "sessions": [
        {
            "session_id": "session_20250113_161145_a1b2c3d4",
            "board_model": "ESP32-DevKitC",
            "images_count": 2,
            "hypotheses_count": 1,
            "status": "completada",
            "style": "técnico",
            "creation_time": "2025-01-13T16:11:45.123456"
        },
        {
            "session_id": "session_20250113_150000_b2c3d4e5",
            "board_model": "Arduino Uno",
            "images_count": 1,
            "hypotheses_count": 0,
            "status": "en_progreso",
            "style": "ingeniero",
            "creation_time": "2025-01-13T15:00:00.000000"
        }
    ]
}
```

---

### DELETE /api/diagnostic/session/{session_id}

**Propósito:** Eliminar una sesión y sus archivos temporales

#### Request

```bash
curl -X DELETE http://localhost:8000/api/diagnostic/session/session_20250113_161145_a1b2c3d4
```

#### Response

```json
{
    "success": true,
    "message": "Sesión session_20250113_161145_a1b2c3d4 eliminada correctamente"
}
```

---

### POST /api/diagnostic/cleanup

**Propósito:** Limpiar sesiones y archivos antiguos

#### Request

```bash
curl -X POST "http://localhost:8000/api/diagnostic/cleanup?max_age_hours=24"
```

**Parámetros:**
- `max_age_hours` (optional, default: 24): Edad máxima en horas

#### Response

```json
{
    "success": true,
    "sessions_removed": 5,
    "directories_removed": 5,
    "cutoff_time": "2025-01-12T16:11:45.123456"
}
```

---

## Códigos de Error

### Códigos HTTP

| Código | Significado | Cuándo Ocurre |
|--------|-------------|---------------|
| 200 | OK | Solicitud exitosa |
| 400 | Bad Request | Parámetros inválidos, formato incorrecto |
| 404 | Not Found | Recurso no encontrado (sesión, archivo) |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Error interno del servidor |
| 503 | Service Unavailable | Módulo no disponible |

### Formato de Error

```json
{
    "detail": "Descripción del error"
}
```

### Errores Comunes

#### 1. Rate Limit Excedido
```json
{
    "detail": "Demasiadas solicitudes. Por favor, espera un momento."
}
```

**Solución:** Esperar 60 segundos antes de reintentar

#### 2. Sesión No Encontrada
```json
{
    "detail": "Sesión session_xxx no encontrada"
}
```

**Solución:** Verificar el ID de la sesión o crear una nueva

#### 3. Módulo No Disponible
```json
{
    "detail": "Módulo de diagnóstico no disponible"
}
```

**Solución:** Verificar que las dependencias estén instaladas

#### 4. Formato de Archivo Inválido
```json
{
    "detail": "Formato no soportado: .txt. Usa .srt, .vtt, .ass o .ssa"
}
```

**Solución:** Usar formato soportado

---

## Rate Limiting

### Límites Globales

- **30 solicitudes por minuto** por dirección IP
- **100 conexiones WebSocket simultáneas** en total
- **10 MB** tamaño máximo por chunk de audio
- **Cleanup automático** de sesiones >24 horas

### Cabeceras de Rate Limit

Actualmente no se envían cabeceras de rate limit, pero se puede agregar en el futuro:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1673626800
```

---

## Ejemplos de Integración

### Ejemplo 1: Cliente JavaScript Completo

```javascript
// Transcripción en tiempo real
class IyariEarClient {
    constructor(serverUrl = 'ws://localhost:8000/ws') {
        this.serverUrl = serverUrl;
        this.ws = null;
    }
    
    connect(language = 'es-ES') {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(this.serverUrl);
            
            this.ws.onopen = () => {
                // Configurar idioma
                this.ws.send(JSON.stringify({
                    type: 'language',
                    language: language
                }));
                resolve();
            };
            
            this.ws.onerror = (error) => {
                reject(error);
            };
        });
    }
    
    sendAudio(audioBlob) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(audioBlob);
        }
    }
    
    onTranscription(callback) {
        this.ws.onmessage = (event) => {
            callback(event.data);
        };
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Uso
const client = new IyariEarClient();
await client.connect('es-ES');
client.onTranscription((text) => {
    console.log('Transcrito:', text);
});
```

### Ejemplo 2: Cliente Python

```python
import requests
import json

# Crear sesión de diagnóstico
response = requests.post(
    'http://localhost:8000/api/diagnostic/session',
    json={
        'board_model': 'ESP32-DevKitC',
        'diagnostic_style': 'técnico'
    }
)
session_data = response.json()
session_id = session_data['session_id']

# Subir imagen
with open('board_front.jpg', 'rb') as f:
    files = {'file': f}
    data = {
        'session_id': session_id,
        'image_type': 'frontal'
    }
    response = requests.post(
        'http://localhost:8000/api/diagnostic/upload',
        files=files,
        data=data
    )

# Analizar
response = requests.post(
    'http://localhost:8000/api/diagnostic/analyze',
    json={'session_id': session_id}
)

# Obtener resultados
response = requests.get(
    f'http://localhost:8000/api/diagnostic/session/{session_id}'
)
results = response.json()
print(results['report_text'])
```

### Ejemplo 3: cURL Script Completo

```bash
#!/bin/bash

# 1. Crear sesión
SESSION=$(curl -s -X POST http://localhost:8000/api/diagnostic/session \
  -H "Content-Type: application/json" \
  -d '{"board_model":"ESP32-DevKitC","diagnostic_style":"técnico"}' \
  | jq -r '.session_id')

echo "Sesión creada: $SESSION"

# 2. Subir imagen
curl -s -X POST http://localhost:8000/api/diagnostic/upload \
  -F "file=@board.jpg" \
  -F "session_id=$SESSION" \
  -F "image_type=frontal"

# 3. Analizar
curl -s -X POST http://localhost:8000/api/diagnostic/analyze \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"$SESSION\"}"

# 4. Esperar un momento
sleep 2

# 5. Obtener resultados
curl -s http://localhost:8000/api/diagnostic/session/$SESSION \
  | jq '.report_text' -r
```

---

## Preguntas Frecuentes

### ¿Necesito autenticación?
No. El sistema está diseñado para uso local sin autenticación.

### ¿Puedo usar en producción?
Actualmente está diseñado para uso local. Para producción, se recomienda:
- Agregar autenticación (API keys, OAuth)
- Configurar HTTPS/WSS
- Implementar rate limiting más robusto
- Usar base de datos para sesiones

### ¿Qué pasa si el servidor se reinicia?
Las sesiones en memoria se pierden. Los archivos temporales permanecen hasta el cleanup automático.

### ¿Puedo integrar con otros sistemas?
Sí, la API REST es estándar y puede ser llamada desde cualquier lenguaje o framework.

---

<div align="center">

**Iyari-ear API** — *Construye lo que imagines*

**Creado con cariño para una amiga. Compartido con amor para el mundo.**

✨ 2025 ✨

</div>

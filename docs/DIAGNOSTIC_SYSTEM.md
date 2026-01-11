# 🔧 Sistema de Diagnóstico Electrónico Real

## Visión General

El sistema de diagnóstico electrónico de Iyari-ear es una herramienta profesional diseñada para técnicos de reparación de electrónica. No es solo reconocimiento visual — es **razonamiento causal** basado en 3 capas de análisis.

## Filosofía del Sistema

### El Problema que Resuelve

Cuando un técnico diagnostica una placa:
- ❌ No puede sostener la placa en el aire mientras trabaja
- ❌ Necesita ambas manos para soldador, multímetro, etc.
- ❌ Necesita comparar con otras placas
- ❌ Necesita documentar el proceso

### La Solución: Modo Asíncrono

```
📸 Foto → Sueltas la placa → 🧠 App procesa → 📋 Diagnóstico completo
```

Este flujo permite:
- ✔ Usar ambas manos para trabajar
- ✔ Usar soldador / aire caliente
- ✔ Tomar mediciones con multímetro
- ✔ Comparar con placas "golden"
- ✔ Generar reportes profesionales

## Arquitectura del Sistema

### Las 3 Capas de Diagnóstico

El sistema piensa como un técnico real, progresando desde localización hasta consecuencias:

#### Capa 1: Localización 📍
**"¿Dónde está la falla?"**

- Topología de la placa
- Bloque funcional (Power, MCU, RF, USB)
- Rail de voltaje (3V3, 5V, VBAT)
- Componente específico (U1, C15, etc.)

```python
DiagnosticLayer1(
    component_id="U1",
    component_type=ComponentType.VOLTAGE_REGULATOR,
    voltage_rail="3V3",
    functional_block="Power",
    confidence=0.8
)
```

#### Capa 2: Causa 🔍
**"¿Por qué existe la falla?"**

- Análisis causal
- Evidencia recolectada
- Razonamiento lógico
- Modos de falla conocidos

Causas comunes:
- Sin voltaje
- Cortocircuito
- Daño ESD
- Sobrecalentamiento
- Corrosión
- Pérdida de señal

```python
DiagnosticLayer2(
    fault_cause=FaultCause.NO_VOLTAGE,
    evidence=[
        "Rail 3V3 identificado",
        "Regulador probable: AMS1117"
    ],
    reasoning="Si 3V3 está ausente, probable falla en regulador de voltaje",
    confidence=0.75
)
```

#### Capa 3: Consecuencia ⚡
**"¿Qué rompe funcionalmente?"**

- Impacto en funcionalidad
- Nivel de severidad (Crítico, Alto, Medio, Bajo)
- Características afectadas
- Efectos en cascada

```python
DiagnosticLayer3(
    functional_impact="Radio no enciende, placa no arranca",
    impact_level=ImpactLevel.CRITICAL,
    affected_features=["WiFi", "Bluetooth", "RF", "MCU"],
    cascading_effects=[]
)
```

### Ejemplo de Diagnóstico Completo

**Entrada:** Placa ESP32-DevKit que no arranca

**Proceso:**

1. **Capa 1 - Localización:**
   - Rail identificado: `3V3`
   - Componente: `Regulador U1 (AMS1117)`
   - Bloque: `Power Supply`

2. **Capa 2 - Causa:**
   - Falla: `Sin voltaje en 3V3`
   - Razonamiento: "Si el regulador AMS1117 falla, no hay salida de 3.3V"
   - Evidencia: "Rail 3V3 ausente, regulador identificado"

3. **Capa 3 - Consecuencia:**
   - Impacto: **CRÍTICO**
   - Efecto: "Radio WiFi no enciende, MCU no arranca"
   - Afecta: WiFi, Bluetooth, MCU, RF

**Próximos pasos:**
- Medir voltaje en TP3 (punto de prueba 3V3)
- Verificar continuidad desde USB_5V
- Revisar AMS1117 con multímetro
- Si está en corto, reemplazar regulador

## Estilos de Diagnóstico

El sistema soporta 3 estilos según el nivel de detalle:

### 1. Técnico (Práctico, Resolutivo)
**Para:** Reparadores de taller que necesitan soluciones rápidas

- Diagnóstico directo
- Pasos prácticos
- Enfocado en resolver
- Lenguaje simple

**Ejemplo:**
```
"3V3 no sale. Revisa regulador U1.
Mide en TP3. Si da 0V, regulador muerto.
Cambia el AMS1117 y listo."
```

### 2. Ingeniero (Causal, Metodológico)
**Para:** Ingenieros que necesitan entender la causa raíz

- Análisis topológico
- Razonamiento causal
- Metodología sistemática
- Documentación técnica

**Ejemplo:**
```
"Análisis de topología de power rail:
USB_5V → AMS1117 → 3V3_NET → MCU_VDD
Punto de falla identificado en regulador.
Verificar secuencia de encendido y enable signal."
```

### 3. Forense (Detallista, Profundo)
**Para:** Análisis exhaustivos, control de calidad, investigación

- Análisis detallado de todas las rutas
- Documentación completa
- Múltiples hipótesis
- Análisis de probabilidades

**Ejemplo:**
```
"Análisis multi-factor:
- Path 1: USB_5V presente (verificado)
- Path 2: AMS1117 enable activo (requiere verificación)
- Path 3: Salida 3V3 ausente (confirmado)
- Path 4: Load capacitors C15, C16 en buenas condiciones
Conclusión: Regulador AMS1117 en circuito abierto interno.
Probabilidad: 87.3%"
```

## Uso del Sistema

### Interfaz Web

1. **Acceder a la interfaz:**
   ```
   http://localhost:8000/diagnostic
   ```

2. **Crear nueva sesión:**
   - Modelo de placa: `ESP32-DevKit`, `iPhone 12`, `DJI Phantom 4`
   - Estilo: Técnico / Ingeniero / Forense
   - Click "Crear Sesión"

3. **Subir imágenes (Multi-shot):**
   - Frontal
   - Reverso (backside)
   - Primer plano (closeup)
   - Microscopio
   - Área RF
   - Área de potencia

4. **Analizar:**
   - Click "Analizar Imágenes"
   - Ver progreso en tiempo real:
     ```
     ✔ Identificando rails...
     ✔ 3V3 encontrado
     ✔ Región RF detectada
     ✔ Posible regulador AMS1117
     ✔ Generando hipótesis...
     ```

5. **Recibir diagnóstico:**
   - Hipótesis con confianza
   - 3 capas de análisis
   - Próximos pasos
   - Puntos de prueba

6. **Exportar reporte:**
   - JSON (para sistemas)
   - Texto (para imprimir/compartir)

### API REST

#### Crear Sesión

```bash
curl -X POST http://localhost:8000/api/diagnostic/session \
  -H "Content-Type: application/json" \
  -d '{
    "board_model": "ESP32-DevKit",
    "diagnostic_style": "técnico"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "session_id": "session_20260111_161645",
  "board_model": "ESP32-DevKit",
  "style": "técnico"
}
```

#### Subir Imagen

```bash
curl -X POST http://localhost:8000/api/diagnostic/upload \
  -F "file=@placa.jpg" \
  -F "session_id=session_20260111_161645" \
  -F "image_type=frontal"
```

**Respuesta:**
```json
{
  "success": true,
  "image_id": "img_1",
  "session_id": "session_20260111_161645",
  "image_type": "frontal"
}
```

#### Iniciar Análisis

```bash
curl -X POST http://localhost:8000/api/diagnostic/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_20260111_161645"
  }'
```

#### Obtener Resultados

```bash
curl http://localhost:8000/api/diagnostic/session/session_20260111_161645
```

**Respuesta:**
```json
{
  "session_id": "session_20260111_161645",
  "board_model": "ESP32-DevKit",
  "status": "completada",
  "images": [...],
  "hypotheses": [
    {
      "hypothesis_id": "hyp_001",
      "confidence": 0.845,
      "layer1": {
        "rail": "3V3",
        "component": "U1"
      },
      "layer2": {
        "cause": "sin_voltaje",
        "reasoning": "..."
      },
      "layer3": {
        "impact": "Radio no enciende, placa no arranca",
        "level": "crítico"
      },
      "next_steps": [...]
    }
  ],
  "report_text": "..."
}
```

### WebSocket para Tiempo Real

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/diagnostic/session_20260111_161645');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'progress') {
    console.log('Progreso:', data.message);
  } else if (data.type === 'hypothesis') {
    console.log('Hipótesis:', data.hypothesis);
  } else if (data.type === 'complete') {
    console.log('Diagnóstico completo:', data.results);
  }
};
```

## Metodologías de Diagnóstico

### Rail-First (Implementado)

Análisis desde la fuente de poder hacia los consumidores:

```
USB_5V → Regulador → 3V3 → MCU → Periféricos
         ↓
      Punto de falla
```

**Ventajas:**
- No requiere hardware extra
- Funciona solo con foto + razonamiento
- Altamente efectivo para fallas de power

### A/B Comparison (Base implementada)

Comparar placa problemática con "Golden Board":

```
Golden Board:  [Foto]  ✓ Todo OK
Problem Board: [Foto]  ✗ Falta componente / Daño visible
```

**Ventajas:**
- Visual e intuitivo
- No requiere mediciones
- Perfecto para componentes faltantes/dañados

### Metodologías Futuras

#### Consumo (Requiere hardware)
- Medición de corriente por rail
- Detección de cortocircuitos
- Análisis térmico

#### Topológico
- Análisis de bloques funcionales
- Dependencias entre subsistemas
- Rutas de señal

## Casos de Uso Reales

### Taller de Reparación

**Escenario:** Cliente trae iPhone 12 que no carga

```
1. Técnico crea sesión: "iPhone 12 - No carga"
2. Toma 3 fotos:
   - Frontal
   - Área de carga
   - Conector Lightning
3. App analiza y diagnostica:
   "Posible falla en Tristar IC (U2).
    Verificar voltaje en PP_VDD_MAIN.
    Medir resistencia en diodos de carga."
4. Técnico confirma con multímetro
5. Exporta reporte para cotización
```

**Tiempo ahorrado:** 20-30 minutos de inspección visual

### Soporte Remoto

**Escenario:** Cliente en otra ciudad necesita diagnóstico

```
1. Cliente toma fotos de la placa
2. Envía fotos vía email/WhatsApp
3. Técnico crea sesión remota
4. Sistema genera diagnóstico
5. Técnico envía cotización y pasos a seguir
```

**Beneficio:** Soporte sin envío físico de equipos

### Capacitación

**Escenario:** Enseñar patrones de fallas comunes

```
1. Instructor muestra 10 placas con fallas conocidas
2. Estudiantes practican diagnóstico
3. Sistema valida el razonamiento
4. Retroalimentación inmediata
```

**Beneficio:** Aprendizaje acelerado con feedback

### Documentación y Auditoría

**Escenario:** Documentar reparación para garantía

```
1. Foto del problema inicial
2. Diagnóstico del sistema
3. Fotos del proceso de reparación
4. Foto de verificación final
5. Reporte completo exportado
```

**Beneficio:** Historial completo y trazable

## Arquitectura Técnica

### Stack Tecnológico

- **Backend:** Python 3.7+ con FastAPI
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **WebSocket:** Para actualizaciones en tiempo real
- **Almacenamiento:** Sesiones en memoria + archivos temporales

### Módulos

```
diagnostic_engine.py
├── DiagnosticEngine       # Motor principal
├── DiagnosticSession      # Sesión de diagnóstico
├── DiagnosticHypothesis   # Hipótesis de 3 capas
├── Component              # Componentes detectados
├── VoltageRail            # Rails de voltaje
└── FunctionalBlock        # Bloques funcionales
```

### Flujo de Datos

```
1. Cliente → POST /api/diagnostic/session
   ↓
2. Servidor crea DiagnosticSession
   ↓
3. Cliente → POST /api/diagnostic/upload (imágenes)
   ↓
4. Servidor almacena en /tmp/diagnostic_{session_id}/
   ↓
5. Cliente → POST /api/diagnostic/analyze
   ↓
6. Servidor conecta WebSocket
   ↓
7. Servidor genera hipótesis (3 capas)
   ↓
8. Servidor envía progreso vía WebSocket
   ↓
9. Cliente muestra diagnóstico en tiempo real
   ↓
10. Cliente exporta reporte (JSON/TXT)
```

## Seguridad y Límites

### Límites Implementados

- **Tamaño de imagen:** Sin límite explícito (usar validación de navegador)
- **Sesiones simultáneas:** Ilimitadas en memoria
- **Archivos temporales:** Se almacenan en `/tmp/diagnostic_{session_id}/`

### Consideraciones de Seguridad

1. **Validación de archivos:**
   - Solo imágenes (JPG, PNG, WebP)
   - Validación de Content-Type

2. **Aislamiento de sesiones:**
   - Cada sesión tiene su propio directorio
   - IDs únicos basados en timestamp

3. **Limpieza:**
   - Archivos temporales en `/tmp/` (se limpian en reinicio)
   - Considerar implementar limpieza automática

## Extensibilidad

### Integraciones Futuras

#### 1. Machine Learning / Computer Vision
```python
# Placeholder para modelo de ML
def detect_components_ml(image_path: str) -> List[Component]:
    """Usar YOLO/Detectron2 para detectar componentes"""
    # Implementación futura
    pass
```

#### 2. Base de Datos de Componentes
```python
# Expandir biblioteca de componentes
component_library = {
    "AMS1117": {...},
    "LM1117": {...},
    "ESP32": {...},
    "STM32": {...},
    # ... miles de componentes
}
```

#### 3. OCR para Referencias de Componentes
```python
# Leer texto en PCB
def ocr_component_labels(image_path: str) -> List[str]:
    """Usar Tesseract/EasyOCR para leer etiquetas"""
    pass
```

#### 4. Comparación A/B Visual
```python
# Comparar con golden board
def compare_boards(problem_img: str, golden_img: str) -> List[Difference]:
    """Detectar diferencias visuales entre placas"""
    pass
```

## Roadmap

### Versión Actual (v1.0)
- ✅ Sistema de 3 capas
- ✅ Estilos de diagnóstico
- ✅ Multi-shot
- ✅ Modo asíncrono
- ✅ API REST
- ✅ WebSocket tiempo real
- ✅ Reportes exportables

### Próximas Versiones

**v1.1 - ML Integration**
- Detección automática de componentes con YOLO
- OCR para referencias de componentes
- Clasificación de tipos de placas

**v1.2 - Golden Board Comparison**
- Sistema de comparación A/B visual
- Biblioteca de placas de referencia
- Detección de diferencias automática

**v1.3 - Hardware Integration**
- Integración con multímetros BLE
- Lectura de voltajes en tiempo real
- Correlación de mediciones con diagnóstico

**v2.0 - Enterprise Features**
- Base de datos persistente
- Múltiples usuarios
- Historial de reparaciones
- Analytics y estadísticas
- Marketplace de diagnósticos

## Contribuir

### Áreas de Mejora

1. **Biblioteca de Componentes:**
   - Agregar más componentes comunes
   - Patrones de falla típicos
   - Valores nominales

2. **Modelos de ML:**
   - Entrenar YOLO para detección de componentes
   - Dataset de placas etiquetadas

3. **UI/UX:**
   - Mejorar visualización de hipótesis
   - Herramientas de anotación en imágenes
   - Modo oscuro mejorado

4. **Testing:**
   - Tests unitarios para diagnostic_engine
   - Tests de integración para API
   - Tests E2E con Playwright

## Licencia

Parte del proyecto Iyari-ear — Creado con cariño para ayudar a técnicos de verdad.

---

> **"No es reconocimiento. Es razonamiento causal."**
> 
> Este sistema piensa como un técnico de taller, no como un tutorial de YouTube.

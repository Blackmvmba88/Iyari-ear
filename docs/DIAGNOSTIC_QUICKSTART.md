# 🚀 Guía de Inicio Rápido - Sistema de Diagnóstico

## En 60 Segundos

```bash
# 1. Inicia el servidor
python main.py

# 2. Abre en tu navegador
http://localhost:8000/diagnostic

# 3. ¡Prueba el Demo!
Click en "▶️ Run Demo (ESP32 3V3 failure)"

# O crea una sesión manual:
# - Modelo: ESP32-DevKit
# - Estilo: Técnico
# - [Crear Sesión]
# - Arrastra imágenes de tu placa
# - [Analizar Imágenes]
# - Recibe diagnóstico en tiempo real
```

## 🎬 Demo Automático (¡NUEVO!)

La forma más rápida de ver el sistema en acción:

1. Abre http://localhost:8000/diagnostic
2. Click en **"▶️ Run Demo (ESP32 3V3 failure)"**
3. El sistema automáticamente:
   - ✅ Crea una sesión de demo
   - ✅ Simula carga de imagen
   - ✅ Ejecuta análisis completo
   - ✅ Muestra diagnóstico en tiempo real

**Duración:** ~10 segundos  
**Resultado:** Diagnóstico completo de falla 3V3 en ESP32

### ¿Qué verás en el demo?

```
📸 Simulando captura de imágenes...
✅ Demo iniciado - Sesión: session_xxx
✅ Imagen frontal cargada
🔍 Iniciando análisis de diagnóstico...

✔ Identificando rails...
✔ 3V3 encontrado
✔ 5V encontrado
✔ Región RF detectada
✔ Posible regulador AMS1117
✔ Analizando topología...
✔ Generando hipótesis...

💡 Hipótesis de Diagnóstico (Confianza: 84.5%)
[Diagnóstico completo de 3 capas]
```

## Ejemplo Completo

### Escenario: Placa ESP32 que no arranca

**Paso 1:** Crear sesión
```
Modelo: ESP32-DevKit
Estilo: Técnico (resolutivo)
```

**Paso 2:** Subir fotos
- Frontal de la placa
- Área de regulador de voltaje

**Paso 3:** Analizar

El sistema procesa y muestra en tiempo real:
```
✔ Identificando rails...
✔ 3V3 encontrado
✔ 5V encontrado
✔ Posible regulador AMS1117
✔ Generando hipótesis...
```

**Paso 4:** Recibir diagnóstico

```
💡 Hipótesis de Diagnóstico (Confianza: 84.5%)

📍 CAPA 1 - LOCALIZACIÓN:
   • Rail: 3V3
   • Componente: Regulador U1 (AMS1117)
   • Bloque: Power Supply

🔍 CAPA 2 - CAUSA:
   • Causa: sin_voltaje
   • Razonamiento: Si 3V3 está ausente, probable falla en regulador
   • Evidencia: Rail 3V3 identificado, Regulador AMS1117 detectado

⚡ CAPA 3 - CONSECUENCIA:
   • Impacto: CRÍTICO
   • Efecto: Radio no enciende, placa no arranca
   • Afecta: WiFi, Bluetooth, RF, MCU

🔧 PRÓXIMOS PASOS:
   • Medir voltaje en TP3
   • Verificar continuidad desde USB_5V
   • Revisar regulador AMS1117
   • Prioridad alta: Resolver antes de continuar

📊 PUNTOS DE PRUEBA: TP3, TP_3V3, Salida del regulador U1
```

**Paso 5:** Exportar reporte
- Formato JSON para sistemas
- Formato texto para imprimir

## Comandos Útiles

### Iniciar servidor
```bash
python main.py
```

### Verificar que el diagnóstico está disponible
```bash
curl http://localhost:8000/health
```

Respuesta:
```json
{
  "status": "ok",
  "diagnostic_support": true
}
```

### Crear sesión vía API
```bash
curl -X POST http://localhost:8000/api/diagnostic/session \
  -H "Content-Type: application/json" \
  -d '{"board_model": "ESP32", "diagnostic_style": "técnico"}'
```

### Listar sesiones
```bash
curl http://localhost:8000/api/diagnostic/sessions
```

## Tips Rápidos

### 🎯 Mejores Prácticas

**Para mejores resultados:**
- Sube 2-3 fotos de diferentes ángulos
- Incluye primer plano del área problemática
- Usa buena iluminación
- Enfoca componentes claramente

**Tipos de imagen recomendados:**
1. **Frontal:** Vista general de la placa
2. **Área de potencia:** Reguladores, capacitores de power
3. **Área RF:** Si hay problemas de radio/conectividad
4. **Microscopio:** Para daños pequeños o corrosión

### 🔧 Flujo de Trabajo Profesional

```
📸 Toma fotos → Suelta la placa → Trabaja con ambas manos
                     ↓
              App procesa en background
                     ↓
              Recibes diagnóstico completo
                     ↓
              Verificas con multímetro
                     ↓
              Reparas y documentas
```

### ⚡ Atajos

**En la interfaz web:**
- Arrastra y suelta múltiples imágenes a la vez
- El análisis inicia automáticamente con WebSocket
- Puedes exportar mientras ves el diagnóstico

**Con la API:**
- Crea sesión una vez, sube múltiples imágenes
- WebSocket te notifica cuando hay nuevas hipótesis
- Exporta JSON para integrar con tu sistema

## Solución de Problemas

### El servidor no inicia
```bash
# Instala dependencias
pip install -r requirements.txt

# Verifica que el puerto esté libre
lsof -i :8000

# Usa otro puerto si es necesario
PORT=8001 python main.py
```

### "Módulo de diagnóstico no disponible"
```bash
# Verifica que diagnostic_engine.py exista
ls diagnostic_engine.py

# Prueba el import
python -c "from diagnostic_engine import DiagnosticEngine; print('OK')"
```

### Las imágenes no se cargan
- Verifica que sean JPG, PNG o WebP
- Asegúrate de crear una sesión primero
- Revisa la consola del navegador (F12)

## Próximos Pasos

1. **Lee la documentación completa:** `docs/DIAGNOSTIC_SYSTEM.md`
2. **Prueba con tus placas reales**
3. **Exporta reportes y comparte feedback**
4. **Integra con tu flujo de trabajo**

## Soporte

- **Reportar bugs:** GitHub Issues
- **Preguntas:** GitHub Discussions
- **Ejemplos:** Ver carpeta `examples/` (próximamente)

---

> **¿Listo para diagnosticar como un pro?** 🔧
> 
> Accede a: http://localhost:8000/diagnostic

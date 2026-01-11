# 🎨 Estilos de Diagnóstico

El sistema de diagnóstico Iyari-ear ofrece tres estilos diferentes, cada uno adaptado a distintos niveles de experiencia y necesidades de documentación.

## 📊 Comparación Rápida

| Característica | Técnico | Ingeniero | Forense |
|---------------|---------|-----------|---------|
| **Longitud** | Corto (~80 chars) | Medio (~300 chars) | Largo (~800+ chars) |
| **Tono** | Directo, práctico | Causal, metodológico | Exhaustivo, detallado |
| **Evidencia** | Mínima (2-3 items) | Moderada (4-5 items) | Completa (5+ items) |
| **Uso ideal** | Reparación rápida | Documentación técnica | Análisis profundo |
| **Audiencia** | Técnico de taller | Ingeniero de diseño | Auditoría/forense |

---

## 🔧 Estilo TÉCNICO

**Perfil:** Técnico de taller con experiencia en reparación de electrónica.

**Objetivo:** Solucionar el problema rápido. Menos teoría, más acción.

### Características
- ✅ **Conciso y directo** - Va al grano
- ✅ **Orientado a solución** - Primeros pasos claros
- ✅ **Lenguaje práctico** - Sin jerga innecesaria
- ✅ **Evidencia mínima** - Solo lo esencial

### Ejemplo Real: ESP32 sin 3V3

#### Hipótesis Generada

```
📍 CAPA 1 - LOCALIZACIÓN:
   • Rail: 3V3
   • Componente: U1 (Regulador)
   • Bloque: Power

🔍 CAPA 2 - CAUSA:
   • Causa: sin_voltaje
   • Razonamiento: 3V3 ausente → Regulador falló. Medir salida, revisar entrada 5V, verificar caps de salida.
   • Evidencia: 
     - Rail 3V3 identificado
     - Regulador probable: AMS1117 o similar

⚡ CAPA 3 - CONSECUENCIA:
   • Impacto: CRÍTICO
   • Efecto: Radio no enciende, placa no arranca
   • Afecta: WiFi, Bluetooth, RF, MCU

🔧 PRÓXIMOS PASOS:
   • Medir voltaje en rail 3V3
   • Verificar continuidad desde fuente
   • Revisar regulador de voltaje
   • Prioridad alta: Resolver antes de continuar

📊 PUNTOS DE PRUEBA: TP3, TP_3V3, Salida del regulador U1
```

**Tiempo estimado de lectura:** 20 segundos

---

## ⚙️ Estilo INGENIERO

**Perfil:** Ingeniero electrónico o técnico senior con conocimientos de diseño.

**Objetivo:** Entender el **por qué** antes de reparar. Documentación metodológica.

### Características
- ✅ **Análisis causal** - Explica topología y flujo
- ✅ **Sistemático** - Orden lógico de verificación
- ✅ **Técnico pero claro** - Usa terminología correcta
- ✅ **Evidencia estructurada** - Datos organizados

### Ejemplo Real: ESP32 sin 3V3

#### Hipótesis Generada

```
📍 CAPA 1 - LOCALIZACIÓN:
   • Rail: 3V3
   • Componente: U1 (Regulador)
   • Bloque: Power

🔍 CAPA 2 - CAUSA:
   • Causa: sin_voltaje
   • Razonamiento: El rail 3V3 es generado por un regulador lineal (probablemente AMS1117-3.3) 
     que recibe 5V de entrada. Si 3V3 está ausente, causas posibles: 
     (1) Regulador dañado por sobrecorriente o ESD, 
     (2) Entrada 5V ausente o insuficiente, 
     (3) Capacitores de salida en cortocircuito. 
     El método de diagnóstico correcto es medir en cascada: VBUS → 5V → 3V3.
   
   • Evidencia: 
     - Ausencia de tensión en rail 3V3
     - Regulador lineal LDO típico para este rail
     - Topología: USB_5V → AMS1117 → 3V3 → RF+MCU

⚡ CAPA 3 - CONSECUENCIA:
   • Impacto: CRÍTICO
   • Efecto: Radio no enciende, placa no arranca
   • Afecta: WiFi, Bluetooth, RF, MCU

🔧 PRÓXIMOS PASOS:
   • Medir voltaje en rail 3V3
   • Verificar continuidad desde fuente
   • Revisar regulador de voltaje
   • Prioridad alta: Resolver antes de continuar

📊 PUNTOS DE PRUEBA: TP3, TP_3V3, Salida del regulador U1
```

**Tiempo estimado de lectura:** 45 segundos

---

## 🔬 Estilo FORENSE

**Perfil:** Análisis post-mortem, auditoría, documentación legal o educativa.

**Objetivo:** Documentar **todo** con precisión. Análisis exhaustivo.

### Características
- ✅ **Exhaustivo** - No deja cabos sueltos
- ✅ **Probabilidades** - Evalúa múltiples escenarios
- ✅ **Evidencia detallada** - Incluye observaciones visuales
- ✅ **Plan de verificación completo** - Paso a paso metodológico

### Ejemplo Real: ESP32 sin 3V3

#### Hipótesis Generada

```
📍 CAPA 1 - LOCALIZACIÓN:
   • Rail: 3V3
   • Componente: U1 (Regulador)
   • Bloque: Power

🔍 CAPA 2 - CAUSA:
   • Causa: sin_voltaje
   
   • Razonamiento: 
     Análisis de cadena de alimentación completa: 
     VBUS (USB) → Fusible/Protección → 5V_IN → U1 (AMS1117-3.3) → 3V3_OUT → Cargas. 
     
     Escenarios posibles ordenados por probabilidad: 
     (1) Falla interna del regulador U1 por stress térmico o ESD (60%), 
     (2) Cortocircuito en rail 3V3 por componente downstream (25%), 
     (3) Entrada 5V_IN insuficiente por caída en USB o fusible abierto (10%), 
     (4) Soldadura fría en pines del regulador (5%). 
     
     Plan de verificación: 
     (A) Medir 5V_IN en pin 1 de U1, 
     (B) Desconectar cargas 3V3 y remedir salida, 
     (C) Medir resistencia a tierra en rail 3V3, 
     (D) Reflow de U1 si mediciones anteriores OK. 
     
     Si U1 está caliente en reposo, indica cortocircuito downstream. 
     Temperatura normal de operación: <50°C al tacto.
   
   • Evidencia: 
     - Rail 3V3 ausente o significativamente bajo (<2.8V)
     - Regulador LDO serie 1117 detectado en posición U1
     - Capacitor electrolítico de salida C15 (10uF) visible
     - Traza de cobre desde regulador hacia módulo RF intacta
     - No se observa daño térmico visible en regulador

⚡ CAPA 3 - CONSECUENCIA:
   • Impacto: CRÍTICO
   • Efecto: Radio no enciende, placa no arranca
   • Afecta: WiFi, Bluetooth, RF, MCU

🔧 PRÓXIMOS PASOS:
   • Medir voltaje en rail 3V3
   • Verificar continuidad desde fuente
   • Revisar regulador de voltaje
   • Prioridad alta: Resolver antes de continuar

📊 PUNTOS DE PRUEBA: TP3, TP_3V3, Salida del regulador U1
```

**Tiempo estimado de lectura:** 90 segundos

---

## 🎯 ¿Cuándo Usar Cada Estilo?

### Usa TÉCNICO cuando:
- ✅ Estás en un taller reparando múltiples placas al día
- ✅ Necesitas diagnóstico rápido sin documentación extensa
- ✅ Ya tienes experiencia y no necesitas explicaciones largas
- ✅ El tiempo es crítico (reparaciones express)

**Ejemplo:** Taller de celulares, servicio técnico de campo

### Usa INGENIERO cuando:
- ✅ Necesitas documentar el proceso para un reporte técnico
- ✅ Estás capacitando a técnicos junior
- ✅ Quieres entender la causa raíz metodológicamente
- ✅ Diseñas o mejoras productos

**Ejemplo:** Departamento de calidad, ingeniería de producto

### Usa FORENSE cuando:
- ✅ Análisis post-mortem de fallas críticas
- ✅ Documentación para garantías o reclamaciones
- ✅ Auditorías de calidad o certificaciones
- ✅ Casos educativos o investigación

**Ejemplo:** RMA analysis, casos legales, publicaciones técnicas

---

## 💡 Tips

### Cambiar estilo en tiempo real
```javascript
// En la interfaz web
Estilo de Diagnóstico: [Seleccionar: Técnico / Ingeniero / Forense]
```

### Vía API
```bash
curl -X POST http://localhost:8000/api/diagnostic/session \
  -H "Content-Type: application/json" \
  -d '{
    "board_model": "ESP32-DevKit",
    "diagnostic_style": "forense"
  }'
```

### Comparar estilos
Puedes crear múltiples sesiones con diferentes estilos para la misma placa y comparar los resultados.

---

## 📚 Referencias

- [Guía de Inicio Rápido](DIAGNOSTIC_QUICKSTART.md)
- [Documentación Completa del Sistema](DIAGNOSTIC_SYSTEM.md)
- [Ejemplos de Casos Reales](../README.md#casos-de-uso)

---

> **¿Qué estilo prefieres?** 
> El sistema aprende de tu uso y puede sugerir el estilo más apropiado según el contexto.

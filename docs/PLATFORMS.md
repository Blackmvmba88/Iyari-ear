# Compatibilidad por Plataforma - Iyari-ear

Este documento describe las opciones de instalación y compatibilidad de Iyari-ear en diferentes plataformas.

## 🎯 Matriz de Compatibilidad

| Plataforma | Método de Instalación | Estado | Auto-inicio | Micrófono | Notas |
|------------|----------------------|---------|-------------|-----------|-------|
| **Windows 10/11** | Ejecutable .exe | ✅ Soportado | ✅ Sí | ✅ Nativo | Doble click y listo |
| **Windows 10/11** | PWA (Chrome/Edge) | ✅ Soportado | ✅ Sí | ✅ Navegador | Instalable desde navegador |
| **macOS** | Python + pip | ✅ Soportado | ⚠️ Manual | ✅ Nativo | Requiere permisos de sistema |
| **macOS** | PWA (Chrome/Safari) | ✅ Soportado | ✅ Sí | ✅ Navegador | Instalable desde navegador |
| **Linux (Ubuntu/Debian)** | pipx / deb | ✅ Soportado | ✅ systemd | ✅ Nativo | Service daemon opcional |
| **Linux (Fedora/Arch)** | pip / pacman | ✅ Soportado | ✅ systemd | ✅ Nativo | Service daemon opcional |
| **Android (Termux)** | Script de instalación | ✅ Soportado | ⚠️ Manual | ✅ Navegador | Power-user friendly |
| **Android** | PWA (Chrome) | ✅ Soportado | ✅ Sí | ✅ Navegador | Método recomendado |
| **iOS/iPadOS** | PWA (Safari) | ⚠️ Limitado | ✅ Sí | ⚠️ Limitaciones | Safari tiene restricciones WebRTC |
| **Chromebook** | PWA (Chrome) | ✅ Soportado | ✅ Sí | ✅ Navegador | Funciona perfectamente |

**Leyenda:**
- ✅ Totalmente funcional
- ⚠️ Funcional con limitaciones
- ❌ No soportado

---

## 📱 Progressive Web App (PWA) - Multiplataforma

### ¿Qué es una PWA?

Una Progressive Web App es una aplicación web que se puede instalar en tu dispositivo y funciona como una app nativa.

### Ventajas de la PWA
- ✅ Se instala desde el navegador (no necesita tienda de apps)
- ✅ Actualizaciones automáticas
- ✅ Funciona offline (parcialmente)
- ✅ Acceso directo en escritorio/menú de apps
- ✅ Funciona en todos los dispositivos modernos

### Instalación PWA

#### En Chrome/Edge (Windows, macOS, Linux, Android, Chromebook):
1. Abre Iyari-ear en Chrome o Edge: `http://localhost:8000`
2. Busca el ícono de instalación en la barra de direcciones (➕ o 📲)
3. Click en "Instalar" o "Instalar Iyari-ear"
4. La app aparecerá como una aplicación en tu sistema

#### En Safari (iOS/iPadOS):
1. Abre Iyari-ear en Safari: `http://localhost:8000` (necesitas servidor local o remoto)
2. Toca el botón "Compartir" (cuadrado con flecha arriba)
3. Desplázate y toca "Agregar a pantalla de inicio"
4. Confirma el nombre y toca "Agregar"

**Nota para iOS:** Debido a limitaciones de Safari, algunas funciones de WebRTC pueden no funcionar completamente. Se recomienda usar Android o desktop para mejor experiencia.

---

## 💻 Windows

### Opción 1: Ejecutable (.exe) - Recomendado para usuarios finales

**Instalación:**
1. Descarga `Iyari-ear.exe` desde Releases
2. Doble click en el ejecutable
3. ¡Listo! El navegador se abrirá automáticamente

**Para desarrolladores - Construir el ejecutable:**
```powershell
# Instalar PyInstaller
pip install pyinstaller

# Ejecutar script de build
cd install/windows
.\build.ps1
```

El ejecutable se generará en `dist/Iyari-ear.exe`

### Opción 2: Python directo

```powershell
# Instalar dependencias
pip install -r requirements.txt

# Iniciar con CLI
python -m pip install -e .
iyari-ear start

# O directamente
python main.py
```

### Opción 3: PWA (ver sección PWA arriba)

---

## 🐧 Linux

### Opción 1: Instalación con script (Ubuntu/Debian)

```bash
# Clonar repositorio
git clone https://github.com/Blackmvmba88/Iyari-ear.git
cd Iyari-ear

# Ejecutar instalador
chmod +x install/linux/install.sh
./install/linux/install.sh
```

El instalador:
- ✅ Instala dependencias del sistema (PortAudio)
- ✅ Instala el paquete Python
- ✅ Crea el comando `iyari-ear`
- ✅ Opcionalmente configura systemd service

### Opción 2: pipx (recomendado)

```bash
# Instalar pipx si no lo tienes
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Instalar Iyari-ear
pipx install git+https://github.com/Blackmvmba88/Iyari-ear.git

# Usar
iyari-ear start
```

### Opción 3: Servicio systemd (auto-inicio)

```bash
# Después de la instalación
systemctl --user enable iyari-ear
systemctl --user start iyari-ear

# Verificar estado
systemctl --user status iyari-ear

# Ver logs
journalctl --user -u iyari-ear -f
```

### Opción 4: PWA (ver sección PWA arriba)

---

## 🤖 Android

### Opción 1: PWA - Método Recomendado ⭐

1. Instala Iyari-ear en un servidor local (PC en la misma red)
2. Desde el Android, abre Chrome y visita: `http://[IP_DEL_SERVIDOR]:8000`
3. Instala la PWA como se describe arriba
4. ¡Listo! Usa la app desde el menú de aplicaciones

### Opción 2: Termux (para usuarios avanzados)

Termux te permite ejecutar Linux y Python en Android.

**Instalación:**
```bash
# 1. Instala Termux desde F-Droid (NO desde Play Store)
# https://f-droid.org/en/packages/com.termux/

# 2. En Termux, ejecuta:
curl -O https://raw.githubusercontent.com/Blackmvmba88/Iyari-ear/main/install/termux/install.sh
chmod +x install.sh
./install.sh

# 3. Inicia el servidor
iyari-ear start --host 0.0.0.0 --port 8000

# 4. Abre Chrome en Android y visita:
# http://127.0.0.1:8000
```

**Importante:**
- Mantén Termux en primer plano mientras usas la app
- Da permisos de almacenamiento si se solicita
- Usa `termux-wake-lock` para evitar que el proceso se detenga

---

## 🍎 macOS

### Instalación con Homebrew (recomendado)

```bash
# Instalar Python 3 si no lo tienes
brew install python3

# Instalar PortAudio
brew install portaudio

# Clonar e instalar
git clone https://github.com/Blackmvmba88/Iyari-ear.git
cd Iyari-ear
pip3 install -e .

# Usar
iyari-ear start
```

### Permisos de Micrófono

macOS te pedirá permiso para que Terminal/iTerm acceda al micrófono:
1. Ve a **Preferencias del Sistema** → **Seguridad y Privacidad** → **Privacidad** → **Micrófono**
2. Activa el checkbox para Terminal o tu emulador de terminal

### PWA en Safari

La PWA funciona en Safari, pero con limitaciones en el acceso al micrófono. Se recomienda usar Chrome para mejor compatibilidad.

---

## 🌐 Chromebook

### Instalación

Chromebooks funcionan perfectamente con la PWA:
1. Inicia un servidor local (si tienes acceso a Linux en Chromebook) o conéctate a un servidor remoto
2. Abre Chrome y visita la URL del servidor
3. Instala la PWA
4. Funciona como una app nativa de Chrome OS

---

## 🔧 Comandos del CLI

Una vez instalado, estos comandos están disponibles:

### `iyari-ear doctor`
Verifica el sistema completo:
- ✅ Versión de Python
- ✅ Dependencias instaladas
- ✅ Micrófono disponible
- ✅ Puerto 8000 disponible
- ✅ Archivos necesarios

```bash
iyari-ear doctor
```

### `iyari-ear test-mic`
Prueba el micrófono con una transcripción corta:
```bash
iyari-ear test-mic
```

### `iyari-ear start`
Inicia el servidor:
```bash
# Local (solo en tu máquina)
iyari-ear start

# En la red local (accesible desde otros dispositivos)
iyari-ear start --host 0.0.0.0

# Puerto personalizado
iyari-ear start --port 8080

# Sin abrir navegador automáticamente
iyari-ear start --no-browser
```

---

## 🚨 Solución de Problemas

### El micrófono no funciona

**En navegador:**
- ✅ Verifica que diste permiso al micrófono
- ✅ Usa HTTPS o localhost (WebRTC requiere conexión segura)
- ✅ Revisa la configuración de permisos del navegador

**En terminal/Python:**
- ✅ Ejecuta `iyari-ear test-mic`
- ✅ Verifica que PyAudio/PortAudio estén instalados
- ✅ En macOS, verifica permisos de sistema

### Puerto 8000 ocupado

```bash
# Usa otro puerto
iyari-ear start --port 8001

# O encuentra qué proceso usa el puerto 8000
# Linux/macOS:
lsof -i :8000

# Windows:
netstat -ano | findstr :8000
```

### Error de conexión WebSocket

- ✅ Verifica que el servidor esté corriendo
- ✅ Si usas HTTPS, el WebSocket debe ser WSS
- ✅ Verifica que no haya firewall bloqueando el puerto

### PWA no se puede instalar

- ✅ Usa Chrome o Edge (Safari tiene limitaciones)
- ✅ Sirve la app vía HTTPS o localhost
- ✅ Verifica que `manifest.json` sea accesible

---

## 📊 Comparación de Métodos

| Método | Facilidad | Portabilidad | Rendimiento | Auto-actualización |
|--------|-----------|--------------|-------------|-------------------|
| **PWA** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Automático |
| **Ejecutable Windows** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ Manual |
| **Python directo** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ Git pull |
| **systemd service** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ Git pull |
| **Termux** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ Git pull |

---

## 🎯 Recomendaciones por Caso de Uso

### Usuario Final (no técnico)
→ **PWA** (más fácil de instalar y actualizar)

### Usuario Técnico en Desktop
→ **Python + CLI** (más control y personalizable)

### Deployment en Servidor
→ **systemd service** (corre en background, auto-inicio)

### Usuario Android avanzado
→ **Termux** (control total desde el dispositivo)

### Desarrollo/Testing
→ **Python directo** (rápido para iterar)

---

## 📞 Soporte

¿Problemas con alguna plataforma?
- 🐛 Abre un issue: https://github.com/Blackmvmba88/Iyari-ear/issues
- 📖 Lee la documentación: https://github.com/Blackmvmba88/Iyari-ear
- 💬 Comparte tu experiencia en Discussions

---

**Última actualización:** 2026-01-04

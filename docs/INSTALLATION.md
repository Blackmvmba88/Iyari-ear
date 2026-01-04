# 🚀 Guía de Instalación Rápida - Iyari-ear

> Elige tu plataforma y sigue los pasos. ¡En 5 minutos estarás transcribiendo!

---

## 📱 Opción 1: PWA (Progressive Web App) - Universal

**Lo más fácil y recomendado para todos los dispositivos** ⭐

### Paso 1: Inicia el servidor

```bash
# Si tienes Python instalado:
pip install -r requirements.txt
python main.py
```

### Paso 2: Instala la PWA

1. Abre Chrome/Edge en: `http://localhost:8000`
2. Click en el ícono de instalar (➕ o 📲) en la barra de direcciones
3. Confirma "Instalar"
4. ¡Listo! Ahora puedes abrir Iyari-ear desde tus apps

**Ventajas:**
- ✅ Sin descargas adicionales
- ✅ Funciona en todos los dispositivos
- ✅ Se actualiza automáticamente
- ✅ Acceso directo como app nativa

---

## 💻 Opción 2: Windows - Ejecutable

**Para usuarios que quieren doble-click y listo**

### Descarga y Ejecuta

1. Descarga `Iyari-ear.exe` desde [Releases](https://github.com/Blackmvmba88/Iyari-ear/releases)
2. Doble click en el ejecutable
3. El navegador se abrirá automáticamente
4. ¡A transcribir!

### Construir tu propio .exe

```powershell
# Requiere Python instalado
pip install pyinstaller
cd install/windows
.\build.ps1
```

---

## 🐧 Opción 3: Linux - Script de Instalación

**Para usuarios de Ubuntu/Debian/Fedora/Arch**

```bash
# Clonar repo
git clone https://github.com/Blackmvmba88/Iyari-ear.git
cd Iyari-ear

# Ejecutar instalador
chmod +x install/linux/install.sh
./install/linux/install.sh

# ¡Ya está! Ahora puedes usar:
iyari-ear start
```

El instalador se encarga de todo:
- ✅ Dependencias del sistema
- ✅ Paquetes de Python
- ✅ Comando `iyari-ear` global
- ✅ Opcional: servicio systemd

---

## 🤖 Opción 4: Android (Termux)

**Para usuarios avanzados de Android**

### Paso 1: Instala Termux
Descarga desde **F-Droid** (NO desde Play Store): https://f-droid.org/en/packages/com.termux/

### Paso 2: Instala Iyari-ear

```bash
# En Termux:
curl -O https://raw.githubusercontent.com/Blackmvmba88/Iyari-ear/main/install/termux/install.sh
chmod +x install.sh
./install.sh
```

### Paso 3: Usa la app

```bash
# Inicia el servidor
iyari-ear start --host 0.0.0.0 --port 8000

# Abre Chrome en tu Android:
# http://127.0.0.1:8000
```

**Consejo:** Instala la PWA desde Chrome para tener un acceso directo.

---

## 🍎 Opción 5: macOS

```bash
# Instala Homebrew si no lo tienes: https://brew.sh

# Instala dependencias
brew install python3 portaudio

# Clona e instala
git clone https://github.com/Blackmvmba88/Iyari-ear.git
cd Iyari-ear
pip3 install -e .

# Usa
iyari-ear start
```

**Importante:** macOS te pedirá permiso para acceder al micrófono. Acepta en:
Preferencias del Sistema → Seguridad y Privacidad → Micrófono → Terminal

---

## 🔧 Instalación para Desarrolladores

```bash
# Clona el repo
git clone https://github.com/Blackmvmba88/Iyari-ear.git
cd Iyari-ear

# Crea entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instala en modo desarrollo
pip install -e .

# Verifica que todo funcione
iyari-ear doctor

# Inicia
iyari-ear start
```

---

## ⚡ Quick Start (Ya tengo Python)

```bash
# 1. Clona
git clone https://github.com/Blackmvmba88/Iyari-ear.git
cd Iyari-ear

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Inicia
python main.py

# 4. Abre navegador en: http://localhost:8000
```

---

## 🏥 Verificación Post-Instalación

Después de instalar, verifica que todo funcione:

```bash
# Diagnóstico completo
iyari-ear doctor

# Prueba el micrófono
iyari-ear test-mic
```

Si todo está verde ✅, ¡estás listo!

---

## 🚨 Solución Rápida de Problemas

### "No puedo instalar PyAudio" (Linux)

```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev

# Fedora
sudo dnf install portaudio-devel python3-devel

# Arch
sudo pacman -S portaudio
```

Luego: `pip install -r requirements.txt`

### "Puerto 8000 ocupado"

```bash
# Usa otro puerto
iyari-ear start --port 8080

# O en Python directo
PORT=8080 python main.py
```

### "El micrófono no funciona"

1. ✅ Verifica permisos del navegador/sistema
2. ✅ Ejecuta: `iyari-ear test-mic`
3. ✅ Intenta con otro navegador (Chrome recomendado)

---

## 📚 Próximos Pasos

Una vez instalado:

1. **Lee la matriz de plataformas**: [docs/PLATFORMS.md](./PLATFORMS.md)
2. **Aprende los comandos CLI**: `iyari-ear --help`
3. **Personaliza**: Edita `styles/style-enhanced.css` para cambiar el tema

---

## 🆘 ¿Necesitas Ayuda?

- 📖 **Documentación completa**: [README.md](../README.md)
- 🐛 **Reporta bugs**: [Issues](https://github.com/Blackmvmba88/Iyari-ear/issues)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/Blackmvmba88/Iyari-ear/discussions)

---

¡Disfruta de Iyari-ear! 🎤✨

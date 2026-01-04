# Install Scripts

Scripts de instalación para diferentes plataformas.

## Estructura

### `/windows` - Windows
- `build.ps1` - Script PowerShell para construir ejecutable .exe con PyInstaller

**Uso:**
```powershell
cd install/windows
.\build.ps1
```

Esto genera `dist/Iyari-ear.exe` que puede ejecutarse con doble-click.

### `/linux` - Linux
- `install.sh` - Script de instalación automática para distribuciones Linux
- `iyari-ear.service` - Archivo de servicio systemd para auto-inicio

**Uso:**
```bash
chmod +x install/linux/install.sh
./install/linux/install.sh
```

El script:
- Instala dependencias del sistema (PortAudio)
- Instala el paquete Python
- Configura el comando `iyari-ear`
- Opcionalmente instala servicio systemd

**Servicio systemd:**
```bash
# Habilitar auto-inicio
systemctl --user enable iyari-ear
systemctl --user start iyari-ear

# Ver estado
systemctl --user status iyari-ear
```

### `/termux` - Android (Termux)
- `install.sh` - Script de instalación para Termux en Android

**Uso:**
```bash
# En Termux:
curl -O https://raw.githubusercontent.com/Blackmvmba88/Iyari-ear/main/install/termux/install.sh
chmod +x install.sh
./install.sh
```

El script:
- Instala Python y dependencias en Termux
- Clona el repositorio
- Configura el comando `iyari-ear`

## Requisitos por Plataforma

### Windows
- Python 3.7+
- PyInstaller (se instala automáticamente)

### Linux
- Python 3.7+
- PortAudio (instalado por el script)
- systemd (opcional, para servicio)

### Android (Termux)
- Termux instalado desde F-Droid
- Conexión a internet

## Construcción Manual

Si prefieres instalar manualmente:

```bash
# Clonar repositorio
git clone https://github.com/Blackmvmba88/Iyari-ear.git
cd Iyari-ear

# Instalar con pip
pip install -e .

# Usar CLI
iyari-ear doctor
iyari-ear start
```

## Troubleshooting

### PyInstaller falla en Windows
- Asegúrate de tener Python 3.7+ instalado
- Ejecuta como administrador si hay problemas de permisos

### PortAudio no encontrado en Linux
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev

# Fedora
sudo dnf install portaudio-devel python3-devel

# Arch
sudo pacman -S portaudio
```

### Termux: "pkg not found"
- Asegúrate de estar en Termux (no en terminal normal de Android)
- Descarga Termux desde F-Droid, NO desde Play Store

## Soporte

Problemas con la instalación?
- 🐛 Issues: https://github.com/Blackmvmba88/Iyari-ear/issues
- 📖 Docs: [../docs/PLATFORMS.md](../docs/PLATFORMS.md)

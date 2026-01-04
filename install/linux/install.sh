#!/bin/bash
# Script de instalación para Linux
# Instala Iyari-ear como servicio systemd (opcional)

echo "🎤 Iyari-ear - Instalador para Linux"
echo "====================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   Fedora/RHEL: sudo dnf install python3 python3-pip"
    echo "   Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"
echo ""

# Instalar dependencias del sistema (PortAudio para PyAudio)
echo "📦 Instalando dependencias del sistema..."
if command -v apt &> /dev/null; then
    echo "Detectado: Debian/Ubuntu"
    sudo apt update
    sudo apt install -y portaudio19-dev python3-dev
elif command -v dnf &> /dev/null; then
    echo "Detectado: Fedora/RHEL"
    sudo dnf install -y portaudio-devel python3-devel
elif command -v pacman &> /dev/null; then
    echo "Detectado: Arch Linux"
    sudo pacman -S --noconfirm portaudio
else
    echo "⚠️  Distribución no detectada. Instala PortAudio manualmente."
fi

# Instalar con pip
echo ""
echo "📦 Instalando Iyari-ear con pip..."
if command -v pipx &> /dev/null; then
    echo "Usando pipx (recomendado)..."
    pipx install .
else
    echo "Usando pip..."
    pip3 install --user .
fi

# Verificar instalación
echo ""
echo "🏥 Verificando instalación..."
iyari-ear doctor

# Preguntar si instalar como servicio
echo ""
read -p "¿Instalar como servicio systemd? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🔧 Instalando servicio systemd..."
    
    # Crear directorio para servicios de usuario
    mkdir -p ~/.config/systemd/user
    
    # Copiar archivo de servicio
    cp install/linux/iyari-ear.service ~/.config/systemd/user/
    
    # Recargar systemd
    systemctl --user daemon-reload
    
    echo ""
    echo "✅ Servicio instalado. Comandos útiles:"
    echo "  systemctl --user start iyari-ear    # Iniciar"
    echo "  systemctl --user stop iyari-ear     # Detener"
    echo "  systemctl --user enable iyari-ear   # Auto-inicio"
    echo "  systemctl --user status iyari-ear   # Estado"
fi

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "🚀 Cómo usar:"
echo "  iyari-ear doctor      # Diagnóstico"
echo "  iyari-ear start       # Iniciar servidor"
echo "  iyari-ear test-mic    # Probar micrófono"
echo ""
echo "📖 Más información: https://github.com/Blackmvmba88/Iyari-ear"

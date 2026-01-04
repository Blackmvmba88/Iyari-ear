#!/bin/bash
# Script de instalación para Termux (Android)
# Permite ejecutar Iyari-ear en dispositivos Android

echo "🎤 Iyari-ear - Instalador para Termux"
echo "======================================"
echo ""

# Verificar que estamos en Termux
if [ ! -d "$PREFIX" ]; then
    echo "❌ Este script debe ejecutarse en Termux"
    echo "   Descarga Termux desde F-Droid: https://f-droid.org/en/packages/com.termux/"
    exit 1
fi

echo "📱 Detectado: Termux en Android"
echo ""

# Actualizar paquetes
echo "📦 Actualizando paquetes de Termux..."
pkg update -y

# Instalar Python y dependencias del sistema
echo ""
echo "🐍 Instalando Python y dependencias..."
pkg install -y python python-pip git

# Instalar PortAudio para PyAudio (si está disponible)
echo ""
echo "🎵 Instalando PortAudio..."
pkg install -y portaudio || echo "⚠️  PortAudio no disponible en Termux, continuando..."

# Navegar al directorio de Iyari-ear (o clonar si no existe)
if [ ! -f "requirements.txt" ]; then
    echo ""
    echo "📥 Clonando Iyari-ear..."
    cd ~
    git clone https://github.com/Blackmvmba88/Iyari-ear.git
    cd Iyari-ear
fi

# Instalar dependencias de Python
echo ""
echo "📦 Instalando dependencias de Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Dar permisos de ejecución al CLI
chmod +x cli/iyari_ear_cli.py

# Crear un wrapper script en $PREFIX/bin
echo ""
echo "🔧 Creando comando 'iyari-ear'..."
cat > $PREFIX/bin/iyari-ear << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Wrapper para Iyari-ear CLI en Termux
cd $HOME/Iyari-ear
python cli/iyari_ear_cli.py "$@"
EOF
chmod +x $PREFIX/bin/iyari-ear

# Verificar instalación
echo ""
echo "🏥 Verificando instalación..."
python cli/iyari_ear_cli.py doctor

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "📱 Cómo usar Iyari-ear en Termux:"
echo ""
echo "  1. Inicia el servidor:"
echo "     iyari-ear start --host 0.0.0.0 --port 8000"
echo ""
echo "  2. Abre el navegador de tu Android y visita:"
echo "     http://127.0.0.1:8000"
echo ""
echo "  3. Da permiso al micrófono cuando lo solicite"
echo ""
echo "  4. ¡Presiona 'Iniciar' y habla!"
echo ""
echo "💡 Consejos:"
echo "  • Mantén Termux en primer plano"
echo "  • Usa 'iyari-ear doctor' para diagnóstico"
echo "  • Usa 'iyari-ear test-mic' para probar el micrófono"
echo ""
echo "🐛 Problemas? https://github.com/Blackmvmba88/Iyari-ear/issues"

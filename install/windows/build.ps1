# Script de empaquetado para Windows con PyInstaller
# Este script crea un ejecutable .exe para Iyari-ear

Write-Host "🚀 Iyari-ear - Windows Package Builder" -ForegroundColor Cyan
Write-Host "=" * 50

# Verificar que PyInstaller esté instalado
Write-Host "`n📦 Verificando PyInstaller..."
$pyinstaller = python -m pip show pyinstaller 2>$null
if (-not $pyinstaller) {
    Write-Host "⚠️  PyInstaller no está instalado. Instalando..." -ForegroundColor Yellow
    python -m pip install pyinstaller
}

# Crear directorio de build si no existe
if (-not (Test-Path "dist")) {
    New-Item -ItemType Directory -Path "dist" | Out-Null
}

Write-Host "`n🔨 Construyendo ejecutable..."

# Ejecutar PyInstaller
python -m PyInstaller `
    --name="Iyari-ear" `
    --onefile `
    --windowed `
    --icon="apps/pwa/icons/icon-512x512.png" `
    --add-data="index.html;." `
    --add-data="js;js" `
    --add-data="styles;styles" `
    --add-data="apps/pwa;apps/pwa" `
    --hidden-import="uvicorn" `
    --hidden-import="fastapi" `
    --hidden-import="speech_recognition" `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Ejecutable creado exitosamente!" -ForegroundColor Green
    Write-Host "📁 Ubicación: dist\Iyari-ear.exe"
    Write-Host "`nPara distribuir:"
    Write-Host "  1. Copia el archivo dist\Iyari-ear.exe"
    Write-Host "  2. Doble clic en Iyari-ear.exe para ejecutar"
    Write-Host "  3. (Opcional) Crea un instalador con InnoSetup"
} else {
    Write-Host "`n❌ Error al crear ejecutable" -ForegroundColor Red
    exit 1
}

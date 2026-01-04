#!/usr/bin/env python3
"""
Iyari-ear CLI - Command Line Interface
Herramienta de línea de comandos para gestionar Iyari-ear
"""
import sys
import os
import argparse
import subprocess
import socket
import webbrowser
from pathlib import Path

# Constants
MAX_MICROPHONES_TO_DISPLAY = 5


def check_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Verifica si un puerto está disponible"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            return True
    except OSError:
        return False


def check_microphone():
    """Verifica si hay un micrófono disponible"""
    print("🎤 Verificando micrófono...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        if mic_list:
            print(f"✅ Encontrados {len(mic_list)} dispositivos de audio:")
            for i, name in enumerate(mic_list[:MAX_MICROPHONES_TO_DISPLAY]):
                print(f"   {i}: {name}")
            if len(mic_list) > MAX_MICROPHONES_TO_DISPLAY:
                print(f"   ... y {len(mic_list) - MAX_MICROPHONES_TO_DISPLAY} más")
            return True
        else:
            print("❌ No se encontraron dispositivos de micrófono")
            return False
    except ImportError:
        print("⚠️  SpeechRecognition no está instalado")
        print("   Instalar con: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"❌ Error al verificar micrófono: {e}")
        return False


def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("📦 Verificando dependencias...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'websockets',
        'speech_recognition',
        'pillow'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NO INSTALADO")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Paquetes faltantes:")
        print(f"   pip install {' '.join(missing)}")
        return False
    return True


def doctor():
    """Ejecuta diagnóstico completo del sistema"""
    print("🏥 Iyari-ear Doctor - Diagnóstico del Sistema")
    print("=" * 50)
    
    # 1. Verificar Python
    print(f"\n🐍 Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        return False
    else:
        print("✅ Versión de Python OK")
    
    # 2. Verificar dependencias
    print()
    deps_ok = check_dependencies()
    
    # 3. Verificar micrófono
    print()
    mic_ok = check_microphone()
    
    # 4. Verificar puerto
    print("\n🔌 Verificando puerto 8000...")
    if check_port_available(8000):
        print("✅ Puerto 8000 disponible")
        port_ok = True
    else:
        print("⚠️  Puerto 8000 en uso (puede ser normal si el servidor está corriendo)")
        port_ok = True  # No es crítico
    
    # 5. Verificar archivos
    print("\n📁 Verificando archivos...")
    required_files = ['main.py', 'index.html', 'js/main.js']
    files_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NO ENCONTRADO")
            files_ok = False
    
    # Resumen
    print("\n" + "=" * 50)
    if deps_ok and mic_ok and files_ok:
        print("✅ Todo listo! Ejecuta: iyari-ear start")
        return True
    else:
        print("⚠️  Hay problemas que resolver antes de iniciar")
        return False


def test_mic():
    """Prueba el micrófono con una grabación corta"""
    print("🎤 Test de Micrófono")
    print("=" * 50)
    
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        
        print("\n📋 Micrófonos disponibles:")
        mic_list = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mic_list):
            print(f"   {i}: {name}")
        
        print("\n🎙️  Habla algo en español durante 3 segundos...")
        print("   (asegúrate de dar permiso al micrófono si se solicita)")
        
        with sr.Microphone() as source:
            print("📢 Ajustando ruido ambiente...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Escuchando... ¡HABLA AHORA!")
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
        
        print("\n🔄 Transcribiendo...")
        try:
            text = r.recognize_google(audio, language='es-ES')
            print(f"\n✅ Texto reconocido: \"{text}\"")
            print("🎉 ¡El micrófono funciona correctamente!")
            return True
        except sr.UnknownValueError:
            print("⚠️  No se pudo entender el audio")
            print("   Intenta hablar más claro o acércate al micrófono")
            return False
        except sr.RequestError as e:
            print(f"❌ Error del servicio de transcripción: {e}")
            print("   Verifica tu conexión a internet")
            return False
            
    except ImportError:
        print("❌ SpeechRecognition no está instalado")
        print("   Instalar con: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def start_server(host: str = "127.0.0.1", port: int = 8000, open_browser: bool = True):
    """Inicia el servidor de Iyari-ear"""
    print("🚀 Iniciando Iyari-ear")
    print("=" * 50)
    
    # Verificar que existe main.py
    if not os.path.exists('main.py'):
        print("❌ Error: main.py no encontrado")
        print("   Asegúrate de estar en el directorio raíz de Iyari-ear")
        return False
    
    # Verificar puerto
    if not check_port_available(port, host):
        print(f"⚠️  Puerto {port} en uso")
        print("   Opciones:")
        print(f"   1. Usa otro puerto: iyari-ear start --port 8001")
        print(f"   2. Detén el proceso que usa el puerto {port}")
        return False
    
    print(f"\n📡 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"🌐 URL: http://{host}:{port}")
    
    if open_browser:
        print("\n🌐 Abriendo navegador...")
        # Esperar un momento antes de abrir el navegador
        import threading
        def open_browser_delayed():
            import time
            time.sleep(2)
            webbrowser.open(f"http://{host}:{port}")
        threading.Thread(target=open_browser_delayed, daemon=True).start()
    
    print("\n✅ Servidor iniciado. Presiona Ctrl+C para detener.\n")
    print("=" * 50)
    
    # Configurar variables de entorno
    os.environ['HOST'] = host
    os.environ['PORT'] = str(port)
    
    # Ejecutar main.py
    try:
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido")
        return True
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")
        return False


def main():
    """Función principal del CLI"""
    parser = argparse.ArgumentParser(
        description='Iyari-ear CLI - Subtítulos en Tiempo Real',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  iyari-ear doctor              # Diagnóstico del sistema
  iyari-ear start               # Iniciar servidor (127.0.0.1:8000)
  iyari-ear start --host 0.0.0.0  # Accesible desde red local
  iyari-ear start --port 8080   # Usar puerto diferente
  iyari-ear test-mic            # Probar micrófono

Para más información: https://github.com/Blackmvmba88/Iyari-ear
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando: doctor
    subparsers.add_parser('doctor', help='Verifica el sistema (mic, puertos, dependencias)')
    
    # Comando: test-mic
    subparsers.add_parser('test-mic', help='Prueba el micrófono')
    
    # Comando: start
    start_parser = subparsers.add_parser('start', help='Inicia el servidor')
    start_parser.add_argument('--host', default='127.0.0.1', 
                            help='Host del servidor (default: 127.0.0.1)')
    start_parser.add_argument('--port', type=int, default=8000,
                            help='Puerto del servidor (default: 8000)')
    start_parser.add_argument('--no-browser', action='store_true',
                            help='No abrir el navegador automáticamente')
    
    args = parser.parse_args()
    
    # Si no se proporciona comando, mostrar ayuda
    if not args.command:
        parser.print_help()
        return
    
    # Ejecutar comando
    if args.command == 'doctor':
        doctor()
    elif args.command == 'test-mic':
        test_mic()
    elif args.command == 'start':
        start_server(
            host=args.host, 
            port=args.port, 
            open_browser=not args.no_browser
        )


if __name__ == '__main__':
    main()

# Subtítulos en Tiempo Real

Esta es una aplicación web sencilla para generar subtítulos en tiempo real. Captura audio desde el micrófono del navegador, lo envía a un servidor backend que lo transcribe a texto, y muestra los subtítulos en la pantalla.

Es una herramienta pensada para ayudar a personas con dificultades auditivas en conversaciones cara a cara, usando un celular o una tablet como pantalla de apoyo.

## Cómo funciona

La aplicación tiene dos partes principales:
1.  **Frontend**: Una página web (HTML, CSS, JavaScript) que se ejecuta en el navegador. Se encarga de pedir permiso para el micrófono, grabar el audio y enviarlo al backend. También recibe el texto transcrito y lo muestra.
2.  **Backend**: Un servidor en Python (FastAPI, WebSockets) que recibe los fragmentos de audio, utiliza la API de reconocimiento de voz de Google para transcribirlos a texto y los devuelve al frontend.

## Requisitos

- Python 3.7 o superior.
- Un micrófono conectado al dispositivo donde se abrirá la página web.
- Conexión a internet (ya que se usa la API de Google para la transcripción).

## Instrucciones de Instalación y Uso

Sigue estos pasos para poner en marcha la aplicación.

### 1. Preparar el Backend (El Servidor)

Primero, necesitamos instalar las dependencias de Python y ejecutar el servidor.

```bash
# 1. (Opcional pero recomendado) Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\\Scripts\\activate

# 2. Instala las librerías necesarias desde requirements.txt
pip install -r requirements.txt

# 3. Inicia el servidor
python main.py
```

Si todo va bien, verás un mensaje como este en tu terminal, lo que significa que el servidor está escuchando:
`Servidor de WebSockets iniciado en ws://0.0.0.0:8000`

**Deja esta terminal abierta mientras usas la aplicación.**

### 2. Usar la Aplicación (El Frontend)

Ahora que el servidor está corriendo, puedes abrir la interfaz.

**Opción A: En la misma computadora**

1.  Abre el archivo `index.html` directamente en tu navegador web (Firefox, Chrome, etc.).
2.  La página se cargará. Presiona el botón "Iniciar".
3.  El navegador te pedirá permiso para usar el micrófono. Debes aceptarlo.
4.  ¡Habla y los subtítulos aparecerán en la pantalla!

**Opción B: En tu celular (o cualquier otro dispositivo)**

Esta es la forma más práctica de usarlo.

1.  Asegúrate de que tu celular y la computadora donde corre el servidor estén **conectados a la misma red Wi-Fi**.
2.  Busca la dirección IP local de tu computadora.
    - **En Windows:** Abre `cmd` y escribe `ipconfig`. Busca la dirección "IPv4 Address".
    - **En macOS o Linux:** Abre una terminal y escribe `hostname -I` o `ifconfig`.
    - Será un número como `192.168.1.10` o `10.0.0.5`.
3.  En el navegador de tu celular, introduce la siguiente dirección:
    `http://<LA_IP_DE_TU_COMPUTADORA>:8000`
    (Reemplaza `<LA_IP_DE_TU_COMPUTADORA>` con el número que encontraste).

4.  La página cargará. Presiona "Iniciar", acepta el permiso del micrófono y ¡listo! El servidor de Python se encarga de todo.

---

## Solución de Problemas

### Error al instalar `PyAudio` en Linux

Si durante la instalación (`pip install -r requirements.txt`) ves un error relacionado con `PyAudio` y `portaudio.h`, significa que te falta una librería del sistema.

Puedes solucionarlo instalando el paquete de desarrollo de PortAudio. En sistemas basados en Debian/Ubuntu, el comando es:

```bash
sudo apt-get update && sudo apt-get install -y portaudio19-dev
```

Después de instalarlo, vuelve a ejecutar `pip install -r requirements.txt`.

---
*Creado con cariño para una amiga.*

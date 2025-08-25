document.addEventListener('DOMContentLoaded', () => {
    // Elementos del DOM
    const subtitlesElement = document.getElementById('subtitles');
    const statusElement = document.getElementById('status');
    const toggleBtn = document.getElementById('toggle-btn');

    // Estado de la aplicación
    let isRecording = false;
    let socket;
    let mediaRecorder;
    let audioChunks = [];

    // Configuración
    const WEBSOCKET_URL = `ws://${window.location.hostname}:8000`;
    const TIMESLICE_MS = 2000; // Enviar audio cada 2 segundos

    function connectWebSocket() {
        statusElement.textContent = 'Estado: Conectando...';
        socket = new WebSocket(WEBSOCKET_URL);

        socket.onopen = () => {
            console.log('WebSocket conectado.');
            statusElement.textContent = 'Estado: Listo para iniciar';
        };

        socket.onmessage = (event) => {
            // Cuando llega un mensaje del servidor (el texto transcrito)
            console.log('Texto recibido:', event.data);
            subtitlesElement.textContent = event.data;
        };

        socket.onclose = () => {
            console.log('WebSocket desconectado.');
            statusElement.textContent = 'Estado: Desconectado';
            isRecording = false;
            updateButton();
        };

        socket.onerror = (error) => {
            console.error('Error en WebSocket:', error);
            statusElement.textContent = 'Estado: Error de conexión';
            isRecording = false;
            updateButton();
        };
    }

    async function startRecording() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('La API de Media Devices no es soportada en este navegador.');
            return;
        }

        try {
            statusElement.textContent = 'Estado: Pidiendo permiso para micrófono...';
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            isRecording = true;
            updateButton();
            statusElement.textContent = 'Estado: Escuchando...';

            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0 && socket.readyState === WebSocket.OPEN) {
                    // Enviamos el fragmento de audio al servidor
                    socket.send(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                // Detener todas las pistas del stream (apaga el indicador del micrófono)
                stream.getTracks().forEach(track => track.stop());
            };

            // Empezamos a grabar y a enviar datos periódicamente
            mediaRecorder.start(TIMESLICE_MS);

        } catch (err) {
            console.error('Error al obtener el stream de audio:', err);
            statusElement.textContent = `Error: ${err.message}`;
            isRecording = false;
            updateButton();
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
        isRecording = false;
        updateButton();
        statusElement.textContent = 'Estado: Inactivo';
    }

    function updateButton() {
        if (isRecording) {
            toggleBtn.textContent = 'Detener';
            toggleBtn.classList.add('recording');
        } else {
            toggleBtn.textContent = 'Iniciar';
            toggleBtn.classList.remove('recording');
        }
    }

    toggleBtn.addEventListener('click', () => {
        if (isRecording) {
            stopRecording();
        } else {
            // Asegurarse de que el socket está conectado antes de grabar
            if (!socket || socket.readyState !== WebSocket.OPEN) {
                connectWebSocket();
                // Pequeña espera para que el socket se conecte antes de empezar a grabar
                setTimeout(startRecording, 1000);
            } else {
                startRecording();
            }
        }
    });

    // Iniciar la conexión al cargar la página
    connectWebSocket();
});

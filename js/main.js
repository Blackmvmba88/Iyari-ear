document.addEventListener('DOMContentLoaded', () => {
    // Elementos del DOM
    const subtitlesElement = document.getElementById('subtitles');
    const subtitlesContainer = document.getElementById('subtitles-container');
    const statusElement = document.getElementById('status');
    const toggleBtn = document.getElementById('toggle-btn');
    const languageSelect = document.getElementById('language-select');
    const rainbowModeCheckbox = document.getElementById('rainbow-mode');
    const highContrastCheckbox = document.getElementById('high-contrast-mode');

    // Verificar que los elementos existan
    if (!subtitlesElement || !statusElement || !toggleBtn || !languageSelect) {
        console.error('Error: Elementos del DOM no encontrados');
        return;
    }

    // Estado de la aplicación
    let isRecording = false;
    let socket = null;
    let mediaRecorder = null;
    let reconnectAttempts = 0;
    const MAX_RECONNECT_ATTEMPTS = 5;
    const RECONNECT_DELAY_MS = 3000;
    const CONNECTION_WAIT_MS = 1000; // Tiempo de espera para conexión antes de iniciar grabación

    // Configuración
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsPort = window.location.port || (window.location.protocol === 'https:' ? '443' : '8000');
    const WEBSOCKET_URL = `${wsProtocol}//${window.location.hostname}:${wsPort}/ws`;
    const TIMESLICE_MS = 2000; // Enviar audio cada 2 segundos

    function connectWebSocket() {
        if (socket && socket.readyState === WebSocket.CONNECTING) {
            console.log('Ya hay una conexión en progreso.');
            return;
        }

        statusElement.textContent = 'Estado: Conectando...';
        
        try {
            socket = new WebSocket(WEBSOCKET_URL);
        } catch (error) {
            console.error('Error al crear WebSocket:', error);
            statusElement.textContent = 'Estado: Error al conectar';
            scheduleReconnect();
            return;
        }

        socket.onopen = () => {
            console.log('WebSocket conectado.');
            statusElement.textContent = 'Estado: Listo para iniciar';
            statusElement.classList.remove('active');
            reconnectAttempts = 0; // Reset reconnect counter on successful connection
            
            // Send initial language preference
            const language = languageSelect.value;
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: 'language', language: language }));
            }
        };

        socket.onmessage = (event) => {
            // Cuando llega un mensaje del servidor (el texto transcrito)
            if (event.data) {
                console.log('Texto recibido:', event.data);
                subtitlesElement.textContent = event.data;
                // Activar animación de pulse cuando llega texto
                if (subtitlesContainer) {
                    subtitlesContainer.classList.add('listening');
                    setTimeout(() => {
                        subtitlesContainer.classList.remove('listening');
                    }, 2000);
                }
            }
        };

        socket.onclose = (event) => {
            console.log('WebSocket desconectado. Código:', event.code);
            statusElement.textContent = 'Estado: Desconectado';
            if (isRecording) {
                stopRecording();
            }
            // Intentar reconectar si no fue un cierre limpio
            if (event.code !== 1000 && event.code !== 1001) {
                scheduleReconnect();
            }
        };

        socket.onerror = (error) => {
            console.error('Error en WebSocket:', error);
            statusElement.textContent = 'Estado: Error de conexión';
            if (isRecording) {
                stopRecording();
            }
        };
    }

    function scheduleReconnect() {
        if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            reconnectAttempts++;
            console.log(`Intentando reconectar (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`);
            statusElement.textContent = `Estado: Reconectando (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`;
            setTimeout(connectWebSocket, RECONNECT_DELAY_MS);
        } else {
            console.error('Se alcanzó el límite de intentos de reconexión.');
            statusElement.textContent = 'Estado: No se pudo conectar. Recarga la página.';
        }
    }

    async function startRecording() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('La API de Media Devices no es soportada en este navegador.');
            statusElement.textContent = 'Estado: Navegador no compatible';
            return;
        }

        // Verificar conexión WebSocket
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            statusElement.textContent = 'Estado: Esperando conexión...';
            connectWebSocket();
            return;
        }

        try {
            statusElement.textContent = 'Estado: Pidiendo permiso para micrófono...';
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            isRecording = true;
            updateButton();
            statusElement.textContent = 'Estado: Escuchando...';
            statusElement.classList.add('active');
            if (subtitlesContainer) {
                subtitlesContainer.classList.add('listening');
            }

            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0 && socket && socket.readyState === WebSocket.OPEN) {
                    // Enviamos el fragmento de audio al servidor
                    try {
                        socket.send(event.data);
                    } catch (error) {
                        console.error('Error al enviar audio:', error);
                    }
                }
            };

            mediaRecorder.onstop = () => {
                // Detener todas las pistas del stream (apaga el indicador del micrófono)
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorder.onerror = (event) => {
                console.error('Error en MediaRecorder:', event.error);
                stopRecording();
                statusElement.textContent = 'Estado: Error de grabación';
            };

            // Empezamos a grabar y a enviar datos periódicamente
            mediaRecorder.start(TIMESLICE_MS);

        } catch (err) {
            console.error('Error al obtener el stream de audio:', err);
            let errorMessage = 'Error desconocido';
            if (err.name === 'NotAllowedError') {
                errorMessage = 'Permiso de micrófono denegado';
            } else if (err.name === 'NotFoundError') {
                errorMessage = 'No se encontró micrófono';
            } else if (err.message) {
                errorMessage = err.message;
            }
            statusElement.textContent = `Estado: ${errorMessage}`;
            isRecording = false;
            updateButton();
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            try {
                mediaRecorder.stop();
            } catch (error) {
                console.error('Error al detener grabación:', error);
            }
        }
        mediaRecorder = null;
        isRecording = false;
        updateButton();
        statusElement.textContent = 'Estado: Inactivo';
        statusElement.classList.remove('active');
        if (subtitlesContainer) {
            subtitlesContainer.classList.remove('listening');
        }
    }

    function updateButton() {
        if (isRecording) {
            toggleBtn.textContent = 'Detener';
            toggleBtn.classList.add('recording');
            toggleBtn.setAttribute('aria-pressed', 'true');
        } else {
            toggleBtn.textContent = 'Iniciar';
            toggleBtn.classList.remove('recording');
            toggleBtn.setAttribute('aria-pressed', 'false');
        }
    }

    toggleBtn.addEventListener('click', async () => {
        if (isRecording) {
            stopRecording();
        } else {
            // Asegurarse de que el socket está conectado antes de grabar
            if (!socket || socket.readyState !== WebSocket.OPEN) {
                connectWebSocket();
                // Esperar a que se conecte antes de iniciar grabación
                setTimeout(() => {
                    if (socket && socket.readyState === WebSocket.OPEN) {
                        startRecording();
                    }
                }, CONNECTION_WAIT_MS);
            } else {
                startRecording();
            }
        }
    });

    // Update language when selection changes
    languageSelect.addEventListener('change', () => {
        const language = languageSelect.value;
        console.log('Idioma cambiado a:', language);
        
        // Send language update to server if connected
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ type: 'language', language: language }));
            subtitlesElement.textContent = `Idioma cambiado a: ${language === 'es-ES' ? 'Español' : 'English'}`;
        }
    });

    // Modo Arcoíris
    if (rainbowModeCheckbox) {
        rainbowModeCheckbox.addEventListener('change', () => {
            if (rainbowModeCheckbox.checked) {
                document.body.classList.add('rainbow-mode');
                console.log('Modo arcoíris activado');
            } else {
                document.body.classList.remove('rainbow-mode');
                console.log('Modo arcoíris desactivado');
            }
        });
    }

    // Modo Alto Contraste
    if (highContrastCheckbox) {
        highContrastCheckbox.addEventListener('change', () => {
            if (highContrastCheckbox.checked) {
                document.body.classList.add('high-contrast');
                console.log('Modo alto contraste activado');
            } else {
                document.body.classList.remove('high-contrast');
                console.log('Modo alto contraste desactivado');
            }
        });
    }

    // Limpiar al cerrar la página
    window.addEventListener('beforeunload', () => {
        if (isRecording) {
            stopRecording();
        }
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.close(1000, 'Página cerrada');
        }
    });

    // Iniciar la conexión al cargar la página
    connectWebSocket();
});

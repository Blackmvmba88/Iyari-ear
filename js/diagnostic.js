/**
 * Sistema de Diagnóstico Electrónico - Cliente JavaScript
 * Modo asíncrono: Foto → Procesa → Diagnóstico
 */

document.addEventListener('DOMContentLoaded', () => {
    // Elementos del DOM
    const boardModelInput = document.getElementById('board-model');
    const diagnosticStyleSelect = document.getElementById('diagnostic-style');
    const createSessionBtn = document.getElementById('create-session-btn');
    const imageTypeSelect = document.getElementById('image-type');
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const imagesPreview = document.getElementById('images-preview');
    const analyzeBtn = document.getElementById('analyze-btn');
    const diagnosisArea = document.getElementById('diagnosis-area');
    const reportSection = document.getElementById('report-section');
    const reportContent = document.getElementById('report-content');
    const exportJsonBtn = document.getElementById('export-json-btn');
    const exportTextBtn = document.getElementById('export-text-btn');
    const newSessionBtn = document.getElementById('new-session-btn');

    // Estado de la aplicación
    let currentSessionId = null;
    let uploadedImages = [];
    let diagnosticResults = null;

    // Configuración de API
    const API_BASE = window.location.origin;
    const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const WS_PORT = window.location.port || (window.location.protocol === 'https:' ? '443' : '8000');

    /**
     * Crear nueva sesión de diagnóstico
     */
    createSessionBtn.addEventListener('click', async () => {
        const boardModel = boardModelInput.value.trim();
        const style = diagnosticStyleSelect.value;

        if (!boardModel) {
            alert('Por favor, ingresa el modelo de la placa');
            return;
        }

        try {
            createSessionBtn.disabled = true;
            createSessionBtn.textContent = 'Creando...';

            const response = await fetch(`${API_BASE}/api/diagnostic/session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    board_model: boardModel,
                    diagnostic_style: style
                })
            });

            if (!response.ok) {
                throw new Error('Error al crear sesión');
            }

            const data = await response.json();
            currentSessionId = data.session_id;

            showMessage('✅ Sesión creada: ' + currentSessionId, 'success');
            createSessionBtn.textContent = '✓ Sesión Activa';
            createSessionBtn.style.background = 'linear-gradient(135deg, #00ff9f 0%, #00d4ff 100%)';
            
            // Habilitar carga de imágenes
            uploadArea.style.pointerEvents = 'auto';
            uploadArea.style.opacity = '1';

        } catch (error) {
            console.error('Error:', error);
            alert('Error al crear sesión. Verifica que el servidor esté corriendo.');
            createSessionBtn.disabled = false;
            createSessionBtn.textContent = 'Crear Sesión';
        }
    });

    /**
     * Manejo de drag & drop
     */
    uploadArea.addEventListener('click', () => {
        if (!currentSessionId) {
            alert('Primero crea una sesión de diagnóstico');
            return;
        }
        fileInput.click();
    });

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (!currentSessionId) {
            alert('Primero crea una sesión de diagnóstico');
            return;
        }

        const files = Array.from(e.dataTransfer.files);
        handleFiles(files);
    });

    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        handleFiles(files);
    });

    /**
     * Manejar archivos subidos
     */
    async function handleFiles(files) {
        const imageFiles = files.filter(file => file.type.startsWith('image/'));
        
        if (imageFiles.length === 0) {
            alert('Por favor, sube solo archivos de imagen');
            return;
        }

        for (const file of imageFiles) {
            try {
                // Subir imagen al servidor
                const formData = new FormData();
                formData.append('file', file);
                formData.append('session_id', currentSessionId);
                formData.append('image_type', imageTypeSelect.value);

                const response = await fetch(`${API_BASE}/api/diagnostic/upload`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Error al subir imagen');
                }

                const data = await response.json();
                
                // Agregar a la lista
                uploadedImages.push({
                    id: data.image_id,
                    type: imageTypeSelect.value,
                    file: file,
                    url: URL.createObjectURL(file)
                });

                // Mostrar preview
                addImagePreview(file, imageTypeSelect.value);

            } catch (error) {
                console.error('Error al subir imagen:', error);
                alert(`Error al subir ${file.name}`);
            }
        }

        // Habilitar botón de análisis si hay imágenes
        if (uploadedImages.length > 0) {
            analyzeBtn.disabled = false;
        }
    }

    /**
     * Agregar preview de imagen
     */
    function addImagePreview(file, type) {
        const item = document.createElement('div');
        item.className = 'image-item';

        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.alt = type;

        const badge = document.createElement('div');
        badge.className = 'badge';
        badge.textContent = type;

        item.appendChild(img);
        item.appendChild(badge);
        imagesPreview.appendChild(item);
    }

    /**
     * Analizar imágenes
     */
    analyzeBtn.addEventListener('click', async () => {
        if (!currentSessionId || uploadedImages.length === 0) {
            alert('Sube al menos una imagen primero');
            return;
        }

        try {
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = '🔄 Analizando...';

            // Limpiar área de diagnóstico
            diagnosisArea.innerHTML = '';

            // Mostrar progreso inicial
            showProgressMessage('📸 Procesando imágenes...', diagnosisArea);

            // Iniciar análisis
            const response = await fetch(`${API_BASE}/api/diagnostic/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: currentSessionId
                })
            });

            if (!response.ok) {
                throw new Error('Error al analizar imágenes');
            }

            // Conectar WebSocket para actualizaciones en tiempo real
            connectDiagnosticWebSocket();

        } catch (error) {
            console.error('Error:', error);
            alert('Error al iniciar análisis');
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = '🔍 Analizar Imágenes';
        }
    });

    /**
     * Conectar WebSocket para actualizaciones en tiempo real
     */
    function connectDiagnosticWebSocket() {
        const ws = new WebSocket(`${WS_PROTOCOL}//${window.location.hostname}:${WS_PORT}/ws/diagnostic/${currentSessionId}`);

        ws.onopen = () => {
            console.log('WebSocket de diagnóstico conectado');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'progress') {
                showProgressMessage(data.message, diagnosisArea);
            } else if (data.type === 'hypothesis') {
                displayHypothesis(data.hypothesis);
            } else if (data.type === 'complete') {
                diagnosticResults = data.results;
                showCompletionMessage();
                displayFullReport(data.results);
                ws.close();
            }
        };

        ws.onerror = (error) => {
            console.error('Error en WebSocket:', error);
        };

        ws.onclose = () => {
            console.log('WebSocket cerrado');
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = '✓ Análisis Completo';
        };
    }

    /**
     * Mostrar mensaje de progreso
     */
    function showProgressMessage(message, container) {
        const msgElement = document.createElement('div');
        msgElement.className = 'progress-message';
        msgElement.textContent = message;
        container.appendChild(msgElement);
        
        // Auto-scroll al final
        container.scrollTop = container.scrollHeight;
    }

    /**
     * Mostrar hipótesis de diagnóstico
     */
    function displayHypothesis(hypothesis) {
        const hypElement = document.createElement('div');
        hypElement.className = 'hypothesis';

        const confidence = (hypothesis.overall_confidence * 100).toFixed(1);
        
        hypElement.innerHTML = `
            <div class="hypothesis-header">
                <h3>💡 Hipótesis de Diagnóstico</h3>
                <span class="confidence-badge">Confianza: ${confidence}%</span>
            </div>

            <div class="layer layer-1">
                <h4>📍 Capa 1 - Localización</h4>
                <p><strong>Rail:</strong> ${hypothesis.layer1.voltage_rail || 'N/A'}</p>
                <p><strong>Componente:</strong> ${hypothesis.layer1.component_id || 'N/A'}</p>
                <p><strong>Bloque:</strong> ${hypothesis.layer1.functional_block || 'N/A'}</p>
            </div>

            <div class="layer layer-2">
                <h4>🔍 Capa 2 - Causa</h4>
                <p><strong>Causa:</strong> ${hypothesis.layer2.fault_cause}</p>
                <p><strong>Razonamiento:</strong> ${hypothesis.layer2.reasoning}</p>
                ${hypothesis.layer2.evidence && hypothesis.layer2.evidence.length > 0 
                    ? `<p><strong>Evidencia:</strong> ${hypothesis.layer2.evidence.join(', ')}</p>` 
                    : ''}
            </div>

            <div class="layer layer-3">
                <h4>⚡ Capa 3 - Consecuencia</h4>
                <p><strong>Impacto:</strong> <span class="impact-${hypothesis.layer3.impact_level}">${hypothesis.layer3.impact_level.toUpperCase()}</span></p>
                <p><strong>Efecto:</strong> ${hypothesis.layer3.functional_impact}</p>
                ${hypothesis.layer3.affected_features && hypothesis.layer3.affected_features.length > 0
                    ? `<p><strong>Afecta:</strong> ${hypothesis.layer3.affected_features.join(', ')}</p>`
                    : ''}
            </div>

            ${hypothesis.next_steps && hypothesis.next_steps.length > 0 ? `
                <div class="next-steps">
                    <h4>🔧 Próximos Pasos</h4>
                    <ul>
                        ${hypothesis.next_steps.map(step => `<li>${step}</li>`).join('')}
                    </ul>
                    ${hypothesis.test_points && hypothesis.test_points.length > 0 
                        ? `<p style="margin-top: 10px;"><strong>Puntos de prueba:</strong> ${hypothesis.test_points.join(', ')}</p>`
                        : ''}
                </div>
            ` : ''}
        `;

        diagnosisArea.appendChild(hypElement);
        diagnosisArea.scrollTop = diagnosisArea.scrollHeight;
    }

    /**
     * Mostrar mensaje de completación
     */
    function showCompletionMessage() {
        const statusElement = document.createElement('div');
        statusElement.className = 'diagnosis-status status-complete';
        statusElement.innerHTML = `
            <strong>✅ Diagnóstico Completo</strong>
            <p style="margin-top: 5px;">El análisis ha finalizado. Puedes revisar el reporte completo abajo.</p>
        `;
        diagnosisArea.insertBefore(statusElement, diagnosisArea.firstChild);
    }

    /**
     * Mostrar reporte completo
     */
    function displayFullReport(results) {
        reportSection.style.display = 'block';
        reportContent.textContent = results.report_text || JSON.stringify(results, null, 2);
    }

    /**
     * Exportar JSON
     */
    exportJsonBtn.addEventListener('click', () => {
        if (!diagnosticResults) {
            alert('No hay resultados para exportar');
            return;
        }

        const dataStr = JSON.stringify(diagnosticResults, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `diagnostico_${currentSessionId}.json`;
        link.click();
        
        URL.revokeObjectURL(url);
    });

    /**
     * Exportar texto
     */
    exportTextBtn.addEventListener('click', () => {
        if (!diagnosticResults || !diagnosticResults.report_text) {
            alert('No hay reporte para exportar');
            return;
        }

        const dataBlob = new Blob([diagnosticResults.report_text], { type: 'text/plain' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `diagnostico_${currentSessionId}.txt`;
        link.click();
        
        URL.revokeObjectURL(url);
    });

    /**
     * Nueva sesión
     */
    newSessionBtn.addEventListener('click', () => {
        if (confirm('¿Deseas iniciar una nueva sesión? Se perderá el estado actual.')) {
            location.reload();
        }
    });

    /**
     * Mostrar mensaje general
     */
    function showMessage(message, type = 'info') {
        const statusElement = document.createElement('div');
        statusElement.className = `diagnosis-status status-${type}`;
        statusElement.textContent = message;
        diagnosisArea.appendChild(statusElement);
        
        setTimeout(() => {
            statusElement.remove();
        }, 5000);
    }

    // Estado inicial
    console.log('Sistema de Diagnóstico Electrónico cargado');
    console.log('Estilo: Modo asíncrono (Foto → Procesa → Diagnóstico)');
});

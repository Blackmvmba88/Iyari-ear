// =================================================================================
// DOM & CANVAS SETUP
// =================================================================================
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');
const controlsPanel = document.getElementById('controls-panel');

// =================================================================================
// CONTROL PANEL INPUTS
// =================================================================================
const colorPicker = document.getElementById('color-picker');
const audioVizToggle = document.getElementById('audio-viz-toggle');
const rainbowModeCheckbox = document.getElementById('rainbow-mode');
const fontSizeSlider = document.getElementById('font-size');
const speedSlider = document.getElementById('speed');
const densitySlider = document.getElementById('density');
const charSetRadios = document.querySelectorAll('input[name="char-set"]');
const fullscreenBtn = document.getElementById('fullscreen-btn');
const resetBtn = document.getElementById('reset-btn');
const toggleControlsBtn = document.getElementById('toggle-controls');

// =================================================================================
// VALUE DISPLAYS
// =================================================================================
const fontSizeValue = document.getElementById('font-size-value');
const speedValue = document.getElementById('speed-value');
const densityValue = document.getElementById('density-value');
const colorPreview = document.querySelector('.color-preview');

// =================================================================================
// GLOBAL STATE
// =================================================================================
// Canvas & Rain State
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let fontSize = parseInt(fontSizeSlider.value);
let columns = canvas.width / fontSize;
let rainDrops = [];
let hue = 0;
let density = parseFloat(densitySlider.value);
const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const nums = '0123456789';
const binary = '01';
let characters = katakana;

// Animation Loop State
let lastTime = 0;
let timer = 0;
let speed = parseInt(speedSlider.value);
let interval = 105 - speed;

// Audio Visualizer State
let isAudioVisualizerEnabled = false;
let audioContext;
let analyser;
let dataArray;
let audioInitialized = false;

// AGC (Automatic Gain Control) & Limiter State for Audio
let audioGain = 1.5;
const targetBassLevel = 40; // The "ideal" bass level for the AGC to target.
const maxGain = 8.0;
const minGain = 0.5;
let waveAmplitude = 0; // The final, smoothed amplitude for drawing the sine wave.

// =================================================================================
// CORE FUNCTIONS
// =================================================================================

/**
 * Initializes the Web Audio API to capture microphone input.
 * This function must be triggered by a user gesture (e.g., a click).
 */
const initAudio = async () => {
    if (audioInitialized) return;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);

        // Configure the analyser
        analyser.fftSize = 256; // Determines the number of frequency bins
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        audioInitialized = true;
        console.log("Audio context initialized successfully.");
    } catch (err) {
        console.error("Error initializing audio context:", err);
        // If permission is denied, uncheck the box and alert the user.
        audioVizToggle.checked = false;
        isAudioVisualizerEnabled = false;
        alert("Could not access the microphone. Audio features will be disabled.");
    }
};

/**
 * Processes audio data to implement Automatic Gain Control (AGC) and a Limiter.
 * This makes the sine wave visualization responsive to both quiet and loud sounds.
 */
const updateAudioState = () => {
    if (!dataArray) return;

    // 1. Calculate the average level of the bass frequencies.
    let bassSum = 0;
    const bassBins = 5; // We'll use the first 5 bins for our bass measurement.
    for (let i = 1; i <= bassBins; i++) {
        bassSum += dataArray[i];
    }
    const currentBassLevel = bassSum / bassBins;

    // 2. Implement AGC: Adjust gain based on how far the current level is from our target.
    const adjustmentSpeed = 0.0005; // Slow adjustment for smooth transitions.
    if (currentBassLevel < targetBassLevel && audioGain < maxGain) {
        audioGain += adjustmentSpeed; // If too quiet, slowly increase gain.
    } else if (audioGain > minGain) {
        audioGain -= adjustmentSpeed; // If loud enough, slowly decrease gain.
    }
    audioGain = Math.max(minGain, Math.min(audioGain, maxGain)); // Clamp gain within bounds.

    // 3. Calculate final amplitude: Apply gain and then a hard limiter.
    const rawAmplitude = (currentBassLevel / 255) * (canvas.height / 3.5);
    const boostedAmplitude = rawAmplitude * audioGain;
    const maxAmplitude = canvas.height / 3.0; // The absolute maximum height of the wave.

    // 4. Smoothly interpolate to the new amplitude value to prevent jerky movements.
    waveAmplitude += (boostedAmplitude - waveAmplitude) * 0.1;
    waveAmplitude = Math.min(waveAmplitude, maxAmplitude); // Apply the limiter.
};

/**
 * Resets the raindrop positions. Called on startup and window resize.
 */
const resetRain = () => {
    columns = Math.floor(canvas.width / fontSize);
    rainDrops = [];
    for (let x = 0; x < columns; x++) {
        rainDrops[x] = {
            y: 1 - Math.floor(Math.random() * canvas.height / fontSize),
            char: '', // Stores the last character to implement the "glow head" effect.
        };
    }
};

/**
 * Draws the reactive sine wave on the canvas.
 * Uses the pre-calculated `waveAmplitude` for a smooth, processed visualization.
 */
const drawSineWave = () => {
    if (!audioInitialized) return;

    const frequency = 0.03;
    const phase = Date.now() * 0.002; // Causes the wave to animate horizontally.
    const verticalOffset = canvas.height / 2;

    ctx.beginPath();
    ctx.moveTo(0, verticalOffset);

    ctx.strokeStyle = 'rgba(0, 80, 200, 0.6)';
    ctx.lineWidth = 2;
    ctx.shadowColor = 'rgba(0, 100, 255, 1)';
    ctx.shadowBlur = 10;

    for (let x = 0; x < canvas.width; x++) {
        const y = verticalOffset + waveAmplitude * Math.sin(frequency * x + phase);
        ctx.lineTo(x, y);
    }

    ctx.stroke();
    ctx.shadowBlur = 0; // Reset shadow to not affect other elements.
};

/**
 * The main drawing function for the Matrix rain effect.
 */
const draw = () => {
    // 1. Draw a semi-transparent black rectangle to create the fading trail effect.
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Draw the audio visualizer behind the rain, if enabled.
    if (isAudioVisualizerEnabled && audioInitialized) {
        drawSineWave();
    }

    // 3. Determine the color for the rain's tail.
    let tailColor;
    if (rainbowModeCheckbox.checked) {
        hue = (hue + 1) % 360;
        tailColor = `hsl(${hue}, 100%, 50%)`;
    } else {
        tailColor = colorPicker.value;
    }
    const headColor = '#f0f0f0'; // Bright, off-white for the leading character.

    ctx.font = `${fontSize}px 'Courier New', 'Monaco', monospace`;

    // 4. Loop through each column to draw the rain.
    for (let i = 0; i < rainDrops.length; i++) {
        const column = rainDrops[i];

        // "Glow Head" Effect Part 1: Redraw the previous head character in the tail color.
        if (column.char) {
            ctx.fillStyle = tailColor;
            ctx.shadowColor = tailColor;
            ctx.shadowBlur = 7;
            ctx.fillText(column.char, i * fontSize, (column.y - 1) * fontSize);
        }

        // "Glow Head" Effect Part 2: Draw the new head character in a bright color.
        const newChar = characters.charAt(Math.floor(Math.random() * characters.length));
        ctx.fillStyle = headColor;
        ctx.shadowColor = headColor;
        ctx.shadowBlur = 12;
        ctx.fillText(newChar, i * fontSize, column.y * fontSize);

        // 5. Update the column's state for the next frame.
        column.char = newChar;
        if (column.y * fontSize > canvas.height && Math.random() > density) {
            column.y = 0;
            column.char = '';
        }
        column.y++;
    }
};

/**
 * The main animation loop, using requestAnimationFrame for performance.
 * @param {number} timeStamp - The timestamp provided by requestAnimationFrame.
 */
function animate(timeStamp = 0) {
    const deltaTime = timeStamp - lastTime;
    lastTime = timeStamp;

    // Audio state should be updated on every frame for maximum smoothness.
    if (isAudioVisualizerEnabled && audioInitialized) {
        analyser.getByteFrequencyData(dataArray);
        updateAudioState();
    }

    // The Matrix rain's drawing speed is controlled by the speed slider.
    if (timer > interval) {
        draw();
        timer = 0;
    } else {
        timer += deltaTime;
    }

    requestAnimationFrame(animate);
}

// =================================================================================
// UI & EVENT LISTENERS
// =================================================================================

/**
 * Updates the animation speed based on the slider value.
 */
const updateAnimationSpeed = () => {
    speed = parseInt(speedSlider.value);
    interval = 105 - speed; // Invert value so higher on slider means faster.
};

/**
 * Resets all controls and settings to their default values.
 */
const resetToDefaults = () => {
    // Reset control panel values
    colorPicker.value = '#00ff00';
    rainbowModeCheckbox.checked = false;
    audioVizToggle.checked = false;
    fontSizeSlider.value = 16;
    speedSlider.value = 30;
    densitySlider.value = 0.015;
    document.querySelector('input[name="char-set"][value="katakana"]').checked = true;

    // Reset internal state
    isAudioVisualizerEnabled = false;

    // Trigger change events to apply the default values
    fontSizeSlider.dispatchEvent(new Event('input'));
    speedSlider.dispatchEvent(new Event('input'));
    densitySlider.dispatchEvent(new Event('input'));
    document.querySelector('input[name="char-set"]:checked').dispatchEvent(new Event('change'));

    updateAnimationSpeed();
};

// --- Attach Event Listeners ---

audioVizToggle.addEventListener('change', (e) => {
    isAudioVisualizerEnabled = e.target.checked;
    // Initialize audio only when the user first enables it.
    if (isAudioVisualizerEnabled && !audioInitialized) {
        initAudio();
    }
});

colorPicker.addEventListener('input', (e) => {
    colorPreview.style.background = e.target.value;
});

fontSizeSlider.addEventListener('input', (e) => {
    fontSize = parseInt(e.target.value);
    fontSizeValue.textContent = fontSize;
    resetRain();
});

speedSlider.addEventListener('input', (e) => {
    speedValue.textContent = e.target.value;
    updateAnimationSpeed();
});

densitySlider.addEventListener('input', (e) => {
    density = parseFloat(e.target.value);
    densityValue.textContent = density;
});

charSetRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        switch (e.target.value) {
            case 'katakana': characters = katakana; break;
            case 'latin': characters = latin + nums; break;
            case 'binary': characters = binary; break;
            case 'mix': characters = katakana + latin + nums + binary; break;
        }
    });
});

fullscreenBtn.addEventListener('click', () => {
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        document.documentElement.requestFullscreen();
    }
});

resetBtn.addEventListener('click', resetToDefaults);

toggleControlsBtn.addEventListener('click', () => {
    controlsPanel.classList.toggle('hidden');
    toggleControlsBtn.textContent = controlsPanel.classList.contains('hidden') ? 'Mostrar Controles' : 'Ocultar Controles';
});

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    resetRain();
});

// =================================================================================
// INITIALIZATION
// =================================================================================
resetToDefaults();
resetRain();
animate(0); // Start the animation loop
colorPreview.style.background = colorPicker.value;
fontSizeValue.textContent = fontSizeSlider.value;
speedValue.textContent = speedSlider.value;
densityValue.textContent = densitySlider.value;

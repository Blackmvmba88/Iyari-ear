// DOM Elements
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');
const controlsPanel = document.getElementById('controls-panel');

// Control Inputs
const colorPicker = document.getElementById('color-picker');
const rainbowModeCheckbox = document.getElementById('rainbow-mode');
const fontSizeSlider = document.getElementById('font-size');
const speedSlider = document.getElementById('speed');
const densitySlider = document.getElementById('density');
const charSetRadios = document.querySelectorAll('input[name="char-set"]');
const fullscreenBtn = document.getElementById('fullscreen-btn');
const resetBtn = document.getElementById('reset-btn');
const toggleControlsBtn = document.getElementById('toggle-controls');

// Value Displays
const fontSizeValue = document.getElementById('font-size-value');
const speedValue = document.getElementById('speed-value');
const densityValue = document.getElementById('density-value');
const colorPreview = document.querySelector('.color-preview');

// Canvas Setup
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Character Sets
const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const nums = '0123456789';
const binary = '01';
let characters = katakana;

// Animation State
let fontSize = parseInt(fontSizeSlider.value);
let columns = canvas.width / fontSize;
let rainDrops = [];
let intervalId;
let hue = 0;
let density = parseFloat(densitySlider.value);

// Functions
const resetRain = () => {
    columns = Math.floor(canvas.width / fontSize);
    rainDrops = [];
    for (let x = 0; x < columns; x++) {
        rainDrops[x] = 1;
    }
};

const draw = () => {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    let color;
    if (rainbowModeCheckbox.checked) {
        hue = (hue + 1) % 360;
        color = `hsl(${hue}, 100%, 50%)`;
    } else {
        color = colorPicker.value;
    }

    ctx.fillStyle = color;
    ctx.font = `${fontSize}px 'Courier New', 'Monaco', monospace`;
    ctx.shadowColor = color;
    ctx.shadowBlur = 10;

    for (let i = 0; i < rainDrops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length));
        ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

        if (rainDrops[i] * fontSize > canvas.height && Math.random() > density) {
            rainDrops[i] = 0;
        }
        rainDrops[i]++;
    }
};

const updateAnimation = () => {
    clearInterval(intervalId);
    const speed = parseInt(speedSlider.value);
    // Invert speed value so higher is faster
    const interval = 105 - speed;
    intervalId = setInterval(draw, interval);
};

const resetToDefaults = () => {
    colorPicker.value = '#00ff00';
    rainbowModeCheckbox.checked = false;
    fontSizeSlider.value = 16;
    speedSlider.value = 30;
    densitySlider.value = 0.975;
    document.querySelector('input[name="char-set"][value="katakana"]').checked = true;

    // Trigger change events to update state
    fontSizeSlider.dispatchEvent(new Event('input'));
    speedSlider.dispatchEvent(new Event('input'));
    densitySlider.dispatchEvent(new Event('input'));
    document.querySelector('input[name="char-set"]:checked').dispatchEvent(new Event('change'));

    updateAnimation();
};

// Event Listeners
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
    updateAnimation();
});

densitySlider.addEventListener('input', (e) => {
    density = parseFloat(e.target.value);
    densityValue.textContent = density;
});

charSetRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        switch (e.target.value) {
            case 'katakana':
                characters = katakana;
                break;
            case 'latin':
                characters = latin + nums;
                break;
            case 'binary':
                characters = binary;
                break;
            case 'mix':
                characters = katakana + latin + nums + binary;
                break;
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
    if (controlsPanel.classList.contains('hidden')) {
        toggleControlsBtn.textContent = 'Mostrar Controles';
    } else {
        toggleControlsBtn.textContent = 'Ocultar Controles';
    }
});

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    resetRain();
});

// Initial Setup
resetToDefaults();
resetRain();
updateAnimation();
colorPreview.style.background = colorPicker.value;
fontSizeValue.textContent = fontSizeSlider.value;
speedValue.textContent = speedSlider.value;
densityValue.textContent = densitySlider.value;

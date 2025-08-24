const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');

const colorPicker = document.getElementById('color-picker');
const rainbowModeCheckbox = document.getElementById('rainbow-mode');
const fontSizeSlider = document.getElementById('font-size');
const speedSlider = document.getElementById('speed');
const charSetRadios = document.querySelectorAll('input[name="char-set"]');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Character sets
const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const nums = '0123456789';

let characters = katakana;

let fontSize = parseInt(fontSizeSlider.value);
let columns = canvas.width / fontSize;
let rainDrops = [];

const resetRain = () => {
    columns = canvas.width / fontSize;
    rainDrops = [];
    for (let x = 0; x < columns; x++) {
        rainDrops[x] = 1;
    }
};

resetRain();

let intervalId;

let hue = 0;
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
    ctx.font = fontSize + 'px monospace';

    ctx.shadowColor = color;
    ctx.shadowBlur = 10;

    for (let i = 0; i < rainDrops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length));
        ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

        if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            rainDrops[i] = 0;
        }
        rainDrops[i]++;
    }
};

const updateAnimation = () => {
    clearInterval(intervalId);
    intervalId = setInterval(draw, 110 - parseInt(speedSlider.value));
};

// Event Listeners
colorPicker.addEventListener('input', () => {
    // No need to restart the animation, color is picked up in the draw loop
});

fontSizeSlider.addEventListener('input', (e) => {
    fontSize = parseInt(e.target.value);
    resetRain();
});

speedSlider.addEventListener('input', () => {
    updateAnimation();
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
            case 'mix':
                characters = katakana + latin + nums;
                break;
        }
    });
});

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    resetRain();
});


updateAnimation();

console.log('Script loaded successfully.');

const canvas = document.getElementById('drawing-canvas');
const toolbarContainer = document.getElementById('toolbar-container');
const toggleToolbarBtn = document.getElementById('toggleToolbar');
const toolbar = document.getElementById('toolbar');
const activeToolText = document.getElementById('activeTool');
const ctx = canvas.getContext('2d');

const saveButton = document.getElementById('saveCanvas');
const loadButton = document.getElementById('loadCanvas');

const canvasOffsetX = canvas.offsetLeft;
const canvasOffsetY = canvas.offsetTop;

canvas.width = window.innerWidth - canvasOffsetX;
canvas.height = window.innerHeight - canvasOffsetY;

let isPainting = false;
let isErasing = false;
let collapsed = false;
let penWidth = 5;
let eraserWidth = 5;

toggleToolbarBtn.addEventListener('click', () => {
    toggleToolbarBtn.textContent = collapsed ? "《 " : " 》";
    toolbarContainer.classList.toggle('collapsed'); // Toggle collapsed class on toolbar container
    collapsed = !collapsed;
});

toolbar.addEventListener('click', e => {

    if (e.target.id === 'clear') {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    if (e.target.classList.contains('tool')) {
        const toolButtons = document.querySelectorAll('.tool');
        toolButtons.forEach(btn => btn.classList.remove('active')); // Remove "active" class from all buttons
        e.target.classList.add('active'); // Add "active" class to the clicked button THS DOESN"T WORK

        activeToolText.textContent = `Active Tool: ${e.target.textContent}`; // Update active tool text

        if (e.target.id === 'eraser') {
            isErasing = !isErasing;
            if (isErasing) {
                ctx.strokeStyle = 'white';
                ctx.lineWidth = eraserWidth;
            } else {
                ctx.strokeStyle = document.getElementById('stroke').value;
                ctx.lineWidth = penWidth;
            }
        } else if (e.target.id === 'pen') {
            isErasing = false;
            ctx.strokeStyle = document.getElementById('stroke').value;
            ctx.lineWidth = penWidth;
        }
    }
});

toolbar.addEventListener('change', e => {
    if (e.target.id === 'stroke' && !isErasing) {
        ctx.strokeStyle = e.target.value;
    }

    if (e.target.id === 'lineWidth') {
        penWidth = e.target.value;
        if (!isErasing) {
            ctx.lineWidth = penWidth;
        }
    }

    if (e.target.id === 'eraserWidth') {
        eraserWidth = e.target.value;
        if (isErasing) {
            ctx.lineWidth = eraserWidth;
        }
    }
});

const draw = (e) => {
    if (!isPainting) {
        return;
    }

    ctx.lineCap = 'round';

    ctx.lineTo(e.clientX - canvasOffsetX, e.clientY);
    ctx.stroke();
}

canvas.addEventListener('mousedown', (e) => {
    isPainting = true;
    ctx.lineWidth = isErasing ? eraserWidth : penWidth;
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvasOffsetX, e.clientY);
});

canvas.addEventListener('mouseup', e => {
    isPainting = false;
});

canvas.addEventListener('mousemove', draw);

const saveCanvas = () => {
    const dataURL = canvas.toDataURL(); // Get the data URL of the canvas
    localStorage.setItem('savedCanvas', dataURL); // Save the data URL to local storage
}

const loadCanvas = () => {
    const savedData = localStorage.getItem('savedCanvas'); // Get the saved data URL from local storage
    if (savedData) {
        const img = new Image();
        img.onload = () => {
            ctx.drawImage(img, 0, 0); // Draw the saved image onto the canvas
        }
        img.src = savedData;
    }
}

saveButton.addEventListener('click', saveCanvas);
loadButton.addEventListener('click', loadCanvas);
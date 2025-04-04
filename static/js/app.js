let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let startBtn = document.getElementById('startBtn');
let stopBtn = document.getElementById('stopBtn');
let ctx = canvas.getContext('2d');
let stream = null;
let isDetecting = false;

// Set canvas size
function setCanvasSize() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
}

// Start video stream
async function startVideo() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            setCanvasSize();
        };
    } catch (err) {
        console.error('Error accessing camera:', err);
        alert('Error accessing camera. Please make sure you have granted camera permissions.');
    }
}

// Motion detection
function detectMotion() {
    if (!isDetecting) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    let data = imageData.data;
    let motionDetected = false;

    // Simple motion detection algorithm
    for (let i = 0; i < data.length; i += 4) {
        let r = data[i];
        let g = data[i + 1];
        let b = data[i + 2];
        
        // Check for significant changes in pixel values
        if (Math.abs(r - 128) > 50 || Math.abs(g - 128) > 50 || Math.abs(b - 128) > 50) {
            motionDetected = true;
            break;
        }
    }

    if (motionDetected) {
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 3;
        ctx.strokeRect(0, 0, canvas.width, canvas.height);
    }

    requestAnimationFrame(detectMotion);
}

// Event listeners
startBtn.addEventListener('click', () => {
    if (!stream) {
        startVideo();
    }
    isDetecting = true;
    detectMotion();
});

stopBtn.addEventListener('click', () => {
    isDetecting = false;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}); 
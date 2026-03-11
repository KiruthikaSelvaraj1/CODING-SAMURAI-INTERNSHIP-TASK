// ================================================
// Image Caption Generator - JavaScript Application
// Professional UI Controller
// ================================================

let selectedFile = null;
let uploadStartTime = null;

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', function () {
    initializeEventListeners();
    console.log('🚀 Application initialized');
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');

    // Upload area click
    uploadArea.addEventListener('click', () => imageInput.click());

    // File input change
    imageInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Upload button
    uploadBtn.addEventListener('click', handleUpload);

    // Clear button
    clearBtn.addEventListener('click', clearSelectedFile);

    // Copy button
    copyBtn.addEventListener('click', copyCaption);
}

/**
 * Handle file selection
 */
function handleFileSelect(file) {
    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload: PNG, JPG, JPEG, GIF, or BMP');
        return;
    }

    // Validate file size
    if (file.size > 16 * 1024 * 1024) {
        showError('File is too large. Maximum size: 16MB');
        return;
    }

    selectedFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImage = document.getElementById('previewImage');
        previewImage.src = e.target.result;
        
        document.getElementById('previewSection').classList.remove('d-none');
        document.getElementById('uploadArea').style.display = 'none';
        document.getElementById('uploadBtn').disabled = false;
        document.getElementById('uploadBtn').innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate Caption';
        
        hideError();
    };
    reader.readAsDataURL(file);

    console.log(`📸 File selected: ${file.name} (${formatFileSize(file.size)})`);
}

/**
 * Handle drag over
 */
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.add('drag-over');
}

/**
 * Handle drag leave
 */
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.remove('drag-over');
}

/**
 * Handle drop
 */
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.remove('drag-over');

    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
}

/**
 * Handle image upload and caption generation
 */
async function handleUpload() {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }

    uploadStartTime = Date.now();
    const uploadBtn = document.getElementById('uploadBtn');
    
    // Show loading state
    showLoadingState();
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';

    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);

        console.log('📤 Uploading image...');

        // Send request
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        // Calculate processing time
        const processingTime = ((Date.now() - uploadStartTime) / 1000).toFixed(2);

        console.log('✓ Caption generated:', data.caption);
        showResultState(data, processingTime);

    } catch (error) {
        console.error('❌ Error:', error);
        showError(error.message || 'Failed to generate caption');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-zap"></i> Generate Caption';
    }
}

/**
 * Show loading state
 */
function showLoadingState() {
    document.getElementById('emptyState').classList.add('d-none');
    document.getElementById('resultState').classList.add('d-none');
    document.getElementById('errorState').classList.add('d-none');
    document.getElementById('loadingState').classList.remove('d-none');
}

/**
 * Show result state
 */
function showResultState(data, processingTime) {
    document.getElementById('loadingState').classList.add('d-none');
    document.getElementById('emptyState').classList.add('d-none');
    document.getElementById('errorState').classList.add('d-none');

    // Populate results
    const captionText = document.getElementById('captionText');
    captionText.textContent = data.caption;

    const wordCount = data.caption.split(' ').length;
    
    document.getElementById('statFilename').textContent = data.filename || 'Unknown';
    document.getElementById('statTime').textContent = processingTime + 's';
    document.getElementById('statWords').textContent = wordCount + ' words';

    document.getElementById('resultState').classList.remove('d-none');
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('emptyState').classList.add('d-none');
    document.getElementById('resultState').classList.add('d-none');
    document.getElementById('loadingState').classList.add('d-none');
    
    const errorState = document.getElementById('errorState');
    document.getElementById('errorText').textContent = message;
    errorState.classList.remove('d-none');

    console.error('❌', message);
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('errorState').classList.add('d-none');
}

/**
 * Clear selected file
 */
function clearSelectedFile() {
    selectedFile = null;
    document.getElementById('imageInput').value = '';
    document.getElementById('previewSection').classList.add('d-none');
    document.getElementById('uploadArea').style.display = 'block';
    
    document.getElementById('uploadBtn').innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Generate Caption';
    document.getElementById('emptyState').classList.remove('d-none');
    document.getElementById('resultState').classList.add('d-none');
    
    console.log('🔄 Selection cleared');
}

/**
 * Copy caption to clipboard
 */
function copyCaption() {
    const caption = document.getElementById('captionText').textContent;
    
    navigator.clipboard.writeText(caption).then(() => {
        const copyBtn = document.getElementById('copyBtn');
        const originalText = copyBtn.innerHTML;
        
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyBtn.disabled = true;
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.disabled = false;
        }, 2000);
        
        console.log('📋 Caption copied to clipboard');
    }).catch(() => {
        showError('Failed to copy caption');
    });
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Log application info
 */
console.log('%c🎯 Image Caption Generator v2.0', 'font-size: 16px; font-weight: bold; color: #6366f1;');
console.log('%cPowered by AI - InceptionV3 + LSTM', 'font-size: 12px; color: #8b5cf6;');
console.log('%cReady to process your images!', 'font-size: 12px; color: #10b981;');

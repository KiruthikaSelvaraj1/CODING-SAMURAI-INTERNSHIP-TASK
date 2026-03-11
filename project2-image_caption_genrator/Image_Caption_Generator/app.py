"""
Advanced Image Caption Generator Web Application
Uses BLIP (Vision-Language Model) for high-quality caption generation.
"""

import os
import sys
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variables
blip_generator = None
model_loaded = False


class AdvancedCaptionGenerator:
    """Generate captions using BLIP vision-language model"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading BLIP model on {self.device}...")
        
        # Load BLIP model
        model_name = "Salesforce/blip-image-captioning-base"
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        
        print("✓ BLIP model loaded successfully!")
    
    def generate_caption(self, image_path, prompt=None, max_length=50, num_beams=5):
        """Generate caption for an image"""
        try:
            raw_image = Image.open(image_path).convert('RGB')
            
            if prompt:
                inputs = self.processor(raw_image, prompt, return_tensors="pt").to(self.device)
            else:
                inputs = self.processor(raw_image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=num_beams,
                    do_sample=False,
                    repetition_penalty=1.1
                )
            
            caption = self.processor.decode(output[0], skip_special_tokens=True)
            return caption.strip()
            
        except Exception as e:
            print(f"Error: {e}")
            return "Could not generate caption"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model():
    """Load the BLIP caption generator model"""
    global blip_generator, model_loaded
    try:
        if not model_loaded:
            print("\n📦 Loading Advanced Caption Generator (BLIP)...")
            blip_generator = AdvancedCaptionGenerator()
            model_loaded = True
            print("✓ Model ready for inference\n")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and caption generation"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate caption
        print(f"\n[*] Processing: {filename}")
        caption = blip_generator.generate_caption(filepath, num_beams=7)
        print(f"[+] Caption: {caption}")
        
        return jsonify({
            'success': True,
            'caption': caption,
            'filename': filename,
            'filepath': f'/uploads/{filename}'
        }), 200
    
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate_caption():
    """Generate caption for existing image"""
    try:
        data = request.get_json()
        image_path = data.get('image_path')
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({'success': False, 'error': 'Image not found'}), 400
        
        caption = blip_generator.generate_caption(image_path, num_beams=7)
        
        return jsonify({
            'success': True,
            'caption': caption
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/uploads/<filename>')
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception:
        return jsonify({'error': 'File not found'}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'model_type': 'BLIP',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/info', methods=['GET'])
def get_info():
    return jsonify({
        'name': 'Advanced Image Caption Generator',
        'version': '3.0',
        'description': 'AI-powered caption generation using BLIP vision-language model',
        'model_loaded': model_loaded,
        'model_type': 'BLIP',
        'capabilities': ['image-upload', 'caption-generation', 'high-quality']
    }), 200


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Max size: 16MB'}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print(" [*] ADVANCED IMAGE CAPTION GENERATOR - BLIP Model v3.0")
    print("="*70)
    
    if load_model():
        print("\n[+] Starting Flask server...")
        print("[*] Access: http://localhost:5000")
        print("\nPress CTRL+C to stop\n")
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    else:
        print("\n[!] Failed to load model")
        sys.exit(1)


# AI Image Caption Generator

A deep learning web application that generates natural language descriptions for images using Facebook's BLIP (Bootstrapped Language-Image Pre-training) vision-language model.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)

## Features

- **High-Quality Captions**: Uses BLIP model for accurate, relevant image descriptions
- **Web Interface**: Easy-to-use Flask web application
- **CLI Support**: Command-line interface for quick caption generation
- **Multiple Image Formats**: Supports JPG, PNG, JPEG, GIF, BMP

## Demo

The model generates accurate captions like:
- Input: A photo of a mountain → Output: "a man standing on top of a snow covered mountain"
- Input: A dog photo → Output: "A golden retriever running in a grassy field"

## Installation

1. **Clone the repository:**
```bash
git clone <repo-url>
cd Image_Caption_Generator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Requirements

```
tensorflow>=2.10.0
keras>=2.10.0
numpy>=1.21.0
pillow>=9.0.0
matplotlib>=3.5.0
pandas>=1.3.0
scikit-learn>=1.0.0
flask>=2.3.0
flask-cors>=4.0.0
werkzeug>=2.3.0
transformers>=4.30.0
torch>=2.0.0
sentencepiece>=0.1.97
protobuf>=3.20.0
```

## Usage

### Option 1: Web Application (Recommended)

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

### Option 2: Command Line

```bash
python predict.py
```

Enter the path to your image when prompted.

### Option 3: Train Your Own Model

To train an improved custom model on your dataset:

```bash
python train_improved.py
```

This will train on all ~8000 images with Bidirectional LSTM.

## Project Structure

```
Image_Caption_Generator/
├── app.py                 # Flask web application
├── predict.py            # CLI caption generator
├── train_improved.py     # Training script
├── requirements.txt      # Dependencies
├── dataset/
│   ├── captions.txt     # Image captions (CSV)
│   └── Images/          # Training images
├── static/
│   ├── css/style.css   # Styling
│   └── js/app.js       # Frontend JavaScript
├── templates/
│   └── index.html      # Web UI template
└── uploads/            # Uploaded images
```

## Model Information

- **Primary Model**: Salesforce/blip-image-captioning-base
- **Architecture**: Vision Transformer + Language Model
- **Training Data**: COCO dataset (pre-trained)
- **Device**: CPU/GPU compatible

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/upload` | POST | Upload image and get caption |
| `/api/health` | GET | Health check |
| `/api/info` | GET | Model information |

## Performance

- **Caption Relevance**: High (uses pre-trained vision-language model)
- **Generation Speed**: ~2-5 seconds per image on CPU
- **Memory Usage**: ~2GB RAM

## Troubleshooting

**Issue**: Model download fails
- Solution: Check internet connection

**Issue**: Slow performance on CPU
- Solution: This is normal - GPU will be faster

**Issue**: Out of memory
- Solution: Close other applications

## License

Open source for educational purposes.

## Credits

- [BLIP Model](https://github.com/salesforce/BLIP) - Salesforce Research
- [Hugging Face Transformers](https://huggingface.co/)
- [Flickr8k Dataset](https://www.kaggle.com/datasets/adityajn105/flickr8k)

---

Made with ❤️ for image captioning

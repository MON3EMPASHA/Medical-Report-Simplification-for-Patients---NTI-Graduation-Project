# Medical Report Simplification for Patients - NTI Graduation Project

A Streamlit-based web application that simplifies complex medical reports into patient-friendly language using a fine-tuned FLAN-T5 model with LoRA adapters. The application supports both direct text input and image upload with OCR text extraction.

## Features

- 📝 **Text Input**: Direct text input for medical reports
- 📷 **Image Upload**: Upload images containing medical text with OCR extraction
- 🔍 **OCR Processing**: Automatic text extraction from images using Tesseract
- 🧠 **Text Preprocessing**: Advanced text processing using spaCy
- 🤖 **AI-Powered Simplification**: Fine-tuned FLAN-T5 model with LoRA adapters for medical text simplification
- 🎨 **Beautiful UI**: Professional, modern interface with gradient designs and responsive layout
- 📊 **Statistics**: Real-time processing statistics and text reduction metrics
- 💾 **Download Results**: Export simplified reports as text files

## Prerequisites

Before running the application, make sure you have the following installed:

### 1. Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Tesseract OCR

The application uses Tesseract for OCR functionality. Install it based on your operating system:

#### Windows:

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install the executable
3. Add Tesseract to your system PATH, or set the path in the code

#### macOS:

```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):

```bash
sudo apt-get install tesseract-ocr
```

### 3. spaCy English Model

Download the English language model for spaCy:

```bash
python -m spacy download en_core_web_sm
```

## Installation

### Quick Setup (Recommended)

Use the automated setup script:

```bash
python setup.py
```

This will automatically:

- Install all Python dependencies
- Download the spaCy English model
- Verify the installation

### Manual Setup

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. **Install Tesseract OCR** (see prerequisites above)

### Streamlit Cloud Deployment

The app is configured for easy deployment on Streamlit Cloud:

1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)** and click "New app"
3. **Select your forked repository** and set main file to `app.py`
4. **Deploy** - the app will automatically:
   - Install all dependencies from `requirements.txt`
   - Install Tesseract OCR from `packages.txt`
   - Download the spaCy English model on first run
   - Work with or without spaCy (graceful fallback)

📖 **Detailed deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

#### Deployment Files

- `requirements.txt` - Python dependencies
- `packages.txt` - System packages (Tesseract OCR)
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets.toml` - Streamlit secrets (can be empty)
- `setup.py` - Optional setup script

#### Automatic spaCy Model Installation

The app automatically attempts to install the spaCy English model when it starts up. If this fails, the app will continue to work with limited text preprocessing capabilities.

## Usage

### Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Using the Application

1. **Choose Input Type**:

   - Select "📝 Text Input" for direct text entry
   - Select "📷 Image Upload" for image-based input

2. **For Text Input**:

   - Paste your medical report text in the text area
   - Click "🚀 Simplify Medical Report"

3. **For Image Upload**:

   - Upload an image file (PNG, JPG, JPEG, GIF, BMP, TIFF)
   - Click "🔍 Extract Text from Image" to perform OCR
   - Review the extracted text
   - Click "🚀 Simplify Medical Report"

4. **View Results**:
   - The simplified report will appear in the output section
   - Download the results using the "📥 Download Simplified Report" button

## File Structure

```
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies with exact versions
├── setup.py                       # Automated setup script
├── packages.txt                   # System packages for Streamlit Cloud
├── README.md                      # This documentation
├── Medical Report Simplifiation notebook.ipynb  # Training notebook
└── medical_lora_adapters/         # Trained LoRA model files
    ├── adapter_config.json
    ├── adapter_model.safetensors
    ├── special_tokens_map.json
    ├── spiece.model
    ├── tokenizer_config.json
    └── tokenizer.json
```

## Model Integration

The application uses a fine-tuned FLAN-T5 model with LoRA adapters for medical report simplification. The model is automatically loaded from the `medical_lora_adapters` directory.

### Model Architecture:

- **Base Model**: Google's FLAN-T5-base
- **Fine-tuning**: LoRA (Low-Rank Adaptation) adapters
- **Task**: Medical text simplification for patients
- **Model Files**: Located in `./medical_lora_adapters/`

### Model Loading Process:

1. **Tokenizer**: Loaded from the base FLAN-T5 model
2. **Base Model**: FLAN-T5-base with 16-bit precision
3. **LoRA Adapters**: Multiple loading strategies for compatibility:
   - Standard PEFT loading
   - Manual configuration loading
   - Direct weight loading from safetensors
4. **Fallback**: Base model if LoRA loading fails

### Model Files Required:

```
medical_lora_adapters/
├── adapter_config.json      # LoRA configuration
├── adapter_model.safetensors # LoRA weights
├── special_tokens_map.json  # Special tokens mapping
├── spiece.model            # SentencePiece model
├── tokenizer_config.json   # Tokenizer configuration
└── tokenizer.json         # Tokenizer data
```

## Technical Details

### OCR Processing

- Uses Tesseract OCR for text extraction from images
- Supports multiple image formats (PNG, JPG, JPEG, GIF, BMP, TIFF)
- Configurable OCR settings for better accuracy

### Text Preprocessing

- spaCy integration for advanced text processing
- Automatic whitespace cleanup and text normalization
- Error handling for preprocessing failures

### User Interface

- Responsive design with custom CSS styling
- Sidebar navigation for input type selection
- Real-time processing indicators
- Download functionality for results

## Troubleshooting

### Common Issues:

1. **spaCy model not found**:

   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Tesseract not found**:

   - Ensure Tesseract is installed and in your system PATH
   - On Windows, you may need to set the path manually

3. **Image upload issues**:

   - Check that the image file is in a supported format
   - Ensure the image contains readable text

4. **Dependencies issues**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Streamlit Cloud Deployment Issues:

1. **spaCy model installation fails**:

   - The app automatically attempts to install the model on startup
   - If it fails, the app will work with limited text preprocessing
   - No manual intervention required

2. **Requirements.txt errors**:

   - Ensure `en-core-web-sm` is NOT in requirements.txt (it's not a PyPI package)
   - The model is installed automatically by the app

3. **Missing files**:

   - Ensure `.streamlit/config.toml` exists
   - Verify `.streamlit/secrets.toml` exists (can be empty)
   - Check that `packages.txt` contains `tesseract-ocr`

4. **Tesseract OCR issues**:
   - The app automatically installs Tesseract via `packages.txt`
   - If OCR fails, use "Text Input" instead of "Image Upload"
   - The app will show OCR availability status in the sidebar

## Future Enhancements

- [ ] Integration with medical NLP models
- [ ] Batch processing capabilities
- [ ] Multiple language support
- [ ] Advanced OCR preprocessing
- [ ] User authentication and history
- [ ] API endpoint for programmatic access

## Contributing

This is a graduation project for NTI. For contributions or suggestions, please contact the project maintainer.

## License

This project is part of an NTI graduation project for medical report simplification.

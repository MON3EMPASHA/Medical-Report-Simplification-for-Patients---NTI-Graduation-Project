# Medical Report Simplification GUI

A Streamlit-based web application that simplifies complex medical reports into patient-friendly language. The application supports both direct text input and image upload with OCR text extraction.

## Features

- 📝 **Text Input**: Direct text input for medical reports
- 📷 **Image Upload**: Upload images containing medical text with OCR extraction
- 🔍 **OCR Processing**: Automatic text extraction from images using Tesseract
- 🧠 **Text Preprocessing**: Advanced text processing using spaCy
- 📊 **Model Integration Ready**: Placeholder for your medical simplification model
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

### Local Development

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
2. **Connect to Streamlit Cloud** and select your forked repository
3. **Deploy** - the app will automatically:
   - Install all dependencies from `requirements.txt`
   - Attempt to install the spaCy English model on startup
   - Work with or without spaCy (graceful fallback)

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
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Model Integration

The application includes a placeholder function `simplify_medical_report()` in `app.py` where you can integrate your medical report simplification model.

### Current Placeholder:

```python
def simplify_medical_report(text: str) -> str:
    """
    Placeholder function for medical report simplification
    This is where you'll integrate your model later
    """
    # Your model integration code goes here
    return simplified_text
```

### Integration Steps:

1. Import your model in the `app.py` file
2. Replace the placeholder logic in `simplify_medical_report()` function
3. Add any necessary preprocessing or postprocessing steps
4. Update the requirements.txt if additional dependencies are needed

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

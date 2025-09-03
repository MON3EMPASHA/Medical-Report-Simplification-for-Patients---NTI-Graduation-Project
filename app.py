import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import base64
import spacy
import pytesseract
from typing import Optional
import tempfile
import os
import subprocess
import sys

# Auto-install spaCy model if not available
def ensure_spacy_model():
    """Ensure spaCy English model is available"""
    try:
        spacy.load("en_core_web_sm")
        return True
    except OSError:
        try:
            # Try to install the model automatically
            subprocess.run([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

# Check and install spaCy model on startup
if not ensure_spacy_model():
    st.warning("⚠️ spaCy English model installation failed. The app will work with limited text processing.")

# Check Tesseract availability
def check_tesseract():
    """Check if Tesseract is available"""
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False

# Store Tesseract availability in session state
if 'tesseract_available' not in st.session_state:
    st.session_state.tesseract_available = check_tesseract()

# Page configuration
st.set_page_config(
    page_title="Medical Report Simplification",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background */
    .main .block-container {
        background-color: #ffffff;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Full page white background */
    .stApp {
        background-color: #ffffff;
    }
    
    .stApp > header {
        background-color: #ffffff;
    }
    
    .stApp > div {
        background-color: #ffffff;
    }
    
    /* Sidebar background - gray styling */
    .css-1d391kg {
        background-color: #f3f4f6 !important;
    }
    
    .css-1lcbmhc {
        background-color: #f3f4f6 !important;
    }
    
    /* Additional sidebar selectors */
    section[data-testid="stSidebar"] {
        background-color: #f3f4f6 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #f3f4f6 !important;
    }
    
    .css-1v0mbdj {
        background-color: #f3f4f6 !important;
    }
    
    .css-1v0mbdj > div {
        background-color: #f3f4f6 !important;
    }
    
    /* Sidebar content styling */
    .css-1v0mbdj .css-1v0mbdj {
        background-color: #f3f4f6 !important;
    }
    
    /* Sidebar text styling */
    .css-1v0mbdj h1,
    .css-1v0mbdj h2,
    .css-1v0mbdj h3,
    .css-1v0mbdj p,
    .css-1v0mbdj div {
        color: #000000 !important;
    }
    
    /* Radio button styling */
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] {
        color: #000000 !important;
        font-weight: 500;
    }
    
    .stRadio > div > label > div[data-testid="stMarkdownContainer"]:hover {
        color: #374151 !important;
    }
    
    /* Sidebar section headers */
    .css-1v0mbdj h2 {
        color: #000000 !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Sidebar tips styling */
    .css-1v0mbdj h3 {
        color: #000000 !important;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar list styling */
    .css-1v0mbdj ul {
        color: #374151 !important;
        line-height: 1.6;
    }
    
    .css-1v0mbdj li {
        margin-bottom: 0.5rem;
        color: #374151 !important;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #ffffff;
    }
    
    /* Report view */
    .reportview-container {
        background-color: #ffffff;
    }
    
    .reportview-container .main .block-container {
        background-color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Section styling */
    .input-section {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    
    .output-section {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f3f4f6;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        font-size: 1rem;
        line-height: 1.5;
        background-color: #ffffff;
        color: #000000 !important;
        transition: all 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
        outline: none;
        color: #000000 !important;
    }
    
    .stTextArea > div > div > textarea:hover {
        border-color: #9ca3af;
        color: #000000 !important;
    }
    
    /* Force dark text in all text areas */
    .stTextArea textarea {
        color: #000000 !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #6b7280 !important;
    }
    
    /* Override any text selection highlighting */
    .stTextArea textarea::selection {
        background-color: #d1d5db !important;
        color: #000000 !important;
    }
    
    /* Ensure text in disabled text areas is also dark */
    .stTextArea textarea:disabled {
        color: #000000 !important;
        background-color: #f9fafb !important;
    }
    
    /* Specific styling for extracted text area */
    .stTextArea[data-testid="stTextArea"] textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Override any highlighting or selection in text areas */
    .stTextArea textarea::-moz-selection {
        background-color: #d1d5db !important;
        color: #000000 !important;
    }
    
    .stTextArea textarea::-webkit-selection {
        background-color: #d1d5db !important;
        color: #000000 !important;
    }
    
    /* Force dark text in all text area content */
    .stTextArea * {
        color: #000000 !important;
    }
    
    /* Override any Streamlit default text styling */
    .stTextArea .stMarkdown {
        color: #000000 !important;
    }
    
    .stTextArea .stMarkdown * {
        color: #000000 !important;
    }
    
    /* Remove any background highlighting */
    .stTextArea textarea {
        background-color: #ffffff !important;
        background-image: none !important;
    }
    
    /* Additional overrides for extracted text specifically */
    div[data-testid="stTextArea"] textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
        background-image: none !important;
    }
    
    /* Override any markdown rendering in text areas */
    .stTextArea .markdown-text {
        color: #000000 !important;
    }
    
    /* Force all text content to be black */
    .stTextArea .stText {
        color: #000000 !important;
    }
    
    /* Remove any text highlighting effects */
    .stTextArea textarea:not(:focus) {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Override any Streamlit default text colors */
    .stTextArea .stTextInput > div > div > input,
    .stTextArea .stTextInput > div > div > textarea {
        color: #000000 !important;
    }
    
    /* Specific styling for extracted text display */
    .stTextArea textarea[disabled] {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
    
    /* Force black text in disabled text areas */
    .stTextArea textarea:disabled {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
    
    /* Override any white text in text areas */
    .stTextArea textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* Target the specific extracted text area */
    div[data-testid="stTextArea"] textarea[disabled] {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
    
    /* Override any CSS that might be making text white */
    .stTextArea textarea,
    .stTextArea textarea:disabled,
    .stTextArea textarea:read-only {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
    
    /* Additional overrides for Streamlit text areas */
    .stTextArea .stTextInput textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    
    /* Force text color in all possible text area states */
    .stTextArea textarea[readonly],
    .stTextArea textarea[disabled="true"],
    .stTextArea textarea[aria-readonly="true"] {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
    
    /* Override any Streamlit default disabled text styling */
    .stTextArea .stTextInput > div > div > textarea[disabled] {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
    
    /* Universal text color override for text areas */
    .stTextArea * {
        color: #000000 !important;
    }
    
    /* Specific override for extracted text content */
    .stTextArea .stMarkdown,
    .stTextArea .stMarkdown *,
    .stTextArea .stText,
    .stTextArea .stText * {
        color: #000000 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border-radius: 8px;
        border: 2px dashed #d1d5db;
        background-color: #ffffff !important;
        transition: all 0.2s ease;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .stFileUploader > div:hover {
        border-color: #9ca3af;
        background-color: #ffffff !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Force white background for all file uploader containers */
    .stFileUploader > div > div {
        background-color: #ffffff !important;
    }
    
    .stFileUploader > div > div > div {
        background-color: #ffffff !important;
    }
    
    /* File uploader text styling */
    .stFileUploader label {
        color: #374151 !important;
    }
    
    .stFileUploader p {
        color: #6b7280 !important;
    }
    
    .stFileUploader div {
        color: #6b7280 !important;
    }
    
    /* File uploader button styling */
    .stFileUploader button {
        background-color: #f3f4f6 !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
    }
    
    .stFileUploader button:hover {
        background-color: #e5e7eb !important;
        color: #1f2937 !important;
    }
    
    /* Additional file uploader styling */
    .stFileUploader .uploadedFile {
        background-color: #f9fafb !important;
        border: 1px solid #d1d5db !important;
        color: #374151 !important;
    }
    
    .stFileUploader .uploadedFile:hover {
        background-color: #f3f4f6 !important;
    }
    
    /* File uploader icon styling */
    .stFileUploader svg {
        color: #6b7280 !important;
    }
    
    /* File uploader drag and drop text */
    .stFileUploader .uploadedFileData {
        color: #374151 !important;
    }
    
    /* File uploader status messages */
    .stFileUploader .uploadedFileStatus {
        color: #6b7280 !important;
    }
    
    /* Comprehensive file uploader white background */
    .stFileUploader * {
        background-color: #ffffff !important;
    }
    
    /* Override any dark backgrounds in file uploader */
    .stFileUploader .uploadedFile {
        background-color: #ffffff !important;
    }
    
    .stFileUploader .uploadedFileData {
        background-color: #ffffff !important;
    }
    
    /* File uploader drag area */
    .stFileUploader .uploadedFileData > div {
        background-color: #ffffff !important;
    }
    
    /* File uploader content area */
    .stFileUploader .uploadedFileData > div > div {
        background-color: #ffffff !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Footer styling */
    .footer {
        background-color: #ffffff;
        color: #6b7280 !important;
        padding: 1rem 2rem;
        margin-top: 3rem;
        text-align: center;
        border-top: 1px solid #e5e7eb;
        font-size: 0.9rem;
    }
    
    .team-names {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }
    
    .team-member {
        color: #6b7280 !important;
        font-weight: 500;
    }
    
    /* Instructions styling */
    .instructions {
        background-color: #f8fafc;
        padding: 2rem;
        border-radius: 8px;
        border-left: 4px solid #2563eb;
        margin-top: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Additional white background coverage */
    body {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Global text color override */
    * {
        color: #000000 !important;
    }
    
    /* Specific text elements */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    p, div, span, label {
        color: #000000 !important;
    }
    
    /* Streamlit specific text elements */
    .stMarkdown {
        color: #000000 !important;
    }
    
    .stMarkdown p {
        color: #000000 !important;
    }
    
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown h5,
    .stMarkdown h6 {
        color: #000000 !important;
    }
    
    /* Main content text */
    .main .block-container * {
        color: #000000 !important;
    }
    
    /* Sidebar text */
    .css-1d391kg * {
        color: #000000 !important;
    }
    
    /* Additional sidebar elements */
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    /* Sidebar radio buttons */
    .stRadio > div {
        background-color: #f3f4f6 !important;
    }
    
    /* Sidebar markdown elements */
    .css-1v0mbdj .stMarkdown {
        color: #000000 !important;
    }
    
    .css-1v0mbdj .stMarkdown * {
        color: #000000 !important;
    }
    
    /* Instructions text */
    .instructions * {
        color: #000000 !important;
    }
    
    /* Footer text */
    .footer * {
        color: #000000 !important;
    }
    
    .stApp > div > div > div > div {
        background-color: #ffffff;
    }
    
    .stApp > div > div > div > div > div {
        background-color: #ffffff;
    }
    
    /* Ensure all containers are white */
    div[data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }
    
    div[data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    
    div[data-testid="stSidebar"] > div {
        background-color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_spacy_model():
    """Load spaCy model for text processing"""
    try:
        # Try to load the English model
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        st.warning("""
        **spaCy English model not available.** 
        
        The app will continue to work without spaCy, but text preprocessing will be limited.
        
        For manual installation:
        ```
        python -m spacy download en_core_web_sm
        ```
        """)
        return None

def extract_text_from_image(image: Image.Image) -> str:
    """Extract text from image using OCR (Tesseract)"""
    try:
        # Convert PIL image to format suitable for Tesseract
        text = pytesseract.image_to_string(image, config='--psm 6')
        return text.strip()
    except Exception as e:
        error_msg = str(e)
        if "tesseract is not installed" in error_msg.lower() or "tesseract" in error_msg.lower():
            st.error("""
            **Tesseract OCR is not available on this platform.**
            
            For Streamlit Cloud deployment, Tesseract should be automatically installed.
            If you're seeing this error, please:
            
            1. **Restart the app** - Tesseract installation may take a moment
            2. **Check if packages.txt contains `tesseract-ocr`**
            3. **Try uploading a different image format**
            
            **Alternative**: Use the "Text Input" option instead of image upload.
            """)
        else:
            st.error(f"Error extracting text from image: {error_msg}")
        return ""

def preprocess_text(text: str, nlp) -> str:
    """Preprocess extracted text using spaCy"""
    if not nlp or not text:
        return text
    
    try:
        doc = nlp(text)
        # Basic preprocessing - remove extra whitespace and clean up
        processed_text = " ".join([token.text for token in doc if not token.is_space])
        return processed_text
    except Exception as e:
        st.warning(f"Text preprocessing failed: {str(e)}")
        return text

def simplify_medical_report(text: str) -> str:
    """
    Placeholder function for medical report simplification
    This is where you'll integrate your model later
    """
    # For now, return a placeholder response
    return f"""
**Simplified Medical Report:**

Original text length: {len(text)} characters

**Simplified Version:**
This is a placeholder for the simplified medical report. Your model will be integrated here to process the following text:

{text[:500]}{'...' if len(text) > 500 else ''}

**Note:** This is a demo version. The actual simplification model will be integrated later.
"""

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Medical Report Simplification</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform complex medical reports into patient-friendly language</p>', unsafe_allow_html=True)
    
    # Load spaCy model
    nlp = load_spacy_model()
    
    # Sidebar for input selection
    st.sidebar.markdown("## ⚙️ Input Options")
    st.sidebar.markdown("---")
    
    # Show Tesseract status
    if st.session_state.tesseract_available:
        st.sidebar.success("✅ OCR (Tesseract) is available")
    else:
        st.sidebar.warning("⚠️ OCR (Tesseract) not available")
    
    input_type = st.sidebar.radio(
        "Choose input type:",
        ["📝 Text Input", "📷 Image Upload"],
        help="Select whether you want to input text directly or upload an image containing medical text"
    )
    
    # Show warning if Tesseract is not available and user selects image upload
    if input_type == "📷 Image Upload" and not st.session_state.tesseract_available:
        st.sidebar.error("""
        **Image Upload Not Available**
        
        Tesseract OCR is not installed on this platform.
        Please use "Text Input" instead.
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Tips:")
    if st.session_state.tesseract_available:
        st.sidebar.markdown("""
        - **Text Input**: Best for digital reports
        - **Image Upload**: For scanned documents or photos
        - Ensure good image quality for better OCR results
        """)
    else:
        st.sidebar.markdown("""
        - **Text Input**: Recommended (OCR not available)
        - **Image Upload**: Not available on this platform
        - Copy and paste text from images manually
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #000000 !important;">📥 Input</h3>', unsafe_allow_html=True)
        
        input_text = ""
        
        if input_type == "📝 Text Input":
            st.markdown('<p style="color: #000000 !important;"><strong>Enter your medical report text:</strong></p>', unsafe_allow_html=True)
            input_text = st.text_area(
                "Medical Report Text",
                height=300,
                placeholder="Paste your medical report text here...",
                help="Enter the medical report text that you want to simplify"
            )
            
        else:  # Image Upload
            if st.session_state.tesseract_available:
                st.markdown('<p style="color: #000000 !important;"><strong>Upload an image containing medical text:</strong></p>', unsafe_allow_html=True)
                uploaded_file = st.file_uploader(
                    "Choose an image file",
                    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'],
                    help="Upload an image file containing medical text. The app will extract text using OCR."
                )
            else:
                st.markdown('<p style="color: #000000 !important;"><strong>Image Upload Not Available</strong></p>', unsafe_allow_html=True)
                st.info("""
                **OCR (Tesseract) is not available on this platform.**
                
                Please use the "Text Input" option instead, or copy and paste text from your images manually.
                """)
                uploaded_file = None
            
            if uploaded_file is not None:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
                
                # Extract text using OCR
                if st.button("🔍 Extract Text from Image"):
                    with st.spinner("Extracting text from image..."):
                        extracted_text = extract_text_from_image(image)
                        if extracted_text:
                            st.success("Text extracted successfully!")
                            input_text = extracted_text
                            
                            # Show extracted text
                            st.markdown('<h4 style="color: #000000 !important;">📄 Extracted Text:</h4>', unsafe_allow_html=True)
                            st.text_area("Extracted Text", extracted_text, height=200, disabled=False)
                        else:
                            st.error("No text could be extracted from the image.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="output-section">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #000000 !important;">📤 Output</h3>', unsafe_allow_html=True)
        
        # Process button
        if st.button("🚀 Simplify Medical Report", disabled=not input_text.strip()):
            if input_text.strip():
                with st.spinner("Processing medical report..."):
                    # Preprocess text if spaCy is available
                    processed_text = preprocess_text(input_text, nlp)
                    
                    # Generate simplified report
                    simplified_report = simplify_medical_report(processed_text)
                    
                    # Display results
                    st.markdown("### ✅ Simplified Report")
                    st.markdown(simplified_report)
                    
                    # Download option
                    st.download_button(
                        label="📥 Download Simplified Report",
                        data=simplified_report,
                        file_name="simplified_medical_report.txt",
                        mime="text/plain"
                    )
            else:
                st.warning("Please provide some text to process.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Instructions section
    st.markdown('<div class="instructions">', unsafe_allow_html=True)
    st.markdown("""
    ### 📋 Instructions:
    1. **Text Input**: Paste your medical report text directly into the text area
    2. **Image Upload**: Upload an image containing medical text, then click "Extract Text from Image"
    3. Click "Simplify Medical Report" to process the text
    4. Download the simplified report using the download button
    
    ### 🔧 Technical Notes:
    - OCR functionality uses Tesseract for text extraction
    - Text preprocessing uses spaCy for better text handling
    - The simplification model will be integrated in the future
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with team names
    st.markdown("""
    <div class="footer">
        <p>© 2024 Medical Report Simplification Project - NTI Graduation Project</p>
        <div class="team-names">
            <span class="team-member">Abdelmonem Hatem</span>
            <span class="team-member">Omar Hisham</span>
            <span class="team-member">Ali Omar</span>
            <span class="team-member">Mohamed Gamal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

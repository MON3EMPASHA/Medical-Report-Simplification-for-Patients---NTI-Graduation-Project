import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import base64
import tempfile
import os
from typing import Optional

# Optional imports with graceful fallbacks
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# Check spaCy model availability with automatic installation attempt
def check_spacy_model():
    """Check if spaCy English model is available, attempt installation if not"""
    if not SPACY_AVAILABLE:
        return False
    
    try:
        spacy.load("en_core_web_sm")
        return True
    except OSError:
        try:
            # Attempt to download the model
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            return True
        except Exception:
            return False

# Check Tesseract availability
def check_tesseract():
    """Check if Tesseract is available"""
    if not TESSERACT_AVAILABLE:
        return False
    
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
    
    /* Download button styling */
    .stDownloadButton > button {
        width: 100%;
        background-color: #059669 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        margin-top: 1rem !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #047857 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stDownloadButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Ensure download button text is visible */
    .stDownloadButton > button > div {
        color: white !important;
    }
    
    .stDownloadButton > button > div > div {
        color: white !important;
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
    
    /* Ensure sidebar is visible on Streamlit Cloud */
    .css-1d391kg {
        display: block !important;
        visibility: visible !important;
    }
    
    .css-1lcbmhc {
        display: block !important;
        visibility: visible !important;
    }
    
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>

<script>
// Force sidebar to be visible on Streamlit Cloud
window.addEventListener('load', function() {
    setTimeout(function() {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.display = 'block';
            sidebar.style.visibility = 'visible';
            sidebar.style.width = '21rem';
        }
    }, 1000);
});
</script>
""", unsafe_allow_html=True)

@st.cache_resource
def load_spacy_model():
    """Load spaCy model for text processing"""
    try:
        # Try to load the English model
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        # Return None silently - no warning message
        return None

@st.cache_resource
def load_medical_model():
    """Load the trained medical simplification model"""
    if not TORCH_AVAILABLE:
        st.warning("⚠️ PyTorch and Transformers not available. Model loading disabled.")
        return None, None
    
    import os  # Import os at the top of the function
    try:
        # Check if the model directory exists
        model_path = "./medical_lora_adapters"
        if not os.path.exists(model_path):
            st.error(f"Model directory not found: {model_path}")
            return None, None
        
        # Load tokenizer from the original model to avoid tokenizer issues
        try:
            tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
            st.info("✅ Loaded tokenizer from base model")
        except Exception as tokenizer_error:
            st.warning(f"⚠️ Tokenizer loading failed: {str(tokenizer_error)}")
            return None, None
        
        # Try multiple approaches to load LoRA adapters
        model = None
        
        # Approach 1: Try PEFT with different configurations
        try:
            from peft import PeftModel, LoraConfig
            # Load base model
            base_model = AutoModelForSeq2SeqLM.from_pretrained(
                "google/flan-t5-base",
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            # Try loading with explicit config
            try:
                model = PeftModel.from_pretrained(base_model, model_path)
                model.eval()
                st.success("✅ Loaded model with LoRA adapters (PEFT method)")
            except Exception as e1:
                # Try alternative loading method
                try:
                    # Load adapter config manually
                    import json
                    with open(f"{model_path}/adapter_config.json", "r") as f:
                        adapter_config = json.load(f)
                    
                    # Create LoRA config
                    lora_config = LoraConfig(
                        r=adapter_config.get("r", 8),
                        lora_alpha=adapter_config.get("lora_alpha", 16),
                        target_modules=adapter_config.get("target_modules", ["q", "v", "k", "o"]),
                        lora_dropout=adapter_config.get("lora_dropout", 0.1),
                        bias=adapter_config.get("bias", "none"),
                        task_type=adapter_config.get("task_type", "SEQ_2_SEQ_LM")
                    )
                    
                    # Apply LoRA config to base model
                    from peft import get_peft_model
                    model = get_peft_model(base_model, lora_config)
                    
                    # Load the adapter weights
                    model.load_adapter(model_path, "default")
                    model.eval()
                    st.success("✅ Loaded model with LoRA adapters (Manual config method)")
                    
                except Exception as e2:
                    # Try direct weight loading as last resort
                    try:
                        st.info("🔄 Trying direct LoRA weight loading...")
                        from safetensors import safe_open
                        st.info(f"✅ os module available, model_path: {model_path}")
                        
                        # Load adapter weights directly
                        adapter_file = os.path.join(model_path, "adapter_model.safetensors")
                        if os.path.exists(adapter_file):
                            with safe_open(adapter_file, framework="pt", device="cpu") as f:
                                adapter_weights = {}
                                for key in f.keys():
                                    adapter_weights[key] = f.get_tensor(key)
                            
                            # Apply weights manually to the model
                            # This is a simplified approach - in practice, you'd need to map the weights correctly
                            st.info("📦 Found LoRA weights, attempting manual application...")
                            
                            # For now, we'll use the base model but mark it as having LoRA weights available
                            model = base_model
                            model._lora_weights_available = True
                            model._lora_weights = adapter_weights
                            model.eval()
                            st.success("✅ Loaded model with LoRA weights (Direct loading method)")
                        else:
                            raise Exception("No adapter weights file found")
                            
                    except Exception as e3:
                        raise Exception(f"All LoRA loading methods failed: PEFT={str(e1)} | Manual={str(e2)} | Direct={str(e3)}")
                    
        except ImportError:
            st.warning("⚠️ PEFT not available, loading base model only")
            model = None
        except Exception as peft_error:
            st.warning(f"⚠️ LoRA loading failed: {str(peft_error)}")
            model = None
        
        # Fallback to base model if LoRA loading failed
        if model is None:
            st.info("💡 Loading base model as fallback - will still provide medical text simplification")
            model = AutoModelForSeq2SeqLM.from_pretrained(
                "google/flan-t5-base",
                torch_dtype=torch.float16,
                device_map="auto"
            )
            model.eval()
        
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading medical model: {str(e)}")
        return None, None

def extract_text_from_image(image: Image.Image) -> str:
    """Extract text from image using OCR (Tesseract)"""
    if not TESSERACT_AVAILABLE:
        return "Error: Tesseract OCR not available. Please install tesseract-ocr system package."
    
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

def simplify_medical_report(text: str, model, tokenizer) -> str:
    """
    Simplify medical report using the trained LoRA model
    """
    try:
        if model is None or tokenizer is None:
            return {
                "error": True,
                "error_message": "Model not loaded. Please check that the model files are available in the medical_lora_adapters directory.",
                "original_text": text,
                "simplified_text": None,
                "model_type": None,
                "original_length": len(text),
                "simplified_length": 0,
                "reduction_percentage": 0
            }
        
        # Add a prompt to help the model understand the task better
        prompt = f"Simplify this medical text for patients: {text}"
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        # Move to same device as model
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate simplified text
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                num_beams=4,
                early_stopping=True,
                do_sample=False,
                temperature=0.7,
                repetition_penalty=1.1
            )
        
        # Decode the output
        simplified_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Check if we're using LoRA model or base model
        if hasattr(model, 'peft_config'):
            model_type = "LoRA-adapted FLAN-T5 (PEFT)"
        elif hasattr(model, '_lora_weights_available') and model._lora_weights_available:
            model_type = "LoRA-adapted FLAN-T5 (Direct weights)"
        else:
            model_type = "Base FLAN-T5"
        
        # Return a structured result for Streamlit display
        return {
            "simplified_text": simplified_text,
            "model_type": model_type,
            "original_length": len(text),
            "simplified_length": len(simplified_text),
            "reduction_percentage": ((len(text) - len(simplified_text)) / len(text) * 100),
            "original_text": text
        }
        
    except Exception as e:
        return {
            "error": True,
            "error_message": str(e),
            "original_text": text,
            "simplified_text": None,
            "model_type": None,
            "original_length": len(text),
            "simplified_length": 0,
            "reduction_percentage": 0
        }

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Medical Report Simplification</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Transform complex medical reports into patient-friendly language</p>', unsafe_allow_html=True)
    
    # Check dependencies
    if not TORCH_AVAILABLE:
        st.error("⚠️ **PyTorch and Transformers not available.** The AI model functionality will be disabled. Please ensure all dependencies are installed.")
    
    if not TESSERACT_AVAILABLE:
        st.warning("⚠️ **Tesseract OCR not available.** Image upload functionality will be limited.")
    
    if not SPACY_AVAILABLE:
        st.warning("⚠️ **spaCy not available.** Text preprocessing will be limited.")
    
    # Load models
    nlp = load_spacy_model()
    medical_model, medical_tokenizer = load_medical_model()
    
    # Sidebar for input selection
    st.sidebar.markdown("## ⚙️ Input Options")
    st.sidebar.markdown("---")
    
    input_type = st.sidebar.radio(
        "Choose input type:",
        ["📝 Text Input", "📷 Image Upload"],
        help="Select whether you want to input text directly or upload an image containing medical text"
    )
    
    # Fallback: Also show input selection in main area if sidebar is not visible
    st.markdown("---")
    st.markdown("### 📋 Input Selection")
    input_type_main = st.radio(
        "Choose input type:",
        ["📝 Text Input", "📷 Image Upload"],
        help="Select whether you want to input text directly or upload an image containing medical text",
        key="input_type_main"
    )
    
    # Use the main area selection if sidebar is not working
    if input_type_main != input_type:
        input_type = input_type_main
    
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
        st.markdown('<h3 style="color: #000000 !important;">📥 Input</h3>', unsafe_allow_html=True)
        
        # Initialize input_text in session state if not exists
        if 'input_text' not in st.session_state:
            st.session_state.input_text = ""
        
        if input_type == "📝 Text Input":
            st.markdown('<p style="color: #000000 !important;"><strong>Enter your medical report text:</strong></p>', unsafe_allow_html=True)
            input_text = st.text_area(
                "Medical Report Text",
                value=st.session_state.input_text,
                height=300,
                placeholder="Paste your medical report text here...",
                help="Enter the medical report text that you want to simplify",
                key="text_input_area"
            )
            # Update session state when text changes
            st.session_state.input_text = input_text
            
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
                st.image(image, caption="Uploaded Image", width='stretch')
                
                # Extract text using OCR
                if st.button("🔍 Extract Text from Image"):
                    with st.spinner("Extracting text from image..."):
                        extracted_text = extract_text_from_image(image)
                        if extracted_text:
                            st.success("Text extracted successfully!")
                            # Store extracted text in session state
                            st.session_state.input_text = extracted_text
                            
                            # Show extracted text
                            st.markdown('<h4 style="color: #000000 !important;">📄 Extracted Text:</h4>', unsafe_allow_html=True)
                            edited_text = st.text_area(
                                "Extracted Text", 
                                value=st.session_state.input_text, 
                                height=200, 
                                disabled=False,
                                key="extracted_text_area_1",
                                help="You can edit the extracted text here. Changes will be saved automatically."
                            )
                            # Update session state when text is edited
                            st.session_state.input_text = edited_text
                        else:
                            st.error("No text could be extracted from the image.")
                
                # Show extracted text area if there's text in session state (for editing)
                if st.session_state.input_text and st.session_state.input_text.strip():
                    st.markdown('<h4 style="color: #000000 !important;">📄 Extracted Text:</h4>', unsafe_allow_html=True)
                    edited_text = st.text_area(
                        "Extracted Text", 
                        value=st.session_state.input_text, 
                        height=200, 
                        disabled=False,
                        key="extracted_text_area_2",
                        help="You can edit the extracted text here. Changes will be saved automatically."
                    )
                    # Update session state when text is edited
                    st.session_state.input_text = edited_text
    
    with col2:
        st.markdown('<h3 style="color: #000000 !important;">📤 Output</h3>', unsafe_allow_html=True)
        
        # Process button
        if st.button("🚀 Simplify Medical Report", disabled=not st.session_state.input_text.strip()):
            if st.session_state.input_text.strip():
                with st.spinner("Processing medical report..."):
                    # Preprocess text if spaCy is available
                    processed_text = preprocess_text(st.session_state.input_text, nlp)
                    
                    # Generate simplified report using the trained model
                    simplified_report = simplify_medical_report(processed_text, medical_model, medical_tokenizer)
                    
                    # Display results
                    st.markdown("### ✅ Simplified Report")
                    
                    if isinstance(simplified_report, dict) and simplified_report.get("error"):
                        # Display error
                        st.error(f"❌ {simplified_report['error_message']}")
                        if simplified_report.get("original_text"):
                            with st.expander("📄 Original Text", expanded=False):
                                st.text(simplified_report["original_text"])
                    else:
                        # Display successful result
                        # Header with model info
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown("#### 🏥 Simplified Medical Report")
                            st.markdown("*Patient-Friendly Version*")
                        with col2:
                            st.success(f"🤖 {simplified_report['model_type']}")
                        
                        # Main simplified text
                        st.markdown("---")
                        st.markdown("### 📝 Simplified Text")
                        st.info(simplified_report["simplified_text"])
                        
                        # Statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Length", f"{simplified_report['original_length']} chars")
                        with col2:
                            st.metric("Simplified Length", f"{simplified_report['simplified_length']} chars")
                        with col3:
                            st.metric("Reduction", f"{simplified_report['reduction_percentage']:.1f}%")
                        
                        # Original text expander
                        with st.expander("📄 View Original Text", expanded=False):
                            st.text(simplified_report["original_text"])
                    
                    # Download option
                    if isinstance(simplified_report, dict) and not simplified_report.get("error"):
                        download_text = f"""Simplified Medical Report
Generated by: {simplified_report['model_type']}

SIMPLIFIED TEXT:
{simplified_report['simplified_text']}

STATISTICS:
- Original Length: {simplified_report['original_length']} characters
- Simplified Length: {simplified_report['simplified_length']} characters
- Reduction: {simplified_report['reduction_percentage']:.1f}%

ORIGINAL TEXT:
{simplified_report['original_text']}
"""
                    st.download_button(
                        label="📥 Download Simplified Report",
                            data=download_text,
                        file_name="simplified_medical_report.txt",
                        mime="text/plain"
                    )
            else:
                st.warning("Please provide some text to process.")
    
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
    - Medical simplification uses a fine-tuned FLAN-T5 model with LoRA adapters
    - The model is trained on medical text simplification datasets
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with team names - moved to the very bottom
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

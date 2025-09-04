#!/usr/bin/env python3
"""
Verification script for Medical Report Simplification Application
This script checks if all dependencies are properly installed and working.
"""

import sys
import importlib
import os

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_dependency(module_name, package_name=None):
    """Check if a dependency is installed"""
    if package_name is None:
        package_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def check_spacy_model():
    """Check if spaCy English model is available"""
    print("🧠 Checking spaCy English model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy English model is available")
        return True
    except OSError:
        print("❌ spaCy English model not found. Run: python -m spacy download en_core_web_sm")
        return False

def check_model_files():
    """Check if model files are present"""
    print("🤖 Checking model files...")
    model_dir = "./medical_lora_adapters"
    required_files = [
        "adapter_config.json",
        "adapter_model.safetensors",
        "special_tokens_map.json",
        "spiece.model",
        "tokenizer_config.json",
        "tokenizer.json"
    ]
    
    if not os.path.exists(model_dir):
        print(f"❌ Model directory not found: {model_dir}")
        return False
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(model_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing model files: {', '.join(missing_files)}")
        return False
    
    print("✅ All model files are present")
    return True

def check_tesseract():
    """Check if Tesseract is available"""
    print("🔍 Checking Tesseract OCR...")
    try:
        import pytesseract
        # Try to get tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR is available (version: {version})")
        return True
    except Exception as e:
        print(f"❌ Tesseract OCR not available: {e}")
        print("   Install Tesseract OCR for your operating system")
        return False

def main():
    """Main verification function"""
    print("🏥 Medical Report Simplification - Installation Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Streamlit", lambda: check_dependency("streamlit")),
        ("PyTorch", lambda: check_dependency("torch")),
        ("Transformers", lambda: check_dependency("transformers")),
        ("PEFT", lambda: check_dependency("peft")),
        ("Accelerate", lambda: check_dependency("accelerate")),
        ("Safetensors", lambda: check_dependency("safetensors")),
        ("spaCy", lambda: check_dependency("spacy")),
        ("Pillow", lambda: check_dependency("PIL", "Pillow")),
        ("Pandas", lambda: check_dependency("pandas")),
        ("NumPy", lambda: check_dependency("numpy")),
        ("spaCy Model", check_spacy_model),
        ("Model Files", check_model_files),
        ("Tesseract OCR", check_tesseract),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n{name}:")
        if check_func():
            passed += 1
        else:
            print(f"   Fix: See installation instructions in README.md")
    
    print("\n" + "=" * 60)
    print(f"📊 Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your installation is ready.")
        print("\nTo run the application:")
        print("  streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nFor help, see the installation section in README.md")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

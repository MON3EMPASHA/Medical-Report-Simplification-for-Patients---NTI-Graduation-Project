#!/usr/bin/env python3
"""
Setup script for Medical Report Simplification Application
This script installs all required dependencies and downloads the spaCy model.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🏥 Medical Report Simplification - Setup Script")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("❌ Failed to download spaCy model")
        sys.exit(1)
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    try:
        import streamlit
        import torch
        import transformers
        import peft
        import spacy
        print("✅ All core dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  streamlit run app.py")
    print("\nMake sure you have:")
    print("  - Tesseract OCR installed on your system")
    print("  - The medical_lora_adapters folder with your trained model")

if __name__ == "__main__":
    main()
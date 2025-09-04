#!/usr/bin/env python3
"""
Test script to verify the app can run with minimal dependencies
"""

import sys
import subprocess

def test_imports():
    """Test if the app can import without errors"""
    print("Testing imports...")
    
    try:
        # Test basic imports
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    # Test optional imports
    try:
        import spacy
        print("✅ spaCy imported successfully")
    except ImportError as e:
        print(f"⚠️ spaCy import failed (optional): {e}")
    
    try:
        import pytesseract
        print("✅ pytesseract imported successfully")
    except ImportError as e:
        print(f"⚠️ pytesseract import failed (optional): {e}")
    
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        print("✅ PyTorch and Transformers imported successfully")
    except ImportError as e:
        print(f"⚠️ PyTorch/Transformers import failed (optional): {e}")
    
    return True

def test_app_import():
    """Test if the app can be imported"""
    print("\nTesting app import...")
    
    try:
        # Import the app module
        import app
        print("✅ App module imported successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Medical Report Simplification App for Deployment")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n❌ Basic imports failed. Check your environment.")
        return 1
    
    # Test app import
    if not test_app_import():
        print("\n❌ App import failed. Check the app code.")
        return 1
    
    print("\n✅ All tests passed! The app should work on Streamlit Cloud.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

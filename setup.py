"""
Setup script for Medical Report Simplification App
This script handles the installation of spaCy English model
"""

import subprocess
import sys
import os

def install_spacy_model():
    """Install spaCy English model"""
    try:
        print("Installing spaCy English model...")
        result = subprocess.run([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ], capture_output=True, text=True, check=True)
        print("✅ spaCy English model installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing spaCy model: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    install_spacy_model()

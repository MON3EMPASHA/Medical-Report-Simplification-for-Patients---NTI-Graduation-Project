# Streamlit Cloud Deployment Guide

## Quick Deployment Steps

1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Click "New app"**
4. **Select your forked repository**
5. **Set the main file path to `app.py`**
6. **Click "Deploy"**

## What Happens During Deployment

### Automatic Installation

- ✅ **Python Dependencies**: Installed from `requirements.txt`
- ✅ **System Packages**: Tesseract OCR installed from `packages.txt`
- ✅ **spaCy Model**: Automatically downloaded on first run
- ✅ **Configuration**: Applied from `.streamlit/config.toml`

### Model Files

- The app will look for your trained model in `./medical_lora_adapters/`
- If model files are missing, it will fall back to the base FLAN-T5 model
- Make sure to commit your model files to the repository

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**

   - The app automatically attempts to download `en_core_web_sm`
   - If it fails, the app continues with limited text preprocessing

2. **Model Loading Errors**

   - Check that `medical_lora_adapters/` folder exists in your repository
   - Ensure all model files are committed to Git

3. **Dependency Conflicts**
   - The requirements.txt uses flexible version ranges for compatibility
   - Streamlit Cloud will resolve the best compatible versions

### File Structure for Deployment

```
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
├── packages.txt                   # System packages (Tesseract)
├── .streamlit/
│   ├── config.toml               # Streamlit configuration
│   └── secrets.toml              # Secrets (can be empty)
├── medical_lora_adapters/         # Your trained model
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── ... (other model files)
└── README.md                      # Documentation
```

## Performance Notes

- **Cold Start**: First load may take 30-60 seconds due to model loading
- **Memory Usage**: The app uses ~2-4GB RAM with the full model
- **Timeout**: Streamlit Cloud has a 30-minute timeout for long-running processes

## Custom Domain (Optional)

After deployment, you can:

1. Go to your app settings in Streamlit Cloud
2. Add a custom domain
3. Update your DNS settings

## Support

If you encounter issues:

1. Check the deployment logs in Streamlit Cloud
2. Verify all files are committed to your repository
3. Ensure model files are not too large (>100MB may cause issues)

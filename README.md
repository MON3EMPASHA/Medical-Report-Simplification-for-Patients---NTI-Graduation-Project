# Medical Report Simplification for Patients

**NTI Internship Graduation Project**

A Streamlit-based web application that simplifies complex medical reports into clear, patient-friendly language using a fine-tuned **FLAN-T5** model with **LoRA adapters**. The app supports both text input and image upload with OCR extraction.

## 🎥 Demo Video

👉 **Watch the demo:**
[https://drive.google.com/file/d/16cIK5Mxh07ohZSjOCjoILQ7PgbPvUed8/view?usp=sharing](https://drive.google.com/file/d/16cIK5Mxh07ohZSjOCjoILQ7PgbPvUed8/view?usp=sharing)

---

## ✨ Features

* 📝 Simplify medical reports from direct text input
* 📷 Upload medical report images with OCR text extraction
* 🤖 AI-powered medical text simplification using FLAN-T5 + LoRA
* 🧠 NLP preprocessing with spaCy
* 💾 Download simplified reports as text files
* 🎨 Clean, modern, and responsive Streamlit UI

---

## 🛠 Tech Stack

* **Programming Language:** Python
* **Frontend:** Streamlit
* **NLP & AI:** FLAN-T5, LoRA, spaCy
* **OCR:** Tesseract OCR

---

## 🚀 Installation & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install spaCy model

```bash
python -m spacy download en_core_web_sm
```

### 3. Install Tesseract OCR

* **Windows:** [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
* **macOS:** `brew install tesseract`
* **Linux:** `sudo apt-get install tesseract-ocr`

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
├── app.py                  # Streamlit application
├── requirements.txt        # Dependencies
├── README.md               # Documentation
├── Medical Report Simplification.ipynb  # Training notebook
└── medical_lora_adapters/  # Fine-tuned LoRA model files
```

---

## 🧠 Model Overview

* **Base Model:** FLAN-T5-base
* **Fine-tuning:** LoRA (Low-Rank Adaptation)
* **Task:** Medical report simplification for patients
* **Model Files:** Loaded from `medical_lora_adapters/`

---

## 📌 Notes

* Designed as an **NTI Graduation Project**
* Focuses on **accessibility**, **clarity**, and **real-world medical NLP use cases**

---

* Make a **shorter version** for portfolio use
* Add **badges** (Python, Streamlit, NLP, AI)


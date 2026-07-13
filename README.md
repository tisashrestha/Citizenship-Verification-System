# Citizenship Validation Project

A secure, privacy-first computer vision pipeline for validating Nepal citizenship documents. This project combines **YOLO-based front-side document validation** with backend text extraction and processing for the back side of the document.

> **Note:** Due to privacy and legal considerations, the dataset used to train the model is **not included** in this repository.

---

## Features

- Front-side citizenship validation using YOLO
- Detection of required document components
- Back-side OCR and data extraction
- Local processing for enhanced privacy
- Modular Python implementation
- Easy-to-use Streamlit interface

---

## Privacy & Security

Because this project processes highly sensitive personally identifiable information (PII), privacy is the primary design goal.

- **All processing is performed locally.**
- **No images or extracted information are uploaded to cloud services.**
- **The training dataset is not publicly distributed.**
- **Only the trained model weights are included (if provided).**

---

## Project Workflow

### 1. Front-Side Validation

The YOLO model analyzes the uploaded front-side image to:

- Detect the citizenship document
- Verify required document components
- Ensure the document is suitable for processing

### 2. Back-Side Data Extraction

The backend pipeline:

- Performs OCR on the back side
- Extracts important information
- Parses the extracted text
- Matches extracted information with user-provided details

---

## Dataset

The original dataset contains sensitive citizenship documents and therefore **cannot be shared publicly**.

To improve model robustness, controlled data augmentation was applied.

### Dataset Statistics

| Dataset | Images |
|---------|-------:|
| Original Images | 9 |
| Augmented Images | 45 |
| Training Images | 48 |
| Validation Images | 6 |
| **Total Images** | **54** |

The augmentation pipeline includes:

- Rotation
- Scaling
- Translation
- Perspective transformation
- Brightness and contrast adjustment

These transformations improve generalization while preserving the visual characteristics of the document.

---

## Prerequisites

Install the following before running the project:

- Python 3.8 or later
- Git

---

## Installation

### Clone the repository

```bash
git clone https://github.com/tisashrestha/Citizenship-Validation-Project.git
cd Citizenship-Validation-Project
```

### Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Launch the Streamlit interface:

```bash
streamlit run ui.py
```

The application will open in your browser, allowing you to upload front and back images of the citizenship document for validation and information extraction.

---

## Model Training

The YOLO model was trained using a custom dataset of Nepal citizenship documents.

Training summary:

- Total Images: **54**
- Training Images: **48**
- Validation Images: **6**

The dataset is intentionally excluded from this repository due to privacy restrictions.

---

## Technologies Used

- Python
- YOLO (Ultralytics)
- OpenCV
- PaddleOCR
- Streamlit
- NumPy
- RapidFuzz

---


## License


The dataset is **not distributed** because it contains sensitive personally identifiable information (PII).

---

## Disclaimer

This repository does **not** include any real citizenship images or personal identity data.

Users wishing to train the model must prepare their own dataset while complying with applicable privacy regulations and legal requirements.

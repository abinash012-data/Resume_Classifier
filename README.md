# Resume_Classifier
A Streamlit-based resume classification app that uses NLP and machine learning to classify job roles and extract years of experience from PDF, DOCX, and DOC resumes.
# 📄 Smart Resume Classification App

A **Streamlit-based resume classification application** that uses Natural Language Processing (NLP) and machine learning to classify resumes into job roles and extract years of professional experience.

The application allows users to upload multiple resumes in **PDF, DOCX, or DOC format**, automatically extracts their text, preprocesses the content, converts it into TF-IDF features, predicts the appropriate job role using a trained machine learning model, and extracts the candidate's years of experience.

---

## 🚀 Features

* 📄 Upload multiple resumes at once
* 📑 Supports PDF, DOCX, and DOC files
* 🧹 Automatic text preprocessing
* 🔤 TF-IDF-based text vectorization
* 🤖 Machine-learning-based job role classification
* 💼 Automatic job-role prediction
* ⏳ Years-of-experience extraction
* 📊 Tabular classification results
* 📥 Download results as CSV
* 🔄 Duplicate resume detection
* 🗑️ Clear previous classification results

## The application supports multiple resume uploads and provides predicted role and experience for each processed resume.

## 🧠 How It Works

The application follows the pipeline below:

```text
Resume Upload
      │
      ▼
PDF / DOCX / DOC Text Extraction
      │
      ▼
Text Cleaning
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Trained ML Classifier
      │
      ▼
Predicted Job Role
      │
      ├──────────────► Experience Extraction
      │
      ▼
Classification Results
      │
      ▼
Download Results as CSV
```

---

## 🔍 Text Preprocessing

Before classification, resume text is converted to lowercase and non-alphabetic characters are removed.

The application uses:

```python
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return text.strip()
```

This produces a simplified text representation suitable for TF-IDF vectorization.

---

## 🔤 TF-IDF Feature Extraction

After preprocessing, the resume text is transformed using a previously trained **TF-IDF vectorizer**.

```python
vector = tfidf.transform([cleaned])
```

The resulting feature vector is passed to the trained classification model.

---

## 🤖 Resume Classification

The trained machine learning classifier predicts a class for each resume.

The predicted class is then converted back into the corresponding job-role label using the trained label encoder.

```python
pred = model.predict(vector)[0]
role = le.inverse_transform([pred])[0]
```

The exact classifier algorithm is **not specified in the uploaded application code**, because the trained model is loaded from `resume_classifier.pkl`.

---

## ⏳ Experience Extraction

The application also attempts to identify years of experience from the resume text.

It recognizes patterns such as:

```text
5 years
3 yrs
2.5 years
experience: 4
exp: 6
```

The extracted value is returned as:

```text
5 Years
```

If no matching experience information is found:

```text
Not Specified
```

---

## 📂 Supported Resume Formats

The application accepts:

| Format | Supported |
| ------ | --------- |
| PDF    | ✅         |
| DOCX   | ✅         |
| DOC    | ✅         |

The Streamlit uploader explicitly allows these three extensions.

### PDF

Text is extracted using `PyPDF2`.

### DOCX

Text is extracted using `python-docx`.

### DOC

The current implementation reads the uploaded file content directly.

---

## 📊 Results

After processing, the application displays a table containing:

| Column         | Description                         |
| -------------- | ----------------------------------- |
| Filename       | Name of the uploaded resume         |
| Predicted Role | Machine-learning predicted job role |
| Experience     | Extracted years of experience       |

The results are maintained using Streamlit session state and displayed as a table.

---

## 📥 Export Results

The application allows the classification results to be downloaded as:

```text
classified_resumes.csv
```

The CSV contains the resume filename, predicted role, and extracted experience.

---

# 🛠️ Tech Stack

### Programming Language

* Python

### Application Framework

* Streamlit

### Data Processing

* Pandas

### NLP / Text Processing

* Regular Expressions
* TF-IDF Vectorization

### Machine Learning

* Scikit-learn
* Joblib

### Document Processing

* PyPDF2
* python-docx

---

# 📁 Project Structure

```text
Smart-Resume-Classifier/
│
├── README.md
├── requirements.txt
├── .gitignore
├── app.py
│
├── models/
│   ├── resume_classifier.pkl
│   ├── tfidf_vectorizer.pkl
│   └── label_encoder.pkl
│
├── sample_resumes/
│   └── README.md
│
└── screenshots/
    ├── home.png
    ├── uploaded_resumes.png
    └── classification_results.png
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Smart-Resume-Classifier.git
cd Smart-Resume-Classifier
```

Replace `<your-username>` with your GitHub username.

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will open the application in your browser.

---

# 📄 Using the Application

### Step 1 — Upload Resumes

Use the sidebar to upload one or multiple resumes.

Supported formats:

```text
PDF
DOCX
DOC
```

### Step 2 — Process Resumes

Click:

```text
Process & Classify
```

The application will:

1. Extract resume text.
2. Clean the text.
3. Convert the text into TF-IDF features.
4. Predict the job role.
5. Extract years of experience.
6. Display the results.

### Step 3 — Download Results

Click:

```text
📥 Download Results as CSV
```

to save the classification results.

---

# 💾 Required Model Files

The application requires the following trained artifacts:

```text
models/
├── resume_classifier.pkl
├── tfidf_vectorizer.pkl
└── label_encoder.pkl
```

These files are required because the application loads the trained classifier, TF-IDF vectorizer, and label encoder when it starts.

If these files are missing, the application displays:

```text
Model files not found.
```

---

# 🔐 Privacy Considerations

Resume documents may contain sensitive personal information such as:

* Names
* Email addresses
* Phone numbers
* Addresses
* Employment history
* Education details

For this reason, **real resumes should not be uploaded to a public GitHub repository**.

Use synthetic or anonymized resumes for demonstrations.

---

# ⚠️ Limitations

### 1. Model Details

The uploaded application code loads a pre-trained classifier but does not contain the model-training code. Therefore, the exact machine-learning algorithm and training dataset cannot be determined from this application file alone.

### 2. Experience Extraction

Experience extraction is based on regular-expression patterns. It may fail when experience is expressed in unusual formats or when the resume contains ambiguous information.

### 3. PDF Extraction

Image-based/scanned PDFs may not produce usable text because the application uses text extraction rather than OCR.

### 4. DOC Support

The current `.doc` handling does not use a dedicated Microsoft Word `.doc` parser. It reads the uploaded file content directly, so compatibility may vary.

### 5. Text Cleaning

The preprocessing removes everything except English alphabetic characters and whitespace. Consequently, numbers and other useful resume information are removed before TF-IDF classification.

---

# 🔮 Future Improvements

Possible improvements include:

* Add OCR support for scanned resumes.
* Improve `.doc` file parsing.
* Use a more robust NLP preprocessing pipeline.
* Preserve useful numerical information such as years of experience.
* Add confidence scores for predictions.
* Display top-N predicted job roles.
* Add resume skill extraction.
* Extract education qualifications.
* Extract contact information.
* Add named entity recognition.
* Add model evaluation metrics.
* Add authentication and secure file handling.
* Deploy the application using Streamlit Community Cloud or another hosting platform.
* Add a dedicated model-training pipeline.

---

# 🎯 Project Objective

The primary objective of this project is to automate an initial stage of resume screening by using NLP and machine learning to classify resumes according to job roles and extract basic experience information.

The application provides a simple interactive interface where multiple resumes can be uploaded and processed automatically.

---

## 👨‍💻 Conclusion

The Smart Resume Classification App combines **Streamlit, NLP, TF-IDF vectorization, and machine learning** into an interactive resume-processing application.

Instead of manually reviewing each resume to determine a potential job category, the application automates the initial classification process and presents the results in a structured format.

The system also extracts years of experience and provides a downloadable CSV containing the classification results.

---

## 📌 Disclaimer

This application is intended as a **resume classification and screening aid**, not as a replacement for human recruitment decisions.

Predictions should be reviewed by qualified users before being used for employment-related decisions.

import streamlit as st
import pandas as pd
import joblib
import re
from docx import Document
import PyPDF2

# -------------------------------------------------
# 1. PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Resume Classifier", layout="wide")

st.title("📄 Smart Resume Classification App")
st.info("Upload multiple resumes to classify job roles and extract experience.")

# -------------------------------------------------
# 2. TEXT PREPROCESSING
# -------------------------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return text.strip()

def extract_experience(text):
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?|experience)',
        r'(?:experience|exp)[:\s-]*(\d+(?:\.\d+)?)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)} Years"
    return "Not Specified"

# -------------------------------------------------
# 3. LOAD MODELS
# -------------------------------------------------
@st.cache_resource
def load_models():
    try:
        model = joblib.load("resume_classifier.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")
        encoder = joblib.load("label_encoder.pkl")
        return model, vectorizer, encoder
    except Exception as e:
        st.error(f"Model loading error: {e}")
        return None, None, None

model, tfidf, le = load_models()

# -------------------------------------------------
# 4. FILE TEXT EXTRACTION
# -------------------------------------------------
def get_text_from_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            text = " ".join([p.text for p in doc.paragraphs])
        elif uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            text = " ".join(
                [page.extract_text() for page in reader.pages if page.extract_text()]
            )
        elif uploaded_file.name.endswith(".doc"):
            text = str(uploaded_file.read())
    except Exception as e:
        st.error(f"Error reading {uploaded_file.name}: {e}")
    return text

# -------------------------------------------------
# 5. SESSION STATE
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# -------------------------------------------------
# 6. SIDEBAR CONTROLS
# -------------------------------------------------
with st.sidebar:
    st.header("Controls")

    uploaded_files = st.file_uploader(
        "Upload Resumes",
        type=["pdf", "docx", "doc"],
        accept_multiple_files=True
    )

    if st.button("Clear Results"):
        st.session_state.history = []
        st.session_state.processed_files = set()
        st.experimental_rerun()

# -------------------------------------------------
# 7. PROCESS & CLASSIFY
# -------------------------------------------------
if st.button("Process & Classify"):
    if uploaded_files and model:
        new_entries = []
        skipped = 0

        for file in uploaded_files:
            if file.name in st.session_state.processed_files:
                skipped += 1
                continue

            raw_text = get_text_from_file(file)
            if not raw_text.strip():
                continue

            cleaned = clean_text(raw_text)
            vector = tfidf.transform([cleaned])
            pred = model.predict(vector)[0]
            role = le.inverse_transform([pred])[0]
            experience = extract_experience(raw_text)

            new_entries.append({
                "Filename": file.name,
                "Predicted Role": role,
                "Experience": experience
            })

            st.session_state.processed_files.add(file.name)

        st.session_state.history.extend(new_entries)

        if new_entries:
            st.success(f"Processed {len(new_entries)} resume(s).")
        if skipped:
            st.info(f"Skipped {skipped} duplicate file(s).")

    elif not model:
        st.error("Model files not found.")
    else:
        st.warning("Please upload resumes first.")

# -------------------------------------------------
# 8. RESULTS & VISUALIZATION
# -------------------------------------------------
if st.session_state.history:
    st.divider()
    st.subheader("📄 Classified Resumes")

    results_df = pd.DataFrame(st.session_state.history)
    st.table(results_df)

        # Download CSV
    csv = results_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Results as CSV",
        data=csv,
        file_name="classified_resumes.csv",
        mime="text/csv"
    )

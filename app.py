import base64
import re
from pathlib import Path

import joblib
import nltk
import streamlit as st
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent
# The .joblib files are currently in the same GitHub root folder as app.py.
MODEL_DIR = BASE_DIR
VINAYAK_PHOTO = BASE_DIR / "vinayak.jpg.jpeg"
MAM_PHOTO = BASE_DIR / "purnima ma.jpeg"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { --ink:#172033; --muted:#667085; --border:#E2E8F0; --canvas:#F6F7FC; }
html, body, [class*="css"], [data-testid="stAppViewContainer"] { font-family:'Inter',sans-serif; }
.stApp { background:var(--canvas); color:var(--ink); }
[data-testid="stHeader"] { background:rgba(246,247,252,.96); }
.block-container { max-width:1200px; padding:2rem 1.5rem 1rem; }
.hero { display:flex; align-items:center; gap:1.2rem; padding:1.8rem; border-radius:20px;
background:linear-gradient(120deg,#211A55,#5143C9 58%,#72B9F8); color:white; margin-bottom:1.4rem; }
.hero-icon { flex:0 0 65px; width:65px; height:65px; display:grid; place-items:center;
background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.35); border-radius:18px; font-size:2rem; }
.hero h1 { color:white!important; font-size:clamp(1.5rem,3vw,2.4rem)!important; margin:0 0 .45rem; line-height:1.2; }
.hero p { color:#F0EEFF!important; margin:0; line-height:1.55; }
.section-title { color:var(--ink); font-size:1.2rem; font-weight:750; margin:.7rem 0 .25rem; }
.section-caption { color:var(--muted); font-size:.9rem; margin-bottom:1rem; }
div[data-testid="stTextArea"] label, div[data-testid="stSelectbox"] label { color:var(--ink)!important; font-weight:650!important; }
div[data-testid="stTextArea"] textarea { background:white!important; color:#172033!important; border:1px solid #D7DBE8!important; border-radius:12px!important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"]>div { background:white!important; color:#172033!important; border-color:#D7DBE8!important; border-radius:10px!important; }
.stButton>button { background:linear-gradient(100deg,#7355EF,#4059E8)!important; color:white!important; border:0!important; border-radius:11px!important; min-height:3rem; font-weight:700!important; }
.result-card { background:white; border:1px solid var(--border); border-radius:16px; padding:1.3rem; margin-top:.8rem; }
.result-positive { color:#15803D!important; } .result-neutral { color:#B45309!important; } .result-negative { color:#B91C1C!important; }
.info-card { background:white; border:1px solid var(--border); border-radius:14px; padding:1rem; min-height:100px; height:100%; }
.info-card .label { color:var(--muted); font-size:.8rem; margin-bottom:.4rem; }
.info-card .value { color:var(--ink); font-weight:700; line-height:1.45; }
.footer { background:#111827; color:#D1D5DB; border:1px solid #273449; border-radius:14px; margin-top:1.5rem; padding:1.4rem 1.2rem 1rem; text-align:center; font-size:.84rem; line-height:1.6; }
.footer-credits { display:flex; flex-direction:row; justify-content:space-evenly; align-items:flex-start; gap:2rem; }
.footer-person { flex:1; min-width:0; text-align:center; padding:.4rem; }
.footer-photo { width:88px; height:88px; object-fit:cover; border-radius:50%; border:3px solid #A5B4FC; display:block; margin:0 auto .7rem; }
.footer-label { color:#C4B5FD; font-size:.82rem; }
.footer-name { color:#FFFFFF; font-size:1rem; font-weight:750; }
.footer-role { color:#D1D5DB; font-size:.82rem; }
.footer-contact { display:flex; justify-content:center; flex-wrap:wrap; gap:1.2rem; margin-top:1rem; }
.footer-contact a { color:#A5B4FC!important; text-decoration:none; }
.footer-contact a:hover { color:#FFFFFF!important; text-decoration:underline; }
.footer-project { color:#A5B4FC; border-top:1px solid #374151; margin-top:1rem; padding-top:.8rem; font-size:.8rem; }
@media(max-width:600px) {
 .block-container { padding:1rem .75rem .5rem!important; }
 .hero { display:block; padding:1.2rem; border-radius:16px; }
 .hero-icon { width:48px; height:48px; font-size:1.5rem; margin-bottom:.8rem; }
 .footer-credits { flex-direction:column; align-items:center; gap:1rem; }
 .footer-person { width:100%; }
 .footer-photo { width:78px; height:78px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<section class="hero">
  <div class="hero-icon">🎧</div>
  <div>
    <h1>Amazon Alexa Sentiment Analyzer</h1>
    <p>Machine-learning-based three-class sentiment analysis.<br>
    Classify customer reviews as Positive, Neutral, or Negative.</p>
  </div>
</section>
""", unsafe_allow_html=True)

@st.cache_resource
def load_nltk_resources():
    for resource in ["punkt", "punkt_tab", "wordnet", "omw-1.4"]:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass
    return WordNetLemmatizer()

lemmatizer = load_nltk_resources()

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    tokens = word_tokenize(text)
    return " ".join(lemmatizer.lemmatize(word) for word in tokens)

MODEL_NAMES = [
    "Multinomial Naive Bayes",
    "Logistic Regression",
    "Support Vector Machine (SVM)",
    "Random Forest",
]
FEATURE_NAMES = ["BoW", "TF-IDF"]

def artifact_path(model_name, feature_name):
    return MODEL_DIR / f"{model_name}__{feature_name}.joblib"

st.markdown('<div class="section-title">Analyze a customer review</div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">Enter a review, select a trained classifier and text representation, then run a real prediction.</div>', unsafe_allow_html=True)

with st.container(border=True):
    review = st.text_area(
        "Customer review",
        placeholder="Example: The sound quality is amazing and Alexa is very useful!",
        height=135,
        max_chars=2000,
    )
    col1, col2 = st.columns(2)
    with col1:
        model_name = st.selectbox("Machine-learning model", MODEL_NAMES)
    with col2:
        feature_name = st.selectbox("Text representation", FEATURE_NAMES)
    predict_clicked = st.button("✨  Predict Sentiment", use_container_width=True)

if predict_clicked:
    if not review.strip():
        st.warning("Please enter a customer review first.")
    else:
        path = artifact_path(model_name, feature_name)
        if not path.exists():
            st.error(f"Trained model not found: `{path.name}`. Check that this exact .joblib file is uploaded beside app.py in GitHub.")
        else:
            try:
                artifact = joblib.load(path)
                vector = artifact["vectorizer"].transform([preprocess_text(review)])
                model = artifact["model"]
                prediction = str(model.predict(vector)[0])
                sentiment_class = {
                    "Positive": "result-positive",
                    "Neutral": "result-neutral",
                    "Negative": "result-negative",
                }.get(prediction, "")
                st.markdown('<div class="section-title">Prediction result</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="result-card"><div style="color:#667085;font-size:.9rem;">Predicted sentiment</div>'
                    f'<h2 class="{sentiment_class}" style="margin:.35rem 0;">{prediction}</h2>'
                    f'<div style="color:#667085;font-size:.85rem;">Model: {model_name} · Features: {feature_name}</div></div>',
                    unsafe_allow_html=True,
                )
                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(vector)[0]
                    st.markdown("#### Class probabilities")
                    for label, probability in sorted(zip(model.classes_, probabilities), key=lambda pair: pair[1], reverse=True):
                        st.write(f"{label}: {probability:.1%}")
                        st.progress(float(probability))
                    st.caption("These are model-estimated probabilities, not a guarantee that the prediction is correct.")
                else:
                    st.info("This SVM model does not provide probability estimates by default. The predicted sentiment is shown without a confidence meter.")
            except Exception as exc:
                st.error(f"Prediction failed: {exc}. Check the app logs if the issue continues.")

st.markdown('<div class="section-title">Research methodology</div>', unsafe_allow_html=True)
st.markdown('<div class="section-caption">The main techniques used in this comparative study.</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="info-card"><div class="label">01 · Text representation</div><div class="value">Bag of Words (BoW)<br>TF-IDF</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="info-card"><div class="label">02 · Classifiers</div><div class="value">Naive Bayes, Logistic Regression, SVM, Random Forest</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="info-card"><div class="label">03 · Evaluation</div><div class="value">Accuracy, Macro Precision, Macro Recall, Macro-F1</div></div>', unsafe_allow_html=True)

def image_as_base64(image_path):
    if not image_path.exists():
        return None
    return base64.b64encode(image_path.read_bytes()).decode("utf-8")

vinayak_photo_data = image_as_base64(VINAYAK_PHOTO)
mam_photo_data = image_as_base64(MAM_PHOTO)
vinayak_photo_html = (
    f'<img class="footer-photo" src="data:image/jpeg;base64,{vinayak_photo_data}" alt="Vinayak Sharma">'
    if vinayak_photo_data else ""
)
mam_photo_html = (
    f'<img class="footer-photo" src="data:image/jpeg;base64,{mam_photo_data}" alt="Ms. Purnima Bindal">'
    if mam_photo_data else ""
)

st.markdown(f"""
<div class="footer">
  <div class="footer-credits">
    <div class="footer-person">
      {vinayak_photo_html}
      <div class="footer-label">Developed by</div>
      <div class="footer-name">Vinayak Sharma</div>
      <div class="footer-role">Computer Science</div>
      <div class="footer-role">VinayakSharma1911@gmail.com</div>
    </div>
    <div class="footer-person">
      {mam_photo_html}
      <div class="footer-label">Under the guidance of</div>
      <div class="footer-name">Ms. Purnima Bindal</div>
      <div class="footer-role">Assistant Professor</div>
      <div class="footer-role">University of Delhi</div>
    </div>
  </div>
  <div class="footer-contact">
    <a href="https://github.com/" target="_blank" rel="noopener noreferrer">GitHub</a>
    <a href="https://www.linkedin.com/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
  </div>
  <div class="footer-project">Amazon Alexa Sentiment Analysis Research Project</div>
</div>
""", unsafe_allow_html=True)

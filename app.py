import streamlit as st

st.set_page_config(
    page_title="Alexa Sentiment Analyzer",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #172033;
    --muted: #667085;
    --primary: #5B4BDB;
    --primary-dark: #4536BF;
    --border: #E5E7F0;
    --surface: #FFFFFF;
    --canvas: #F6F7FC;
}
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: var(--canvas);
    color: var(--ink);
}
[data-testid="stHeader"] {
    background: rgba(246, 247, 252, 0.95);
}
.block-container {
    max-width: 1100px;
    padding: 2.2rem 2rem 1rem;
}
.hero {
    padding: 2rem 2.1rem;
    border-radius: 22px;
    background: linear-gradient(120deg, #211A55 0%, #5143C9 58%, #7468EB 100%);
    color: #FFFFFF;
    margin-bottom: 1.6rem;
    box-shadow: 0 12px 32px rgba(64, 53, 173, 0.16);
}
.hero .eyebrow {
    color: #DAD7FF;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 0.7rem;
}
.hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(1.8rem, 3vw, 2.5rem) !important;
    line-height: 1.15;
    margin: 0 0 0.65rem 0;
    font-weight: 800;
}
.hero p {
    color: #F0EEFF !important;
    font-size: 1rem;
    margin: 0;
    line-height: 1.6;
}
.section-title {
    color: var(--ink);
    font-size: 1.2rem;
    font-weight: 750;
    margin: 0.6rem 0 0.3rem;
}
.section-caption {
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 1.15rem;
}
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.35rem 1.4rem;
    box-shadow: 0 5px 18px rgba(22, 34, 66, 0.035);
    margin-bottom: 1rem;
}
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    color: var(--ink) !important;
    font-weight: 650 !important;
    font-size: 0.92rem !important;
}
div[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #172033 !important;
    border: 1px solid #D7DBE8 !important;
    border-radius: 12px !important;
    font-size: 0.98rem !important;
    line-height: 1.55 !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(91,75,219,0.12) !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #172033 !important;
    border-color: #D7DBE8 !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border: 1px solid var(--primary) !important;
    border-radius: 11px !important;
    padding: 0.72rem 1.15rem !important;
    font-weight: 700 !important;
    min-height: 3rem;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background: var(--primary-dark) !important;
    border-color: var(--primary-dark) !important;
    box-shadow: 0 6px 14px rgba(91,75,219,0.2);
}
.result-placeholder {
    border: 1px dashed #C9CBE5;
    border-radius: 16px;
    padding: 1.4rem;
    background: #FCFCFF;
    color: var(--muted);
    text-align: center;
}
.info-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 1rem 1.1rem;
    min-height: 105px;
}
.info-card .label {
    color: var(--muted);
    font-size: 0.8rem;
    margin-bottom: 0.45rem;
}
.info-card .value {
    color: var(--ink);
    font-weight: 750;
    font-size: 1rem;
}
.footer {
    text-align: center;
    border-top: 1px solid var(--border);
    margin-top: 2.5rem;
    padding: 1.5rem 0 0.8rem;
    color: var(--muted);
    font-size: 0.84rem;
    line-height: 1.8;
}
.footer strong {
    color: var(--ink);
    font-size: 1rem;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
@media (max-width: 700px) {
    .block-container { padding: 1.2rem 1rem 0.8rem; }
    .hero { padding: 1.5rem; border-radius: 17px; }
    .panel { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<section class="hero">
  <div class="eyebrow">Machine Learning Research Project</div>
  <h1>Alexa Sentiment Analyzer</h1>
  <p>Understand customer opinions with three-class sentiment analysis.<br>
  Classify reviews as Positive, Neutral, or Negative.</p>
</section>
""", unsafe_allow_html=True)

# Review form
st.markdown('<div class="section-title">Analyze a customer review</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">Enter a review and choose one of the machine-learning models.</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    review = st.text_area(
        "Customer review",
        placeholder="Example: The sound quality is amazing and Alexa is very useful!",
        height=145,
        key="review_text",
    )
    model_name = st.selectbox(
        "Machine-learning model",
        [
            "Multinomial Naive Bayes",
            "Logistic Regression",
            "Support Vector Machine (SVM)",
            "Random Forest",
        ],
        key="selected_model",
    )
    predict_clicked = st.button("✨  Predict sentiment", use_container_width=True)

# This UI intentionally does not fake model output.
if predict_clicked:
    if not review.strip():
        st.warning("Please enter a customer review before predicting.")
    else:
        st.info(
            f"You selected **{model_name}**. The interface is ready, but real predictions "
            "will appear after the trained model, its matching vectorizer, and the "
            "training-time preprocessing pipeline are connected."
        )

st.markdown('<div class="section-title">Research methodology</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">The main techniques used in this comparative study.</div>',
    unsafe_allow_html=True,
)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="info-card">
      <div class="label">01 · Text representation</div>
      <div class="value">Bag of Words &amp; TF-IDF</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="info-card">
      <div class="label">02 · Classifiers</div>
      <div class="value">MNB, Logistic Regression, SVM, Random Forest</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="info-card">
      <div class="label">03 · Evaluation</div>
      <div class="value">Accuracy &amp; Macro-F1</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  <div>Developed under the guidance of</div>
  <strong>Ms. Purnima Bindal</strong><br>
  Assistant Professor, University of Delhi<br>
  <span>Amazon Alexa Sentiment Analysis Research Project</span>
</div>
""", unsafe_allow_html=True)

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
    --border: #E2E8F0;
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
    background: rgba(246, 247, 252, 0.96);
}
.block-container {
    max-width: 1240px;
    padding: 2rem 2rem 1rem;
}
.hero {
    display: flex;
    align-items: center;
    gap: 1.4rem;
    padding: 2rem;
    border-radius: 22px;
    background: linear-gradient(120deg, #211A55 0%, #5143C9 58%, #72B9F8 100%);
    color: white;
    margin-bottom: 1.35rem;
    box-shadow: 0 12px 32px rgba(64, 53, 173, 0.16);
}
.hero-icon {
    flex: 0 0 76px;
    width: 76px;
    height: 76px;
    display: grid;
    place-items: center;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.38);
    border-radius: 22px;
    font-size: 2.4rem;
}
.hero-copy { min-width: 0; }
.hero .eyebrow {
    color: #DAD7FF;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 0.65rem;
}
.hero h1 {
    color: white !important;
    font-size: clamp(1.65rem, 3vw, 2.55rem) !important;
    line-height: 1.15;
    margin: 0 0 0.55rem 0;
    font-weight: 800;
    overflow-wrap: anywhere;
}
.hero p {
    color: #F0EEFF !important;
    font-size: 0.98rem;
    margin: 0;
    line-height: 1.6;
}
.section-title {
    color: var(--ink);
    font-size: 1.2rem;
    font-weight: 750;
    margin: 0.55rem 0 0.25rem;
}
.section-caption {
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 1rem;
}
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    color: var(--ink) !important;
    font-weight: 650 !important;
    font-size: 0.92rem !important;
}
div[data-testid="stTextArea"] textarea {
    background: white !important;
    color: #172033 !important;
    border: 1px solid #D7DBE8 !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    line-height: 1.55 !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(91,75,219,0.12) !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: white !important;
    color: #172033 !important;
    border-color: #D7DBE8 !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: linear-gradient(100deg, #7355EF, #4059E8) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 11px !important;
    padding: 0.72rem 1.15rem !important;
    font-weight: 700 !important;
    min-height: 3rem;
    width: 100%;
}
.stButton > button:hover {
    filter: brightness(0.96);
    box-shadow: 0 6px 14px rgba(91,75,219,0.2);
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border) !important;
    border-radius: 17px !important;
    background: rgba(255,255,255,0.82);
}
.info-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 1.1rem;
    min-height: 110px;
    height: 100%;
    box-sizing: border-box;
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
    line-height: 1.45;
    overflow-wrap: anywhere;
}

.footer {
    background: #111827;
    color: #D1D5DB;
    border: 1px solid #273449;
    border-radius: 14px;
    margin-top: 1.5rem;
    padding: 1.1rem 1.5rem;
    text-align: center;
    font-size: 0.82rem;
    line-height: 1.5;
}

.footer .credits {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    flex-wrap: wrap;
}

.footer .credit-block {
    padding: 0.25rem 0.5rem;
}

.footer .student-name,
.footer .supervisor-name {
    color: #FFFFFF;
    font-size: 1rem;
    font-weight: 750;
}

.footer .project-name {
    color: #A5B4FC;
    font-size: 0.78rem;
    margin-top: 0.65rem;
}

@media (max-width: 760px) {
    .footer {
        padding: 1rem 0.75rem;
        margin-top: 1rem;
    }

    .footer .credits {
        flex-direction: column;
        gap: 0.65rem;
    }
}

div[data-testid="stAlert"] { border-radius: 12px; }

/* Mobile and narrow-screen adjustments */
@media (max-width: 760px) {
    .block-container {
        padding: 1rem 0.8rem 0.6rem !important;
    }
    .hero {
        display: block;
        padding: 1.25rem 1.1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    .hero-icon {
        width: 52px;
        height: 52px;
        font-size: 1.7rem;
        border-radius: 15px;
        margin-bottom: 0.9rem;
    }
    .hero .eyebrow {
        font-size: 0.65rem;
        letter-spacing: 0.09em;
    }
    .hero h1 {
        font-size: 1.65rem !important;
        line-height: 1.18;
    }
    .hero p { font-size: 0.9rem; }
    .section-title { font-size: 1.08rem; }
    .section-caption { font-size: 0.86rem; line-height: 1.45; }
    div[data-testid="stTextArea"] textarea { font-size: 0.95rem !important; }
    .info-card {
        min-height: auto;
        padding: 0.95rem;
        margin-bottom: 0.25rem;
    }
    .info-card .value { font-size: 0.95rem; }
    .footer {
        margin-top: 1.3rem;
        padding: 1.1rem 0.7rem;
    }
    .stButton > button { min-height: 2.9rem; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<section class="hero">
  <div class="hero-icon">🎧</div>
  <div class="hero-copy">
    <div class="eyebrow">Machine Learning Research Project</div>
    <h1> Review Lens Sentiment Analyzer</h1>
    <p>Three-class sentiment analysis for customer reviews.<br>
    Classify reviews as Positive, Neutral, or Negative.</p>
  </div>
</section>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Analyze a customer review</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">Enter a review and choose a machine-learning model.</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    review = st.text_area(
        "Customer review",
        placeholder="Example: The sound quality is amazing and Alexa is very useful!",
        height=145,
        max_chars=500,
        key="review_text",
    )
    model_name = st.selectbox(
        "Select machine-learning model",
        [
            "Multinomial Naive Bayes",
            "Logistic Regression",
            "Support Vector Machine (SVM)",
            "Random Forest",
        ],
        key="selected_model",
    )
    predict_clicked = st.button("✨  Predict Sentiment", use_container_width=True)

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
      <div class="value">Bag of Words (BoW)<br>&amp; TF-IDF</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="info-card">
      <div class="label">02 · Classifiers</div>
      <div class="value">Naive Bayes, Logistic Regression, SVM, Random Forest</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="info-card">
      <div class="label">03 · Evaluation</div>
      <div class="value">Accuracy, Macro Precision, Macro Recall, Macro-F1</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""

<div class="footer">
    <div class="credits">
        <div class="credit-block">
            <div>Developed by</div>
            <div class="student-name">Vinayak Sharma</div>
        </div>

        <div class="credit-block">
            <div>Under the guidance of</div>
            <div class="supervisor-name">Ms. Purnima Bindal</div>
            <div>Assistant Professor, University of Delhi</div>
        </div>
    </div>

    <div class="project-name">
        Review Lens Sentiment Analysis Research Project using NLP 
    </div>
</div>

""", unsafe_allow_html=True)


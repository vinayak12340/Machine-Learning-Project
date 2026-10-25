
import streamlit as st

st.set_page_config(
    page_title="Alexa Sentiment Analyzer",
    page_icon="🎧",
    layout="wide"
)

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background: #F8FAFF;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #EEF2FF, #F5F3FF);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #E0E7FF;
    margin-bottom: 25px;
}
.result-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #E2E8F0;
    text-align: center;
}
.footer {
    text-align: center;
    color: #64748B;
    padding: 25px 10px 5px;
    border-top: 1px solid #E2E8F0;
    margin-top: 40px;
}
.stButton > button {
    background: #5145CD;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    width: 100%;
}
.stButton > button:hover {
    background: #4338CA;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🎧 Alexa Sentiment Analyzer</h1>
    <p>Machine Learning-Based Three-Class Sentiment Analysis</p>
    <p>Analyze customer reviews as Positive, Neutral, or Negative.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Review input ----------
st.subheader("📝 Analyze a Customer Review")

review = st.text_area(
    "Enter your Amazon Alexa review",
    placeholder="Example: The sound quality is amazing and Alexa is very useful!",
    height=140
)

model_name = st.selectbox(
    "Select Machine Learning Model",
    [
        "Multinomial Naive Bayes",
        "Logistic Regression",
        "Support Vector Machine (SVM)",
        "Random Forest"
    ]
)

if st.button("✨ Predict Sentiment"):
    if not review.strip():
        st.warning("Please enter a review first.")
    else:
        st.info(
            f"You selected **{model_name}**. "
            "The prediction will be available after the trained model "
            "and its matching vectorizer are connected."
        )

# ---------- Research information ----------
st.divider()
st.subheader("🔬 About the Research")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Feature Extraction")
    st.write("Bag of Words (BoW) and TF-IDF")

with col2:
    st.markdown("#### Model Evaluation")
    st.write("Accuracy, Macro Precision, Macro Recall and Macro-F1")

st.markdown("""
<div class="footer">
    <p>Developed under the guidance of</p>
    <h4>Ms. Purnima Bindal</h4>
    <p>Assistant Professor, University of Delhi</p>
    <p>Amazon Alexa Sentiment Analysis Research Project</p>
</div>
""", unsafe_allow_html=True)

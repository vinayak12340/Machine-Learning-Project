# Amazon Alexa Sentiment Analysis

## Project Description
This research project studies three-class sentiment analysis of Amazon Alexa customer reviews. It aims to classify a review as **Positive**, **Neutral**, or **Negative** using traditional machine-learning algorithms and compare their performance.

The project workflow includes exploratory data analysis, text cleaning and preprocessing, text feature extraction, model training, and evaluation. A Streamlit interface is planned so users can enter a review, select a trained model, and view the predicted sentiment. Probability information should be shown only when it is supported by the selected model.

## Tech Stack
- **Language:** Python
- **Data handling:** pandas, NumPy
- **Machine learning:** scikit-learn
- **Text processing:** NLTK
- **Frontend:** Streamlit
- **Plots (optional):** Matplotlib

## Models and Techniques
- **Feature extraction:** Bag of Words (BoW), TF-IDF
- **Classifiers:** Multinomial Naive Bayes, Logistic Regression, Linear Support Vector Machine (LinearSVC), Random Forest
- **Evaluation:** Accuracy, macro precision, macro recall, macro-F1, classification report
- **Data split:** Stratified 60:40 train-test split with `random_state=42` (as used in the current methodology)

## Dataset and Labels
Dataset filename: `amazon_alexa.tsv`

The three-class target is derived from the `rating` column:
- Ratings 1–2: Negative
- Rating 3: Neutral
- Ratings 4–5: Positive

Do not use `rating` as a model input because it is used to derive the target label. The original binary `feedback` column is not the three-class target.

## Setup Guidance

### 1. Create a virtual environment (recommended)
Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Run the Streamlit app

From the folder containing `app.py`:

```powershell
python -m streamlit run app.py
```

Streamlit will show a local URL, usually `http://localhost:8501`.

## Important Implementation Notes
- Keep preprocessing consistent between model training and live predictions.
- Save and load the fitted vectorizer that matches each trained model.
- Fit vectorizers on training data only to avoid data leakage.
- Use the same train-test split when comparing models.
- `LinearSVC` does not provide probability estimates by default. Use calibrated probabilities if the interface needs probability bars for SVM.
- The frontend must be connected to real saved models before it can produce actual predictions.
- Do not report sample or illustrative predictions as real model results.

## Project Guidance
**Developed under the guidance of Ms. Purnima Bindal, Assistant Professor, University of Delhi.**

## Current Status
Project documentation and dependency list are prepared. Update this section when the trained models and Streamlit prediction pipeline are integrated.

## Dataset and Repository Note
Check the dataset's usage terms before sharing it publicly. Do not upload passwords, API keys, private information, or other secrets to GitHub.

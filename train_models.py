import re
from pathlib import Path

import joblib
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.utils.class_weight import compute_sample_weight

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "amazon_alexa.tsv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

# Download tokenizer and lemmatizer resources needed by NLTK.
for resource in ["punkt", "punkt_tab", "wordnet", "omw-1.4"]:
    nltk.download(resource, quiet=True)

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "amazon_alexa.tsv not found. Put it in the same folder as train_models.py."
        )

    df = pd.read_csv(DATA_PATH, sep="\t")

    # Follow the notebook's cleaning and label definitions.
    df = df.drop_duplicates().copy()
    df = df.dropna(subset=["verified_reviews", "rating"]).copy()
    df = df[df["verified_reviews"].astype(str).str.strip().ne("")].copy()

    df["sentiment"] = pd.cut(
        df["rating"],
        bins=[0, 2, 3, 5],
        labels=["Negative", "Neutral", "Positive"],
        include_lowest=True,
    )
    df = df.dropna(subset=["sentiment"]).copy()
    df["processed_reviews"] = df["verified_reviews"].apply(preprocess_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["processed_reviews"],
        df["sentiment"].astype(str),
        test_size=0.40,
        random_state=42,
        stratify=df["sentiment"].astype(str),
    )

    # Fit each vectorizer on training data only to avoid data leakage.
    vectorizers = {
        "BoW": CountVectorizer(),
        "TF-IDF": TfidfVectorizer(),
    }

    sample_weights = compute_sample_weight("balanced", y_train)
    saved = 0

    for feature_name, vectorizer in vectorizers.items():
        Xtr = vectorizer.fit_transform(X_train)
        Xte = vectorizer.transform(X_test)

        for model_name in [
            "Multinomial Naive Bayes",
            "Logistic Regression",
            "Support Vector Machine (SVM)",
            "Random Forest",
        ]:
            if model_name == "Multinomial Naive Bayes":
                model = MultinomialNB()
                model.fit(Xtr, y_train, sample_weight=sample_weights)
            elif model_name == "Logistic Regression":
                model = LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42,
                )
                model.fit(Xtr, y_train)
            elif model_name == "Support Vector Machine (SVM)":
                model = LinearSVC(class_weight="balanced", random_state=42)
                model.fit(Xtr, y_train)
            else:
                model = RandomForestClassifier(
                    class_weight="balanced",
                    random_state=42,
                )
                model.fit(Xtr, y_train)

            key = f"{model_name}__{feature_name}"
            artifact = {
                "model": model,
                "vectorizer": vectorizer,
                "feature_name": feature_name,
                "model_name": model_name,
                "classes": list(model.classes_),
            }
            joblib.dump(artifact, MODEL_DIR / f"{key}.joblib")
            saved += 1
            print(f"Saved: models/{key}.joblib")

    print(f"\nFinished. Saved {saved} model/vectorizer combinations.")
    print("The notebook's train/test split was stratified with test_size=0.40 and random_state=42.")
    print("SVM predictions will show the class label; LinearSVC does not provide probabilities by default.")

if __name__ == "__main__":
    main()

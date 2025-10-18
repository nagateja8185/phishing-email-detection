from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import re

# Load the trained model
model = joblib.load('models/phishing_logreg_tfidf.pkl')

app = FastAPI(title="Phishing Email Detection API")

# ---------- Root route ----------
@app.get("/")
def root():
    return {"message": "Phishing Detection API is running. Use /predict to POST emails."}

# ---------- Email input schema ----------
class Email(BaseModel):
    subject: str
    body: str

# ---------- Feature extraction ----------
def extract_numeric_from_text(subject: str, body: str):
    num_urls = len(re.findall(r'http[s]?://', body))
    num_exclaims = subject.count('!') + body.count('!')
    return {
        'subject_len': len(subject),
        'body_len': len(body),
        'num_urls': num_urls,
        'num_exclaims': num_exclaims
    }

# ---------- Predict endpoint ----------
@app.post("/predict")
def predict(email: Email):
    """
    Predict whether an email is phishing (1) or legitimate (0)
    Returns probability and label
    """
    # Create a single-row DataFrame matching training features
    numeric = extract_numeric_from_text(email.subject, email.body)
    X_df = pd.DataFrame([numeric])
    X_df['text'] = email.subject + ' ' + email.body

    prob = model.predict_proba(X_df)[0,1]
    label = int(prob > 0.5)
    return {"label": label, "probability": float(prob)}

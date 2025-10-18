# 🧠 Phishing Email Detection Using Machine Learning

## 📖 Project Overview
This project uses **Machine Learning (AI)** to detect phishing emails automatically. It combines **text analysis (NLP)** with numeric features extracted from emails (like number of URLs, message length, and exclamation marks) to classify emails as:

- **0 → Legitimate email**
- **1 → Phishing email**

The backend API is built with **FastAPI**, allowing users to send emails and get **real-time predictions**.

---

## 🤖 AI / Machine Learning

- **Model:** Logistic Regression (from scikit-learn)
- **Features:**
  - TF-IDF vectors of email text (subject + body)
  - Numeric features: subject length, body length, number of URLs, number of exclamation marks
- **Training:** The model learns patterns from a dataset of labeled emails.
- **Prediction:** The trained model returns both a probability and a label for new emails.

---

## 📂 Folder Structure

```
phishing-detection/
│
├─ data/
│   └─ processed/emails.csv       # Preprocessed dataset for training
│
├─ models/
│   └─ phishing_logreg_tfidf.pkl  # Trained model saved here
│
├─ src/
│   ├─ train.py                   # Script to train the ML model
│   ├─ data_prep.py               # Data preprocessing functions
│   └─ predict_api.py             # FastAPI server for predictions
│
├─ requirements.txt               # Python dependencies
└─ README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd phishing-detection
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
.env\Scripts\Activate.ps1
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧠 Training the Model

Run the training script to preprocess data and create the trained model:
```bash
python src\train.py
```
**Output:** `models/phishing_logreg_tfidf.pkl`  
**Ensure:** Your dataset exists at `data/processed/emails.csv`

---

## 🚀 Running the FastAPI Server

Start the API locally:
```bash
uvicorn src.predict_api:app --reload
```

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **Base URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000) → Shows status message

---

## 📩 Using the API

### `POST /predict`

Send JSON data with the email to get predictions.

**Request Example:**
```json
{
  "subject": "Verify your account",
  "body": "Click http://fakebank.com/login to verify your account now!"
}
```

**Response Example:**
```json
{
  "label": 1,
  "probability": 0.987654
}
```

- **label: 1 → phishing**  
- **label: 0 → legitimate**  
- **probability → model confidence**

---

## 🧪 Testing Multiple Emails

You can create a Python tester script (`test_api.py`):

```python
import requests

emails = [
    {"subject":"Verify your account","body":"Click http://fakebank.com/login to verify your account now!"},
    {"subject":"Meeting rescheduled","body":"The team meeting has been moved to 3 PM tomorrow."},
    {"subject":"Urgent: Your password will expire","body":"Login immediately at http://secure-login.com"},
    {"subject":"Lunch plans","body":"Hey, do you want to grab lunch at 1 PM today?"},
    {"subject":"Congratulations! You won a prize","body":"Claim your $1000 gift card here: http://fakeprizes.com"}
]

for email in emails:
    r = requests.post("http://127.0.0.1:8000/predict", json=email)
    print(email["subject"], "->", r.json())
```

Run it:
```bash
python test_api.py
```

---

## 🧬 How AI is Used

1. **Feature Extraction:** Converts text and numeric attributes into vectors.  
2. **Training:** Logistic Regression learns phishing patterns from labeled emails.  
3. **Prediction:** Determines the probability of phishing for new emails.  
4. **Automation:** Can scan emails in bulk and flag phishing attempts automatically.

---

## 📝 Notes

- Ensure **Python ≥ 3.10**
- Install **Microsoft C++ Build Tools** if you face dependency errors during installation.
- The API uses **FastAPI** — the Swagger UI is very useful for testing endpoints.

---

⭐ This README provides complete setup, AI explanation, and API testing guidance for your **Phishing Email Detection Project**.

# src/train.py
import os
import joblib
import pandas as pd
from data_prep import preprocess_data
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score

RANDOM_SEED = 42

# ---------- Load and preprocess ----------
X_text, X_numeric, y, df = preprocess_data('data/processed/emails.csv')

# Combine numeric and text features into a single DataFrame
X_numeric = X_numeric.reset_index(drop=True)
X_text = X_text.reset_index(drop=True).rename("text")
X_df = pd.concat([X_numeric, X_text], axis=1)

# ---------- ColumnTransformer ----------
numeric_cols = X_numeric.columns.tolist()

preprocessor = ColumnTransformer(transformers=[
    ('text', TfidfVectorizer(ngram_range=(1,2), max_features=1000), 'text'),
    ('num', StandardScaler(), numeric_cols)
], remainder='drop')

# ---------- Pipeline ----------
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced', random_state=RANDOM_SEED))
])

# ---------- Cross-validation ----------
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
y_pred = cross_val_predict(pipeline, X_df, y, cv=skf, method='predict')
y_prob = cross_val_predict(pipeline, X_df, y, cv=skf, method='predict_proba')[:,1]

# ---------- Metrics ----------
print("=== Classification Report ===")
print(classification_report(y, y_pred, digits=4))
print("=== Confusion Matrix ===")
print(confusion_matrix(y, y_pred))
print("ROC AUC:", roc_auc_score(y, y_prob))
print("PR AUC:", average_precision_score(y, y_prob))

# ---------- Train final model ----------
pipeline.fit(X_df, y)

# ---------- Ensure models folder exists ----------
os.makedirs('models', exist_ok=True)

# ---------- Save the trained model ----------
joblib.dump(pipeline, 'models/phishing_logreg_tfidf.pkl')
print("Model saved to models/phishing_logreg_tfidf.pkl")

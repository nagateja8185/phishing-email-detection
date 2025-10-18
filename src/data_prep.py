# src/data_prep.py
import pandas as pd
import re

def load_data(file_path):
    """
    Load CSV data into a pandas DataFrame
    """
    df = pd.read_csv(file_path)
    df['subject'] = df['subject'].astype(str)
    df['body'] = df['body'].astype(str)
    df['subject_body'] = df['subject'] + ' ' + df['body']
    return df

def extract_numeric_features(df):
    """
    Extract simple numeric/metadata features from emails
    """
    features = pd.DataFrame()
    # Length features
    features['subject_len'] = df['subject'].apply(len)
    features['body_len'] = df['body'].apply(len)
    # Number of URLs in the email body
    features['num_urls'] = df['body'].apply(lambda s: len(re.findall(r'http[s]?://', s)))
    # Number of exclamation marks
    features['num_exclaims'] = df['subject'].apply(lambda s: s.count('!')) + df['body'].apply(lambda s: s.count('!'))
    return features

def preprocess_data(file_path):
    """
    Load data and return feature matrix X and labels y
    """
    df = load_data(file_path)
    X_numeric = extract_numeric_features(df)
    X_text = df['subject_body']
    y = df['label']
    return X_text, X_numeric, y, df

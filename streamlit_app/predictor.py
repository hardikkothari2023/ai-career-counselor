import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
import os

# Global paths
MODEL_PATH = os.path.join("models", "career_model.pkl")
DATA_PATH = os.path.join("data", "career_data.csv")

def load_data():
    df = pd.read_csv(DATA_PATH)
    df['skills'] = df['skills'].apply(lambda x: x.split(","))
    return df

def train_model():
    df = load_data()

    # Label encode target
    le = LabelEncoder()
    df["career_label"] = le.fit_transform(df["career"])
    joblib.dump(le, os.path.join("models", "label_encoder.pkl"))

    # Preprocessing
    mlb = MultiLabelBinarizer()
    X_skills = mlb.fit_transform(df["skills"])
    edu_encoder = OneHotEncoder(sparse_output=False)
    X_edu_encoded = edu_encoder.fit_transform(df["education"].values.reshape(-1, 1))

    X = np.hstack([X_skills, X_edu_encoded])
    y = df["career_label"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Save model and encoders
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(mlb, os.path.join("models", "mlb.pkl"))
    joblib.dump(edu_encoder, os.path.join("models", "edu_encoder.pkl"))

    # Evaluation
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)

    print("\n📊 Model Evaluation Metrics:")
    print(f"✅ Accuracy:  {acc:.4f}")
    print(f"✅ Precision: {precision:.4f}")
    print(f"✅ Recall:    {recall:.4f}")
    print("\n📃 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0))

def predict_career(skills, education):
    clf = joblib.load(MODEL_PATH)
    mlb = joblib.load(os.path.join("models", "mlb.pkl"))
    edu_encoder = joblib.load(os.path.join("models", "edu_encoder.pkl"))
    le = joblib.load(os.path.join("models", "label_encoder.pkl"))

    skill_input = mlb.transform([skills])
    edu_input = edu_encoder.transform([[education]])
    X = np.hstack([skill_input, edu_input])

    prediction = clf.predict(X)
    return le.inverse_transform(prediction)[0]

# Run training if file is executed directly
if __name__ == "__main__":
    train_model()

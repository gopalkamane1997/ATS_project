import os
import random
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# ---------------- CREATE SYNTHETIC DATASET ----------------
data = []

for _ in range(300):
    skills_match = random.randint(1, 15)
    ratio = skills_match / 15
    experience_match = random.choice([0, 1])
    education_match = random.choice([0, 1])
    keyword_overlap = random.uniform(0.1, 1.0)

    score = (
        ratio * 0.4 +
        experience_match * 0.2 +
        education_match * 0.1 +
        keyword_overlap * 0.3
    )
    label = 1 if score > 0.6 else 0

    data.append([skills_match, ratio, experience_match, education_match, keyword_overlap, label])

df = pd.DataFrame(data, columns=[
    "skills_match", "ratio", "experience", "education", "keyword_overlap", "label"
])

# ---------------- TRAIN ----------------
X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ---------------- EVALUATE ----------------
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))
print("F1 Score:", f1_score(y_test, preds))

# ---------------- SAVE ----------------
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")
print("Model saved to model/model.pkl")

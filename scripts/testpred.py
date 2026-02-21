# test_prediction.py
import joblib
import os

# --- Paths ---
MODEL_DIR = "models"
category_model = joblib.load(os.path.join(MODEL_DIR, "category_model.pkl"))
vectorizer = joblib.load(os.path.join(MODEL_DIR, "category_vectorizer.pkl"))
label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

print("✅ Models loaded successfully!\n")

def predict_department(complaint):
    """Predict which department the complaint belongs to"""
    if not complaint.strip():
        return "⚠️ Empty input."
    X = vectorizer.transform([complaint])
    pred = category_model.predict(X)[0]
    department = label_encoder.inverse_transform([pred])[0]
    # Confidence (probability)
    probs = category_model.predict_proba(X)[0]
    confidence = max(probs) * 100
    return department, confidence

# --- Simple demo loop ---
print("🧾 Complaint Classification Demo")
print("Type any complaint and press Enter (type 'exit' to quit)\n")

while True:
    complaint = input("Enter complaint: ").strip()
    if complaint.lower() == "exit":
        print("👋 Exiting...")
        break

    dept, conf = predict_department(complaint)
    print(f"→ Department: {dept}  (Confidence: {conf:.2f}%)")
    print("-" * 60)

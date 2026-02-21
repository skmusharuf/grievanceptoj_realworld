import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib
import os

df = pd.read_csv(r'C:\\Users\\musha\\Downloads\\grievance-system (fifthmain)\\finalgrievancesfortraining_transportonly.csv')

# Prepare data
descriptions = df['Description'].values
categories = df['Category'].values

label_encoder = LabelEncoder()
encoded_categories = label_encoder.fit_transform(categories)

category_vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
X_category = category_vectorizer.fit_transform(descriptions)

criticality_vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
X_criticality = criticality_vectorizer.fit_transform(descriptions)

print("Training Naive Bayes model for category classification...")
nb_model = MultinomialNB(alpha=1.0)
nb_model.fit(X_category, encoded_categories)
print(f"Naive Bayes trained! Categories: {list(label_encoder.classes_)}")

print("\nTraining Logistic Regression for criticality detection...")
critical_keywords = {
    "emergency", "fire", "accident", "danger", "hazard", "injury", "collapse",
    "flood", "explosion", "crime", "robbery", "death", "contamination",
    "sewage overflow", "power failure", "outage", "electric shock", "pipe burst",
    "flooding", "open defecation", "unsafe", "toxicity", "urgent repair",
    "collapse risk", "road accident", "injury risk", "disease outbreak","murder", "robbery", "assault", "fire", "violence", "accident", "death", "emergency",
    "threat", "harassment", "corruption", "fraud", "police", "bribery", "collapsed", "riot",
    "criminal", "hijack", "abuse", "molestation", "rape", "kidnap", "illegal", "scam"
}

# Create criticality labels based on keyword presence
y_critical = []
for desc in descriptions:
    desc_lower = desc.lower()
    is_critical = any(keyword in desc_lower for keyword in critical_keywords)
    y_critical.append(1 if is_critical else 0)

lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_criticality, y_critical)

critical_count = sum(y_critical)
non_critical_count = len(y_critical) - critical_count
print(f"Logistic Regression trained! Critical: {critical_count}, Non-Critical: {non_critical_count}")

os.makedirs('models', exist_ok=True)
joblib.dump(category_vectorizer, 'models/category_vectorizer.pkl')
joblib.dump(nb_model, 'models/category_model.pkl')
joblib.dump(criticality_vectorizer, 'models/criticality_vectorizer.pkl')
joblib.dump(lr_model, 'models/criticality_model.pkl')
joblib.dump(label_encoder, 'models/label_encoder.pkl')
joblib.dump(critical_keywords, 'models/critical_keywords.pkl')

print("\n✅ All models trained and saved successfully!")
print(f"   - Category Model (Naive Bayes): models/category_model.pkl")
print(f"   - Category Vectorizer: models/category_vectorizer.pkl")
print(f"   - Criticality Model (Logistic Regression): models/criticality_model.pkl")
print(f"   - Criticality Vectorizer: models/criticality_vectorizer.pkl")
print(f"   - Label Encoder: models/label_encoder.pkl")
print(f"   - Critical Keywords: models/critical_keywords.pkl")


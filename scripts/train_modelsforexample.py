
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

# ============================
# LOAD DATA
# ============================
df = pd.read_csv(r'C:\\Users\\musha\\Downloads\\grievance-system (fifthmain)\\final_realistic_grievances_balanced(vscode)_5000.csv')

# Prepare data
descriptions = df['Description'].values
categories = df['Category'].values

label_encoder = LabelEncoder()
encoded_categories = label_encoder.fit_transform(categories)

# ============================
# CATEGORY MODEL (Naive Bayes)
# ============================

# Split data into training and testing
X_train_desc, X_test_desc, y_train_cat, y_test_cat = train_test_split(
    descriptions, encoded_categories, test_size=0.3, random_state=42
)

# TF-IDF vectorization
category_vectorizer = TfidfVectorizer(max_features=6000, stop_words='english', ngram_range=(1, 2))
X_train_category = category_vectorizer.fit_transform(X_train_desc)
X_test_category = category_vectorizer.transform(X_test_desc)

print("Training Naive Bayes model for category classification...")
nb_model = MultinomialNB(alpha=1.0)
nb_model.fit(X_train_category, y_train_cat)
print(f"Naive Bayes trained! Categories: {list(label_encoder.classes_)}")

# Evaluate category model
y_pred_cat = nb_model.predict(X_test_category)
acc_cat = accuracy_score(y_test_cat, y_pred_cat)

print("\n==============================")
print(" CATEGORY MODEL EVALUATION")
print("==============================")
print(f"✅ Category Model Accuracy: {acc_cat*100:.2f}%\n")
print("Classification Report:")
print(classification_report(y_test_cat, y_pred_cat, target_names=label_encoder.classes_))
print("Confusion Matrix:")
print(confusion_matrix(y_test_cat, y_pred_cat))

# ============================
# CRITICALITY MODEL (Logistic Regression)
# ============================

# Define critical keywords
critical_keywords = {
    "emergency", "fire", "accident", "danger", "hazard", "injury", "collapse",
    "flood", "explosion", "crime", "robbery", "death", "contamination",
    "sewage overflow", "power failure", "outage", "electric shock", "pipe burst",
    "flooding", "open defecation", "unsafe", "toxicity", "urgent repair",
    "collapse risk", "road accident", "injury risk", "disease outbreak", "murder",
    "robbery", "assault", "violence", "threat", "harassment", "corruption", 
    "fraud", "police", "bribery", "collapsed", "riot", "criminal", "hijack", 
    "abuse", "molestation", "rape", "kidnap", "illegal", "scam"
}

# Create labels based on keyword presence
y_critical = []
for desc in descriptions:
    desc_lower = desc.lower()
    is_critical = any(keyword in desc_lower for keyword in critical_keywords)
    y_critical.append(1 if is_critical else 0)

# Split for criticality
X_train_crit, X_test_crit, y_train_crit, y_test_crit = train_test_split(
    descriptions, y_critical, test_size=0.2, random_state=42
)

# TF-IDF vectorization for criticality
criticality_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
X_train_criticality = criticality_vectorizer.fit_transform(X_train_crit)
X_test_criticality = criticality_vectorizer.transform(X_test_crit)

print("\nTraining Logistic Regression for criticality detection...")
lr_model = LogisticRegression(max_iter=100, random_state=42)
lr_model.fit(X_train_criticality, y_train_crit)

# Evaluate criticality model
y_pred_crit = lr_model.predict(X_test_criticality)
acc_crit = accuracy_score(y_test_crit, y_pred_crit)

critical_count = sum(y_critical)
non_critical_count = len(y_critical) - critical_count
print(f"Logistic Regression trained! Critical: {critical_count}, Non-Critical: {non_critical_count}")

print("\n==============================")
print(" CRITICALITY MODEL EVALUATION")
print("==============================")
print(f"✅ Criticality Model Accuracy: {acc_crit*100:.2f}%\n")
print("Classification Report:")
print(classification_report(y_test_crit, y_pred_crit, target_names=['Non-Critical', 'Critical']))
print("Confusion Matrix:")
print(confusion_matrix(y_test_crit, y_pred_crit))

# ============================
# SAVE MODELS
# ============================
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

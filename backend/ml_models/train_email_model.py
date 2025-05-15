import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Correct path to the dataset (go up one level then into datasets)
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'email_dataset.csv')

# Load dataset
try:
    df = pd.read_csv(dataset_path)
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print(f"Error: Could not find dataset at {dataset_path}")
    print("Current working directory:", os.getcwd())
    print("Please ensure:")
    print("1. The file 'email_dataset.csv' exists in backend/datasets/")
    print("2. You're running the script from the correct directory")
    exit(1)

# Rest of your code remains the same...
X = df['email_content']
y = df['label']

# Feature extraction
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3,5))
X_transformed = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_transformed, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print(f"Training Accuracy: {model.score(X_train, y_train):.2f}")
print(f"Test Accuracy: {model.score(X_test, y_test):.2f}")

# Save models
models_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(models_dir, exist_ok=True)

model_path = os.path.join(models_dir, 'email_model.pkl')
vectorizer_path = os.path.join(models_dir, 'email_vectorizer.pkl')

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print(f"Models saved to {models_dir}")
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from preprocess import load_and_preprocess

def train_and_save_model(dataset_name, model_filename):
    print(f"Training models for {dataset_name}...")
    try:
        X_train, X_test, y_train, y_test, scaler, feature_names = load_and_preprocess(dataset_name)
    except Exception as e:
        print(f"Error loading {dataset_name}: {e}")
        return
        
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(probability=True, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print(f"  - {name} Accuracy: {score:.4f}")
        
        if score > best_score:
            best_score = score
            best_model = model
            best_name = name
            
    print(f"  => Best Model selected for {dataset_name}: {best_name} (Accuracy: {best_score:.4f})")
    
    os.makedirs('models', exist_ok=True)
    # Save the model, scaler, and expected feature names
    joblib.dump({
        'model': best_model,
        'scaler': scaler,
        'features': feature_names
    }, f'models/{model_filename}')
    print(f"Saved {model_filename}\n")

if __name__ == '__main__':
    train_and_save_model('heart', 'heart_model.pkl')
    train_and_save_model('diabetes', 'diabetes_model.pkl')
    train_and_save_model('breast_cancer', 'cancer_model.pkl')
    print("All models trained and saved.")

import joblib
import pandas as pd
import numpy as np

def predict_disease(model_name, input_data):
    """
    model_name: 'heart', 'diabetes', or 'cancer'
    input_data: dictionary of feature values from the frontend
    """
    model_files = {
        'heart': 'models/heart_model.pkl',
        'diabetes': 'models/diabetes_model.pkl',
        'cancer': 'models/cancer_model.pkl'
    }
    
    if model_name not in model_files:
        raise ValueError("Invalid model name")
        
    try:
        data = joblib.load(model_files[model_name])
    except FileNotFoundError:
        raise FileNotFoundError(f"Model for {model_name} not found. Please train models first.")
        
    model = data['model']
    scaler = data['scaler']
    expected_features = data['features']
    
    # Mapping frontend names to backend names where they differ
    feature_mapping = {
        # Diabetes
        'Pregnancies': 'preg', 'Glucose': 'plas', 'BloodPressure': 'pres', 
        'SkinThickness': 'skin', 'Insulin': 'insu', 'BMI': 'mass', 
        'DiabetesPedigreeFunction': 'pedi', 'Age': 'age',
        
        # Heart
        'age': 'age', 'sex': 'sex', 'cp': 'chest', 
        'trestbps': 'resting_blood_pressure', 'chol': 'serum_cholestoral', 
        'thalach': 'maximum_heart_rate_achieved'
    }
    
    # Create an array initialized with the mean values of the training data
    # This ensures that any missing features have neutral impact on the prediction
    input_array = np.copy(scaler.mean_)
    
    for key, val in input_data.items():
        # Get the corresponding backend feature name
        backend_name = feature_mapping.get(key, key)
        
        if backend_name in expected_features:
            idx = expected_features.index(backend_name)
            input_array[idx] = float(val)
            
    # Scale the input array
    # transform expects 2D array
    input_scaled = scaler.transform([input_array])
    
    # Predict
    prediction = model.predict(input_scaled)[0]
    
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(input_scaled)[0].max()
    elif hasattr(model, "decision_function"):
        # For some models like linear SVM without probability=True
        dec = model.decision_function(input_scaled)[0]
        # rough sigmoid approximation
        probability = 1 / (1 + np.exp(-dec))
        if prediction == 0:
            probability = 1 - probability
    else:
        probability = 1.0
    
    # Convert numpy types to native Python types for JSON serialization
    return int(prediction), float(probability)

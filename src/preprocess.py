import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def load_and_preprocess(dataset_name):
    """
    Loads dataset, handles missing values, splits into train/test, and scales features.
    """
    data_path = f'data/{dataset_name}.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset {data_path} not found.")
        
    df = pd.read_csv(data_path)
    
    # Handle different target column names
    target_col = None
    if dataset_name == 'breast_cancer':
        target_col = 'target'
    elif dataset_name == 'diabetes':
        target_col = 'class' if 'class' in df.columns else 'Outcome'
    elif dataset_name == 'heart':
        target_col = 'class' if 'class' in df.columns else 'target'
        
    if target_col not in df.columns:
        raise ValueError(f"Target column not found for {dataset_name}. Available columns: {df.columns}")
    
    # Basic missing value handling
    df = df.dropna()
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Robust target encoding using LabelEncoder
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, list(X.columns)

if __name__ == '__main__':
    print("Preprocessing module ready.")

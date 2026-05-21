import os
import pandas as pd
from sklearn.datasets import load_breast_cancer, fetch_openml

def download_datasets():
    os.makedirs('data', exist_ok=True)
    
    print("Downloading Breast Cancer dataset...")
    bc = load_breast_cancer(as_frame=True)
    bc_df = bc.frame
    bc_df.to_csv('data/breast_cancer.csv', index=False)
    print("Saved breast_cancer.csv")
    
    print("Downloading Diabetes dataset (Pima Indians)...")
    try:
        diabetes = fetch_openml(name='diabetes', version=1, as_frame=True, parser='auto')
        diabetes_df = diabetes.frame
        diabetes_df.to_csv('data/diabetes.csv', index=False)
        print("Saved diabetes.csv")
    except Exception as e:
        print(f"Failed to fetch diabetes from OpenML: {e}")
        # fallback url
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
        df = pd.read_csv(url, names=names)
        df.to_csv('data/diabetes.csv', index=False)
        print("Saved diabetes.csv from fallback URL")

    print("Downloading Heart Disease dataset...")
    try:
        heart = fetch_openml(name='heart-statlog', version=1, as_frame=True, parser='auto')
        heart_df = heart.frame
        heart_df.to_csv('data/heart.csv', index=False)
        print("Saved heart.csv")
    except Exception as e:
        print(f"Failed to fetch heart from OpenML: {e}")
        # fallback url
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/heart.csv" # not standard, but let's try
        try:
            df = pd.read_csv(url)
            df.to_csv('data/heart.csv', index=False)
            print("Saved heart.csv from fallback URL")
        except:
            print("Downloading from standard UCI URL...")
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
            names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
            df = pd.read_csv(url, names=names, na_values='?')
            df.to_csv('data/heart.csv', index=False)
            print("Saved heart.csv from UCI URL")

if __name__ == '__main__':
    download_datasets()

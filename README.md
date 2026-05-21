# Multi-Disease Prediction System (HealthLens)

A professional Machine Learning healthcare dashboard that predicts the likelihood of Heart Disease, Diabetes, and Breast Cancer based on user vitals and cytological features.

## Project Structure
- `data/`: Contains the datasets used for training (Heart Disease, Pima Indians Diabetes, Breast Cancer).
- `models/`: Saved `.pkl` models using RandomForest.
- `src/`: Machine learning pipeline scripts (`preprocess.py`, `train.py`, `predict.py`).
- `notebooks/`: Jupyter notebooks for EDA and experimentation.
- `app.py`: Flask application to serve the dashboard and prediction APIs.
- `templates/` & `static/`: Frontend web files (HTML, CSS, JS).

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Datasets**
   ```bash
   python fetch_data.py
   ```

3. **Train Models**
   ```bash
   python src/train.py
   ```

4. **Run Web Application**
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in your browser.

## Tech Stack
- **Backend:** Flask, Python
- **Machine Learning:** Scikit-Learn, Pandas
- **Frontend:** Vanilla HTML/CSS/JS (Glassmorphism design, Modern Typography)

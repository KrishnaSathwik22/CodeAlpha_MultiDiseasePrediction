from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os

# Add src to path so we can import predict
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from predict import predict_disease

app = Flask(__name__)
app.config['SECRET_KEY'] = 'healthlens-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # Landing page
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please log in.', 'danger')
            return redirect(url_for('signup'))
            
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/predict/<disease>', methods=['POST'])
def predict(disease):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
            
        prediction, probability = predict_disease(disease, data)
        
        # Standardize prediction so 1 ALWAYS means High Risk / Danger for the frontend
        is_high_risk = False
        
        if disease == 'heart':
            is_high_risk = (prediction == 1)
            result_text = "High Risk of Heart Disease" if is_high_risk else "Low Risk of Heart Disease"
        elif disease == 'diabetes':
            is_high_risk = (prediction == 1)
            result_text = "High Risk of Diabetes" if is_high_risk else "Low Risk of Diabetes"
        elif disease == 'cancer':
            # In sklearn breast cancer dataset: 0 is Malignant (High Risk), 1 is Benign (Low Risk)
            is_high_risk = (prediction == 0)
            result_text = "Malignant (High Risk)" if is_high_risk else "Benign (Low Risk)"
        else:
            result_text = "Unknown"
            
        return jsonify({
            'prediction': 1 if is_high_risk else 0,
            'probability': float(probability),
            'result_text': result_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

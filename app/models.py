import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.feature_selection import SelectKBest, f_regression
import joblib

# ✅ IMPORTANT FIX: use db from app (DO NOT create new one)
from app.extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    predictions = db.relationship('Prediction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    features = db.Column(db.Text, nullable=False)  # JSON string
    predicted_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


def load_dataset():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'FINAL_USO.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    feature_cols = [
        'SP_open', 'SP_high', 'SP_low', 'SP_close',
        'DJ_open', 'DJ_close', 'EU_Price',
        'USB_Price', 'USO_Close', 'GDX_Close'
    ]
    
    df = df[feature_cols + ['Close']].dropna()
    return df


def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'gold_model.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'scaler.pkl')
    features_path = os.path.join(os.path.dirname(__file__), '..', 'features.pkl')
    
    try:
        print("Loading pre-trained model, scaler, and features...")
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        selected_features = joblib.load(features_path)

        print(f"✅ Loaded model with features: {selected_features}")
        return model, scaler, selected_features

    except FileNotFoundError as e:
        print(f"⚠️ Missing files: {e}. Training new model...")
        return load_or_train_model_and_save()


def load_or_train_model_and_save():
    df = load_dataset()
    X = df.drop('Close', axis=1)
    y = df['Close']
    
    # Feature selection
    selector = SelectKBest(score_func=f_regression, k=10)
    X_selected = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()].tolist()
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, y, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    print(f'✅ Model trained (R²: {r2:.4f}) with features: {selected_features}')
    
    # Save model
    base_path = os.path.join(os.path.dirname(__file__), '..')
    joblib.dump(model, os.path.join(base_path, 'gold_model.pkl'))
    joblib.dump(scaler, os.path.join(base_path, 'scaler.pkl'))
    joblib.dump(selected_features, os.path.join(base_path, 'features.pkl'))
    
    return model, scaler, selected_features
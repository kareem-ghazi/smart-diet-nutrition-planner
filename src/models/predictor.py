import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import streamlit as st
import os

class CaloriePredictor:
    """
    Robust MLP-based predictor for daily caloric needs.
    Handles NaNs and scales target to prevent numerical instability.
    """
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.target_scaler = StandardScaler()
        self.test_samples = []
        self._initialize()

    def _initialize(self):
        print("\n=== Initializing Robust Calorie Predictor Training (Dataset V2) ===")
        data_path = "data/calorie_intake_dataset.csv"
        if not os.path.exists(data_path):
            st.error("Training data not found!")
            return

        df = pd.read_csv(data_path)
        
        # Target: Required_Daily_Calories
        target_col = "Required_Daily_Calories"
        
        # Immediate fix: Drop rows where target is NaN before anything else
        df = df.dropna(subset=[target_col])
        
        # Features
        X = df.drop(columns=["ID", target_col])
        y = df[[target_col]] # Use double brackets for scaler compatibility

        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # Reserve 10 rows for UI presets (ensure they are clean)
        self.test_samples = df.iloc[:10].copy()
        
        X_working = X.iloc[10:]
        y_working = y.iloc[10:]

        # 20% Test Set
        X_train, X_test, y_train, y_test = train_test_split(
            X_working, y_working, test_size=0.05, random_state=42
        )

        # Robust Preprocessing pipeline
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ])

        # Prepare Features
        X_train_proc = self.preprocessor.fit_transform(X_train)
        X_test_proc = self.preprocessor.transform(X_test)
        
        # Scale Target (Prevents Exploding Gradients/NaNs)
        y_train_scaled = self.target_scaler.fit_transform(y_train)
        y_test_scaled = self.target_scaler.transform(y_test)
        
        input_dim = X_train_proc.shape[1]

        # Build model
        self.model = self._build_model(input_dim)
        
        print(f"Training on {len(X_train)} samples...")
        
        # Early stopping to prevent overfitting if needed
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

        self.model.fit(
            X_train_proc, y_train_scaled, 
            epochs=50, 
            batch_size=32, 
            validation_data=(X_test_proc, y_test_scaled),
            callbacks=[early_stop],
            verbose=1
        )

        # Evaluation
        loss, mae = self.model.evaluate(X_test_proc, y_test_scaled, verbose=0)
        # Convert MAE back to real calorie units for reporting
        real_mae = mae * np.sqrt(self.target_scaler.var_[0])
        
        print("\n=== Model Training Complete ===")
        print(f"Validation Loss (MSE): {loss:.4f}")
        print(f"Validation MAE (Real Units): {real_mae:.4f} calories")
        print("===============================\n")

    def _build_model(self, input_dim):
        model = models.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(), # Improves stability
            layers.Dropout(0.1),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='linear')
        ])
        # Use a slightly lower learning rate for stability
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        return model

    def predict(self, user_profile_dict):
        if self.model is None or self.preprocessor is None:
            return 2000.0

        input_df = pd.DataFrame([user_profile_dict])
        input_processed = self.preprocessor.transform(input_df)
        prediction_scaled = self.model.predict(input_processed, verbose=0)
        
        # Inverse transform to get actual calories
        prediction_real = self.target_scaler.inverse_transform(prediction_scaled)
        
        return round(float(prediction_real[0][0]), 2)

    def get_test_samples(self):
        return self.test_samples

# Utility to wrap transformers in a pipeline for predictor.py internal use
from sklearn.pipeline import Pipeline

@st.cache_resource
def get_predictor():
    return CaloriePredictor()

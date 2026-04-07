import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import streamlit as st
import os

class CaloriePredictor:
    """
    Improved MLP-based predictor for daily caloric needs.
    Includes target scaling, better architecture, and early stopping.
    """
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.target_scaler = StandardScaler()
        self.test_samples = []
        self._initialize()

    def _initialize(self):
        print("\n=== Initializing Calorie Predictor Training ===")
        data_path = "data/calorie_intake_dataset.csv"
        if not os.path.exists(data_path):
            st.error("Training data not found!")
            return

        df = pd.read_csv(data_path)
        
        # Target
        target = "Daily_Caloric_Intake"
        
        # Features
        X = df.drop(columns=["Patient_ID", target])
        y = df[target]

        # Categorical and Numeric identification
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # Reserve 10 rows for the "Load Patient Profile" UI feature
        self.test_samples = df.iloc[:10].copy()
        
        # Training/Evaluation data (everything else)
        X_working = X.iloc[10:]
        y_working = y.iloc[10:]

        # 20% Test Set for Accuracy Validation
        X_train, X_test, y_train, y_test = train_test_split(
            X_working, y_working, test_size=0.20, random_state=42
        )

        # Preprocessing pipeline
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
            ])

        # Prepare feature data
        X_train_proc = self.preprocessor.fit_transform(X_train)
        X_test_proc = self.preprocessor.transform(X_test)
        
        # FIX 1: Scale the target variable to stabilize training gradients
        self.target_scaler = StandardScaler()
        y_train_scaled = self.target_scaler.fit_transform(y_train.values.reshape(-1, 1))
        y_test_scaled = self.target_scaler.transform(y_test.values.reshape(-1, 1))

        input_dim = X_train_proc.shape[1]

        # Build improved model architecture
        self.model = self._build_model(input_dim)
        
        print(f"Training on {len(X_train)} samples, validating on {len(X_test)} samples...")
        
        # FIX 2: Early stopping to prevent overfitting
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss', 
            patience=50, 
            restore_best_weights=True
        )

        # Train model with progress output
        history = self.model.fit(
            X_train_proc, y_train_scaled, 
            epochs=150,
            batch_size=32,
            validation_data=(X_test_proc, y_test_scaled),
            callbacks=[early_stopping],
            verbose=1 # Output progress to console
        )

        # Evaluate on the scaled validation targets
        scaled_loss, scaled_mae = self.model.evaluate(X_test_proc, y_test_scaled, verbose=0)
        
        # Inverse transform the predictions for accurate metric calculation
        y_pred_scaled = self.model.predict(X_test_proc, verbose=0)
        y_pred = self.target_scaler.inverse_transform(y_pred_scaled)
        
        # Calculate Real-World metrics
        real_mae = np.mean(np.abs(y_test.values.reshape(-1, 1) - y_pred))
        
        print("\n=== Model Training Complete ===")
        print(f"Final Validation MSE (Scaled Loss): {scaled_loss:.4f}")
        print(f"Final Validation MAE: {real_mae:.4f} calories")
        
        # Calculate R-squared for "accuracy" representation
        y_bar = np.mean(y_test)
        ss_res = np.sum((y_test.values.reshape(-1, 1) - y_pred)**2)
        ss_tot = np.sum((y_test - y_bar)**2)
        r2 = 1 - (ss_res / ss_tot)
        print(f"Regression Accuracy (R² Score): {r2:.4f}")
        print("===============================\n")

    def _build_model(self, input_dim):
        # FIX 3: Expanded network with Dropout for robust representation
        model = models.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2), # Dropout to prevent overfitting
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='linear')
        ])
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        return model

    def predict(self, user_profile_dict):
        if self.model is None or self.preprocessor is None:
            return 2000.0

        # Transform inputs
        input_df = pd.DataFrame([user_profile_dict])
        input_processed = self.preprocessor.transform(input_df)
        
        # Make scaled prediction
        prediction_scaled = self.model.predict(input_processed, verbose=0)
        
        # FIX 4: Inverse transform the prediction back to actual calories
        prediction = self.target_scaler.inverse_transform(prediction_scaled)
        
        return round(float(prediction[0][0]), 2)

    def get_test_samples(self):
        return self.test_samples

@st.cache_resource
def get_predictor():
    return CaloriePredictor()
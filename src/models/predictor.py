import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import streamlit as st
import os

class CaloriePredictor:
    """
    MLP-based predictor for daily caloric needs using all features from the dataset.
    """
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.test_samples = []
        self._initialize()

    def _initialize(self):
        # Load dataset
        data_path = "data/calorie_intake_dataset.csv"
        if not os.path.exists(data_path):
            st.error("Training data not found!")
            return

        df = pd.read_csv(data_path)
        
        # Target
        target = "Daily_Caloric_Intake"
        
        # Features
        # Drop Patient_ID and Target
        X = df.drop(columns=["Patient_ID", target])
        y = df[target]

        # Categorical and Numeric column identification
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # Put aside 10 test samples for the "Load Patient Profile" option
        # We take the first 10 rows as our "special" test set
        self.test_samples = df.iloc[:10].copy()
        
        # Training data (everything else)
        X_train_full = X.iloc[10:]
        y_train_full = y.iloc[10:]

        # Preprocessing pipeline
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
            ])

        # Prepare data
        X_processed = self.preprocessor.fit_transform(X_train_full)
        input_dim = X_processed.shape[1]

        # Build model
        self.model = self._build_model(input_dim)
        
        # Train model (for prototype, we do a very quick fit)
        # In a real app, you'd load pre-trained weights
        self.model.fit(X_processed, y_train_full, epochs=10, batch_size=32, verbose=0)

    def _build_model(self, input_dim):
        model = models.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def predict(self, user_profile_dict):
        """
        Predicts caloric needs based on a full profile dictionary.
        """
        if self.model is None or self.preprocessor is None:
            return 2000.0 # Fallback

        # Convert dict to DataFrame
        input_df = pd.DataFrame([user_profile_dict])
        
        # Preprocess
        input_processed = self.preprocessor.transform(input_df)
        
        # Predict
        prediction = self.model.predict(input_processed, verbose=0)
        
        return round(float(prediction[0][0]), 2)

    def get_test_samples(self):
        return self.test_samples

@st.cache_resource
def get_predictor():
    return CaloriePredictor()

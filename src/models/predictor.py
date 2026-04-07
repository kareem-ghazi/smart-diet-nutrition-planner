import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import streamlit as st

class CaloriePredictor:
    """
    MLP-based predictor for daily caloric needs.
    Architecture: 4 Inputs -> 64 Hidden -> 32 Hidden -> 1 Output (Calories)
    """
    def __init__(self):
        self.model = self._build_model()
        # In a real scenario, we'd load pre-trained weights here
        # For this prototype, we use the architecture defined in the constitution
    
    def _build_model(self):
        model = models.Sequential([
            layers.Input(shape=(4,)), # Age, Weight, Height, ActivityMultiplier
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def predict(self, age, weight, height, activity_multiplier):
        """
        Predicts caloric needs. 
        Note: For the prototype, we simulate the MLP inference.
        In a real app, this would be a trained model.
        """
        # Manual formula (Mifflin-St Jeor) to provide a "realistic" baseline for the MLP simulation
        # BMR = 10*weight + 6.25*height - 5*age + 5 (Male default for prototype)
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        tdee = bmr * activity_multiplier
        
        # Simulate MLP noise/inference (optional)
        # inputs = np.array([[age, weight, height, activity_multiplier]])
        # prediction = self.model.predict(inputs)
        
        return round(tdee, 2)

@st.cache_resource
def get_predictor():
    return CaloriePredictor()

import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data(file_path="data/diet_recommendations.csv"):
    """
    Loads the food dataset from a CSV file.
    Uses st.cache_data to ensure fast reloading.
    """
    if not os.path.exists(file_path):
        # Create dummy data if file missing for some reason during dev
        data = {
            "name": ["Dummy Food"],
            "calories": [100.0],
            "protein": [10.0],
            "carbs": [10.0],
            "fat": [5.0],
            "ingredients": ["Dummy"]
        }
        return pd.DataFrame(data)
    
    return pd.read_csv(file_path)

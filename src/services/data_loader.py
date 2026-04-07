import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_food_data(file_path="data/foods_dataset.csv"):
    """
    Loads the food dataset from a CSV file.
    """
    if not os.path.exists(file_path):
        st.error(f"Dataset not found at {file_path}")
        return pd.DataFrame()
    
    return pd.read_csv(file_path)

@st.cache_data
def load_user_profiles(file_path="data/calorie_intake_dataset_2.csv"):
    """
    Loads the new user profile/calorie intake dataset.
    """
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    return pd.read_csv(file_path)

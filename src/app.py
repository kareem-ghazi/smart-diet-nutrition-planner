import streamlit as st
import pandas as pd
import numpy as np
from services.data_loader import load_food_data
from models.predictor import get_predictor
from models.optimizer import MealOptimizer
from models.filter import AllergyFilter

def add_custom_css():
    st.markdown("""
    <style>
    .main {
        background-color: #000000;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #366bff;
    }
    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }
    .meal-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1e3a8a;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def safe_index(options, value, default=0):
    if pd.isna(value) or value is None:
        return default
    val_str = str(value).strip()
    try:
        return options.index(val_str)
    except (ValueError, KeyError):
        for i, opt in enumerate(options):
            if opt.lower() == val_str.lower():
                return i
        return default

def main():
    st.set_page_config(page_title="Smart Diet Nutrition Planner", layout="wide")
    add_custom_css()
    
    st.title("🍎 Smart Diet Nutrition Planner")
    st.markdown("A smart approach to personalized nutrition")
    st.markdown("---")
    
    # 1. Initialize Predictor & Get Test Samples
    predictor = get_predictor()
    test_samples_df = predictor.get_test_samples()
    
    # Sidebar: User Inputs
    st.sidebar.header("User Profile")
    
    if isinstance(test_samples_df, list):
        test_samples_df = pd.DataFrame(test_samples_df)
    
    # Option to load from dataset (using the 10 test samples)
    st.sidebar.subheader("Presets (Test Samples)")
    selected_id = st.sidebar.selectbox(
        "Load ID Profile", 
        ["Manual"] + test_samples_df['ID'].astype(str).tolist() if not test_samples_df.empty else ["Manual"]
    )
    
    defaults = {}
    if selected_id != "Manual" and not test_samples_df.empty:
        patient_data = test_samples_df[test_samples_df['ID'].astype(str) == selected_id].iloc[0]
        defaults = patient_data.to_dict()
    
    # Profile Fields (Dataset V2: Age, Gender, Working_Type, Sleep_Hours, Height_m)
    age = st.sidebar.number_input("Age (years)", 1, 120, int(float(defaults.get('Age', 25))))
    
    gender_opts = ["Male", "Female"]
    gender = st.sidebar.selectbox("Gender", gender_opts, index=safe_index(gender_opts, defaults.get('Gender')))
    
    working_type_opts = ["Unemployed", "Desk Job", "Freelancer", "Healthcare", "Service Industry", "Education", "Other"]
    working_type = st.sidebar.selectbox("Working Type", working_type_opts, index=safe_index(working_type_opts, defaults.get('Working_Type', 'Desk Job')))
    
    sleep_hours = st.sidebar.slider("Sleep Hours", 0.0, 24.0, float(defaults.get('Sleep_Hours', 7.0)))
    height_m = st.sidebar.number_input("Height (meters)", 0.5, 2.5, float(defaults.get('Height_m', 1.75)))
    
    # Preferences & Restrictions (Still needed for KBS part)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Dietary Filters")
    all_allergies = ["None", "Peanuts", "Gluten", "Dairy", "Eggs", "Soy", "Fish"]
    selected_allergies = st.sidebar.multiselect("Allergies / Restrictions", all_allergies)
    
    # Construct the dictionary for prediction
    user_profile_dict = {
        "Age": age,
        "Gender": gender,
        "Working_Type": working_type,
        "Sleep_Hours": sleep_hours,
        "Height_m": height_m
    }

    st.sidebar.markdown("---")
    
    # 2. NN (Prediction)
    predicted_target = predictor.predict(user_profile_dict)
    
    # If loading from dataset, show original intake too
    dataset_intake = float(defaults.get('Required_Daily_Calories', 0))
    
    # Main Page Layout
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.header("1. Calculated Needs (NN)")
        st.metric("Predicted Daily Target", f"{predicted_target} kcal")
        if dataset_intake > 0:
            st.metric("Dataset Original Intake", f"{dataset_intake:.2f} kcal", delta=f"{predicted_target - dataset_intake:.2f}")
        
        with st.expander("Detailed Profile Summary"):
            st.write(f"**Work**: {working_type}")
            st.write(f"**Sleep**: {sleep_hours} hours")
            st.write(f"**Height**: {height_m} m")
    
    with col2:
        st.header("2. Filtered Menu (KBS)")
        raw_food_data = load_food_data()
        allergy_filter = AllergyFilter()
        
        filtered_menu = allergy_filter.filter_menu(raw_food_data, selected_allergies)
        
        st.dataframe(filtered_menu[['Food_Item', 'Category', 'Calories (kcal)', 'Meal_Type']], 
                     use_container_width=True, hide_index=True)
        st.success(f"Safety Filter: {len(filtered_menu)} items available.")
    
    st.markdown("---")
    
    # 3. OT (Selection)
    st.header("3. Optimized Daily Plan (OT)")
    optimizer = MealOptimizer()
    plan = optimizer.select_daily_plan(filtered_menu, predicted_target)
    
    if plan:
        total_calories = 0
        cols = st.columns(3)
        
        meal_names = ["Breakfast", "Lunch", "Dinner"]
        for i, meal_name in enumerate(meal_names):
            with cols[i]:
                st.subheader(f"🍴 {meal_name}")
                meal_df = plan.get(meal_name, pd.DataFrame())
                
                if isinstance(meal_df, list):
                    meal_df = pd.DataFrame(meal_df)
                
                if not meal_df.empty:
                    for _, row in meal_df.iterrows():
                        st.markdown(f"""
                        <div class='meal-card'>
                            <strong>{row['Food_Item']}</strong><br/>
                            <small>{row['Category']}</small><br/>
                            {row['Calories (kcal)']} kcal | P: {row['Protein (g)']}g
                        </div>
                        """, unsafe_allow_html=True)
                    meal_cal = meal_df['Calories (kcal)'].sum()
                    st.write(f"**Meal Total**: {meal_cal:.2f} kcal")
                    total_calories += meal_cal
                else:
                    st.warning("No items selected.")
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Daily Calories", f"{total_calories:.2f} kcal")
        with c2:
            st.metric("Daily Target", f"{predicted_target} kcal")
        with c3:
            diff = total_calories - predicted_target
            st.metric("Difference", f"{diff:.2f} kcal", delta=f"{diff:.2f}")
    else:
        st.warning("No optimized plan could be generated.")

if __name__ == "__main__":
    main()

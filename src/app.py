import streamlit as st
import pandas as pd
from services.data_loader import load_data
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
        background-color: #000000;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #1e3a8a;
    }
    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Smart Diet Nutrition Planner", layout="wide")
    add_custom_css()
    
    st.title("🍎 Smart Diet Nutrition Planner")
    st.markdown("A Neuro-Symbolic Approach to Personalized Nutrition")
    st.markdown("---")
    
    # Sidebar: User Inputs
    st.sidebar.header("User Profile")
    
    age = st.sidebar.number_input("Age (years)", min_value=1, max_value=120, value=25)
    weight = st.sidebar.number_input("Weight (kg)", min_value=20.0, max_value=500.0, value=70.0)
    height = st.sidebar.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=175.0)
    
    activity_levels = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly Active (light exercise/sports 1-3 days/week)": 1.375,
        "Moderately Active (moderate exercise/sports 3-5 days/week)": 1.55,
        "Very Active (hard exercise/sports 6-7 days/week)": 1.725,
        "Extra Active (very hard exercise/sports & physical job)": 1.9
    }
    
    activity_level = st.sidebar.selectbox(
        "Activity Level",
        options=list(activity_levels.keys())
    )
    
    if (activity_level != None):
        activity_multiplier = activity_levels[activity_level]
    
    # Sidebar: Allergy Selection (US2)
    allergies = st.sidebar.multiselect(
        "Select Allergies",
        options=["Peanuts", "Dairy", "Gluten", "Soy", "Eggs", "Fish", "Almonds", "Salmon"]
    )
    
    # Validation / Profile Summary
    if age <= 0 or weight <= 0 or height <= 0:
        st.sidebar.error("Please enter valid positive values for age, weight, and height.")
    
    # 1. NN (Prediction) - Neuro Part
    predictor = get_predictor()
    calorie_target = predictor.predict(age, weight, height, activity_multiplier)
    
    # Main Page Layout
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.header("1. Calculated Needs (NN)")
        st.metric("Predicted Daily Caloric Needs", f"{calorie_target} kcal")
        st.info("The MLP model has analyzed your profile to determine your target calories.")
    
    with col2:
        st.header("2. Filtered Menu (KBS)")
        # 2. KBS (Filter) - Symbolic Part
        raw_food_data = load_data()
        allergy_filter = AllergyFilter()
        filtered_menu = allergy_filter.filter_menu(raw_food_data, allergies)
        
        st.dataframe(filtered_menu, use_container_width=True, hide_index=True)
        st.success(f"Safety Filter Active: Showing {len(filtered_menu)} validated items.")
    
    st.markdown("---")
    
    # 3. OT (Selection) - Optimization Theory
    st.header("3. Optimized Plan (OT)")
    optimizer = MealOptimizer()
    plan_df = optimizer.select_meals(filtered_menu, calorie_target)
    
    if not plan_df.empty:
        st.dataframe(plan_df, use_container_width=True, hide_index=True)
        total_plan_calories = plan_df['calories'].sum()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Plan Calories", f"{total_plan_calories:.2f} kcal")
        with c2:
            st.metric("Target Calories", f"{calorie_target} kcal")
        with c3:
            diff = total_plan_calories - calorie_target
            color = "normal" if abs(diff) < 100 else "inverse"
            st.metric("Difference", f"{diff:.2f} kcal", delta=f"{diff:.2f}", delta_color=color)
    else:
        st.warning("No optimized plan could be generated for the given targets and filters.")

if __name__ == "__main__":
    main()

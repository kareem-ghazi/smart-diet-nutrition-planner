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
        color: #1e3a8a;
    }
    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }
    .meal-card {
        background-color: #000000;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1e3a8a;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def safe_index(options, value, default=0):
    """
    Safely finds the index of a value in a list of options.
    Handles NaN and missing values by returning the default index.
    """
    if pd.isna(value) or value is None:
        return default
    
    val_str = str(value).strip()
    try:
        return options.index(val_str)
    except (ValueError, KeyError):
        # If the exact value isn't found, try to find a partial match or return default
        for i, opt in enumerate(options):
            if opt.lower() == val_str.lower():
                return i
        return default

def main():
    st.set_page_config(page_title="Smart Diet Nutrition Planner", layout="wide")
    add_custom_css()
    
    st.title("🍎 Smart Diet Nutrition Planner")
    st.markdown("A Neuro-Symbolic Approach to Personalized Nutrition")
    st.markdown("---")
    
    # 1. Initialize Predictor & Get Test Samples
    predictor = get_predictor()
    test_samples_df = predictor.get_test_samples()
    
    if isinstance(test_samples_df, list):
        test_samples_df = pd.DataFrame(test_samples_df)
    
    # Sidebar: User Inputs
    st.sidebar.header("User Profile")
    
    # Option to load from dataset (using the 10 test samples)
    st.sidebar.subheader("Presets (Test Samples)")
    selected_patient = st.sidebar.selectbox(
        "Load Patient Profile", 
        ["Manual"] + test_samples_df['Patient_ID'].tolist() if not test_samples_df.empty else ["Manual"]
    )
    
    defaults = {}
    if selected_patient != "Manual" and not test_samples_df.empty:
        patient_data = test_samples_df[test_samples_df['Patient_ID'] == selected_patient].iloc[0]
        defaults = patient_data.to_dict()
    
    # Profile Fields (all features from CSV)
    age = st.sidebar.number_input("Age (years)", 1, 120, int(defaults.get('Age', 25)))
    
    gender_opts = ["Male", "Female"]
    gender = st.sidebar.selectbox("Gender", gender_opts, index=safe_index(gender_opts, defaults.get('Gender')))
    
    weight = st.sidebar.number_input("Weight (kg)", 20.0, 500.0, float(defaults.get('Weight_kg', 70.0)))
    height = st.sidebar.number_input("Height (cm)", 50.0, 250.0, float(defaults.get('Height_cm', 175.0)))
    
    # Calculate/Use BMI
    bmi = weight / ((height/100) ** 2)
    st.sidebar.info(f"Calculated BMI: {bmi:.2f}")
    
    disease_opts = ["None", "Obesity", "Diabetes", "Hypertension"]
    disease_type = st.sidebar.selectbox("Disease Type", disease_opts, 
                                       index=safe_index(disease_opts, defaults.get('Disease_Type', 'None')))
    
    severity_opts = ["Mild", "Moderate", "Severe"]
    severity = st.sidebar.selectbox("Severity", severity_opts,
                                   index=safe_index(severity_opts, defaults.get('Severity', 'Mild')))
    
    activity_levels = {
        "Sedentary": 1.2,
        "Moderate": 1.55,
        "Active": 1.725
    }
    activity_opts = list(activity_levels.keys())
    activity_label = st.sidebar.selectbox("Physical Activity Level", activity_opts,
                                         index=safe_index(activity_opts, defaults.get('Physical_Activity_Level', 'Moderate')))
    
    if (activity_label != None):
        activity_multiplier = activity_levels[activity_label]
    
    # Health Metrics
    cholesterol = st.sidebar.number_input("Cholesterol (mg/dL)", 0.0, 500.0, float(defaults.get('Cholesterol_mg/dL', 180.0)))
    blood_pressure = st.sidebar.number_input("Blood Pressure (mmHg)", 0.0, 250.0, float(defaults.get('Blood_Pressure_mmHg', 120.0)))
    glucose = st.sidebar.number_input("Glucose (mg/dL)", 0.0, 500.0, float(defaults.get('Glucose_mg/dL', 90.0)))
    
    # Preferences & Restrictions
    restriction_opts = ["None", "Low_Sugar", "Low_Sodium", "Vegetarian"]
    dietary_restrictions = st.sidebar.selectbox("Dietary Restrictions", restriction_opts,
                                               index=safe_index(restriction_opts, defaults.get('Dietary_Restrictions', 'None')))
    
    allergy_opts = ["None", "Peanuts", "Gluten", "Dairy", "Eggs", "Soy", "Fish"]
    allergies_val = st.sidebar.selectbox("Allergies", allergy_opts,
                                        index=safe_index(allergy_opts, defaults.get('Allergies', 'None')))
    
    cuisine_opts = ["Mexican", "Chinese", "Italian", "Indian", "American"]
    preferred_cuisine = st.sidebar.selectbox("Preferred Cuisine", cuisine_opts,
                                            index=safe_index(cuisine_opts, defaults.get('Preferred_Cuisine', 'Mexican')))
    
    # Score metrics
    exercise_hours = st.sidebar.slider("Weekly Exercise Hours", 0.0, 50.0, float(defaults.get('Weekly_Exercise_Hours', 3.0)))
    adherence = st.sidebar.slider("Adherence to Diet Plan (%)", 0.0, 100.0, float(defaults.get('Adherence_to_Diet_Plan', 80.0)))
    imbalance_score = st.sidebar.slider("Nutrient Imbalance Score", 0.0, 10.0, float(defaults.get('Dietary_Nutrient_Imbalance_Score', 2.0)))
    
    # Recommendation field (included in training)
    recommendation_opts = ["Balanced", "Low_Carb", "Low_Sodium", "High_Protein"]
    diet_recommendation = st.sidebar.selectbox("Diet Recommendation", recommendation_opts,
                                              index=safe_index(recommendation_opts, defaults.get('Diet_Recommendation', 'Balanced')))

    # Construct the dictionary for prediction
    user_profile_dict = {
        "Age": age,
        "Gender": gender,
        "Weight_kg": weight,
        "Height_cm": height,
        "BMI": bmi,
        "Disease_Type": disease_type,
        "Severity": severity,
        "Physical_Activity_Level": activity_label,
        "Cholesterol_mg/dL": cholesterol,
        "Blood_Pressure_mmHg": blood_pressure,
        "Glucose_mg/dL": glucose,
        "Dietary_Restrictions": dietary_restrictions,
        "Allergies": allergies_val,
        "Preferred_Cuisine": preferred_cuisine,
        "Weekly_Exercise_Hours": exercise_hours,
        "Adherence_to_Diet_Plan": adherence,
        "Dietary_Nutrient_Imbalance_Score": imbalance_score,
        "Diet_Recommendation": diet_recommendation
    }

    st.sidebar.markdown("---")
    
    # 2. NN (Prediction)
    predicted_target = predictor.predict(user_profile_dict)
    
    # If loading from dataset, show original intake too
    dataset_intake = float(defaults.get('Daily_Caloric_Intake', 0))
    
    # Main Page Layout
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.header("1. Calculated Needs (NN)")
        st.metric("Predicted Daily Target", f"{predicted_target} kcal")
        if dataset_intake > 0:
            st.metric("Dataset Original Intake", f"{dataset_intake} kcal", delta=f"{predicted_target - dataset_intake:.2f}")
        
        st.info(f"System Recommendation: {diet_recommendation}")
        
        with st.expander("Detailed Health Profile"):
            st.write(f"**BMI**: {bmi:.2f}")
            st.write(f"**Disease**: {disease_type} ({severity})")
            st.write(f"**Glucose**: {glucose} mg/dL")
            st.write(f"**Cholesterol**: {cholesterol} mg/dL")
    
    with col2:
        st.header("2. Filtered Menu (KBS)")
        raw_food_data = load_food_data()
        allergy_filter = AllergyFilter()
        
        # Filtering logic
        filter_terms = []
        if allergies_val != "None": filter_terms.append(allergies_val)
        if dietary_restrictions != "None": filter_terms.append(dietary_restrictions)
            
        filtered_menu = allergy_filter.filter_menu(raw_food_data, filter_terms)
        
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

# UI/UX Contract: Streamlit Meal Planner

## Sidebar Interface
- **Age**: Numeric input slider (1-100).
- **Weight**: Numeric input (kg).
- **Height**: Numeric input (cm).
- **Activity**: Selectbox (Sedentary, Lightly Active, Moderately Active, Very Active, Extra Active).
- **Allergies**: Multi-select (Peanuts, Dairy, Gluten, Soy, Eggs, Fish).

## Main Page Layout
### 1. Calculated Needs (NN Output)
- Metric: Daily Calorie Target.
- Metric: Predicted Macronutrient Ratios.

### 2. Filtered Menu (KBS Output)
- `st.dataframe` showing food items that passed the allergy filter.

### 3. Optimized Plan (OT Output)
- `st.dataframe` showing the 3-5 selected meals for the day.
- Visual summary of total calories vs. target.

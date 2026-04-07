# Quickstart: Neuro-Symbolic Meal Planner

## Prerequisites
- Python 3.11+
- Pip

## Installation
```bash
# Clone the repository
git clone <repo-url>
cd smart-diet-nutrition-planner

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application
```bash
streamlit run src/app.py
```

## Application Flow
1. **Sidebar**: 
   - **Presets**: Select a Patient ID from the "Load Patient Profile" dropdown to test the model with unseen samples (10 reserved test cases).
   - **Manual Input**: Fill out the full clinical profile including Cholesterol, Blood Pressure, and Glucose.
2. **NN Prediction**: The MLP model (64-32 architecture) processes all 18 features using a scikit-learn preprocessing pipeline to predict target calories.
3. **KBS Filter**: The Knowledge-Based System validates the food menu against your allergies and restrictions.
4. **OT Selection**: The Optimization Theory layer selects 3 meals (Breakfast, Lunch, Dinner) with 3-4 items each to match the target.

## Data Requirements
The application requires:
- `data/foods_dataset.csv`
- `data/calorie_intake_dataset.csv`

## Testing
```bash
pytest
```

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
1. **Sidebar**: Enter your Age, Weight, Height, and Activity Level.
2. **Allergies**: Select any allergies to filter the food menu.
3. **NN Prediction**: View your predicted daily calorie needs.
4. **KBS Filter**: Review the safety-validated food menu.
5. **OT Selection**: See the optimized daily meal plan that fits your needs.

## Data Requirements
The application uses `data/diet_recommendations.csv`. A sample version is included for testing.

## Testing
```bash
pytest
```

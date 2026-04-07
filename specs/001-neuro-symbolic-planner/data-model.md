# Data Model: Neuro-Symbolic Meal Planner

## Entities

### User Profile (Input Data)
- `age`: Integer (years)
- `weight`: Float (kg)
- `height`: Float (cm)
- `activity_level`: Float (multiplier: 1.2, 1.375, 1.55, 1.725, 1.9)
- `allergies`: List of strings

### Food Item (Dataset Record)
- `name`: String
- `calories`: Float
- `protein`: Float
- `carbs`: Float
- `fat`: Float
- `allergens`: String/List (data to filter against)

### Meal Plan (Output Selection)
- `items`: List of Food Items
- `total_calories`: Float (Sum of items)
- `total_macros`: Dictionary (Sum of protein, carbs, fat)

## Validation Rules
- **Age**: 0 < Age < 120
- **Weight**: 20kg < Weight < 500kg
- **Height**: 50cm < Height < 250cm
- **Selection Constraint**: Plan MUST contain between 3 and 5 unique items.

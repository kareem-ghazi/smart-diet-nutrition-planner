import numpy as np
import pandas as pd

class MealOptimizer:
    """
    Selection Optimization using Greedy Search (OT).
    Generates 3 different meals (Breakfast, Lunch, Dinner), 
    each consisting of 3-4 food combinations.
    Optimizes to reach the target daily intake.
    """
    def select_daily_plan(self, menu_df, target_calories, percentages=None):
        """
        Generates a full day plan with 3 meals.
        """
        if menu_df.empty:
            return {}

        if percentages is None:
            percentages = {"Breakfast": 0.25, "Lunch": 0.35, "Dinner": 0.40}

        # Split menu by meal type
        breakfast_menu = menu_df[menu_df['Meal_Type'] == 'Breakfast']
        lunch_menu = menu_df[menu_df['Meal_Type'] == 'Lunch']
        dinner_menu = menu_df[menu_df['Meal_Type'] == 'Dinner']
        
        # Fallback if specific categories are empty
        if breakfast_menu.empty:
            breakfast_menu = menu_df
        if lunch_menu.empty:
            lunch_menu = menu_df
        if dinner_menu.empty:
            dinner_menu = menu_df

        # Target distribution
        plan = {
            "Breakfast": self._select_meal_items(breakfast_menu, target_calories * percentages.get("Breakfast", 0.25)),
            "Lunch": self._select_meal_items(lunch_menu, target_calories * percentages.get("Lunch", 0.35)),
            "Dinner": self._select_meal_items(dinner_menu, target_calories * percentages.get("Dinner", 0.40))
        }
        
        return plan

    def _select_meal_items(self, meal_menu, target_meal_calories, min_items=3, max_items=4):
        """
        Selects 3-4 items for a single meal to reach target_meal_calories.
        """
        if meal_menu.empty:
            return pd.DataFrame()

        calorie_col = 'Calories (kcal)'
        
        # We'll use a slightly more sophisticated greedy approach:
        # 1. Start with a random set of 3 items.
        # 2. If below target, try to swap items or add a 4th to get closer.
        
        best_items = []
        best_diff = float('inf')
        
        # Try multiple random iterations to find the "best" combination
        for _ in range(50):
            # Pick number of items
            num_items = np.random.randint(min_items, max_items + 1)
            if len(meal_menu) < num_items:
                current_selection = meal_menu
            else:
                current_selection = meal_menu.sample(n=num_items)
            
            current_calories = current_selection[calorie_col].sum()
            diff = abs(current_calories - target_meal_calories)
            
            if diff < best_diff:
                best_diff = diff
                best_items = current_selection
                
            if best_diff < 10: # Close enough
                break
                
        return best_items

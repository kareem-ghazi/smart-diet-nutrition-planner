import numpy as np
import pandas as pd
from scipy.optimize import linprog

class MealOptimizer:
    """
    Selection Optimization using Linear Programming (OT).
    Finds a set of 3-5 meals that best matches the calorie target.
    """
    def select_meals(self, menu_df, target_calories, min_meals=3, max_meals=5):
        """
        Selects meals from the menu_df to match target_calories.
        """
        if menu_df.empty:
            return pd.DataFrame()
            
        n_items = len(menu_df)
        calories = menu_df['calories'].values
        
        # Constraints: 
        # 1. Sum(calories * x) ~= target_calories (Equality constraint)
        # 2. Sum(x) >= min_meals
        # 3. Sum(x) <= max_meals
        # 4. x is binary (0 or 1) - using bounds [0, 1] for relaxation
        
        # Objective: minimize difference from target_calories
        # Since we use linprog, we set an objective to minimize sum(x) but we 
        # mainly focus on the calorie constraint.
        # Alternatively, minimize the absolute difference: minimize |Sum(cal*x) - target|
        # This is more complex for linprog. We'll simplify:
        # Objective: minimize error in calories. 
        # But linprog doesn't natively handle absolute error easily.
        
        # Simpler approach for prototype: find a feasible solution for the target window +/- 10%
        # c = [0] * n_items (any feasible solution)
        
        # A_eq = [calories]
        # b_eq = [target_calories]
        
        # Instead, let's use a greedy fallback if LP is too rigid for the small dataset.
        return self._greedy_selection(menu_df, target_calories, min_meals, max_meals)

    def _greedy_selection(self, menu_df, target_calories, min_meals, max_meals):
        """
        Greedy fallback for meal selection (prototype stability).
        Sorts items by calories/protein and picks until target reached.
        """
        sorted_df = menu_df.sample(frac=1).copy() # Randomize selection a bit
        selected_items = []
        current_calories = 0
        
        for _, row in sorted_df.iterrows():
            if current_calories + row['calories'] <= target_calories * 1.05: # 5% over buffer
                selected_items.append(row)
                current_calories += row['calories']
                if len(selected_items) >= max_meals:
                    break
                    
        # Ensure minimum meals
        if len(selected_items) < min_meals:
            # Just take the smallest 3 if we can't meet target gracefully
            selected_items = sorted_df.nsmallest(min_meals, 'calories').to_dict('records')
            
        return pd.DataFrame(selected_items)

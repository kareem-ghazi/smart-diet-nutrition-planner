class FoodFilter:
    """
    Knowledge-Based System (KBS) for dietary safety filtering.
    Filters based on Food_Item and Category keywords.
    """
    def filter_menu(self, menu_df, selected_allergies=None, health_conditions=None, selected_cuisine="All"):
        """
        Filters out items based on allergies, health conditions, and cuisine.
        """
        if menu_df.empty:
            return menu_df

        filtered_df = menu_df.copy()

        # 1. Allergy Filtering
        if selected_allergies:
            pattern = '|'.join(selected_allergies)
            mask = (
                filtered_df['Food_Item'].str.contains(pattern, case=False, na=False) |
                filtered_df['Category'].str.contains(pattern, case=False, na=False)
            )
            filtered_df = filtered_df[~mask]

        # 2. Health Condition Filtering
        if health_conditions:
            if "Diabetes" in health_conditions:
                # Filter out high sugar items
                filtered_df = filtered_df[filtered_df['Sugars (g)'] < 10]
            if "Hypertension" in health_conditions:
                # Filter out high sodium items
                filtered_df = filtered_df[filtered_df['Sodium (mg)'] < 400]
            if "Obesity" in health_conditions:
                # Filter out high calorie/fat items
                filtered_df = filtered_df[filtered_df['Calories (kcal)'] < 500]
                filtered_df = filtered_df[filtered_df['Fat (g)'] < 20]

        # 3. Cuisine Filtering
        if selected_cuisine != "All":
            # Assign cuisine based on keywords
            filtered_df = self.assign_cuisines(filtered_df)
            filtered_df = filtered_df[filtered_df['Cuisine'] == selected_cuisine]

        return filtered_df

    def assign_cuisines(self, df):
        """
        Assigns cuisines based on food names/categories.
        Groups into: Mediterranean, Asian, American, Indian, Mexican, Others.
        """
        def get_cuisine(row):
            food = row['Food_Item'].lower()
            category = row['Category'].lower()
            
            if any(k in food or k in category for k in ['salad', 'salmon', 'quinoa', 'broccoli', 'olive', 'mediterranean', 'greek']):
                return 'Mediterranean'
            if any(k in food or k in category for k in ['rice', 'stir fry', 'sushi', 'tofu', 'ramen', 'asian', 'soy']):
                return 'Asian'
            if any(k in food or k in category for k in ['burger', 'steak', 'sandwich', 'pancake', 'toast', 'american', 'fries']):
                return 'American'
            if any(k in food or k in category for k in ['curry', 'lentil', 'paneer', 'indian', 'naan']):
                return 'Indian'
            if any(k in food or k in category for k in ['taco', 'burrito', 'quesadilla', 'mexican', 'salsa', 'bean']):
                return 'Mexican'
            return 'Others'

        df['Cuisine'] = df.apply(get_cuisine, axis=1)
        return df

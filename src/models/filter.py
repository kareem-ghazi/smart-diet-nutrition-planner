import pandas as pd

class AllergyFilter:
    """
    Knowledge-Based System (KBS) for allergy safety filtering.
    Filters based on Food_Item and Category keywords as 'ingredients' column is absent.
    """
    def filter_menu(self, menu_df, selected_allergies):
        """
        Filters out items where Food_Item or Category matches selected allergies.
        """
        if not selected_allergies or menu_df.empty:
            return menu_df
            
        # Create a regex pattern from selected allergies
        pattern = '|'.join(selected_allergies)
        
        # Check both Food_Item and Category for allergy keywords
        # Note: In foods_dataset.csv, column names are 'Food_Item' and 'Category'
        mask = (
            menu_df['Food_Item'].str.contains(pattern, case=False, na=False) |
            menu_df['Category'].str.contains(pattern, case=False, na=False)
        )
        
        filtered_df = menu_df[~mask]
        
        return filtered_df

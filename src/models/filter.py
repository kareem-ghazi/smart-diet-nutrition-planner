import pandas as pd

class AllergyFilter:
    """
    Knowledge-Based System (KBS) for allergy safety filtering.
    Uses Boolean indexing for efficient menu refinement.
    """
    def filter_menu(self, menu_df, selected_allergies):
        """
        Filters out items containing any of the selected allergies.
        """
        if not selected_allergies:
            return menu_df
            
        # Decision: df[~df['ingredients'].str.contains('|'.join(allergies))]
        # We ensure case-insensitive matching
        pattern = '|'.join(selected_allergies)
        filtered_df = menu_df[~menu_df['ingredients'].str.contains(pattern, case=False, na=False)]
        
        return filtered_df

# Feature Specification: Streamlit Neuro-Symbolic Meal Planner

**Feature Branch**: `001-neuro-symbolic-planner`  
**Created**: 2026-04-07  
**Status**: Draft  
**Input**: User description: "Build a 'Streamlit Neuro-Symbolic Meal Planner': Sidebar: User inputs for Age, Weight, Height, Activity, and a multi-select for Allergies (e.g., Peanuts, Dairy, Gluten). Main Page: - A 'Calculated Needs' section showing the MLP's prediction. A 'Filtered Menu' section showing the KBS results. An 'Optimized Plan' section showing the final meal selection. Data: Use the Kaggle Diet Recommendations CSV for food items."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Personalized Meal Plan (Priority: P1)

As a health-conscious individual, I want to input my physical profile so that the system can calculate my nutritional needs and suggest a viable meal plan from the available food dataset.

**Why this priority**: This is the core functionality that provides immediate value. Without the ability to calculate needs and select meals, the system has no purpose.

**Independent Test**: Can be fully tested by entering valid profile data and verifying that a "Calculated Needs" prediction and an "Optimized Plan" are displayed.

**Acceptance Scenarios**:

1. **Given** the app is loaded, **When** I enter age, weight, height, and activity level in the sidebar, **Then** the "Calculated Needs" section should display specific calorie and macronutrient predictions.
2. **Given** valid profile inputs, **When** I view the "Optimized Plan" section, **Then** I should see a selection of food items that collectively meet my predicted needs.

---

### User Story 2 - Allergy Safety Filtering (Priority: P2)

As a user with specific dietary restrictions, I want to select my allergies so that any unsafe food items are automatically excluded from my meal plan recommendations.

**Why this priority**: Safety is critical for a nutrition planner. This story ensures the "KBS (Safety Filter)" principle is effectively implemented.

**Independent Test**: Enter a profile and select "Peanuts" as an allergy; verify that the "Filtered Menu" excludes any peanut-containing items and the final "Optimized Plan" only contains peanut-free items.

**Acceptance Scenarios**:

1. **Given** I have selected "Dairy" in the allergy multi-select, **When** the system generates the "Filtered Menu", **Then** no items containing dairy should be present in that list.
2. **Given** an allergy selection, **When** the "Optimized Plan" is finalized, **Then** it MUST ONLY contain items from the "Filtered Menu".

## Edge Cases

- **Zero/Negative Inputs**: What happens when a user enters 0 or negative values for age, height, or weight? (Default: Validation error message in sidebar).
- **No Viable Plan**: How does the system handle a situation where allergies exclude all available food items? (Default: Display a "No viable plan found for these constraints" message).
- **Extreme Activity Levels**: How does the MLP handle outlier activity multipliers? (Default: Clip to reasonable physiological ranges).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001: Profile Input**: System MUST provide sidebar inputs for Age (years), Weight (kg), Height (cm), and Activity Level (categorical/multiplier).
- **FR-002: Allergy Selection**: System MUST provide a multi-select for common allergies (Peanuts, Dairy, Gluten, etc.) in the sidebar.
- **FR-003: Needs Prediction (MLP)**: System MUST use a Neural Network (MLP) to predict caloric and macronutrient needs based on profile inputs.
- **FR-004: Safety Filtering (KBS)**: System MUST filter the Kaggle Diet Recommendations dataset against user-selected allergies to produce a "Filtered Menu".
- **FR-005: Plan Selection (OT)**: System MUST select a combination of meals from the Filtered Menu that best fits the Predicted Needs.
- **FR-006: Visual Hierarchy**: System MUST display outputs in three distinct sections on the main page: "Calculated Needs", "Filtered Menu", and "Optimized Plan".
- **FR-007: Data Source**: System MUST load and process the Kaggle Diet Recommendations CSV as the primary food database.

### Key Entities *(include if feature involves data)*

- **User Profile**: Represents the user's physical attributes (Age, Weight, Height, Activity) and constraints (Allergies).
- **Food Item**: Represents a specific record from the Kaggle dataset, including name, nutritional content, and ingredient/allergen markers.
- **Meal Plan**: A collection of Food Items selected to meet a specific nutritional target while adhering to safety filters.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can generate a complete, filtered meal plan in under 1 minute from initial input.
- **SC-002**: 100% of generated "Optimized Plans" MUST NOT contain items marked with the user's selected allergies.
- **SC-003**: The "Optimized Plan" total calories MUST be within +/- 10% of the MLP's "Calculated Needs" prediction.
- **SC-004**: System successfully loads and parses at least 95% of records from the Kaggle Diet Recommendations CSV without errors.

## Assumptions

- **Allergen Data**: The Kaggle Diet Recommendations CSV contains sufficient ingredient or category data to allow for effective KBS filtering.
- **MLP Training**: A pre-trained or standard formula-based MLP weights set is available for the "Needs Prediction" logic.
- **Activity Scale**: The activity level input maps to standard Harris-Benedict multipliers unless otherwise specified.
- **User Interface**: Streamlit's default components are sufficient for all input and display needs as per Constitution Principle IV.

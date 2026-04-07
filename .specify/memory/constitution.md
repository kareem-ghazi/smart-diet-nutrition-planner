<!--
Sync Impact Report:
- Version change: none → 1.0.0
- List of modified principles:
    - [PRINCIPLE_1_NAME] → Frameworks
    - [PRINCIPLE_2_NAME] → Optimizer
    - [PRINCIPLE_3_NAME] → Architecture
    - [PRINCIPLE_4_NAME] → Simplicity
    - [PRINCIPLE_5_NAME] → Removed (consolidated)
- Added sections:
    - Technical Stack & Performance
    - Development & Quality
- Removed sections: none
- Templates requiring updates (✅ updated / ⚠ pending):
    - .specify/templates/plan-template.md (✅ aligned)
    - .specify/templates/spec-template.md (✅ aligned)
    - .specify/templates/tasks-template.md (✅ aligned)
- Follow-up TODOs: none
-->

# Smart Diet Nutrition Planner Constitution

## Core Principles

### I. Frameworks
The project MUST use **Streamlit** for the frontend UI and **TensorFlow/Keras** for the Multi-Layer Perceptron (MLP) model implementation. This ensures a consistent, high-performance stack for both interactive user experience and machine learning inference.

### II. Optimizer
All MLP models MUST use the **Adam optimizer** for training. This standardization ensures predictable convergence behavior and simplifies hyperparameter tuning across different model iterations.

### III. Architecture: Neuro-Symbolic Flow
The system MUST maintain a strict Neuro-Symbolic architectural flow:
1. **NN (Prediction)**: Neural Network generates initial meal/nutrition candidates.
2. **KBS (Safety Filter)**: Knowledge-Based System filters candidates against health and safety constraints (e.g., allergies, medical restrictions).
3. **OT (Selection)**: Optimization Theory selects the final plan based on user preferences and goals.

### IV. Simplicity
UI development MUST prioritize out-of-the-box Streamlit components:
- Use `st.sidebar` for all user input controls and filters.
- Use `st.dataframe` for meal plan and nutritional data visualization.
Custom CSS/HTML components should be avoided unless a requirement cannot be met with standard primitives.

## Technical Stack & Performance

### MLP Specifications
- **Framework**: TensorFlow 2.x / Keras.
- **Loss Function**: Mean Squared Error (MSE) or Cross-Entropy depending on the specific task (Regression/Classification).
- **Optimizer**: Adam (Standard).

### UI Standards
- **Framework**: Streamlit.
- **Theme**: Default Streamlit "Light/Dark" support.
- **Layout**: Sidebar-driven interaction.

### Performance Gates
- **Model Inference**: Candidate generation must complete within < 200ms.
- **Safety Filtering**: KBS validation must complete within < 100ms.

## Development & Quality

### Testing Discipline
- **Neuro-Symbolic Validation**: Every prediction must be traceable through the KBS safety filter.
- **Unit Testing**: Pytest for KBS logic and OT selection algorithms.
- **Integration Testing**: Streamlit testing framework for UI-to-Model flows.

### Review Process
- All Architectural changes must explicitly state how they maintain the NN -> KBS -> OT flow.
- Code reviews must verify that `st.sidebar` and `st.dataframe` are used as primary interaction/display patterns.

## Governance

### Amendment Procedure
- Minor wording changes or clarifications: PATCH bump.
- Adding or modifying a Principle: MINOR bump.
- Removing a Principle or changing the Core Architecture (NN->KBS->OT): MAJOR bump.

### Compliance
The Constitution takes precedence over all other documentation. Deviations must be justified in the `plan.md` "Complexity Tracking" section and approved by the project lead.

**Version**: 1.0.0 | **Ratified**: 2026-04-07 | **Last Amended**: 2026-04-07

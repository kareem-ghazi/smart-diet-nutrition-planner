# Research Findings: Neuro-Symbolic Meal Planner

## Decision: MLP Architecture & Training
- **Choice**: Keras MLP with Input layer, Hidden Layer 1 (64), Hidden Layer 2 (32), and Output (1 node for Calories).
- **Rationale**: Standard feed-forward architecture suitable for tabular numerical data regression (BMR/TDEE calculation).
- **Optimizer**: Adam (as per Constitution).
- **Loss Function**: Mean Squared Error (MSE).

## Decision: KBS Allergy Filtering
- **Choice**: Pandas Boolean Indexing.
- **Rationale**: Extremely fast and readable filtering for tabular data.
- **Logic**: `df[~df['ingredients'].str.contains('|'.join(allergies))]`.

## Decision: Selection Optimization (OT)
- **Choice**: `scipy.optimize.linprog`.
- **Rationale**: A Linear Programming (LP) approach is more robust than a greedy search for finding a combination of 3-5 meals that sum up to a specific calorie target while maximizing or minimizing other constraints (e.g., protein).
- **Alternatives Considered**: Greedy Search (rejected for lack of precision in multi-variable optimization).

## Decision: Streamlit Performance
- **Choice**: `st.cache_data` for CSV loading, `st.cache_resource` for model loading.
- **Rationale**: Prevents redundant file I/O and model initialization on every widget interaction.

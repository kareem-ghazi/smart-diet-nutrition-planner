# Tasks: Streamlit Neuro-Symbolic Meal Planner

**Input**: Design documents from `/specs/001-neuro-symbolic-planner/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the spec, but basic validation is included in implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan (src/models, src/services, tests/)
- [x] T002 Create `requirements.txt` with streamlit, tensorflow, pandas, scipy, and pytest
- [x] T003 [P] Configure linting (flake8/black) and basic folder structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement `DataLoader` in `src/services/data_loader.py` to load Kaggle Diet Recommendations CSV with `st.cache_data`
- [x] T005 Create initial `src/app.py` with Streamlit sidebar inputs (Age, Weight, Height, Activity) as per UI Contract
- [x] T006 Implement input validation for sidebar numeric inputs (Age, Weight, Height) in `src/app.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Personalized Meal Plan (Priority: P1) 🎯 MVP

**Goal**: Calculate nutritional needs using MLP and select optimized meals using OT.

**Independent Test**: Enter profile data; verify "Calculated Needs" display and "Optimized Plan" table appears with 3-5 meals.

### Implementation for User Story 1

- [x] T007 [P] [US1] Implement `CaloriePredictor` (MLP: 64, 32 nodes, Adam) in `src/models/predictor.py`
- [x] T008 [P] [US1] Implement `MealOptimizer` (Scipy `linprog` selection) in `src/models/optimizer.py`
- [x] T009 [US1] Integrate `CaloriePredictor` into `src/app.py` to show "Calculated Needs" section
- [x] T10 [US1] Integrate `MealOptimizer` into `src/app.py` to display "Optimized Plan" table (`st.dataframe`)
- [x] T11 [US1] Add visual summary of total calories vs. target in `src/app.py`

**Checkpoint**: User Story 1 is functional as an MVP (without allergy filtering).

---

## Phase 4: User Story 2 - Allergy Safety Filtering (Priority: P2)

**Goal**: Implement Knowledge-Based System (KBS) to filter menu based on selected allergies.

**Independent Test**: Select "Peanuts"; verify "Filtered Menu" and "Optimized Plan" exclude peanut-containing items.

### Implementation for User Story 2

- [x] T012 [P] [US2] Implement `AllergyFilter` (KBS logic via Pandas indexing) in `src/models/filter.py`
- [x] T013 [US2] Add Allergy multi-select to sidebar in `src/app.py` as per UI Contract
- [x] T014 [US2] Integrate `AllergyFilter` into `src/app.py` main page to display "Filtered Menu" section
- [x] T015 [US2] Update `src/app.py` to pass filtered menu to `MealOptimizer` for final selection

**Checkpoint**: User Story 2 is functional; safety constraints are now applied to the planner.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T016 [P] Add CSS/Styling to improve visual hierarchy as per Constitution Principle IV (Simplicity)
- [x] T017 [P] Update `specs/001-neuro-symbolic-planner/quickstart.md` with final run instructions
- [x] T018 Ensure all `st.cache_resource` and `st.cache_data` calls are optimized for performance
- [x] T019 Final cleanup and adherence check to Constitution (NN -> KBS -> OT flow)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on T001-T003.
- **User Stories (Phase 3 & 4)**: Both depend on Phase 2 completion.
  - US1 can be implemented first (MVP).
  - US2 depends on US1's integration in `app.py` for full end-to-end verification.
- **Polish (Final Phase)**: Depends on all stories.

### Parallel Opportunities

- T007 [US1] and T008 [US1] can be developed in parallel as they are in separate files.
- T012 [US2] can be developed in parallel with US1 tasks.
- All Setup tasks (Phase 1) can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Implement US1: Needs Prediction and Meal Optimization.
3. Verify that the core calculation-to-selection pipeline works.

### Incremental Delivery

1. Deliver MVP (US1).
2. Add Safety Filtering (US2) as an enhancement.
3. Apply final polish.

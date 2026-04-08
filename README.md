# 🍎 Smart Diet Nutrition Planner

A personalized, data-driven nutrition planning system that combines **Neural Networks (NN)** for calorie prediction, a **Knowledge-Based System (KBS)** for dietary filtering, and an **Optimization Engine (OT)** for meal selection.

## 🚀 Overview

The **Smart Diet Nutrition Planner** is designed to provide users with a highly personalized meal plan based on their unique physiological profile, daily activity levels, and dietary restrictions. By leveraging machine learning and constraint satisfaction, the app calculates your precise caloric needs and recommends a balanced, safe daily menu.

## ✨ Key Features

- **Personalized Calorie Prediction (NN)**: Uses a TensorFlow/Keras neural network to estimate daily caloric targets based on age, gender, working type, sleep hours, and height.
- **Dietary Restriction Filtering (KBS)**: Intelligently filters a comprehensive food dataset for allergies (Peanuts, Gluten, Dairy, Eggs, Soy, Fish) and other preferences.
- **Daily Meal Optimization (OT)**: Generates an optimized daily plan (Breakfast, Lunch, and Dinner) that matches your calculated caloric target while ensuring nutritional variety.
- **Interactive Dashboard**: A clean, modern Streamlit UI for easy profile management and meal plan visualization.
- **Preset Profiles**: Load test samples directly from the dataset to explore the planner's capabilities.
- **Nutritional Transparency**: View detailed breakdown of Protein, Calories, and suggested Water Intake for every meal.

## 📚 Documentation

Extensive documentation is available in the [docs/](./docs) folder:
- [Overview](./docs/OVERVIEW.md): Project philosophy and hybrid architecture.
- [Technical Details](./docs/TECHNICAL_DETAILS.md): Deep dive into NN, KBS, and OT models.
- [Dataset Documentation](./docs/DATASET.md): Detailed column descriptions and data formats.
- [Usage Guide](./docs/USAGE.md): Step-by-step instructions for users.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Machine Learning**: [TensorFlow](https://www.tensorflow.org/), [Keras](https://keras.io/)
- **Data Science**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Optimization**: [SciPy](https://scipy.org/)
- **Programming Language**: [Python 3.11](https://www.python.org/)

## 📂 Project Structure

```text
smart-diet-nutrition-planner/
├── data/               # CSV datasets for foods and calorie intake
├── src/                # Source code
│   ├── models/         # NN Predictor, KBS Filter, and OT Optimizer
│   ├── services/       # Data loaders and external integrations
│   ├── utils/          # Shared utility functions
│   └── app.py          # Streamlit entry point
├── tests/              # Unit and integration tests
├── LICENSE             # MIT License
└── requirements.txt    # Project dependencies
```

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kareemghazi/smart-diet-nutrition-planner.git
   cd smart-diet-nutrition-planner
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

To start the application, run:

```bash
streamlit run src/app.py
```

Navigate to `http://localhost:8501` in your browser to interact with the planner.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

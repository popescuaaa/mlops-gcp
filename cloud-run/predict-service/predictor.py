"""
This should be run locally; only the joblib model should be used in the cloud run service.
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Set the random seed for dummy data generation
seed = 42
np.random.seed(seed=seed)


class Predictor:
    def __init__(self, name: str) -> None:
        self.name = name

    def create_model(self):
        # Create dummy data
        n_samples = 1000

        # Create numeric features
        age = np.random.normal(40, 10, n_samples).astype(int)
        income = np.random.normal(50000, 15000, n_samples).astype(int)
        credit_score = np.random.normal(700, 100, n_samples).astype(int)

        # Create categorical features
        categories = ["A", "B", "C", "D"]
        category1 = np.random.choice(categories, n_samples)
        category2 = np.random.choice(["X", "Y", "Z"], n_samples)

        # Create target variable (binary classification)
        # Higher probability of class 1 if age > 40, income > 50000, and category1 is 'A'
        target_prob = (
            0.3 + 0.4 * (age > 40) + 0.2 * (income > 50000) + 0.1 * (category1 == "A")
        )
        target = np.random.binomial(1, np.clip(target_prob, 0, 1))

        # Create DataFrame
        data = pd.DataFrame(
            {
                "age": age,
                "income": income,
                "credit_score": credit_score,
                "category1": category1,
                "category2": category2,
                "target": target,
            }
        )

        # Define features and target
        X = data.drop("target", axis=1)
        y = data["target"]

        # Split numeric and categorical features
        numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
        categorical_features = X.select_dtypes(include=["object"]).columns

        # Create preprocessing pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), numeric_features),
                ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ]
        )

        # Create the full pipeline
        model_pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    RandomForestClassifier(n_estimators=100, random_state=seed),
                ),
            ]
        )

        # Train the model
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=seed
        )
        model_pipeline.fit(X_train, y_train)

        # Save the model
        with open("classification_pipeline.pkl", "wb") as f:
            pickle.dump(model_pipeline, f)

        print(f"Model accuracy: {model_pipeline.score(X_test, y_test):.4f}")
        return model_pipeline


if __name__ == "__main__":
    predictor = Predictor(
        name="dummy_credit_score_predictor",
    )
    predictor.create_model()

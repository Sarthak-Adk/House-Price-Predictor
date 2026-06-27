import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


def train_model():
    # Load cleaned data
    df = pd.read_csv("../data/processed/cleaned_house_data.csv")

    # Features and target
    X = df.drop("price", axis=1)
    y = np.log1p(df["price"])

    # Encode categorical columns
    X = pd.get_dummies(
        X,
        columns=["location", "facing", "furnish_status"],
        drop_first=True
    )

    # Save feature columns
    joblib.dump(X.columns.tolist(), "models/model_columns.pkl")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Convert back to original scale
    actual_prices = np.expm1(y_test)
    predicted_prices = np.expm1(y_pred)

    # Evaluation
    print("R2 Score:", r2_score(y_test, y_pred))
    print("MAE:", mean_absolute_error(actual_prices, predicted_prices))

    # Save model
    joblib.dump(model, "../models/house_price_model.pkl")

    print("Model training completed successfully!")


if __name__ == "__main__":
    train_model()
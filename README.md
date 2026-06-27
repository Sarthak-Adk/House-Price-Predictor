# House Price Predictor

A machine learning project that predicts house prices based on features like location, area, bedrooms, bathrooms, road access, parking, floor, and furnishing status.

## Project Overview

This project covers the complete machine learning workflow:

- Data collection
- Data cleaning
- Feature engineering
- Model training
- Model evaluation
- Model saving

The dataset contains Nepal house listing data.

---

## Features

Input features:

- Location
- Bedrooms
- Bathrooms
- Area
- Road Access
- Facing Direction
- Floor
- Parking
- Furnishing Status

Target:

- Price

---

## Project Structure

House-Price-Predictor/
│── data/
│ ├── raw/
│ ├── processed/
│
│── models/
│ ├── house_price_model.pkl
│ ├── model_columns.pkl
│
│── notebooks/
│ ├── data_cleaning.ipynb
│ ├── model_training.ipynb
│
│── src/
│ ├── scraping.py
│ ├── preprocess.py
│ ├── train.py
│
│── .gitignore
│── README.md

---

## Data Cleaning Steps

- Removed empty columns
- Filled missing values
- Removed rental listings
- Converted price into numeric values
- Converted area into numeric values
- Converted parking into total count
- Converted road access into numeric values
- Standardized text data
- Removed duplicate rows

---

## Model Used

- Random Forest Regressor

---

## Model Performance

- R² Score: 0.2665
- Mean Absolute Error: 12,000,106

Current performance is low because of:

- Limited dataset quality
- Missing important features
- Outliers
- High price variance

This project focuses on learning and building the full ML pipeline.

---

## Installation

Clone the repo:

git clone https://github.com/yourusername/house-price-predictor.git

Install dependencies:

pip install -r requirements.txt

---

## Run Preprocessing

python src/preprocess.py

---

## Train Model

python src/train.py

---

## Future Improvements

- Better dataset
- More features
- Outlier handling
- XGBoost model
- Flask deployment

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Jupyter Notebook
- Flask
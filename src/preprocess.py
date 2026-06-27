import pandas as pd
import re


# Convert price into numeric
def convert_price(price):
    price = str(price).replace("Rs.", "").replace(",", "").strip()

    if "Cr" in price:
        return float(price.replace("Cr", "").strip()) * 10000000

    elif "Lac" in price:
        return float(price.replace("Lac", "").strip()) * 100000

    return None


# Convert parking text into total parking count
def extract_parking(parking):
    nums = re.findall(r"\d+", str(parking))
    return sum(map(int, nums)) if nums else 0


def preprocess_data():
    # Load raw dataset
    df = pd.read_csv("../data/raw/raw_house_data.csv")

    # Drop useless column
    if "property_type" in df.columns:
        df.drop(columns=["property_type"], inplace=True)

    # Fill missing numerical values
    df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].median())
    df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms"].median())
    df["floor"] = df["floor"].fillna(df["floor"].median())

    # Fill missing categorical values
    df["road_access"] = df["road_access"].fillna(df["road_access"].mode()[0])
    df["facing"] = df["facing"].fillna(df["facing"].mode()[0])
    df["parking"] = df["parking"].fillna(df["parking"].mode()[0])
    df["furnish_status"] = df["furnish_status"].fillna(df["furnish_status"].mode()[0])

    # Clean area
    df["area"] = df["area"].str.extract(r"(\d+)")
    df["area"] = df["area"].astype(float)
    df["area"] = df["area"].fillna(df["area"].median())

    # Remove rental and invalid prices
    df = df[~df["price"].str.contains("/m", na=False)]
    df = df[~df["price"].str.contains("/y", na=False)]
    df = df[~df["price"].str.contains("Price on call", na=False)]

    # Convert price
    df["price"] = df["price"].apply(convert_price)

    # Remove invalid prices
    df.dropna(subset=["price"], inplace=True)

    # Remove unrealistic low prices
    df = df[df["price"] > 5000000]

    # Clean road_access
    df["road_access"] = df["road_access"].str.extract(r"(\d+)")
    df["road_access"] = df["road_access"].astype(float)

    # Clean parking
    df["parking"] = df["parking"].apply(extract_parking)

    # Standardize text
    text_cols = ["location", "facing", "furnish_status"]

    for col in text_cols:
        df[col] = df[col].str.lower().str.strip()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Save cleaned data
    df.to_csv("../data/processed/cleaned_house_data.csv", index=False)

    print("Data preprocessing completed successfully!")


if __name__ == "__main__":
    preprocess_data()
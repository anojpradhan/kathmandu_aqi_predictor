from pathlib import Path

import joblib
import pandas as pd

from scripts.data_collection import download_current_data
from scripts.feature_engineering import (
    PM10_FEATURES,
    PM25_FEATURES,
    create_pm10_features,
    create_pm25_features,
)

# PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "live" / "ratnapark"

MODEL_DIR = PROJECT_ROOT / "models"


PM25_MODEL_PATH = MODEL_DIR / "pm25_linear_regression_ewma.joblib"

PM10_MODEL_PATH = MODEL_DIR / "pm10_extra_trees_500_change.joblib"


# LOAD RAW DATA


def load_raw_data():

    pm1 = pd.read_csv(RAW_DIR / "pm1.csv")

    pm10 = pd.read_csv(RAW_DIR / "pm10.csv")

    pm25 = pd.read_csv(RAW_DIR / "pm25.csv")

    # Convert datetime
    pm1["datetime"] = pd.to_datetime(
        pm1["datetime"],
        utc=True,
    )

    pm10["datetime"] = pd.to_datetime(
        pm10["datetime"],
        utc=True,
    )

    pm25["datetime"] = pd.to_datetime(
        pm25["datetime"],
        utc=True,
    )

    # Merge pollutants
    merged = (
        pm1.merge(
            pm10,
            on="datetime",
            how="outer",
        )
        .merge(
            pm25,
            on="datetime",
            how="outer",
        )
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    return merged


# CREATE DAILY DATA


def create_daily_data(
    merged: pd.DataFrame,
) -> pd.DataFrame:

    daily = (
        merged.set_index("datetime").resample("D").mean(numeric_only=True).reset_index()
    )

    daily = daily.rename(
        columns={
            "datetime": "date",
            "pm25": "pm2_5",
        }
    )

    daily = daily.sort_values("date").reset_index(drop=True)

    return daily


# LOAD MODELS


def load_models():

    pm25_model = joblib.load(PM25_MODEL_PATH)

    pm10_model = joblib.load(PM10_MODEL_PATH)

    return (
        pm25_model,
        pm10_model,
    )


# FORECAST


def forecast_tomorrow():

    print()
    print("=" * 70)
    print("KATHMANDU AQI FORECAST")
    print("=" * 70)

    # 1. Download latest data

    print("\n[1/5] Downloading latest air-quality data...")

    download_current_data()

    # 2. Load and merge raw data

    print("\n[2/5] Loading and merging data...")

    merged = load_raw_data()

    print(
        "Raw observations:",
        len(merged),
    )

    # 3. Create daily data

    print("\n[3/5] Creating daily data...")

    daily = create_daily_data(merged)

    print(
        "Daily rows:",
        len(daily),
    )

    print(
        "Date range:",
        daily["date"].min(),
        "→",
        daily["date"].max(),
    )

    # 4. Create features

    print("\n[4/5] Creating forecast features...")

    pm25_df = create_pm25_features(daily)

    pm10_df = create_pm10_features(daily)

    # Latest available observation
    latest_pm25 = pm25_df.sort_values("date").iloc[-1]

    latest_pm10 = pm10_df.sort_values("date").iloc[-1]

    latest_date = latest_pm25["date"]

    forecast_date = latest_date + pd.Timedelta(days=1)

    print(
        "Latest available date:",
        latest_date,
    )

    print(
        "Forecast date:",
        forecast_date,
    )

    # PM2.5 feature validation

    missing_pm25 = [
        feature for feature in PM25_FEATURES if pd.isna(latest_pm25[feature])
    ]

    if missing_pm25:
        raise ValueError("Missing PM2.5 features: " + ", ".join(missing_pm25))

    # PM10 feature validation

    missing_pm10 = [
        feature for feature in PM10_FEATURES if pd.isna(latest_pm10[feature])
    ]

    if missing_pm10:
        raise ValueError("Missing PM10 features: " + ", ".join(missing_pm10))

    # Build model input

    X_pm25 = pd.DataFrame(
        [[latest_pm25[feature] for feature in PM25_FEATURES]],
        columns=PM25_FEATURES,
    )

    X_pm10 = pd.DataFrame(
        [[latest_pm10[feature] for feature in PM10_FEATURES]],
        columns=PM10_FEATURES,
    )

    # 5. Load models and predict

    print("\n[5/5] Loading models and predicting...")

    pm25_model, pm10_model = load_models()

    predicted_pm25 = pm25_model.predict(X_pm25)[0]

    predicted_pm10 = pm10_model.predict(X_pm10)[0]

    # Results

    print()
    print("=" * 70)
    print("TOMORROW'S FORECAST")
    print("=" * 70)

    print(f"Forecast date : {forecast_date.date()}")

    print(f"PM2.5         : {predicted_pm25:.2f} µg/m³")

    print(f"PM10          : {predicted_pm10:.2f} µg/m³")

    print("=" * 70)

    return {
        "forecast_date": (forecast_date.date().isoformat()),
        "pm2_5": float(predicted_pm25),
        "pm10": float(predicted_pm10),
    }


# RUN DIRECTLY

if __name__ == "__main__":
    forecast = forecast_tomorrow()

    print("\nForecast result:")
    print(forecast)

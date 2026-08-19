# Ratnapark AQI Forecasting

A machine learning project for **next-day air-quality forecasting in Ratnapark** using real-world observations from the Government of Nepal.

The system forecasts **PM2.5 and PM10** concentrations and estimates the corresponding **AQI and air-quality category**.

---

## Table of Contents

- [Problem](#problem)
- [Data Source](#data-source)
- [Data Processing](#data-processing)
- [Feature Engineering](#feature-engineering)
- [Model Selection](#model-selection)
- [Forecasting Pipeline](#forecasting-pipeline)
- [AQI Calculation](#aqi-calculation)
- [Application](#application)
- [Installation](#installation)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Conclusion](#conclusion)

---

## Problem

Air-quality monitors show current pollution levels but don't indicate what tomorrow's air quality will be. This project uses recent pollution patterns to forecast the next day's PM2.5 and PM10 and estimate the AQI.

---

## Data Source

**Government of Nepal Air-Quality Monitoring System**
https://pollution.gov.np/gss/api/observation

**Location:** Ratnapark monitoring station, Kathmandu (central urban area)

**Pollutants:**

- PM1 _(tested as feature, not in final models)_
- PM2.5 _(forecasted)_
- PM10 _(forecasted)_

---

## Data Processing

Raw observations are processed through:

1. Timestamp conversion (UTC)
2. Invalid value handling (`-9999` → missing)
3. Duplicate removal
4. Missing value handling
5. Daily aggregation (mean)

---

## Feature Engineering

Multiple approaches were tested:

| Feature Type    | Description                            |
| --------------- | -------------------------------------- |
| Lag Features    | Previous day values (t-1, t-2, t-3...) |
| Rolling Mean    | 3-day, 7-day, 15-day averages          |
| EWMA            | Exponentially weighted moving average  |
| Change Features | Difference between consecutive values  |
| Combined        | Mixed feature sets                     |

---

## Model Selection

Models tested: Linear Regression, Ridge, Random Forest, Gradient Boosting, Extra Trees

Evaluation metrics: **MAE**, **RMSE**, **R²**

### Final Models

| Pollutant | Features | Model             | MAE   | RMSE  | R²    |
| --------- | -------- | ----------------- | ----- | ----- | ----- |
| **PM2.5** | EWMA     | Linear Regression | 10.70 | 14.38 | 0.789 |
| **PM10**  | Change   | Extra Trees (500) | 15.18 | 20.87 | 0.808 |

**PM1 Experiment:** Tested as a feature but removed from final models due to insufficient improvement.

---

## Forecasting Pipeline

Recent Data (15 days)
↓
Data Processing
↓
Feature Engineering
↓
Trained Models
↓
PM2.5 + PM10 Forecast
↓
AQI Calculation
↓
AQI Category Display

The application downloads ~15 days of recent observations, generates required features, and forecasts the **next day only**.

---

## AQI Calculation

Predicted concentrations are converted to AQI sub-indices using breakpoint interpolation:
I = ((I_high - I_low) / (C_high - C_low)) × (C - C_low) + I_low

The highest sub-index determines the final AQI and air-quality category.

---

## Application

Built with **Python** and **Streamlit**.

---

## Installation

```bash
# Clone repository
cd ktm-aqi-forecasting

# Create virtual environment
python -m venv .aqi

# Activate (Windows)
.aqi\Scripts\activate

# Activate (Linux/macOS)
source .aqi/bin/activate

# Install dependencies
pip install -r requirements.txt

#Running app
streamlit run app.py

```

## Limitations

Single station – Ratnapark only

Limited historical data – constrains model robustness

No weather data – temperature, humidity, wind not included

One-day forecast – no multi-day predictions

PM1 excluded – tested but not beneficial enough

No uncertainty estimates – point predictions only

## Future Improvements

Collect larger historical dataset

Integrate meteorological variables (temperature, humidity, wind, rainfall, pressure)

Support multiple stations across Kathmandu Valley

Test additional models (XGBoost, LightGBM, CatBoost, LSTM, GRU)

Extend to multi-day forecasting (3–7 days)

Implement automatic model retraining with new data

Add prediction intervals/uncertainty estimates

## Conclusion

This project demonstrates an end-to-end machine learning solution for air-quality forecasting using real-world data from Nepal. The system collects observations, processes them into daily values, engineers appropriate features, applies trained models to forecast PM2.5 and PM10, and converts predictions into AQI with an air-quality category. The complete pipeline is exposed through a Streamlit web application.

# Ratnapark AQI Forecasting

Machine learning project for short-term air-quality forecasting at the
**Ratnapark monitoring station**.

## Data Source

The project uses historical air-quality data from the Department of
Environment of Nepal.

The available datasets currently used are:

- **2016–2020** historical Excel data
- **2024** Excel data
- **2025** Excel data
- Recent data from the **Nepal Air Quality Monitoring API**

## Data Extraction

The 2016–2020 and 2024–2025 datasets have different Excel structures.

The **2024 and 2025** datasets contain a dedicated `Ratnapark` sheet with
daily measurements, so the data can be extracted directly.

The **2016–2020** dataset contains the Ratnapark data in separate sections
for `PM1`, `PM2.5`, `PM10`, and `TSP`. Each pollutant contains data for
2016–2020 arranged horizontally by year. These sections are extracted,
reshaped, and combined using the date.

The extracted data is stored as raw CSV files.

**No missing values are modified or removed during extraction.**

## Ratnapark Data

The main pollutants currently available are:

| Pollutant | Description                 |
| --------- | --------------------------- |
| PM1       | Particulate matter ≤ 1 μm   |
| PM2.5     | Particulate matter ≤ 2.5 μm |
| PM10      | Particulate matter ≤ 10 μm  |
| TSP       | Total suspended particles   |

PM2.5 will be the primary variable used for the initial forecasting
experiments.

## Current Pipeline

```text
Historical Excel Data
        ↓
Ratnapark Extraction
        ↓
Raw CSV
        ↓
Missing Data Analysis
        ↓
Data Cleaning
        ↓
EDA
        ↓
Feature Engineering
        ↓
Model Training
        ↓
PM2.5 Forecast
        ↓
AQI Calculation
```

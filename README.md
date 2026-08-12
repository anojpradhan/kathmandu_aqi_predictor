# Kathmandu Valley AQI Forecasting

Machine learning project for short-term air-quality forecasting using
air-quality sensor data from Kathmandu Valley.

## Current Objective

The initial objective is to predict the next-hour PM2.5 concentration
using historical air-quality measurements.

## Current Station

Bhaisepati

### Series IDs

| Pollutant | Series ID |
| --------- | --------: |
| PM10      |       523 |
| PM1       |       524 |
| PM2.5     |       525 |

## Planned ML Pipeline

```text
Air Quality API
       ↓
Data Collection
       ↓
Data Cleaning
       ↓
Minute → Hourly Aggregation
       ↓
Feature Engineering
       ↓
Random Forest Regressor
       ↓
Next-Hour PM2.5 Prediction
       ↓
AQI Calculation
```

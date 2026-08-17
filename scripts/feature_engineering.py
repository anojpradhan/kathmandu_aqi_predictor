import pandas as pd

# PM2.5 FEATURES

PM25_FEATURES = [
    "pm2_5_ewma_3",
    "pm2_5_ewma_7",
    "pm10_ewma_3",
    "pm10_ewma_7",
]


def create_pm25_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["pm2_5_ewma_3"] = df["pm2_5"].shift(1).ewm(span=3, adjust=False).mean()

    df["pm2_5_ewma_7"] = df["pm2_5"].shift(1).ewm(span=7, adjust=False).mean()

    df["pm10_ewma_3"] = df["pm10"].shift(1).ewm(span=3, adjust=False).mean()

    df["pm10_ewma_7"] = df["pm10"].shift(1).ewm(span=7, adjust=False).mean()

    return df


# PM10 FEATURES

PM10_FEATURES = [
    "pm2_5_change_1",
    "pm2_5_change_3",
    "pm2_5_change_7",
    "pm2_5_pct_change_1",
    "pm2_5_pct_change_3",
    "pm2_5_pct_change_7",
    "pm10_change_1",
    "pm10_change_3",
    "pm10_change_7",
    "pm10_pct_change_1",
    "pm10_pct_change_3",
    "pm10_pct_change_7",
]


def create_pm10_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for pollutant in ["pm2_5", "pm10"]:
        df[f"{pollutant}_change_1"] = df[pollutant] - df[pollutant].shift(1)

        df[f"{pollutant}_change_3"] = df[pollutant] - df[pollutant].shift(3)

        df[f"{pollutant}_change_7"] = df[pollutant] - df[pollutant].shift(7)

        df[f"{pollutant}_pct_change_1"] = df[pollutant].pct_change(1)

        df[f"{pollutant}_pct_change_3"] = df[pollutant].pct_change(3)

        df[f"{pollutant}_pct_change_7"] = df[pollutant].pct_change(7)

    return df

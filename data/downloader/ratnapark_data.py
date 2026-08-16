from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://pollution.gov.np/gss/api/observation"

# Latest 15 calendar days
# August 2 through August 16, 2026
DATE_FROM = "2026-08-02T00:00:00"
DATE_TO = "2026-08-17T00:00:00"


# Ratnapark series IDs
SERIES = {
    "pm10": 3,
    "pm1": 5,
    "pm25": 4,
}


OUTPUT_DIR = Path("data/raw/ratnapark")


def download_series(name, series_id):

    print()
    print("=" * 70)
    print(f"Downloading {name.upper()}")
    print(f"Series ID: {series_id}")
    print("=" * 70)

    params = {
        "series_id": series_id,
        "date_from": DATE_FROM,
        "date_to": DATE_TO,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=60,
    )

    print("Status:", response.status_code)

    response.raise_for_status()

    result = response.json()

    if isinstance(result, dict):
        data = result.get("data", [])
    else:
        data = result

    print("Observations:", len(data))

    if not data:
        print("❌ No data found.")
        return

    print("\nFirst observation:")
    print(data[0])

    print("\nLast observation:")
    print(data[-1])

    df = pd.DataFrame(data)

    print("\nOriginal columns:")
    print(df.columns.tolist())

    # Keep required columns
    df = df[["datetime", "value"]]

    # Rename value
    df = df.rename(
        columns={
            "value": name,
        }
    )

    # Convert datetime
    df["datetime"] = pd.to_datetime(
        df["datetime"],
        utc=True,
    )

    # Convert values to numeric
    df[name] = pd.to_numeric(
        df[name],
        errors="coerce",
    )

    # Count invalid -9999 values
    invalid_count = (df[name] == -9999).sum()

    print(f"\nInvalid -9999 values: {invalid_count:,}")

    # Replace -9999 with NaN
    df.loc[
        df[name] == -9999,
        name,
    ] = pd.NA

    # Remove duplicate timestamps
    before = len(df)

    df = df.drop_duplicates(subset="datetime")

    duplicates_removed = before - len(df)

    print(f"Duplicates removed: {duplicates_removed:,}")

    # Sort chronologically
    df = df.sort_values("datetime").reset_index(drop=True)

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save CSV
    output_file = OUTPUT_DIR / f"{name}.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    print("\nSaved:")
    print(output_file)

    print("\nFinal rows:", len(df))

    print(
        "Date range:",
        df["datetime"].min(),
        "→",
        df["datetime"].max(),
    )

    print("\nMissing values:")
    print(df[name].isna().sum())


def main():

    print()
    print("RATNAPARK AIR QUALITY DATA DOWNLOADER")

    print(f"\nRequested date range:\n{DATE_FROM}\n→ {DATE_TO}")

    print("\nStation: Ratnapark")

    print("\nSeries:")
    print("PM10  → 3")
    print("PM1   → 5")
    print("PM2.5 → 4")

    for name, series_id in SERIES.items():
        download_series(
            name,
            series_id,
        )

    print()
    print("=" * 70)
    print("DOWNLOAD COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

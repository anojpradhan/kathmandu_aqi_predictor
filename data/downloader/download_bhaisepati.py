from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://pollution.gov.np/gss/api/observation"

DATE_FROM = "2026-07-27T00:00:00"
DATE_TO = "2026-08-12T00:00:00"


# Bhaisepati series
SERIES = {
    "pm10": 523,
    "pm1": 524,
    "pm25": 525,
}


OUTPUT_DIR = Path("data/raw/bhaisepati")


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
    df = df.rename(columns={"value": name})

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

    # remove invalid count
    invalid_count = (df[name] == -9999).sum()

    print(f"\nInvalid -9999 values: {invalid_count:,}")

    df.loc[df[name] == -9999, name] = pd.NA

    # removeduplicates

    before = len(df)

    df = df.drop_duplicates(subset="datetime")

    duplicates_removed = before - len(df)

    print(f"Duplicates removed: {duplicates_removed:,}")

    # sort values

    df = df.sort_values("datetime")

    # createdirectory

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    # saving

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


def main():

    print()
    print("BHAISEPATI AIR QUALITY DATA DOWNLOADER")

    print(f"\nDate range:\n{DATE_FROM}\n→ {DATE_TO}")

    for name, series_id in SERIES.items():
        download_series(
            name,
            series_id,
        )

    print()
    print("DOWNLOAD COMPLETE")


if __name__ == "__main__":
    main()

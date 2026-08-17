from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://pollution.gov.np/gss/api/observation"

SERIES = {
    "pm10": 3,
    "pm1": 5,
    "pm25": 4,
}

OUTPUT_DIR = Path("data/live/ratnapark")


def get_date_range():
    today = datetime.now(timezone.utc).date()

    date_from = today - timedelta(days=15)
    date_to = today + timedelta(days=1)

    return (
        f"{date_from}T00:00:00",
        f"{date_to}T00:00:00",
    )


def download_series(name, series_id, date_from, date_to):

    params = {
        "series_id": series_id,
        "date_from": date_from,
        "date_to": date_to,
    }

    print(f"Downloading {name.upper()} ({date_from} → {date_to})")

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=60,
    )

    response.raise_for_status()

    result = response.json()

    if isinstance(result, dict):
        data = result.get("data", [])
    else:
        data = result

    if not data:
        raise RuntimeError(f"No data returned for {name}")

    df = pd.DataFrame(data)

    df = df[["datetime", "value"]].copy()

    df = df.rename(columns={"value": name})

    df["datetime"] = pd.to_datetime(
        df["datetime"],
        utc=True,
    )

    df[name] = pd.to_numeric(
        df[name],
        errors="coerce",
    )

    # Replace API invalid value
    df.loc[df[name] == -9999, name] = pd.NA

    # Remove duplicate timestamps
    df = (
        df.drop_duplicates(subset="datetime")
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = OUTPUT_DIR / f"{name}.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    print(f"Saved {output_file} ({len(df):,} rows)")

    return df


def download_current_data():

    date_from, date_to = get_date_range()

    print("=" * 70)
    print("RATNAPARK CURRENT DATA")
    print("=" * 70)

    print("From:", date_from)
    print("To:  ", date_to)

    for name, series_id in SERIES.items():
        download_series(
            name=name,
            series_id=series_id,
            date_from=date_from,
            date_to=date_to,
        )


if __name__ == "__main__":
    download_current_data()

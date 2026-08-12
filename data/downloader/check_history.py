import requests

URL = "https://pollution.gov.np/gss/api/observation"


DATE_FROM = "2026-07-26T00:00:00"
DATE_TO = "2026-08-12T00:00:00"


STATIONS = {
    "Bhaisepati": {
        "PM10": 523,
        "PM1": 524,
        "PM2.5": 525,
    },
    "Bhaktapur": {
        "PM10": 501,
        "PM1": 502,
        "PM2.5": 503,
    },
    "Khumaltar": {
        "PM10": 2480,
        "PM1": 2481,
        "PM2.5": 2482,
    },
    "Pulchowk": {
        "PM10": 92,
        "PM1": 95,
        "PM2.5": 98,
    },
    "TU Kirtipur": {
        "PM10": 478,
        "PM1": 479,
        "PM2.5": 480,
    },
    "Ratnapark": {
        "PM10": 3,
        "PM1": 5,
        "PM2.5": 4,
    },
    "Shankapark": {
        "PM10": 546,
        "PM1": 544,
        "PM2.5": 542,
    },
}


def check_series(station, pollutant, series_id):

    params = {
        "series_id": series_id,
        "date_from": DATE_FROM,
        "date_to": DATE_TO,
    }

    try:
        response = requests.get(
            URL,
            params=params,
            timeout=60,
        )

        response.raise_for_status()

        result = response.json()

        # API returns a dictionary containing "data"
        if isinstance(result, dict):
            data = result.get("data", [])
        else:
            data = result

        count = len(data)

        if count > 0:
            print(f"  {pollutant:<6} Series {series_id:<4} ✅ {count:,} observations")

            # Show first and last observation
            print(f"           FIRST: {data[0]}")
            print(f"           LAST:  {data[-1]}")

        else:
            print(f"  {pollutant:<6} Series {series_id:<4} ❌ No data")

        return count

    except requests.RequestException as error:
        print(f"  {pollutant:<6} Series {series_id:<4} ⚠️ ERROR: {error}")

        return -1


def main():

    print()

    print("=" * 70)
    print("KATHMANDU VALLEY AIR QUALITY DATA CHECK")
    print("=" * 70)

    print(f"\nDate from: {DATE_FROM}")
    print(f"Date to:   {DATE_TO}")

    total_series = 0
    series_with_data = 0
    series_without_data = 0
    series_with_error = 0

    print()
    for station, pollutants in STATIONS.items():
        print("-" * 70)
        print(station)
        print("-" * 70)

        for pollutant, series_id in pollutants.items():
            total_series += 1

            count = check_series(
                station,
                pollutant,
                series_id,
            )

            if count > 0:
                series_with_data += 1

            elif count == 0:
                series_without_data += 1

            else:
                series_with_error += 1

    print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"\nTotal series checked: {total_series}")
    print(f"Series with data:     {series_with_data}")
    print(f"Series without data:  {series_without_data}")
    print(f"Series with errors:   {series_with_error}")

    print()

    print("=" * 70)


if __name__ == "__main__":
    main()

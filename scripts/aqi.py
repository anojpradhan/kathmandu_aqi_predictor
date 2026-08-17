# AQI CALCULATION

# AQI breakpoint ranges
AQI_BREAKPOINTS = [
    (0, 50),
    (51, 100),
    (101, 150),
    (151, 200),
    (201, 300),
    (301, 400),
    (401, 500),
]


# PM2.5 concentration breakpoints (µg/m³)
PM25_BREAKPOINTS = [
    (0.0, 15.4),
    (15.5, 40.4),
    (40.5, 65.4),
    (65.5, 150.4),
    (150.5, 250.4),
    (250.5, 350.4),
    (350.5, 500.4),
]


# PM10 concentration breakpoints (µg/m³)
PM10_BREAKPOINTS = [
    (0.0, 54),
    (55, 154),
    (155, 254),
    (255, 354),
    (355, 424),
    (425, 504),
    (505, 604),
]


# SUB-INDEX


def calculate_sub_index(
    concentration: float,
    concentration_breakpoints,
) -> float:

    if concentration < 0:
        raise ValueError("Pollutant concentration cannot be negative.")

    for index, (
        concentration_low,
        concentration_high,
    ) in enumerate(concentration_breakpoints):
        if concentration_low <= concentration <= concentration_high:
            aqi_low, aqi_high = AQI_BREAKPOINTS[index]

            sub_index = (
                (aqi_high - aqi_low) / (concentration_high - concentration_low)
            ) * (concentration - concentration_low) + aqi_low

            return round(sub_index)

    # Above highest breakpoint
    highest_concentration = concentration_breakpoints[-1][1]

    if concentration > highest_concentration:
        return 500

    raise ValueError("Unable to calculate AQI sub-index.")


# PM2.5 SUB-INDEX


def calculate_pm25_sub_index(
    pm25: float,
) -> int:

    return calculate_sub_index(
        pm25,
        PM25_BREAKPOINTS,
    )


# PM10 SUB-INDEX


def calculate_pm10_sub_index(
    pm10: float,
) -> int:

    return calculate_sub_index(
        pm10,
        PM10_BREAKPOINTS,
    )


# AQI CATEGORY


def get_aqi_category(
    aqi: int,
) -> str:

    if aqi <= 50:
        return "Good"

    if aqi <= 100:
        return "Moderate"

    if aqi <= 150:
        return "Unhealthy for Sensitive Groups"

    if aqi <= 200:
        return "Unhealthy"

    if aqi <= 300:
        return "Very Unhealthy"

    if aqi <= 400:
        return "Hazardous"

    return "Very Hazardous"


# COMPLETE AQI CALCULATION


def calculate_aqi(
    pm25: float,
    pm10: float,
) -> dict:

    pm25_sub_index = calculate_pm25_sub_index(pm25)

    pm10_sub_index = calculate_pm10_sub_index(pm10)

    aqi = max(
        pm25_sub_index,
        pm10_sub_index,
    )

    if pm25_sub_index >= pm10_sub_index:
        dominant_pollutant = "PM2.5"
    else:
        dominant_pollutant = "PM10"

    category = get_aqi_category(aqi)

    return {
        "pm2_5_sub_index": pm25_sub_index,
        "pm10_sub_index": pm10_sub_index,
        "aqi": aqi,
        "category": category,
        "dominant_pollutant": dominant_pollutant,
    }

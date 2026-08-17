import streamlit as st

from scripts.aqi import calculate_aqi
from scripts.forecasting import forecast_tomorrow

# PAGE CONFIG

st.set_page_config(
    page_title="Kathmandu AQI Forecast",
    layout="wide",
)


# HEADER

st.title("Kathmandu Air Quality Forecast")

st.subheader("Ratnapark Monitoring Station")

st.write(
    "Forecast tomorrow's PM2.5 and PM10 concentrations "
    "using machine-learning models trained on historical "
    "air-quality data."
)


st.divider()


# FORECAST BUTTON

if st.button(
    " Forecast Tomorrow",
    type="primary",
    use_container_width=True,
):
    with st.spinner("Downloading latest data and generating forecast..."):
        try:
            forecast = forecast_tomorrow()

            # Calculate AQI from predictions
            aqi_result = calculate_aqi(
                pm25=forecast["pm2_5"],
                pm10=forecast["pm10"],
            )

            # Combine results
            result = {
                **forecast,
                **aqi_result,
            }

            st.session_state["forecast"] = result

        except Exception as e:
            st.error(f"Forecast failed: {e}")


# DISPLAY FORECAST

if "forecast" in st.session_state:
    forecast = st.session_state["forecast"]

    st.divider()

    st.header("Tomorrow's Forecast")

    st.write(f"Forecast date: **{forecast['forecast_date']}**")

    # Pollutant predictions

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="PM2.5",
            value=(f"{forecast['pm2_5']:.2f} µg/m³"),
        )

    with col2:
        st.metric(
            label="PM10",
            value=(f"{forecast['pm10']:.2f} µg/m³"),
        )

    st.divider()

    # AQI

    st.header("Predicted AQI")

    aqi_col, category_col = st.columns(2)

    with aqi_col:
        st.metric(
            label="AQI",
            value=forecast["aqi"],
        )

    with category_col:
        st.metric(
            label="Air Quality",
            value=forecast["category"],
        )

    # Sub-indices

    st.subheader("AQI Sub-index Breakdown")

    sub_col1, sub_col2 = st.columns(2)

    with sub_col1:
        st.metric(
            label="PM2.5 Sub-index",
            value=forecast["pm2_5_sub_index"],
        )

    with sub_col2:
        st.metric(
            label="PM10 Sub-index",
            value=forecast["pm10_sub_index"],
        )

    st.write(f"**Dominant pollutant:** {forecast['dominant_pollutant']}")

    st.divider()

    st.info("The AQI is determined by the highest predicted pollutant sub-index.")


# FOOTER

st.divider()

st.caption("Data source: Government of Nepal air-quality observation API")

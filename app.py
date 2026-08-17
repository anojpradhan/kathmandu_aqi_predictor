import streamlit as st

from scripts.forecasting import forecast_tomorrow

# PAGE CONFIG

st.set_page_config(
    page_title="Ratnapark AQI Forecast",
    layout="wide",
)


# HEADER

st.title("Ratnapark Air Quality Forecast")

st.subheader("Ratnapark Monitoring Station")

st.write(
    "Forecast tomorrow's PM2.5 and PM10 concentrations "
    "using machine-learning models trained on historical "
    "air-quality data."
)


st.divider()


# FORECAST BUTTON

if st.button(
    "Forecast Tomorrow",
    type="primary",
    use_container_width=True,
):
    with st.spinner("Downloading latest air-quality data and generating forecast..."):
        try:
            result = forecast_tomorrow()

            st.session_state["forecast"] = result

        except Exception as e:
            st.error(f"Forecast failed: {e}")


# DISPLAY FORECAST

if "forecast" in st.session_state:
    forecast = st.session_state["forecast"]

    st.divider()

    st.header("Tomorrow's Forecast")

    st.write(f"Forecast date: **{forecast['forecast_date']}**")

    col1, col2 = st.columns(2)

    # PM2.5

    with col1:
        st.metric(
            label="PM2.5",
            value=f"{forecast['pm2_5']:.2f} µg/m³",
        )

    # PM10

    with col2:
        st.metric(
            label="PM10",
            value=f"{forecast['pm10']:.2f} µg/m³",
        )

    st.divider()

    st.info(
        "The forecast is generated using the latest "
        "available Ratnapark air-quality observations."
    )


# INFORMATION

st.divider()

st.caption("Data source: Government of Nepal air-quality observation API")

import os
from datetime import datetime
import requests
import streamlit as st

st.set_page_config(page_title="Live Weather App", page_icon="🌦️", layout="centered")

st.title("🌦️ Live Weather App")
st.write("Check current temperature, humidity, wind, and a multi-day forecast for a city.")
st.caption("Powered by OpenWeather. Add your API key in the sidebar or configure it as a Streamlit secret.")

def get_api_key():
    try:
        secret_key = st.secrets.get("OPENWEATHER_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("OPENWEATHER_API_KEY", "")

with st.sidebar:
    st.header("API configuration")
    api_key = st.text_input(
        "OpenWeather API key",
        value=get_api_key(),
        type="password",
        help="Your key is kept out of the source code. For a public deployment, use Streamlit Secrets.",
    )
    st.markdown("[Get a free API key from OpenWeather](https://openweathermap.org/api)")
    st.caption("New keys may take a little time to become active.")

city = st.text_input("Enter city", value="Pune", placeholder="e.g., Mumbai, London, Tokyo")
units_label = st.radio("Temperature units", ["Celsius (°C)", "Fahrenheit (°F)"], horizontal=True)
units = "metric" if units_label.startswith("Celsius") else "imperial"
temp_unit = "°C" if units == "metric" else "°F"
speed_unit = "m/s" if units == "metric" else "mph"

def request_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 401:
            raise RuntimeError("The API key is invalid or not active yet. Check your key and try again later.")
        if response.status_code == 404:
            raise RuntimeError("City not found. Check the spelling and try again.")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("The weather service timed out. Please try again.") from exc
    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f"Weather API returned an HTTP error: {exc}") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Could not connect to the weather service: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError("The service returned an unreadable JSON response.") from exc

def fetch_weather(city_name, key, units):
    current = request_json(
        "https://api.openweathermap.org/data/2.5/weather",
        {"q": city_name, "appid": key, "units": units},
    )
    forecast = request_json(
        "https://api.openweathermap.org/data/2.5/forecast",
        {"q": city_name, "appid": key, "units": units},
    )
    return current, forecast

if st.button("Get weather", type="primary", use_container_width=True):
    if not city.strip():
        st.warning("Please enter a city name.")
    elif not api_key.strip():
        st.warning("Please enter your OpenWeather API key in the sidebar first.")
    else:
        with st.spinner(f"Fetching live weather for {city.strip()}..."):
            try:
                current, forecast = fetch_weather(city.strip(), api_key.strip(), units)
                st.session_state["weather_current"] = current
                st.session_state["weather_forecast"] = forecast
                st.session_state["weather_city"] = city.strip()
                st.session_state["weather_units"] = units
                st.session_state["weather_temp_unit"] = temp_unit
                st.session_state["weather_speed_unit"] = speed_unit
            except RuntimeError as error:
                st.error(str(error))

if "weather_current" in st.session_state:
    current = st.session_state["weather_current"]
    forecast = st.session_state["weather_forecast"]
    saved_units = st.session_state["weather_units"]
    saved_temp_unit = st.session_state["weather_temp_unit"]
    saved_speed_unit = st.session_state["weather_speed_unit"]
    weather = current.get("weather", [{}])[0]
    st.subheader(f"{current.get('name', st.session_state['weather_city'])}, {current.get('sys', {}).get('country', '')}")
    st.caption(f"Current conditions · {datetime.now().strftime('%d %b %Y, %I:%M %p')} (your local display time)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{current.get('main', {}).get('temp', '—')}{saved_temp_unit}")
    col2.metric("Feels like", f"{current.get('main', {}).get('feels_like', '—')}{saved_temp_unit}")
    col3.metric("Humidity", f"{current.get('main', {}).get('humidity', '—')}%")
    col4, col5 = st.columns(2)
    col4.metric("Wind speed", f"{current.get('wind', {}).get('speed', '—')} {saved_speed_unit}")
    col5.metric("Pressure", f"{current.get('main', {}).get('pressure', '—')} hPa")
    st.markdown(f"### {weather.get('description', 'Weather').title()}")
    st.write(f"Cloud cover: {current.get('clouds', {}).get('all', '—')}%")

    st.subheader("Forecast")
    st.caption("The API provides forecasts in 3-hour intervals. The table below shows one reading per day for the next five days.")
    daily = {}
    for item in forecast.get("list", []):
        day = item.get("dt_txt", "").split(" ")[0]
        if not day:
            continue
        # Select the forecast reading closest to 12:00 for each day.
        hour = int(item.get("dt_txt", "00:00").split(" ")[1].split(":")[0])
        if day not in daily or abs(hour - 12) < abs(daily[day]["hour"] - 12):
            daily[day] = {"item": item, "hour": hour}
    rows = []
    for day, entry in list(daily.items())[:5]:
        item = entry["item"]
        details = item.get("weather", [{}])[0]
        rows.append({
            "Date": day,
            "Forecast": details.get("description", "").title(),
            f"Temp ({saved_temp_unit})": item.get("main", {}).get("temp"),
            "Humidity (%)": item.get("main", {}).get("humidity"),
            f"Wind ({saved_speed_unit})": item.get("wind", {}).get("speed"),
        })
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Forecast data was not available for this city.")
    st.caption("Weather and forecast values are supplied by OpenWeather and may change.")

with st.expander("How this project works"):
    st.markdown(
        "1. The app sends REST API requests with `requests`.\n"
        "2. It checks HTTP status codes and handles network errors.\n"
        "3. It parses the JSON response returned by OpenWeather.\n"
        "4. It displays current conditions and forecast readings in Streamlit.\n\n"
        "**Security:** Do not put your API key in `app.py` or commit it to GitHub. "
        "For a deployed app, add `OPENWEATHER_API_KEY` under Streamlit app Secrets."
    )

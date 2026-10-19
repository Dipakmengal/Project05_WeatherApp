# Project 05 — Live Weather App

A Python weather application built with **Requests**, **OpenWeather API**, and **Streamlit**. Search for a city to view current temperature, feels-like temperature, humidity, wind speed, pressure, cloud cover, and a five-day forecast based on available forecast intervals.

## 🚀 Live Demo



**[Open Live Demo](https://project05weatherapp-7w7jcwbngrs7sumgwmt7cy.streamlit.app/)**

## Features

- Live current weather for a user-entered city.
- Temperature in Celsius or Fahrenheit.
- Humidity, feels-like temperature, wind speed, pressure, and cloud cover.
- Multi-day forecast table.
- REST API calls using Requests.
- JSON response parsing.
- Handles invalid API keys, unknown cities, timeouts, and connection/API errors.
- Streamlit web interface that works in a browser.

## Technologies

- Python
- Requests
- OpenWeather API
- Streamlit
- JSON

## 1. Get an OpenWeather API key

1. Create an account at [OpenWeather](https://openweathermap.org/).
2. Generate an API key in your account.
3. New keys may take some time to activate.
4. Never commit your API key to GitHub.

## 2. Run locally on Windows

1. Download or clone this repository and open PowerShell in the project folder.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

4. Open the local URL printed in PowerShell, usually `http://localhost:8501`.
5. Enter your OpenWeather API key in the sidebar, enter a city, and click **Get weather**.

## 3. Upload to GitHub

Create a public repository named `Project05_WeatherApp` and upload:

```text
Project05_WeatherApp/
├── app.py
├── requirements.txt
└── README.md
```

## 4. Deploy a public live demo

1. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
2. Create a new app from your repository.
3. Select branch `main` and main file path `app.py`.
4. Before deploying or opening the deployed app, configure the API key in **App settings → Secrets**:

   ```toml
   OPENWEATHER_API_KEY = "paste-your-own-api-key-here"
   ```

5. Deploy the app. Copy the generated `.streamlit.app` URL and replace the live-demo placeholder at the top of this README.

Do not paste your real API key into the README, source code, screenshots, or a public GitHub commit. If a key is accidentally exposed, revoke it and create a replacement.

## API endpoints used

- Current weather: `https://api.openweathermap.org/data/2.5/weather`
- 5-day / 3-hour forecast: `https://api.openweathermap.org/data/2.5/forecast`

Access to endpoints and request limits depend on your OpenWeather account and plan. Check the current OpenWeather documentation and your account dashboard for API availability.

## Learning outcomes

- Calling REST APIs with Requests.
- Reading and validating JSON responses.
- Handling HTTP errors and network timeouts.
- Displaying real-world API data in a Python user interface.
- Protecting API credentials when publishing a project.

## Author

**Dipak Mengal**

GitHub: https://github.com/Dipakmengal

## Educational use

Created as an internship learning project.

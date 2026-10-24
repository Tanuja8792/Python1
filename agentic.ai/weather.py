
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0f6075, #62c5d5);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 25px;
        }

        .container {
            width: 100%;
            max-width: 650px;
            background: white;
            padding: 35px;
            border-radius: 22px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
        }

        h1 {
            text-align: center;
            color: #0f6075;
            margin-bottom: 8px;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 28px;
        }

        form {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 14px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 16px;
        }

        button {
            padding: 14px 20px;
            background: #0f6075;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 15px;
        }

        button:hover {
            background: #094655;
        }

        .weather-card {
            margin-top: 28px;
            padding: 25px;
            background: #edfaff;
            border-radius: 16px;
            text-align: center;
        }

        .city {
            color: #0f6075;
            font-size: 25px;
            font-weight: bold;
        }

        .temperature {
            font-size: 55px;
            font-weight: bold;
            color: #222;
            margin: 15px 0;
        }

        .condition {
            color: #555;
            font-size: 18px;
        }

        .details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 25px;
        }

        .detail {
            background: white;
            padding: 16px 10px;
            border-radius: 12px;
            border: 1px solid #dceef2;
        }

        .detail p {
            margin: 6px 0;
        }

        .label {
            color: #777;
            font-size: 14px;
        }

        .value {
            color: #0f6075;
            font-size: 19px;
            font-weight: bold;
        }

        .message {
            margin-top: 20px;
            padding: 12px;
            background: #fff2f0;
            color: #b42318;
            border-radius: 8px;
            text-align: center;
        }

        footer {
            margin-top: 25px;
            text-align: center;
            font-size: 13px;
            color: #888;
        }

        @media (max-width: 480px) {
            .container {
                padding: 22px;
            }

            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }

            .temperature {
                font-size: 45px;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>🌤 Weather Dashboard</h1>
        <p class="subtitle">Discover the weather in any city</p>

        <form method="POST">
            <input
                type="text"
                name="city"
                placeholder="Enter city name"
                value="{{ city }}"
                required
            >
            <button type="submit">Search Weather</button>
        </form>

        {% if weather %}
        <div class="weather-card">
            <div class="city">📍 {{ weather.city }}</div>

            <div class="temperature">
                {{ weather.temperature }}°C
            </div>

            <div class="condition">
                {{ weather.condition }}
            </div>

            <div class="details">
                <div class="detail">
                    <p>💧 Humidity</p>
                    <p class="value">{{ weather.humidity }}%</p>
                </div>

                <div class="detail">
                    <p>💨 Wind Speed</p>
                    <p class="value">{{ weather.wind }} km/h</p>
                </div>

                <div class="detail">
                    <p>🌡 Feels Like</p>
                    <p class="value">{{ weather.feels_like }}°C</p>
                </div>

                <div class="detail">
                    <p>🕒 Local Time</p>
                    <p class="value">{{ weather.time }}</p>
                </div>
            </div>
        </div>
        {% endif %}

        {% if error %}
        <div class="message">{{ error }}</div>
        {% endif %}

        <footer>
            Weather data powered by Open-Meteo
        </footer>
    </div>
</body>
</html>
"""

def get_condition(code):
    conditions = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤",
        2: "Partly Cloudy ⛅",
        3: "Overcast ☁️",
        45: "Foggy 🌫",
        48: "Foggy 🌫",
        51: "Light Drizzle 🌦",
        53: "Drizzle 🌦",
        55: "Heavy Drizzle 🌧",
        61: "Light Rain 🌧",
        63: "Moderate Rain 🌧",
        65: "Heavy Rain 🌧",
        71: "Light Snow ❄️",
        73: "Snowfall ❄️",
        75: "Heavy Snow ❄️",
        80: "Rain Showers 🌦",
        81: "Rain Showers 🌧",
        82: "Heavy Rain Showers 🌧",
        95: "Thunderstorm ⛈",
        96: "Thunderstorm with Hail ⛈",
        99: "Thunderstorm with Hail ⛈"
    }
    return conditions.get(code, "Weather information unavailable")


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        else:
            try:
                # Find the city's latitude and longitude
                geo_response = requests.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={"name": city, "count": 1, "language": "en"},
                    timeout=10
                )
                geo_response.raise_for_status()
                geo_data = geo_response.json()

                if not geo_data.get("results"):
                    error = "City not found. Please check the spelling."
                else:
                    place = geo_data["results"][0]
                    latitude = place["latitude"]
                    longitude = place["longitude"]

                    # Get current weather
                    response = requests.get(
                        "https://api.open-meteo.com/v1/forecast",
                        params={
                            "latitude": latitude,
                            "longitude": longitude,
                            "current": (
                                "temperature_2m,relative_humidity_2m,"
                                "apparent_temperature,is_day,weather_code,"
                                "wind_speed_10m"
                            ),
                            "timezone": "auto"
                        },
                        timeout=10
                    )
                    response.raise_for_status()
                    data = response.json()

                    current = data["current"]

                    weather = {
                        "city": place["name"] + (
                            ", " + place["country"]
                            if place.get("country") else ""
                        ),
                        "temperature": current["temperature_2m"],
                        "humidity": current["relative_humidity_2m"],
                        "feels_like": current["apparent_temperature"],
                        "wind": current["wind_speed_10m"],
                        "condition": get_condition(
                            current["weather_code"]
                        ),
                        "time": current["time"].split("T")[-1]
                    }

            except requests.RequestException:
                error = "Unable to get weather data. Please try again."
            except (KeyError, ValueError, TypeError):
                error = "Weather data could not be processed."

    return render_template_string(
        HTML_PAGE, city=city, weather=weather, error=error
    )


if __name__ == "__main__":
    app.run(debug=True)

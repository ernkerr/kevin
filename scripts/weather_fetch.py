#!/usr/bin/env python3
"""Shared weather fetcher using Open-Meteo."""

import json
import sys
import urllib.request
from datetime import datetime

LAT = 37.9998
LON = -121.5735

BASE_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    "&current=temperature_2m,apparent_temperature,wind_speed_10m,wind_direction_10m,"
    "relative_humidity_2m,precipitation,weather_code,cloud_cover,is_day"
    "&daily=sunrise,sunset&timezone=auto"
)

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light showers",
    81: "Moderate showers",
    82: "Violent showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


def fetch_weather(lat: float = LAT, lon: float = LON) -> dict:
    url = BASE_URL.format(lat=lat, lon=lon)
    with urllib.request.urlopen(url) as resp:
        data = json.load(resp)
    current = data["current"]
    weather_code = current.get("weather_code")
    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "timestamp": current.get("time"),
        "temperature_c": current.get("temperature_2m"),
        "feels_like_c": current.get("apparent_temperature"),
        "wind_speed_kmh": current.get("wind_speed_10m"),
        "wind_direction_deg": current.get("wind_direction_10m"),
        "humidity_pct": current.get("relative_humidity_2m"),
        "precipitation_mm": current.get("precipitation"),
        "cloud_cover_pct": current.get("cloud_cover"),
        "is_day": bool(current.get("is_day")),
        "condition": WEATHER_CODES.get(weather_code, f"Code {weather_code}"),
        "sunrise": data["daily"]["sunrise"][0],
        "sunset": data["daily"]["sunset"][0],
    }


def main():
    data = fetch_weather()
    json.dump(data, sys.stdout, indent=2)


if __name__ == "__main__":
    main()

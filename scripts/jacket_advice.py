#!/usr/bin/env python3
"""Return jacket recommendation based on current weather."""

import json
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
FETCHER = SCRIPTS_DIR / "weather_fetch.py"

# Thresholds
TEMP_CHILLY = 15  # below this adds jacket pressure
TEMP_COLD = 10    # strong jacket push
WIND_BREEZE = 15  # km/h where wind matters
PRECIP_LIGHT = 0.3  # mm/hr


def score_jacket(temp_c: float, wind_kmh: float, precip_mm: float) -> float:
    score = 0.0
    if temp_c < TEMP_CHILLY:
        score += (TEMP_CHILLY - temp_c) * 0.5
    if temp_c < TEMP_COLD:
        score += (TEMP_COLD - temp_c) * 0.5
    if wind_kmh > WIND_BREEZE:
        score += (wind_kmh - WIND_BREEZE) * 0.08
    if precip_mm:
        score += max(precip_mm, PRECIP_LIGHT) * 3
    return score


def classify(score: float) -> dict:
    if score >= 8:
        return {"recommend": True, "strength": "definitely", "emoji": "🧥"}
    if score >= 4:
        return {"recommend": True, "strength": "probably", "emoji": "🧢"}
    if score <= 1:
        return {"recommend": False, "strength": "no", "emoji": "😎"}
    return {"recommend": False, "strength": "maybe", "emoji": "🤔"}


def build_message(weather: dict, verdict: dict) -> str:
    temp = weather["temperature_c"]
    feels = weather["feels_like_c"]
    wind = weather["wind_speed_kmh"]
    condition = weather["condition"].lower()
    precip = weather["precipitation_mm"]

    pieces = [
        f"It’s {temp:.0f}°C (feels {feels:.0f}°C)",
        f"{condition}",
        f"winds {wind:.0f} km/h",
    ]
    if precip:
        pieces.append(f"precip {precip:.1f} mm")
    summary = ", ".join(pieces)

    if verdict["recommend"]:
        detail = {
            "definitely": "Definitely grab a jacket",
            "probably": "I’d grab a light layer",
        }[verdict["strength"]]
    else:
        detail = {
            "no": "You’re fine without one",
            "maybe": "Could go either way",
        }[verdict["strength"]]

    return f"{verdict['emoji']} {detail}. {summary}."


def main():
    raw = subprocess.check_output([str(FETCHER)])
    weather = json.loads(raw)
    score = score_jacket(
        weather["temperature_c"],
        weather["wind_speed_kmh"],
        weather["precipitation_mm"],
    )
    verdict = classify(score)
    print(json.dumps({
        "weather": weather,
        "score": score,
        "verdict": verdict,
        "message": build_message(weather, verdict)
    }, indent=2))


if __name__ == "__main__":
    main()

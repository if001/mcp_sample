import requests
from datetime import datetime
import pytz
import os
from typing import Dict

from dotenv import load_dotenv
load_dotenv(verbose=True)

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather_service")

# API_KEY = "YOUR_API_KEY"
API_KEY = os.environ.get("API_KEY")

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@mcp.tool(
        description="1時間ごとの指定した都市(なければ東京)の天気を取得"
)
def get_hourly_weather(city_name=None) -> Dict:
    """1時間ごとの指定した都市(なければ東京)の天気を取得"""
    print('call get_hourly_weather...')

    if not city_name:
        city_name = "Tokyo"

    # 都市名から緯度経度を取得
    geo_params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }
    geo_response = requests.get(GEOCODE_URL, params=geo_params)
    geo_data = geo_response.json()

    if not geo_data:
        raise ValueError("都市名が見つかりませんでした")

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # 天気データ取得（1時間ごとの情報を含む）
    weather_params = {
        "lat": lat,
        "lon": lon,
        "exclude": "current,minutely,daily,alerts",
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }
    weather_response = requests.get(ONECALL_URL, params=weather_params)
    weather_data = weather_response.json()

    timezone = weather_data.get("timezone", "Asia/Tokyo")
    tz = pytz.timezone(timezone)
    today = datetime.now(tz).date()

    hourly_weather = []
    for hour_data in weather_data.get("hourly", []):
        dt = datetime.fromtimestamp(hour_data["dt"], tz)
        if dt.date() == today:
            hourly_weather.append({
                "time": dt.strftime("%H:%M"),
                "temp": hour_data["temp"],
                "weather": hour_data["weather"][0]["description"]
            })
    # result = f"{city_name}の天気は以下です。\n" + "\n---\n".join(hourly_weather)
    return {
        "city": city_name,
        "hourly_weather": hourly_weather
    }

@mcp.tool(description="現在の天気を取得")
def get_current_weather(city_name=None):
    if not city_name:
        city_name = "Tokyo"

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ja"
    }

    response = requests.get(CURRENT_WEATHER_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        raise Exception(f"エラーが発生しました: {data.get('message', '不明なエラー')}")

    weather_info = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
    return weather_info

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
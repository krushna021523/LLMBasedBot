import httpx
import os
from typing import Dict, Optional

async def get_weather(city: str) -> Dict:
    """
    Fetch current weather for a given city.
    
    Args:
        city: Name of the city
        
    Returns:
        Dictionary containing weather information
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {"error": "WEATHER_API_KEY not set. Please set it in .env file"}
    
    # Using OpenWeatherMap API (free tier available)
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }
            else:
                return {"error": f"Weather API returned status {response.status_code}"}
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}
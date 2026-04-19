from mcp.server.fastmcp import FastMCP
import aiohttp
import json
from datetime import datetime

mcp = FastMCP("weatherServer")

@mcp.tool()
async def query_weather(city: str) -> str:
    """
    Input a city name, return current weather results.
    :param location: city name
    :return: current weather results in predefined format
     {
        "location": "city name",
        "temperature": "current temperature",
        "condition": "current weather condition"
    }
     Note: the temperature should be in Celsius and the condition should be a brief description like "sunny", "cloudy", "rainy", etc.
     You can use any public weather API to get the current weather information, but make sure to handle API keys securely if required.
     If the city name is invalid or the weather information cannot be retrieved, return an appropriate error message.
    """
    data = await fetch_weather(city=city)
    if "error" in data:
        return data["error"]
    
    season = get_current_season()
    tips = await get_weather_tips(season)
    data["season"] = season
    data["tips"] = tips
    return format_weather(data)

@mcp.tool()
async def get_weather_tips(season: str) -> str:
    """
    Input a season, return weather-related tips for that season.
    :param season: season name (e.g., "spring", "summer", "autumn", "winter")
    :return: weather-related tips for the given season
     For example:
     - Spring: "Carry an umbrella as spring can be rainy. Wear layers as temperatures can vary."
     - Summer: "Stay hydrated and wear sunscreen to protect against sunburn."
     - Autumn: "Wear a light jacket as temperatures can be cool. Watch out for slippery leaves."
     - Winter: "Dress warmly in layers and be cautious of icy roads."
    If the season name is invalid, return an appropriate error message.
    """
    tips = {
        "spring": "Carry an umbrella as spring can be rainy. Wear layers as temperatures can vary.",
        "summer": "Stay hydrated and wear sunscreen to protect against sunburn.",
        "autumn": "Wear a light jacket as temperatures can be cool. Watch out for slippery leaves.",
        "winter": "Dress warmly in layers and be cautious of icy roads."
    }
    return tips.get(season.lower(), "Invalid season name. Please enter 'spring', 'summer', 'autumn', or 'winter'.") 

def get_current_season() -> str:
    """Return meteorological season based on current month (Northern Hemisphere)"""
    month = datetime.now().month
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        return "winter"
    
async def fetch_weather(city: str) -> dict:
    """
    Fetch weather data from Open-Meteo API (free, no API key required).
    """
    try:
        # First, get coordinates from city name using geocoding
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(geocode_url) as resp:
                geo_data = await resp.json()
                
                if not geo_data.get("results"):
                    return {"error": f"City '{city}' not found"}
                
                location = geo_data["results"][0]
                lat = location["latitude"]
                lon = location["longitude"]
                city_name = location["name"]
                
                # Now fetch weather data
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&temperature_unit=celsius"
                
                async with session.get(weather_url) as weather_resp:
                    weather_data = await weather_resp.json()
                    current = weather_data["current"]
                    
                    return {
                        "location": city_name,
                        "temperature": current["temperature_2m"],
                        "condition": decode_weather_code(current["weather_code"])
                    }
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}

def decode_weather_code(code: int) -> str:
    """Convert WMO weather codes to descriptions."""
    codes = {
        0: "sunny", 1: "mainly clear", 2: "partly cloudy", 3: "cloudy",
        45: "foggy", 48: "foggy", 51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
        61: "light rain", 63: "rain", 65: "heavy rain", 71: "light snow", 73: "snow",
        75: "heavy snow", 80: "light showers", 81: "showers", 82: "heavy showers",
        85: "light snow showers", 86: "snow showers", 95: "thunderstorm"
    }
    return codes.get(code, "unknown")

def format_weather(data: dict) -> str:
    """Format weather data as JSON string."""
    return json.dumps(data)

if __name__ == "__main__":
    mcp.run(transport="stdio")
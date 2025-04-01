from dotenv import load_dotenv
import requests
import os

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

def getWeather(userInput):
    location = None
    words = userInput.split()
    highestIndex = 0
        
    for i, word in enumerate(words):
        if word == "in":
            if i > highestIndex:
                highestIndex = i

    if highestIndex > 0:
        location = " ".join(words[highestIndex + 1:])
    else:
        return "Please specify a location after 'in'."

    responseAPI = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}",
    )

    if responseAPI.status_code == 200:
        data = responseAPI.json()
        return f"The weather in {location.lower()} is {data['current']['condition']['text']} with a temperature of {data['current']['temp_c']}°C."
    else:
        return f"Failed to fetch weather data for {location}. Error: {responseAPI.status_code}"
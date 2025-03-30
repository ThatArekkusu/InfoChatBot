from dotenv import load_dotenv
import requests
import os

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

def getWeather(userInput):
    locationList = ["London", "Ireland", "Paris", "New York", "Tokyo", "Los Angeles", "Berlin", "Madrid", "Rome", "Sydney"]
    location = None
    words = userInput.split()

    try: 
        if "weather" in locationList:
            locationIndex = words.index(words)
    except ValueError:
        return "Please specify a valid query containing 'weather'.", 
            
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            potential_location = " ".join(words[i:j]) 
            if potential_location in locationList:
                location = potential_location
                break
        if location:
            break

    if location == None:
        return f"Please specify a valid location from list {locationList} ", 

    responseAPI = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}",
    )

    if responseAPI.status_code == 200:
        data = responseAPI.json()
        return f"The weather in {location} is {data['current']['condition']['text']} with a temperature of {data['current']['temp_c']}°C."
    else:
        return f"Failed to fetch weather data for {location}. Error: {responseAPI.status_code}"
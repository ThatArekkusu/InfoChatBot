from datetime import datetime
import pytz

def getTimezone(userInput, pending_timezones=None):
    # Check if the user input is a valid timezone and return the time
    if pending_timezones:
        if userInput in pending_timezones:
            tz = pytz.timezone(userInput)
            current_time = datetime.now(tz).strftime("%H:%M:%S")
            return f"The current time in {userInput} is {current_time}.", None
        else:
            return "Please specify a valid timezone from the list.", pending_timezones

    # Split the input into words
    words = userInput.split()
    location = None
    
    # Find the first uppercase word in the input
    for i in range(len(words)):
        if words[i].isupper():
            location = words[i]
            break

    # If no uppercase word is found, return a message
    if not location:
        return "Please specify a valid uppercase country code for the time.", None

    # Check if the location is a valid timezone
    if location in pytz.all_timezones:
        tz = pytz.timezone(location)
        current_time = datetime.now(tz).strftime("%H:%M:%S")
        return f"The current time in {location} is {current_time}.", None
    country_code = location
    timezones = pytz.country_timezones.get(country_code, None)

    # If the country code is not found, return a message
    if not timezones:
        return f"No timezones found for the country code '{country_code}'.", None
    elif len(timezones) == 1:
        tz = pytz.timezone(timezones[0])
        current_time = datetime.now(tz).strftime("%H:%M:%S")
        return f"The current time in {country_code} is {current_time}.", None

    # If the country code has multiple timezones, return a message
    return (
        f"{country_code} has multiple timezones: {', '.join(timezones)}. Please specify one.",
        timezones,
    )

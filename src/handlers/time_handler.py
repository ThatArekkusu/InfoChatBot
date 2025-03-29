from datetime import datetime
import pytz

def getTimezone(userInput, pending_timezones=None):
    # Check if the user input is a valid timezone
    if pending_timezones:
        # Check if the user input is in the list of pending timezones
        # If the user input is in the list of pending timezones, return the current time
        if userInput in pending_timezones:
            tz = pytz.timezone(userInput)
            current_time = datetime.now(tz).strftime("%H:%M:%S")
            return f"The current time in {userInput} is {current_time}.", None
        else:
            return "Please specify a valid timezone from the list.", pending_timezones

    # Split the input into words
    words = userInput.split()
    location = None

    # Check if the user input contains "time" or "timezone"
    try:
        if "time" in words:
            time_index = words.index("time")
        elif "timezone" in words:
            time_index = words.index("timezone")
        else:
            return "Please specify a valid query containing 'time' or 'timezone'.", None

        # Find the first uppercase word after "time" or "timezone"
        for i in range(time_index + 1, len(words)):
            if words[i].isupper():  
                location = words[i]
                break
    except ValueError:
        return "I couldn't find a valid location in your query.", None

    # If no uppercase word is found, return a message
    if not location:
        return "Please specify a valid uppercase country code for the time.", None

    # Check if the location is a valid timezone
    if location in pytz.all_timezones:
        tz = pytz.timezone(location)
        current_time = datetime.now(tz).strftime("%H:%M:%S")
        return f"The current time in {location} is {current_time}.", None

    # Check if the location is a valid country code
    country_code = location
    timezones = pytz.country_timezones.get(country_code, None)

    # If the country code is not found, return a message
    if not timezones:
        return f"No timezones found for the country code '{country_code}'.", None

    # If the country code is found, check if it has multiple timezones
    if len(timezones) == 1:
        tz = pytz.timezone(timezones[0])
        current_time = datetime.now(tz).strftime("%H:%M:%S")
        return f"The current time in {country_code} is {current_time}.", None

    # If the country code has multiple timezones, return a message
    return (
        f"{country_code} has multiple timezones: {', '.join(timezones)}. Please specify one.",
        timezones,
    )

from datetime import datetime
import pytz

def getTimezone(userInput, pending_timezones=None):
    # Handle specific timezone input if pending_timezones is provided
    if pending_timezones:
        if userInput in pending_timezones:
            # Match the input to a valid timezone in the pending list
            tz = pytz.timezone(userInput)
            current_time = datetime.now(tz).strftime("%H:%M:%S")
            return f"The current time in {userInput} is {current_time}.", None  # Clear pending_timezones
        else:
            # If the input doesn't match, prompt the user again
            return "Please specify a valid timezone from the list.", pending_timezones

    # Split the input into words
    words = userInput.split()
    location = None

    # Find the word after "time" or "timezone"
    try:
        if "time" in words:
            time_index = words.index("time")
        elif "timezone" in words:
            time_index = words.index("timezone")
        else:
            return "Please specify a valid query containing 'time' or 'timezone'.", None

        # Iterate through the words after "time" or "timezone"
        for i in range(time_index + 1, len(words)):
            if words[i].isupper():  # Check if the word is uppercase
                location = words[i]
                break
    except ValueError:
        return "I couldn't find a valid location in your query.", None

    if not location:
        return "Please specify a valid uppercase country code for the time.", None

    # Check if the input is a specific timezone
    if location in pytz.all_timezones:
        tz = pytz.timezone(location)
        current_time = datetime.now(tz).strftime("%H:%M:%S")
        return f"The current time in {location} is {current_time}.", None

    # Otherwise, treat the input as a country code
    country_code = location
    timezones = pytz.country_timezones.get(country_code, None)

    if not timezones:
        return f"No timezones found for the country code '{country_code}'.", None

    if len(timezones) == 1:
        tz = pytz.timezone(timezones[0])
        current_time = datetime.now(tz).strftime("%H:%M:%S")
        return f"The current time in {country_code} is {current_time}.", None

    # If multiple timezones exist, return the list of timezones
    return (
        f"{country_code} has multiple timezones: {', '.join(timezones)}. Please specify one.",
        timezones,
    )

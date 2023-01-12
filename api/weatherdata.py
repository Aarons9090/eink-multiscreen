import requests


def get_weatherdata():
    url = "https://api.open-meteo.com/v1/forecast?latitude=62.24&longitude=25.72&hourly=temperature_2m,weathercode,apparent_temperature,precipitation,cloudcover,windspeed_10m&windspeed_unit=ms&current_weather=true"

    resp = requests.get(url)

    data = resp.json()
    hourly_data = data["hourly"]
    current_time = data["current_weather"]["time"]
    index = hourly_data["time"].index(current_time)

    temp = hourly_data["temperature_2m"][index]
    apparent_temperature = hourly_data["apparent_temperature"][index]
    precipitation = hourly_data["precipitation"][index]
    cloudcover = hourly_data["cloudcover"][index]
    windspeed = hourly_data["windspeed_10m"][index]
    weathercode = hourly_data["weathercode"][index]

    return {
        "temp": temp,
        "apparent_temp": apparent_temperature,
        "precipitation": precipitation,
        "cloudcover": cloudcover,
        "windspeed": windspeed,
        "weathercode": weathercode
    }




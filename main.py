import json
import requests
import os
import boto3

omw_api_key = os.environ.get("MY_API_KEY")
snsclient = boto3.client("sns")


def lambda_handler(event, lambda_context):
    # Arguments
    phone_number = event["phone_number"]
    latitude_degrees = event["latitude_degrees"]
    longitude_degrees = event["longitude_degrees"]

    OPEN_WM = "https://api.openweathermap.org/data/2.5/onecall"
    parameters = {
        "lat": latitude_degrees,
        "lon": longitude_degrees,
        "exclude": "current,minutely,daily",
        "appid": omw_api_key,
    }

    response = requests.get(OPEN_WM, params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    hour_list = weather_data["hourly"]

    weather_12_hour = []
    for i in range(0, 11):
        code = weather_data["hourly"][i]["weather"][0]["id"]
        weather_12_hour.append(code)

    count = 0
    for i in weather_12_hour:
        if i < 700:
            count += 1

    if count > 0:
        response = snsclient.publish(
            PhoneNumber=phone_number,
            Message="Its going to rain today! â›ˆ Make sure you bring an â˜‚ï¸!",
        )

    return {
        "statusCode": 200,
        "body": json.dumps(f"Success. Text message sent to {phone_number}."),
    }

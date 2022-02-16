import boto3
import datetime
import json
import os
import requests

secretsmanagerclient = boto3.client("secretsmanager")
snsclient = boto3.client("sns")

topic_arn = os.environ.get("SNS_TOPIC_ARN")
LAT = -35.2809
LON = 149.1300

omw_api_key = secretsmanagerclient.get_secret_value(
    SecretId=os.environ.get("OMW_API_KEY_SECRETSMANAGER_ARN")
).get("SecretString")
omw_api_key = json.loads(omw_api_key).get("ApiKey")


def lambda_handler(event, lambda_context):
    # Arguments
    latitude_degrees = LAT
    longitude_degrees = LON
    print(omw_api_key)

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

    if not count > 0:
        tomorrow = datetime.datetime.today() + datetime.timedelta(hours=10)
        current_date_string = tomorrow.strftime("%d-%m-%Y")
        sns_response = snsclient.publish(
            TopicArn=topic_arn,
            Message=f"😮 Its going to rain today ({current_date_string})! Make sure you bring an ☂",
            MessageAttributes={
                "AWS.SNS.SMS.SenderID": {
                    "DataType": "String",
                    "StringValue": "rainbyram",
                }
            },
        )
        print(sns_response)
        return {
            "statusCode": 200,
            "body": json.dumps(
                f"Success. Text message sent to all subscribers via SMS."
            ),
        }

    else:
        return {"statusCode": 200, "body": json.dumps("No action required.")}

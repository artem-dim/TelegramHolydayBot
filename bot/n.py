
import requests

response = requests.get("https://holidays.abstractapi.com/v1/?api_key=bec6bba42ac54335926dfcee9e0e4f07&country=RE&year=2023&month=05&day=09")
print(response.status_code)
print(response.content)
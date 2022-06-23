import requests
import datetime
import time
from lib_42api.intra import ic

def test():
    ic.progress_bar=True
    user_login = "apavel"
    params = {
        "range[begin_at]":"2021-06-13,2022-06-23",
    }
    response = ic.pages_threaded(f"/users/{user_login}/locations", params=params)
    print(len(response))

test()
"""

user_login = "narroyo-"
start_date = datetime.datetime(2022, 6, 13)
end_date = datetime.datetime(2022, 6, 23)


headers = {
    "Authorization": f"Bearer {access_token}"
}

params = {
    "page[size]": 100,
    "sort": "-begin_at"
}
locations = requests.get(f"https://api.intra.42.fr/v2/users/{user_login}/locations", headers=headers, params=params).json()

total = 0

for location in locations:

  location_begin_at = datetime.datetime.strptime(location['begin_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

  if location_begin_at.timestamp() > end_date.timestamp():
    continue

  location_end_at = datetime.datetime.now()

  if (location['end_at'] is not None):
    location_end_at = datetime.datetime.strptime(location['end_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

  if location_begin_at.timestamp() < start_date.timestamp():
    break

  total = total + (location_end_at.timestamp() - location_begin_at.timestamp())

hours = total / 60 / 60

print(hours)
"""

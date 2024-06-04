import requests
from datetime import datetime
import smtplib

MY_LAT = 44.786568
MY_LONG = 20.448921
MY_EMAIL = "necamark@gmail.com"
PASSWORD = "abcd1234"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
hour_now = time_now.hour


def is_latitude_match(iss_lat, my_lat):
    if iss_lat >= my_lat + 5 or iss_latitude <= my_lat - 5:
        return False
    return True


def is_longitude_match(iss_lng, my_lat):
    if iss_lng >= my_lat + 5 or iss_lng <= my_lat - 5:
        return False
    return True


def is_dark(time, sunr, suns):
    if suns <= time <= sunr:
        return True
    return False


if is_latitude_match(iss_latitude, MY_LAT) and is_longitude_match(iss_longitude, MY_LONG) and is_dark(hour_now, sunrise, sunset):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="example@gmail.com",msg="Subject:ISS\n\nLOOK UP!")

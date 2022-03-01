from importlib.util import set_loader
import requests
import json
import time

class Sensor():

    def __init__(self, owm_key):
        self.telemetry = {}

        response = requests.get("https://get.geojs.io/v1/ip/geo.json")
        geo = response.json() 

        self.city = geo['city']
        self.country = geo['country']

        self.lat = geo["latitude"]
        self.lng = geo["longitude"]

        # Nairobi, Kenya
        self.lat = -1.286389
        self.lng = 36.817223
        self.country = 'Kenya'

        self.weather_url = "http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={owm_key}&units=metric".format(lat = self.lat, lng = self.lng, owm_key = owm_key)
        self.pollution_url = "http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lng}&appid={owm_key}".format(lat = self.lat, lng = self.lng, owm_key = owm_key)

        self.telemetry = None
        self.last_request_time = 0

    async def get_weather(self):

        # get current epoch time
        now = time.time()

        # If less than 15 minutes then return cached telemetry
        # Open Weather map updates weather every 15 minutes (15 x 60 seconds)
        if (now - self.last_request_time < 15 * 60):
            return self.telemetry

        self.last_request_time = now

        response = requests.get(self.weather_url)
        weather = response.json() 

        # {'main': {'aqi': 1}, 'components': {'co': 200.27, 'no': 1.38, 'no2': 6.17, 'o3': 18.6, 'so2': 3.16, 'pm2_5': 2.1, 'pm10': 3.49, 'nh3': 0.38}, 'dt': 1646107200}
        response = requests.get(self.pollution_url)
        pollution = response.json() 

        self.telemetry = {
            "city" : weather['name'],
            "latitude" : self.lat,
            "longitude" : self.lng,
            "temperature": weather['main']['temp'],
            "humidity" : weather['main']['humidity'],
            "pressure" : weather['main']['pressure'],
            "windspeed" : weather['wind']['speed'],
            "aqi" : pollution['list'][0]['main']['aqi'],
            "co" : pollution['list'][0]['components']['co'],
            "no" : pollution['list'][0]['components']['no'],
            "no2" : pollution['list'][0]['components']['no2'],
            "o3" : pollution['list'][0]['components']['o3'],
            "so2" : pollution['list'][0]['components']['so2'],
            "pm2_5" : pollution['list'][0]['components']['pm2_5'],
            "pm10" : pollution['list'][0]['components']['pm10'],
            "nh3" : pollution['list'][0]['components']['nh3']
        }

        return self.telemetry
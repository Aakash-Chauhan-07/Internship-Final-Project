import requests
from geopy.geocoders import Nominatim
from pyautogui import typewrite
from time import sleep

def get_my_location():

    def get_location_ipinfo():
        url = 'https://ipinfo.io'
        response = requests.get(url)
        location_data = response.json()

        loc = location_data['loc']
        lat, lon = map(float, loc.split(','))

        return lat, lon, location_data['city'], location_data['region'], location_data['country']

    def reverse_geocode(lat, lon):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((lat, lon), exactly_one=True)
        address = location.address

        return address

    latitude, longitude, city, region, country = get_location_ipinfo()

    sleep(8)
 

    try:
        address = reverse_geocode(latitude, longitude)
        typewrite(f"Latitude: {latitude}, Longitude: {longitude}, City: {city}, Region: {region}, Country: {country}, Address: {address}")
    except:
        pass

import requests
from django.conf import settings
from addressesapp.models import Address


def fetch_coordinates(address):
    apikey = settings.YANDEX_GEO_API_KEY
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_coordinates_from_db_or_yandex(address):
    try:
        address = Address.objects.get(address=address)
        lat, lon = address.lat, address.lon
        return lat, lon
    except Address.DoesNotExist:
        pass

    try:
        lon, lat = fetch_coordinates(address)
        address = Address.objects.create(address=address,
                                         lat=lat,
                                         lon=lon)
    except requests.exceptions.HTTPError:
        lat, lon = None, None
    return lat, lon

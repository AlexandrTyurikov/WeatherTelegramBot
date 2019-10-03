import requests
from constants import api_key_yandex_geocoder
from db_operations import db_update_city, db_update_name_loc, db_update_name_loc_full, db_update_loc_city


# reverse_geocoding
def reverse_geocoding(lat, lon):
    url_osm_reverse = f'https://nominatim.openstreetmap.org/reverse?&format=json&lat={lat}&lon={lon}&addressdetails=1'
    r_osm_reverse = requests.get(url_osm_reverse).json()
    name_loc = str
    if 'error' in r_osm_reverse or 'country' not in r_osm_reverse['address'] or r_osm_reverse['address'][
                'country'] not in ['Беларусь', 'РФ', 'Казахстан']:
        url_ya = f'https://geocode-maps.yandex.ru/1.x/?format=json&apikey={api_key_yandex_geocoder}&geocode=' \
                 f'{lon},{lat}&results=1'
        r_ya = requests.get(url_ya).json()

        if 'description' in r_ya['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']:
            name_loc = r_ya['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['description']
            name_loc_full = r_ya['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                'metaDataProperty']['GeocoderMetaData']['text']
        else:
            name_loc = r_ya['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
            name_loc_full = r_ya['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
    else:
        if 'water' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['water']}, {r_osm_reverse['address']['country']}"
        elif 'village' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['village']}, {r_osm_reverse['address']['country']}"
        elif 'town' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['town']}, {r_osm_reverse['address']['country']}"
        elif 'hamlet' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['hamlet']}, {r_osm_reverse['address']['country']}"
        elif 'locality' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['locality']}, {r_osm_reverse['address']['country']}"
        elif 'sports_centre' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['sports_centre']}, {r_osm_reverse['address']['country']}"
        elif 'city' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['city']}, {r_osm_reverse['address']['country']}"
        elif 'county' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['county']}, {r_osm_reverse['address']['country']}"
        elif 'state' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['state']}, {r_osm_reverse['address']['country']}"
        elif 'body_of_water' in r_osm_reverse['address']:
            name_loc = f"{r_osm_reverse['address']['body_of_water']}"
        name_loc_full = r_osm_reverse['display_name'].split(',')
        name_loc_full.reverse()
        name_loc_full = ','.join(name_loc_full)
    return name_loc, name_loc_full


def save_name_city_country_and_loc(message):
    url_ya = f"https://geocode-maps.yandex.ru/1.x/?apikey={api_key_yandex_geocoder}&format=json&geocode=" \
             f"{message.text}&results=1"
    r_ya = requests.get(url_ya).json()
    r_ya_loc_g = r_ya['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    r_ya_loc = r_ya_loc_g.split(' ')
    r_ya_loc_lat = float(r_ya_loc[1])
    r_ya_loc_lon = float(r_ya_loc[0])

    db_update_city(message, reverse_geocoding(r_ya_loc_lat, r_ya_loc_lon)[0])
    db_update_loc_city(message, r_ya_loc_lat, r_ya_loc_lon)


def save_name_loc_and_full(message):
    db_update_name_loc(message, reverse_geocoding(message.location.latitude, message.location.longitude)[0])
    db_update_name_loc_full(message, reverse_geocoding(message.location.latitude, message.location.longitude)[1])

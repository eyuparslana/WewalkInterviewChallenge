import requests
from django.conf import settings

from api.exception import ClientException


class FoursquareClient:
    api_endpoint = 'https://api.foursquare.com/v2/venues/'
    client_id = settings.FOURSQUARE_CLIENT_ID
    client_secret = settings.FOURSQUARE_CLIENT_SECRET
    version = '20200625'

    def get_places_by_coordinates(self, lat, long, radius):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'v': self.version,
            'll': '{},{}'.format(lat, long),
            'radius': radius,
        }
        url = self.api_endpoint + 'search/'

        response = requests.get(url=url, params=params)
        if response.status_code != 200:
            raise ClientException("Something went wrong. Please try again")
        data = response.json()

        return data['response']['venues']

    def get_place_by_id(self, place_id):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'v': self.version,
        }

        url = self.api_endpoint + place_id

        response = requests.get(url=url, params=params)
        data = response.json()

        return data['response']['venue']

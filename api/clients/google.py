import requests
from django.conf import settings

from api.exception import ClientException


class GoogleClient:
    api_endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    mode = 'walking'

    def search(self, origin_latlong, destination_latlong):
        request_url = '{}origin={}&destination={}&mode={}&key={}'.format(self.api_endpoint, origin_latlong,
                                                                         destination_latlong, self.mode,
                                                                         settings.GOOGLE_API_KEY)

        response = requests.get(request_url)
        if response.status_code != 200:
            raise ClientException("Something went wrong. Please try again.")

        data = response.json()
        return data['routes'][0]['legs'][0]

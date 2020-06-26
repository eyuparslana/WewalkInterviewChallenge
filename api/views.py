from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.clients.foursquare import FoursquareClient
from api.clients.google import GoogleClient
from api.models import Route, Place
from api.serializers import PlaceSerializer


def get_place_dict(venue):
    place = Place()
    place.name = venue.get('name', '').capitalize()
    place.place_id = venue.get('id')
    place.phone = venue.get('contact', {}).get('phone')

    location = venue.get('location', {})
    place.latitude = location.get('lat', 0.0)
    place.longitude = location.get('lng', 0.0)
    place.address = location.get('address')

    if location.get('formattedAddress'):
        place.address = ' '.join([address for address in location.get('formattedAddress')])

    place.category = ','.join([category.get('name') for category in venue.get('categories', [])])
    place.neighborhood = location.get('neighborhood')
    place.city = location.get('city')
    place.state = location.get('state')
    place.country = location.get('country')

    return place


@api_view(['GET'])
def get_places_on_route(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')

    if not len(origin.split(',')) == 2 or not len(destination.split(',')) == 2:
        response = {
            'status': 'Bad request',
            'message': 'Please enter 2 latitude and longitude. Format(origin=lat,lng&destination=lat,lng)'
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    google = GoogleClient()
    leg = google.search(origin, destination)

    user = request.user

    route = Route()
    route.user = user
    route.origin_latitude, route.origin_longitude = origin.split(',')
    route.destination_latitude, route.destination_longitude = destination.split(',')
    route.start_address = leg.get('start_address')
    route.end_address = leg.get('end_address')
    route.distance = leg.get('distance', {}).get('value')
    route.duration = leg.get('duration', {}).get('value')
    route.save()

    steps = leg.get('steps')
    response_places = []

    foursquare = FoursquareClient()

    for step in steps:
        radius = step.get('distance', {}).get('value')
        start_location = step.get('start_location')
        lat = start_location.get('lat')
        long = start_location.get('lng')

        venues = foursquare.get_places_by_coordinates(lat, long, radius)
        for venue in venues:
            place = get_place_dict(venue)
            place.user = user

            if place not in response_places:
                response_places.append(place)

    serializer = PlaceSerializer(response_places, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def favourites(request):
    if request.method == 'GET':
        places = Place.objects.filter(user=request.user)
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    place_ids = request.data.get('places')

    if not place_ids:
        resp = {'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Please enter any place id'
                }
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    foursquare = FoursquareClient()

    fav_places = []
    for place_id in place_ids:
        venue = foursquare.get_place_by_id(place_id)
        place = get_place_dict(venue)
        place.user = request.user
        fav_places.append(place)

    Place.objects.bulk_create(fav_places)

    serializer = PlaceSerializer(fav_places, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import serializers

from api.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('place_id', 'name', 'latitude', 'longitude',
                  'address', 'phone', 'category', 'neighborhood',
                  'state', 'city', 'country')

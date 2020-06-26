from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin_latitude = models.FloatField()
    origin_longitude = models.FloatField()
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()
    timestamp = models.IntegerField(default=datetime.now().timestamp())
    start_address = models.CharField(max_length=255)
    end_address = models.CharField(max_length=255)
    distance = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)

    def __str__(self):
        return 'search by: {} origin: {},{} destination: {},{}'.format(self.user.username, self.origin_latitude,
                                                                       self.origin_longitude, self.destination_latitude,
                                                                       self.destination_longitude)


class PlaceManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        non_exists_places = []
        for obj in objs:
            if not Place.objects.filter(place_id=obj.place_id).exists():
                non_exists_places.append(obj)
        return super(PlaceManager, self).bulk_create(non_exists_places, batch_size, ignore_conflicts)


class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)

    objects = PlaceManager()

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.place_id == other.place_id

from django.db import models
from django.contrib.auth.models import User
import trains.helper as helper

# Create your models here.

class UserInfo(models.Model):
   username = models.CharField(max_length=256)
   display_name = models.CharField(max_length=256)

   def __unicode__(self):
      return self.display_name


class Office(models.Model):
   location = models.CharField(max_length=256)
   name = models.CharField(max_length=256)
   latitude = models.DecimalField(decimal_places=5, max_digits=10)
   longitude = models.DecimalField(decimal_places=5, max_digits=10)

   def __unicode__(self):
      return self.name


class Restaurant(models.Model):
   name = models.CharField(max_length=256)
   address = models.CharField(max_length=256)
   phone = models.CharField(max_length=256)
   notes = models.CharField(max_length=256)
   icon = models.ImageField(upload_to='users/icons')
   url = models.URLField()
   menu_url = models.URLField()
   latitude = models.DecimalField(decimal_places=5, max_digits=10)
   longitude = models.DecimalField(decimal_places=5, max_digits=10)

   def __unicode__(self):
      return self.name

MAX_WALK_DISTANCE_METERS = 900

class Train(models.Model):
   departure_time = models.DateTimeField()
   captain = models.ForeignKey(User, related_name='+')
   passengers = models.ManyToManyField(User)
   destination = models.ForeignKey('Restaurant', blank=True, null=True)
   one_off_destination_name = models.CharField(max_length=256, blank=True, null=True)
   notes = models.TextField()

   def destination_display(self):
      if self.destination:
         return self.destination.name
      return self.one_off_destination_name

   def captain_info(self):
      if not self.captain:
         return None
      return UserInfo.objects.get(username = self.captain.username)

   def passengers_info(self):
      return [ UserInfo.objects.get(username = user.username) for user in self.passengers.all() ]

   def transport(self):
      if self.destination:
         if helper.distance(self.destination, Office.objects.all()[0]) > MAX_WALK_DISTANCE_METERS:
            return 'drive'
         return 'walk'
      return 'unknown'

   def passenger_display(self):
      result = []
      for passenger in self.passengers.all():
         result.append(UserInfo.objects.get(username = passenger.username).display_name)
      return result

   def __unicode__(self):
      return u'%s train to %s' % (self.departure_time, self.destination)


from trains.models import User, Train, Restaurant
import math

def suggestCompanionUsers(user):
   people = []
   people.append(User.objects.get(username='oliver'))
   people.append(User.objects.get(username='rwest'))
   return people


def reorderTrains(trains, user):
   retTrains = []

   # Move the train you are on to the front
   for t in trains:
      for p in t.passengers.all():
         if p == user:
            retTrains.append(t)
            trains.remove(t)            
            break

   # Now order the rest of the trains by suggested companions
   people = suggestCompanionUsers(user)
   for p in people:
      for t in trains:
         for u in t.passengers.all():
            if u == p:
               retTrains.append(t)
               trains.remove(t)

   # Add the remainder of the trains to the return list
   for t in trains:
      retTrains.add(t)

   return retTrains

EARTH_RADIUS_METERS = 63710000

def distance(one, two):
   dLat = math.radians(two.latitude - one.latitude)
   dLon = math.radians(two.longitude - one.longitude)
   lat1 = math.radians(one.latitude)
   lat2 = math.radians(two.latitude)

   a = (math.sin(dLat/2) * math.sin(dLat/2) +
        math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2))
   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
   return EARTH_RADIUS_METERS * c

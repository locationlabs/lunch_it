from trains.models import User, Train, Restaurant

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


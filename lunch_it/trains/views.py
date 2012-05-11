from django.shortcuts import render, HttpResponseRedirect
from trains.models import UserInfo, Train, Restaurant
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
import trains.helper as helper
from forms import * 
import datetime
import time

def login(request):

   if request.method == 'GET':
      form = LoginForm()
      return render(request,'login.html',{'form':form})
   elif request.method == 'POST':
      form = LoginForm(request.POST)
      if not form.is_valid:
         return render(request,'login.html', {'errors':["The data you entered is invalid"], 'form':form})
      else:
         username = form.data['username']
         #print username
         password = 'password'
         user = authenticate(username=username, password=password)
      if user is not None:
         if user.is_active:
            auth_login(request, user)
            #print 'yup!'
            return HttpResponseRedirect('/')
         else:
            return render(request,'login.html', {'errors':["Uh oh. Looks like your account has been disabled."],'form':form})
      else:
         return render(request,'login.html', {'errors':["Sorry - looks like your name isn't in the database."],'form':form})

def logout(request):
   auth_logout(request)
   return HttpResponseRedirect('/login/')
        
def index(request):
   if not request.user.is_authenticated():
      return HttpResponseRedirect('/login/')

   user = request.user

   # Stuff we need to get 
   # all today's trains
   trains = list(Train.objects.filter(departure_time__year = datetime.datetime.today().year,
                                      departure_time__month = datetime.datetime.today().month,
                                      departure_time__day = datetime.datetime.today().day))

   # Order the list of trains
   trains = helper.reorderTrains(trains, user)

   if trains and (trains[0].captain == user or user in trains[0].passengers.all()):
      your_train = trains[0]
   else:
      your_train = None

   # Suggested destinations
   places = Restaurant.objects.all()

   # user info for current user
   user_info = UserInfo.objects.get(username = request.user.username)

   view = 'main_template.html'
   return render(request, view, {
         'trains': trains,
         'your_train' : your_train,
         'places' : places,
         'user_info' : user_info })

def createNewGroup(request):
   if not request.user.is_authenticated():
      return HttpResponseRedirect('/login/')

   place_str = request.POST['place']
   time_str = str(request.POST['time'])
   notes = request.POST['notes']
   restaurant_query = Restaurant.objects.filter(name__iexact = place_str)
   if restaurant_query.count() == 0:
      restaurant = None
      one_off_name = place_str.strip()
   else:
      restaurant = restaurant_query[0]
      one_off_name = None
   time_split = time_str.split(':')
   timeformat = int(time_split[0])
   if timeformat < 8:
       tdelta = 12
   else: 
       tdelta = 0

   time_str = '%s %s' % (str(datetime.date.today()), time_str)
   print time_str
   dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M") + datetime.timedelta(hours=tdelta)

   train = Train(departure_time = dt,
         captain = request.user,
         destination = restaurant,
         one_off_destination_name = one_off_name,
         notes = notes)
   train.save()

   return index(request)

def joinGroup(request):
   if not request.user.is_authenticated():
      return HttpResponseRedirect('/login/')

   group_id = request.POST['train_id']
   train = Train.objects.get(id=group_id)
   user = request.user

   # Add the user the the group
   train.passengers.add(user)
   train.save()

   return index(request)

def leaveGroup(request):
   if not request.user.is_authenticated():
      return HttpResponseRedirect('/login/')

   group_id = request.POST['train_id']
   train = Train.objects.get(id=group_id)
   user = request.user

   # Remove the user from the group
   for u in train.passengers.all():
      print "processing user " , u
      if u == user:
         train.passengers.remove(u)
         return index(request)
   
   if train.captain == user:
      if train.passengers.count() == 0:
         # Nobody left on the train.
         print "Empty train, deleting it"
         train.delete()
         return index(request)

      # The captain has left, promote the first joiner to captain
      print "Captain left"
      newCap = train.passengers.all()[0]
      print "New captain will be " , newCap
      print "About to remove passenger 0. " , train.passengers.all()
      train.passengers.remove(newCap)
      print "Removed passenger, new passenger list is " , train.passengers.all()
      train.captain = newCap
      train.save()

   return index(request)

def profile(request):
   if not request.user.is_authenticated():
      return HttpResponseRedirect('/login/')

   username = request.GET['u']
   user = User.objects.get(username = username)
   user_info = UserInfo.objects.get(username = username)

   if user_info.username == request.user.username:
      is_you = True
   else:
      is_you = None

   favorite_places = []

   for place in Restaurant.objects.all():
      visits = 0
      for train in Train.objects.filter(destination = place):
         if train.captain == user or user in train.passengers.all():
            visits = visits + 1
      if visits > 0:
         favorite_places.append({
               'restaurant' : place,
               'visits' : visits
            })

   favorite_places.sort(lambda x, y : cmp(x['visits'], y['visits']), None, True)

   co_lunchers = []
   # for user in 
   # for train in Train.objects.all():
   #   if train.captain == user and 

   view = 'profile_template.html'
   return render(request, view, {
         'user_info': user_info,
         'is_you' : is_you,
         'favorite_places' : favorite_places[0:5],
         'co_lunchers' : co_lunchers })



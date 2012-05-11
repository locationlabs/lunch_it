from django.shortcuts import render, HttpResponseRedirect
from trains.models import UserInfo, Train, Restaurant
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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

   # Stuff we need to get 
   # all today's trains  TODO filter this by today's date
   trains = list(Train.objects.all())

   # Order the list of trains
   trains = helper.reorderTrains(trains, request.user)

   # Suggested destinations
   places = Restaurant.objects.all()

   # user info for current user
   user_info = UserInfo.objects.get(username = request.user.username)

   view = 'main_template.html'
   return render(request, view, {'destination': trains, 'places' : places, 'user_info' : user_info })

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

   view = 'main_template.html'
   return index(request)

def joinGroup(request):
   if not request.user.is_authenticated():
      return HttpResponseRedirect('/login/')

   view = 'main_template.html'
   return render(request, view, {})

def leaveGroup(request):
   if not request.user.is_authenticated():
      return HttpResponseRedirect('/login/')

   view = 'main_template.html'
   return render(request, view, {})


from django.shortcuts import render, HttpResponseRedirect
from trains.models import UserInfo, Train, Restaurant
import trains.helper as helper
from forms import * 
import datetime

# checks if users are logged in
def hasAuth(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        pass

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid:
            return render(request,'login.html', {'errors':["The data you entered is invalid"]})
        else:
            username = self.cleaned_data['username']
            password = 'password'
            user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request,'login.html', {'errors':["Uh oh. Looks like your account has been disabled."]})
        else:
            return render(request,'login.html', {'errors':["Sorry - looks like your name isn't in the database."]})
        
def index(request):
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
   return render(request, view, {'destination': trains, 'user_info' : user_info })

def createNewGroup(request):

   place_str = request.POST['place']
   time_str = request.POST['time']
   notes = request.POST['notes']

   restaurant_query = Restaurant.objects.filter(name__iexact = place_str)
   if restaurant_query.count() == 0:
      restaurant = None
      one_off_name = place_str.strip()
   else:
      restaurant = restaurant_query[0]
      one_off_name = None

   time_split = time_str.split(':')
   hours = int(time_split[0])
   if len(time_split) > 1:
      minutes = int(time_split[1])
   else:
      minutes = 0
   dt = datetime.datetime.combine(datetime.date.today(), datetime.time(hours, minutes))

   train = Train(departure_time = dt,
         captain = request.user,
         destination = restaurant,
         one_off_destination_name = one_off_name,
         notes = notes)
   train.save()

   view = 'main_template.html'
   return index(request)

def joinGroup(request):
   view = 'main_template.html'
   return render(request, view, {})

def leaveGroup(request):
   view = 'main_template.html'
   return render(request, view, {})


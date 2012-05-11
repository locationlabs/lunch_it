from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render
from trains.models import User, Train, Restaurant
import trains.helper as helper
from forms import * 

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
   # Suggested destinations
   places = list(Restaurant.objects.all())

   # Order the list of trains
   trains = helper.reorderTrains(trains, request.user)

   view = 'main_template.html'
   return render(request, view, {'destination': trains})

def createNewGroup(request):
   view = 'createGroup.html'
   return render(request, view, {})

def joinGroup(request):
   view = 'main_template.html'
   return render(request, view, {})

def leaveGroup(request):
   view = 'main_template.html'
   return render(request, view, {})


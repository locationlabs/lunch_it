from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render
from trains.models import User, Train, Restaurant
from django.contrib.auth import authenticate, login as auth_login
from forms import * 

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
            print username
            password = 'password'
            user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                print 'yup!'
                return HttpResponseRedirect('/')
            else:
                return render(request,'login.html', {'errors':["Uh oh. Looks like your account has been disabled."],'form':form})
        else:
            return render(request,'login.html', {'errors':["Sorry - looks like your name isn't in the database."],'form':form})
        
def index(request):
   # Stuff we need to get 
   # all today's trains  TODO filter this by today's date
   trains = Train.objects.all()
   # Suggested destinations
   places = Restaurant.objects.all()
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


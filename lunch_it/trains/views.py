# Create your views here.

from django.shortcuts import render
from trains.models import User, Train, Restaurant
import trains.helper as helper

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

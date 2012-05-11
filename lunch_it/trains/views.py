# Create your views here.

from django.shortcuts import render

def index(request):
   view = 'main.html'
   return render(view, {})

def createNewGroup(request):
   view = 'createGroup.html'
   return render(view, {})

def joinGroup(request):
   view = 'main.html'
   return render(view, {})

def leaveGroup(request):
   view = 'main.html'
   return render(view, {})

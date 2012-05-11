from django.shortcuts import render, HttpResponseRedirect
#checks if users are logged in 

def hasAuth(request):
if not request.user.is_authenticated():
    return HttpResponseRedirect('/login/')
else:
    pass

def login(request):
    if request.method == 'GET':
        return render(request,'login.html'}
    elif request.method == 'POST':
        username = request.POST['username']
        password = 'password'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request,'login.html', {'errors':["Uh oh. Looks like your account has been disabled."]}
        else:
            return render(request,'login.html', {'errors':["Sorry - looks like your name isn't in the database."]}
        
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

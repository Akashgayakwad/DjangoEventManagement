from django.shortcuts import render
from event_manager.forms import UserForm,UserProfileInfoForm,EventForm
from event_manager.models import UserProfile,Event
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here

def index(request):
    if (request.user.is_authenticated):
        u1 = User.objects.get(username = request.user)
        role = u1.userprofile.user_role
    else:
        role = ''
    my_context = {'my_role':role}
    return render(request,'event_manager/index.html',context=my_context)

@login_required
def create(request):
    return render(request,'event_manager/create_event.html')

@login_required
def delete(request):
    return render(request,'event_manager/delete_event.html')

@login_required
def edit(request):
    return render(request,'event_manager/edit_event.html')

def show(request):
    return render(request,'event_manager/events.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    my_context = {'user_form':user_form,
                'profile_form':profile_form,
                'registered':registered}
    return render(request, 'event_manager/register.html',context=my_context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                print(user)
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: "+username+" and password: "+password)
            return HttpResponse("Invalid Login Details Supplied")
    else:
        return render(request,'event_manager/login.html',{})

from django.shortcuts import render
from event_manager.forms import UserForm,UserProfileInfoForm,EventForm
from event_manager.models import UserProfile,Event
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
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
    if (request.user.is_authenticated):
        u1 = User.objects.get(username = request.user)
        role = u1.userprofile.user_role
    else:
        role = ''

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.event_organizer = request.user
            obj.save()
            return HttpResponseRedirect(reverse('event_manager:show'))
        else:
            print('ERROR FORM INVALID')
    else:
        form = EventForm()
        my_context = {'my_role':role, 'form': form}
        return render(request,'event_manager/create_event.html',context=my_context)





@login_required
def delete(request, id):
    if (request.user.is_authenticated):
        u1 = User.objects.get(username = request.user)
        role = u1.userprofile.user_role
    else:
        role = ''

    if role =='O':
        event = Event.objects.get(event_id = id)
        if str(event.event_organizer) == str(request.user):
            delete = 'YES'
        else:
            delete = 'NO'
    else:
        delete = 'NO'


    if delete == 'YES':
        Event.objects.filter(event_id=id).delete()
        return HttpResponseRedirect(reverse('event_manager:show'))
    else:
        return HttpResponse('<h1>You Dont have Permission To Delete</h1>')



@login_required
def edit(request, id):
    if (request.user.is_authenticated):
        u1 = User.objects.get(username = request.user)
        role = u1.userprofile.user_role
    else:
        role = ''

    if role =='O':
        event = Event.objects.get(event_id = id)
        if str(event.event_organizer) == str(request.user):
            edit = 'YES'
        else:
            edit = 'NO'
    else:
        edit = 'NO'


    if request.method == "POST":
        event = Event.objects.get(event_id = id)
        if 'event_poster' not in request.FILES:
            request.FILES['event_poster'] = event.event_poster
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event_form = EventForm(request.POST, instance = event)
            myevent = event_form.save(commit = False)
            myevent.event_poster = request.FILES['event_poster']
            myevent.save()
            return HttpResponseRedirect(reverse('event_manager:show'))
        else:
            return HttpResponse('<h1>ERROR FORM INVALID</h1>')
    else:
        event = Event.objects.get(event_id = id)
        form = EventForm(initial = {'event_name':event.event_name,
                                    'event_poster':event.event_poster,
                                    'event_date':event.event_date,
                                    'event_time':event.event_time,
                                    'event_duration':event.event_duration,
                                    'event_visibility':event.event_visibility,
                                    'event_venue':event.event_venue})
        my_context = {'editaccess':edit,'form': form}
        return render(request,'event_manager/edit_event.html',context=my_context)




def show(request):
    event_list = Event.objects.filter(event_visibility="V").order_by('event_date')
    my_context = {'events':event_list}
    return render(request,'event_manager/events.html',context=my_context)




def event(request, id):
    my_event = get_object_or_404(Event, event_id = id)
    print(my_event)
    my_context = {'event':my_event}
    return render(request,'event_manager/details.html',context=my_context)






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

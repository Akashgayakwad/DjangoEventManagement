from django import forms
from django.contrib.auth.models import User
from event_manager.models import UserProfile,Event

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_role',)

class EventForm(forms.ModelForm):
    event_date = forms.DateField(widget = forms.SelectDateWidget())
    class Meta:
        model = Event
        labels = {
        "event_time":"Event time(hh:mm:ss)",
        "event_duration": "Event duration(hh:mm:ss)"
        }
        exclude = ("event_organizer",)

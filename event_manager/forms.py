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
    class Meta:
        model = Event
        fields = '__all__'

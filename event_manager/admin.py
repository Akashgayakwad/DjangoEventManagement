from django.contrib import admin
from event_manager.models import UserProfile,Event
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)

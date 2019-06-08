from django.db import models
from django.contrib.auth.models import User
# Create your models here.

user_roles = (
    ('O','Organizer'),
    ('A','Attendee'),
)

Visibility = (
    ('V','Visible'),
    ('I','Invisible'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.CharField( max_length=1,
                                  choices=user_roles)
    def __str__(self):
        return self.user.username


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField( max_length= 40)
    event_poster = models.ImageField(upload_to='event_posters',blank=False)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_duration = models.DurationField()
    event_venue = models.CharField( max_length= 100)
    event_visibility = models.CharField( max_length=1,
                                  choices=Visibility)
    def __str__(self):
        return self.event_name

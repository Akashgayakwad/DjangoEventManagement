from django.urls import path
from event_manager import views

app_name = 'event_manager'
urlpatterns = [
    path('<int:id>/',views.event, name="event"),
    path('',views.show, name="show"),
    path('create/',views.create,name="create"),
    path('delete/<int:id>/',views.delete,name="delete"),
    path('edit/<int:id>/',views.edit,name="edit"),
    path('register/',views.register,name="register"),
    path('user_login/',views.user_login,name="user_login"),
]

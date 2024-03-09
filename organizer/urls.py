from django.urls import path
from . import views

app_name = 'organizer'

urlpatterns = [
    path('register', views.register_organizer, name='register'),
]
from django.urls import path
from . import views

app_name = 'participant'

urlpatterns = [
    path('register', views.register_participant, name='register'),
]
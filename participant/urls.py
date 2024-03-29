from django.urls import path
from . import views

app_name = 'participant'

urlpatterns = [
    path('register', views.register_participant, name='register'),
    path('follow_list/', views.follow_list, name='follow_list'),
    path('participations/', views.participations, name='participations'),
]
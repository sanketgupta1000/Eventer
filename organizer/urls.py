from django.urls import path
from . import views

app_name = 'organizer'

urlpatterns = [
    path('register', views.register_organizer, name='register'),
    # to follow an organizer
    path('follow/<int:id>', views.follow_organizer, name='follow_organizer'),
    path('unfollow/<int:id>', views.unfollow_organizer, name='unfollow_organizer'),
    path('view/<int:id>', views.view_organizer, name='view_organizer'),
    path('my_events/', views.my_events, name='my_events'),
    path('all/', views.all_organizers, name='all'),
]
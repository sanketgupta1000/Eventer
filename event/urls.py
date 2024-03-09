from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('host/', views.host_event, name='host'),
    path('delete/<int:id>', views.delete_event, name='delete_event'),
    path('participate/<int:id>', views.participate, name='participate'),
]
from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('host/', views.host_event, name='host'),
    path('view/<int:id>', views.view_event, name='view_event'),
    path('delete/<int:id>', views.delete_event, name='delete_event'),
    path('participate/<int:id>', views.participate, name='participate'),
    path('cancel/<int:id>', views.cancel_event, name='cancel_event'),
    path('checkin/<int:id>', views.checkin_event, name='checkin'),
    path('complete/<int:id>', views.complete_event, name='complete_event')
]
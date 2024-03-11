from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import *
from .models import Account
from event.models import Event
from organizer.models import Organizer
from participant.models import FollowList
# Create your views here.

# view to log user in
@logout_required()
def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

# view for showing home page
@login_required
def home(request):
    if request.user.type==Account.Types.O:
        # fetching all events of organizer
        events = Event.objects.filter(account=request.user).order_by("-date")
        return render(request, "organizer_home.html", {'org_events': events})
    else:
        # user is a participant
        # getting upcoming events of the user
        upcoming_events = Event.objects.filter(participation__account=request.user, status='u').order_by("date")
        # getting unfollowed organizers
        featured_organizers = Organizer.objects.exclude(followlist__participant=request.user.participant)
        # for testing only
        new_events = Event.objects.all()
        return render(request, "participant_home.html", {"upcoming_events":upcoming_events, "featured_organizers":featured_organizers, "new_events": new_events})


# view to log user out
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
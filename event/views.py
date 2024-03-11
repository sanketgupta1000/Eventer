from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from .forms import *
from participant.models import Participation

# Create your views here.

# view to host an event
@login_required
@permission_required("event.host_event", raise_exception=True)
def host_event(request):
    if request.method=='POST':
        form = EventHostForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(False)
            event.account = request.user
            event.save()
            return redirect('home')
    else:
        form = EventHostForm()
    return render(request, 'host_event.html', {'form': form})

# view to delete an event
@login_required
@permission_required("event.delete_own_event", raise_exception=True)
def delete_event(request, id):
    # get the event
    event = get_object_or_404(Event, pk=id)
    if event.account==request.user:
        # it is the user's event
        # delete it
        event.delete()
        return redirect("home")
    else:
        # not the user's event
        raise PermissionDenied
    
# view to participate in an event
@login_required
@permission_required("event.participate_in_event", raise_exception=True)
def participate(request, id):
    # getting the event
    event = get_object_or_404(Event, pk=id)
    # creating participation object
    participation = Participation(account=request.user, event=event)
    # save it
    participation.save()
    # redirect to home
    return redirect("home")

# view to view an event with a given id
# any one can view an event
def view_event(request, id):
    # getting event details
    event = get_object_or_404(Event, pk=id)
    # will fill template paths of availabe actions in this array
    actions = []
    if request.user.has_perm("event.delete_own_event") and request.user==event.account:
        actions+="cancel_event_btn.html"
    if request.user.has_perm("event.participant_in_event"):
        actions+="participate_event_btn.html"
    return render(request, "view_event.html")
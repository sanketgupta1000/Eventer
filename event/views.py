from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied

from account.decorators import navbar_required
from .forms import *
from participant.models import Participation
from django.utils import timezone
from datetime import timedelta
import zoneinfo
from django.utils.dateparse import parse_datetime

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
def participate(request, id):
    # getting the event
    event = get_object_or_404(Event, pk=id)

    if canParticipateInEvent(request, event):
        # create new participation
        newparticipation = Participation(account=request.user, event=event)
        newparticipation.save()
    return redirect("event:view_event", id=id)

# view to view an event with a given id
# any one can view an event
# @navbar_required()
# def view_event(request, ctx, id):
#     # getting event details
#     event = get_object_or_404(Event, pk=id)
#     # will fill template paths of availabe actions in this array
#     actions = []
#     current_time = timezone.now()
#     if request.user.has_perm("event.delete_own_event") and request.user==event.account:
#         # checking if already canceled or not
#         if event.status=="x":
#             # already canceled
#             actions.append("canceled_event_btn.html")
#         else:
#             # not already canceled
#             # checking if time <= one day before event
#             if event.date-current_time>=timedelta(days=1):
#                 # can cancel
#                 actions.append("cancel_event_btn.html")
#             else:
#                 # cannot cancel
#                 actions.append("cannot_cancel_event_btn.html")
#     if request.user.has_perm("event.participate_in_event") and event.status=='u':
#         # checking if already participated or not
#         try:
#             participation = Participation.objects.get(account=request.user, event=event)
#         except Participation.DoesNotExist:
#             participation = None
#         if(participation==None):
#             # not already participated
#             # check if not already started
#             if event.date>current_time:
#                 # not started
#                 # show btn to participate
#                 actions.append("participate_event_btn.html")
#             else:
#                 # already started
#                 actions.append("started_event_btn.html")
#         else:
#             # already participated
#             # checking if already checked in
#             if participation.status=="checked_in":
#                 # checked in
#                 # show checked in
#                 actions.append("checked_in_event_btn.html")
#             else:
#                 # not checked in
#                 # check if time between 0 to 10 mins after start or not
#                 if timedelta(minutes=0)<=(current_time-event.date)<=timedelta(minutes=10):
#                     actions.append("check_in_event_btn.html")
#                 else:
#                     # cannot checkin now
#                     actions.append("started_event_btn.html")
#     # merging to ctx
#     ctx.update({'event': event, 'actions': actions})
#     print(actions)
#     return render(request, "view_event.html", ctx)


# to view an event
@navbar_required()
def view_event(request, ctx, id):
    # getting the event
    event = get_object_or_404(Event, pk=id)

    actions = []

    if event.status=='u':

        if canCancelEvent(request, event):
            actions.append("cancel_event_btn.html")
        
        if canMarkEventCompleted(request, event):
            actions.append("mark_as_complete_event_btn.html")
        
        if canParticipateInEvent(request, event):
            actions.append("participate_event_btn.html")

        if participatedInEvent(request, event):
            actions.append("participated_event_btn.html")
        
        if canCheckInEvent(request, event)!=False:
            actions.append("check_in_event_btn.html")

        if checkedInEvent(request, event):
            actions.append("checked_in_event_btn.html")
    
    ctx.update({'event': event, 'actions': actions})

    return render(request, "view_event.html", ctx)


# helper functions
def canCancelEvent(request, event):

    if event.status=='u' and request.user.has_perm("event.delete_own_event") and request.user==event.account and (event.date-timezone.now())>=timedelta(days=1):
        return True
    return False

def canMarkEventCompleted(request, event):

    if event.status=='u' and request.user.has_perm("event.complete_own_event") and request.user==event.account and timezone.now()>=event.date:
        return True
    return False

def canParticipateInEvent(request, event):

    # getting participation if exists
    try:
        participation = Participation.objects.get(account=request.user, event=event)
    except Participation.DoesNotExist:
        participation = None
    
    if event.status=='u' and request.user.has_perm("event.participate_in_event") and participation==None and timezone.now()<event.date:
        return True
    return False

def participatedInEvent(request, event):

    # get participation
    try:
        participation = Participation.objects.get(account=request.user, event=event)
    except Participation.DoesNotExist:
        participation = None

    if participation==None:
        return False
    return True

def canCheckInEvent(request, event):

    # getting participation
    try:
        participation = Participation.objects.get(account=request.user, event=event)
    except Participation.DoesNotExist:
        participation = None
    print(timezone.is_aware(event.date))
    print(event.date)
    print(timezone.is_aware(timezone.now()))
    print(timezone.now())
    # naive = parse_datetime(event.date.)
    # print(naive)
    if event.status=='u' and participation!=None and participation.status!="checked_in" and timezone.now()>=event.date:
        print("can check in")
        return participation
    return False

def checkedInEvent(request, event):

    try:
        participation = Participation.objects.get(account=request.user, event=event)
    except Participation.DoesNotExist:
        participation = None

    if participation!=None and participation.status=="checked_in":
        return True
    return False


# to cancel an event
def cancel_event(request, id):
    
    # getting event
    event = get_object_or_404(Event, pk=id)

    if canCancelEvent(request, event):
        # cancel it
        event.status = 'x'
        event.save()

    # redirect to the event page
    return redirect("event:view_event", id=id)


# view to checkin event
def checkin_event(request, id):

    # getting the event
    event = get_object_or_404(Event, pk=id)

    participation = canCheckInEvent(request, event)

    if participation!=False:
        # can check in
        participation.status = "checked_in"
        participation.save()
    return redirect("event:view_event", id=id)

# view to mark an event as complete
def complete_event(request, id):
    # getting the event
    event = get_object_or_404(Event, pk=id)

    if canMarkEventCompleted(request, event):
        event.status = 'c'
        event.save()
    return redirect("event:view_event", id=id)
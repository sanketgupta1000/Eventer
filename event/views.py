from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied

from account.decorators import navbar_required
from account.models import Account
from .forms import *
from participant.models import Participation
from django.utils import timezone
from datetime import timedelta
import zoneinfo
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, is_naive
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

# view to host an event
@login_required
@permission_required("event.host_event", raise_exception=True)
@navbar_required()
def host_event(request, ctx):
    if request.method=='POST':
        form = EventHostForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(False)
            event.account = request.user
            # set date's timezone to current user's timezone
            # since small app, statically setting it, if TIME_ZONE = "UTC" in settings
            # event.date = event.date.replace(tzinfo=zoneinfo.ZoneInfo("Asia/Kolkata"))
            # or, set TIME_ZONE to Asia/Kolkata in settings.py, this is suitable only if app has users of only one region
            # ideally, set TIME_ZONE to utc
            # ask each user for their timezone at the tiem of registeration
            # whenever needed, add tzinfo to the date like: event.date=event.date.replace(tzinfo=ZoneInfo(request.user.timezone))
            # and when displaying in templates, display in the user's timezone
            event.save()
            return redirect('home')
    else:
        form = EventHostForm()
    ctx.update({'form': form})
    return render(request, 'pages/host_event.html', ctx)

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
        # send mail to participant
        # first render the template
        html_resp = render_to_string("mail/event_ticket.html", {'event': event}, request)
        # send email
        send_mail(
            "Event Ticket",
            strip_tags(html_resp),
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email,],
            False,
            settings.EMAIL_HOST_USER,
            settings.EMAIL_HOST_PASSWORD,
            html_message=html_resp
        )
    return redirect("event:view_event", id=id)


# to view an event
@navbar_required()
def view_event(request, ctx, id):
    # getting the event
    event = get_object_or_404(Event, pk=id)

    actions = []

    if event.status=='u':

        if canCancelEvent(request, event):
            actions.append("event/actions/cancel_event_btn.html")
        
        if canMarkEventCompleted(request, event):
            actions.append("event/actions/mark_as_complete_event_btn.html")
        
        if canParticipateInEvent(request, event):
            actions.append("event/actions/participate_event_btn.html")

        if participatedInEvent(request, event):
            actions.append("event/actions/participated_event_btn.html")
        
        if canCheckInEvent(request, event)!=False:
            actions.append("event/actions/check_in_event_btn.html")

        if checkedInEvent(request, event):
            actions.append("event/actions/checked_in_event_btn.html")
    
    ctx.update({'event': event, 'actions': actions})

    return render(request, "pages/view_event.html", ctx)


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
        participation = Participation.objects.get(account=request.user.id, event=event)
    except Participation.DoesNotExist:
        participation = None
    
    if event.status=='u' and request.user.has_perm("event.participate_in_event") and participation==None and timezone.now()<event.date:
        return True
    return False

def participatedInEvent(request, event):

    # get participation
    try:
        participation = Participation.objects.get(account=request.user.id, event=event)
    except Participation.DoesNotExist:
        participation = None

    if participation==None:
        return False
    return True

def canCheckInEvent(request, event):

    # getting participation
    try:
        participation = Participation.objects.get(account=request.user.id, event=event)
    except Participation.DoesNotExist:
        participation = None

    if event.status=='u' and participation!=None and participation.status!="checked_in" and timezone.now()>=event.date:
        print("can check in")
        return participation
    return False

def checkedInEvent(request, event):

    try:
        participation = Participation.objects.get(account=request.user.id, event=event)
    except Participation.DoesNotExist:
        # print("not found")
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

        # mail all participants
        # get the participant list
        participant_accounts = Account.objects.filter(participation__event=event)
        # get their emails
        emails = [participant_account.email for participant_account in participant_accounts]
        print(emails)
        # get the rendered template as str
        html_resp = render_to_string("mail/event_cancellation.html", {'event': event}, request)
        # get the plain text response
        plain_resp = strip_tags(html_resp)
        # email msg obj
        msg = EmailMultiAlternatives(
            "Event Cancellation",
            plain_resp,
            settings.DEFAULT_FROM_EMAIL,
            bcc=emails
        )
        msg.attach_alternative(html_resp, "text/html")
        msg.send()

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


# view to show all events
@navbar_required()
def all_events(request, ctx):
    # will get all events and update in ctx
    events = Event.objects.all()

    ctx.update({'events': events})

    return render(request, 'pages/all_events.html', ctx)
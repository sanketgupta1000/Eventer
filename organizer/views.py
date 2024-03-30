from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from account.models import Account
from .forms import *
from account.forms import AccountCreationForm
from account.decorators import logout_required, navbar_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, login_required
from participant.models import FollowList
from event.models import Event

# Create your views here.

# view to register organizer
@logout_required()
def register_organizer(request):
    if request.method=='POST':
        # get filled data
        account_form = AccountCreationForm(request.POST)
        organizer_form = OrganizerCreationForm(request.POST)

        # validating
        if account_form.is_valid() and organizer_form.is_valid():

            # good data filled
            # first will create account
            organizer_account = account_form.save(False)
            organizer_account.type = Account.Types.O
            organizer_account.save()

            # now adding group
            organizer_account.groups.add(Group.objects.get(name='Organizer'))

            # will create organizer now
            organizer = organizer_form.save(False)
            organizer.account = organizer_account
            organizer.save()

            return redirect('login')
    else:
        account_form = AccountCreationForm()
        organizer_form = OrganizerCreationForm()
    
    return render(request, "register.html", {'forms': [account_form, organizer_form]})


# view to let a participant follow an organizer
def follow_organizer(request, id):

    # check if it is a participant or not
    if request.user.is_authenticated and request.user.type==Account.Types.P:
        # participant
        # get the organizer
        organizer = get_object_or_404(Organizer, pk=id)
        # check if follow_list object already exists
        try:
            follow_obj = FollowList.objects.get(participant=request.user.participant, organizer=organizer)
        except FollowList.DoesNotExist:
            follow_obj = None
        
        if follow_obj==None:
            # not already following
            new_follow_obj = FollowList(participant=request.user.participant, organizer=organizer)
            new_follow_obj.save()
            # redirect to organizers page
            return redirect("organizer:view_organizer", id=id)
        else:
            # already following
            return redirect("organizer:view_organizer", id=id)

    else:
        # not a participant
        return redirect("organizer:view_organizer", id=id)
    
# view to let a participant unfollow an organizer
def unfollow_organizer(request, id):

    # check if it is a participant or not
    if request.user.is_authenticated and request.user.type==Account.Types.P:
        # participant
        # get the organizer
        organizer = get_object_or_404(Organizer, pk=id)
        # check if follow_list object exists
        try:
            follow_obj = FollowList.objects.get(participant=request.user.participant, organizer=organizer)
        except FollowList.DoesNotExist:
            follow_obj = None
        
        if follow_obj==None:
            # not following
            # redirect to organizers page
            return redirect("organizer:view_organizer", id=id)
        else:
            # following
            # delete the follow obj
            follow_obj.delete()
            return redirect("organizer:view_organizer", id=id)
    else:
        # not a participant
        return redirect("organizer:view_organizer", id=id)
    
@navbar_required()
def view_organizer(request, ctx, id):
    organizer = get_object_or_404(Organizer, pk=id)

    # getting all events of the organizer
    events = Event.objects.filter(account=organizer.account)

    actions=[]

    if request.user.is_authenticated and request.user.type == Account.Types.P:

        # is following
        try:
            follow_obj = FollowList.objects.get(participant=request.user.participant, organizer=organizer)
        except FollowList.DoesNotExist:
            follow_obj = None
        if follow_obj==None:
            actions.append("follow_organizer_btn.html")
        else:
            actions.append("unfollow_organizer_btn.html")

    ctx.update({'organizer': organizer, 'actions': actions, 'events': events})

    return render(request, "view_organizer.html", ctx)


# view to show my_events
@login_required
@permission_required("event.host_event", raise_exception=True)
@navbar_required()
def my_events(request, ctx):

    # first, will fetch the upcoming events
    upcoming_events = Event.objects.filter(account=request.user, status='u').order_by('date')

    # past events
    past_events = Event.objects.filter(account=request.user).exclude(status='u').order_by('-date')

    ctx.update({'upcoming_events': upcoming_events, 'past_events': past_events})

    return render(request, 'my_events.html', ctx)


# view to show all organizers
@navbar_required()
def all_organizers(request, ctx):

    # get all organizers
    organizers = Organizer.objects.all()

    ctx.update({'organizers': organizers})

    return render(request, 'all_organizers.html', ctx)
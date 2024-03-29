from django.shortcuts import render, redirect
from .models import *
from account.models import Account
from .forms import *
from account.forms import AccountCreationForm
from account.decorators import logout_required, navbar_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

# view to register participant
@logout_required()
def register_participant(request):
    if request.method=='POST':
        # get filled data
        account_form = AccountCreationForm(request.POST)
        participant_form = ParticipantCreationForm(request.POST)

        # validating
        if account_form.is_valid() and participant_form.is_valid():

            # good data filled
            # first will create account
            participant_account = account_form.save(False)
            participant_account.type = Account.Types.P
            participant_account.save()

            # now adding group
            participant_account.groups.add(Group.objects.get(name='Participant'))

            # will create participant now
            participant = participant_form.save(False)
            participant.account = participant_account
            participant.save()

            return redirect('login')
    else:
        account_form = AccountCreationForm()
        participant_form = ParticipantCreationForm()
    
    return render(request, "register.html", {'forms': [account_form, participant_form]})


# view to show a participant's follow list
@login_required
@navbar_required()
def follow_list(request, ctx):

    if request.user.type==Account.Types.P:

        # it is a participant
        # get all the organizers that the participant has followed
        followed_organizers = Organizer.objects.filter(followlist__participant=request.user.participant)
        print(followed_organizers)
        ctx.update({'followed_organizers': followed_organizers})
        return render(request, "follow_list.html", ctx)
    else:
        return redirect("home")
    

# view to show all participations
@login_required
@permission_required("event.participate_in_event", raise_exception=True)
@navbar_required()
def participations(request, ctx):
    # getting events the user participated in
    events = Event.objects.filter(participation__account=request.user)

    ctx.update({'events': events})

    return render(request, 'participations.html', ctx)
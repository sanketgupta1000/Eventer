from django.shortcuts import render, redirect
from .models import *
from account.models import Account
from .forms import *
from account.forms import AccountCreationForm
from account.decorators import logout_required

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

            # will create participant now
            participant = participant_form.save(False)
            participant.account = participant_account
            participant.save()

            return redirect('login')
    else:
        account_form = AccountCreationForm()
        participant_form = ParticipantCreationForm()
    
    return render(request, "register.html", {'forms': [account_form, participant_form]})
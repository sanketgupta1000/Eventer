from django.shortcuts import render, redirect
from .models import *
from account.models import Account
from .forms import *
from account.forms import AccountCreationForm
from account.decorators import logout_required

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

            # will create organizer now
            organizer = organizer_form.save(False)
            organizer.account = organizer_account
            organizer.save()

            return redirect('login')
    else:
        account_form = AccountCreationForm()
        organizer_form = OrganizerCreationForm()
    
    return render(request, "register.html", {'forms': [account_form, organizer_form]})
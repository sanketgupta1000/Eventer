from functools import wraps
from django.shortcuts import redirect
from django.conf import settings

from account.models import Account

# to ensure that the view is accessed only by logged out users
def logout_required():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # user is logged in
                # send to LOGOUT_URL specified in settings
                return redirect(settings.LOGOUT_URL)
            else:
                # not logged in, so return the result of view itself
                return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# to ensure that view will include necessary navlinks based on permissions in context
def navbar_required():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            # logic to include navlinks based on permissionsa and groups go here

            nav_links=[]

            if request.user.is_authenticated:
                nav_links=['navbar/home_navlink.html']
            # else:
            #     nav_links=['landing_page_navlink.html']

            if request.user.has_perm("event.host_event"):
                nav_links.append("navbar/host_event_navlink.html")
                nav_links.append("navbar/my_events_navlink.html")

            nav_links.append("navbar/all_events_navlink.html")

            if request.user.has_perm("event.participate_in_event"):
                nav_links.append('navbar/participations_navlink.html')

            if request.user.is_authenticated and request.user.type==Account.Types.P:
                nav_links.append('navbar/follow_list_navlink.html')

            nav_links.append("navbar/all_organizers_navlink.html")

            if request.user.is_authenticated:
                nav_links.append("navbar/logout_navlink.html")
            else:
                nav_links.append("navbar/login_navlink.html")
                nav_links.append("navbar/register_as_organizer_navlink.html")
                nav_links.append("navbar/register_as_participant_navlink.html")
            
            # context to be sent to view, view will add in this context
            ctx={'nav_links':nav_links}
            # print(ctx)
            return view(request, ctx, *args, **kwargs)
        return _wrapped_view
    return decorator
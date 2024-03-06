from functools import wraps
from django.shortcuts import redirect
from django.conf import settings

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
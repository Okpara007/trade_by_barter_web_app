from django.core.exceptions import PermissionDenied

def agent_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.role == 'agent' and request.user.profile.approved:
                return view_func(request, *args, **kwargs)
        raise PermissionDenied("You do not have permission to access this page.")
    return wrapper

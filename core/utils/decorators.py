from functools import wraps
from http import HTTPStatus
from django.http import HttpResponse

def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(
                {"message": "User not authenticated"},
                content_type="application/json", status=HTTPStatus.UNAUTHORIZED
              )
        return view(request, *args, **kwargs)
    return wrapper

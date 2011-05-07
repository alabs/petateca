from django.http import Http404
from piston.utils import rc
from functools import wraps

def catch_404(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Http404:
            return rc.NOT_FOUND
    return wrap


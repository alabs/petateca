from django.http import Http404
from piston.utils import rc
from functools import wraps

from django.contrib.sites.models import Site

def catch_404(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Http404:
            return rc.NOT_FOUND
    return wrap


def get_urlprefix():
    current_site = Site.objects.get_current()
    urlprefix = 'http://' + current_site.domain
    return urlprefix

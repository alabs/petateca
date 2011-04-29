from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

from django.conf import settings
from django.http import HttpResponseRedirect, get_host

SSL = 'SSL'

# LOGIN REQUIRED

EXEMPT_URLS = [compile(settings.LOGIN_URL_INDEX.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        if settings.INVITE_MODE and not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL_INDEX)


# SSL REDIRECT MIDDLEWARE

def request_is_secure(request):
    if request.is_secure():
        return True

    # Handle forwarded SSL (used at Webfaction)
    if 'HTTP_X_FORWARDED_SSL' in request.META:
        return request.META['HTTP_X_FORWARDED_SSL'] == 'on'

    if 'HTTP_X_SSL_REQUEST' in request.META:
        return request.META['HTTP_X_SSL_REQUEST'] == '1'

    return False

class SSLRedirect:
    def process_request(self, request):
        if request_is_secure(request):
            request.IS_SECURE=True
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):          
        if SSL in view_kwargs:
            secure = view_kwargs[SSL]
            del view_kwargs[SSL]
        else:
            secure = False

        if settings.DEBUG:
            return None

        if getattr(settings, "TESTMODE", False):
            return None

        if not secure == request_is_secure(request):
            return self._redirect(request, secure)

    def _redirect(self, request, secure):
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError(
            """Django can't perform a SSL redirect while maintaining POST data.
                Please structure your views so that redirects only occur during GETs.""")

        protocol = secure and "https" or "http"

        newurl = "%s://%s%s" % (protocol,get_host(request),request.get_full_path())


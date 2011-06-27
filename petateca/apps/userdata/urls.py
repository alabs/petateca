from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from registration.forms import RegistrationFormUniqueEmail
from registration.views import register

urlpatterns = patterns('',
    # Usuarios, registros, avatar, etc
    url(r'^register/$',
        register,
        {
            'backend': 'registration.backends.default.DefaultBackend',
            'form_class': RegistrationFormUniqueEmail
        },
        name='registration_register'),
    url(r'^activate/$', 'userdata.views.activate_by_code', name="activate_by_code"),
    (r'^', include('registration.backends.default.urls')),
    (r'^profile/$', 'userdata.views.view_profile'),
    (r'^avatar/', include('avatar.urls')),

    url(r'^signin/$', redirect_to, { 'url': '/accounts/login/' }, name='signin'),
)

from django.conf.urls.defaults import *
from registration.forms import RegistrationFormTermsOfService
from invitation.views import register 
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Usuarios, invitaciones, registros, avatar, etc
    # TODO: mover a apps/userdata/urls.py
    (r'^', include('invitation.urls')),
    (r'^profile/$', 'userdata.views.view_profile'),
    url(r'^register/$',
        register,
        {
            'form_class': RegistrationFormTermsOfService,
            'backend': 'invitation.backends.InvitationBackend',
        },
        name='registration_register'),
    url(r'^signin/$',
        auth_views.login,
        {
            'template_name': 'invitation/signin.html', 
        },
        name='auth_login'),
    (r'^', include('registration.urls')),
    (r'^avatar/', include('avatar.urls')),
    url(r'^invitation/request/$', 'userdata.views.request_invitation', name='request_invitation'),

)

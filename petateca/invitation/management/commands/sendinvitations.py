"""
Un comando de management que envia invitaciones a todos los usuarios
que todavia no hayan sido invitados

Para que este funcione es necesario que haya un usuario valido 
en el settings en la variable USER_WHO_INVITES

"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management.base import NoArgsCommand, CommandError
from django.template.loader import render_to_string

from invitation.models import InvitationKey
from userdata.models import UserToInvite, User

class Command(NoArgsCommand):
    help = "Envia invitaciones a los primeros 5 usuarios no invitados de UserToInvite"

    def handle_noargs(self, **options):
        users_to_invite = UserToInvite.objects.filter(has_been_invited=False)
        try:
            liberateca = User.objects.get(username=settings.USER_WHO_INVITES)
        except:
            raise CommandError("User %s not exists. Please create" % settings.USER_WHO_INVITES)

        for user in users_to_invite:
            invitation = InvitationKey.objects.create_invitation(liberateca)
            invitation.send_to(user.mail)

            # Marcamos al usuario que se ha enviado 
            user.has_been_invited = True
            user.save()
            print 'Invited %s' % user.mail

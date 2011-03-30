"""
Un comando de management que envia invitaciones a todos los usuarios
que todavia no hayan sido invitados

Para que este funcione es necesario que haya un usuario llamado liberateca

"""

from django.core.management.base import NoArgsCommand
from invitation.models import InvitationKey
from userdata.models import UserToInvite, User

class Command(NoArgsCommand):
    help = "Envia invitaciones a los primeros 5 usuarios no invitados de UserToInvite"

    def handle_noargs(self, **options):
        users_to_invite = UserToInvite.objects.filter(has_been_invited=False)
        liberateca = User.objects.get(username='liberateca')
        for user in users_to_invite:
            invitation = InvitationKey.objects.create_invitation(liberateca)
            invitation.send_to(user.mail)
            user.has_been_invited = True
            user.save()
            print 'Invited %s' % user.mail

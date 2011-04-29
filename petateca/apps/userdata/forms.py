from django.forms import ModelForm, TextInput
from userdata.models import UserToInvite


class UserToInviteForm(ModelForm):
    class Meta:
        model = UserToInvite


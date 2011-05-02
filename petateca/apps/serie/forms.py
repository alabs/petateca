from django.forms import ModelForm, TextInput
from serie.models import Link, LinkSeason

class LinkForm(ModelForm):
    class Meta:
        model = Link
        widgets = {
            'url': TextInput(attrs={'size':55}),
     }


class LinkSeasonForm(ModelForm):
    class Meta:
        model = LinkSeason
        widgets = {
            'url': TextInput(attrs={'size':60}),
     }

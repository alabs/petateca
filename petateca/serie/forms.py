from django.forms import ModelForm, TextInput
from serie.models import Link

class LinkForm(ModelForm):
    class Meta:
        model = Link
        widgets = {
            'url': TextInput(attrs={'size':80}),
     }

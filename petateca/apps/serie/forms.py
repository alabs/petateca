from django.forms import ModelForm, TextInput
from serie import models as m

class LinkForm(ModelForm):
    class Meta:
        model = m.Link
        widgets = {
            'url': TextInput(attrs={'size':40}),
     }


class LinkSeasonForm(ModelForm):
    class Meta:
        model = m.LinkSeason
        widgets = {
            'url': TextInput(attrs={'size':40}),
     }


class SerieForm(ModelForm):
    class Meta:
        model = m.Serie
        
        
class EpisodeForm(ModelForm):
    class Meta:
        model = m.Episode
        widgets = {
            'episode': TextInput(attrs={'size':2}),
     }
        

class EpisodeImageForm(ModelForm):
    class Meta:
        model = m.ImageEpisode

class RoleForm(ModelForm):
    class Meta:
        model = m.Role

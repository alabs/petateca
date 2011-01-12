from liberweb.serie.models import Genre, Network
from django import template

register = template.Library()

@register.inclusion_tag('serie/serie_sidebar.html')
def serie_sidebar():
    genre_list = Genre.objects.order_by('name').all()
    network_list = Network.objects.order_by('name').all()
    return {
        'genre_list': genre_list,
        'network_list': network_list,
    }

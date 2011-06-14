from serie.models import Serie
from django import template

register = template.Library()

@register.inclusion_tag('comments/show_serie_poster.html')
def process_serie_id(serie_id):
    serie = Serie.objects.get(id=serie_id)
    return {'serie': serie}

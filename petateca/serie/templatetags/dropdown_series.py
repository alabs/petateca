from serie.models import Serie
from django import template

register = template.Library()


@register.inclusion_tag('serie/dropdown.html')
def dropdown_series():
    all_series = Serie.objects.order_by('name')
    return {'all_series': all_series}
